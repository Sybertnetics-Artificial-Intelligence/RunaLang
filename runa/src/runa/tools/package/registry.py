#!/usr/bin/env python3
"""
Runa Package Registry Server

Multi-language package registry with REST API supporting all language tiers.
Provides package hosting, search, authentication, and cross-language dependency management.
"""

import os
import json
import hashlib
import sqlite3
import tempfile
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
import threading
import time
import secrets
import jwt
import bcrypt
from flask import Flask, request, jsonify, send_file, abort
from werkzeug.utils import secure_filename
from werkzeug.middleware.proxy_fix import ProxyFix
import semver

from .manager import PackageVersion, PackageMetadata, PackageDependency


@dataclass
class RegistryUser:
    """Registry user account."""
    username: str
    email: str
    password_hash: str
    api_tokens: List[str]
    created_at: datetime
    is_active: bool = True
    is_admin: bool = False
    
    def check_password(self, password: str) -> bool:
        """Verify password against hash."""
        return bcrypt.checkpw(password.encode(), self.password_hash.encode())
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Generate password hash."""
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


@dataclass
class PackageRecord:
    """Database record for a published package."""
    name: str
    version: str
    author: str
    email: str
    description: str
    license: str
    homepage: Optional[str]
    repository: Optional[str]
    
    # Multi-language support
    primary_language: str
    supported_languages: List[str]
    language_targets: Dict[str, Any]
    
    # Package metadata
    dependencies: Dict[str, Any]
    keywords: List[str]
    categories: List[str]
    minimum_runa_version: Optional[str]
    
    # File metadata
    checksum: str
    size_bytes: int
    download_count: int = 0
    
    # Timestamps
    published_at: datetime
    updated_at: datetime
    
    # Package file path
    file_path: str


class PackageDatabase:
    """SQLite database for package metadata and user management."""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.lock = threading.Lock()
        self._init_database()
    
    def _init_database(self):
        """Initialize database schema."""
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    api_tokens TEXT NOT NULL DEFAULT '[]',
                    created_at TIMESTAMP NOT NULL,
                    is_active BOOLEAN NOT NULL DEFAULT 1,
                    is_admin BOOLEAN NOT NULL DEFAULT 0
                );
                
                CREATE TABLE IF NOT EXISTS packages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    version TEXT NOT NULL,
                    author TEXT NOT NULL,
                    email TEXT NOT NULL,
                    description TEXT NOT NULL,
                    license TEXT NOT NULL,
                    homepage TEXT,
                    repository TEXT,
                    primary_language TEXT NOT NULL,
                    supported_languages TEXT NOT NULL,
                    language_targets TEXT NOT NULL,
                    dependencies TEXT NOT NULL,
                    keywords TEXT NOT NULL,
                    categories TEXT NOT NULL,
                    minimum_runa_version TEXT,
                    checksum TEXT NOT NULL,
                    size_bytes INTEGER NOT NULL,
                    download_count INTEGER NOT NULL DEFAULT 0,
                    published_at TIMESTAMP NOT NULL,
                    updated_at TIMESTAMP NOT NULL,
                    file_path TEXT NOT NULL,
                    UNIQUE(name, version)
                );
                
                CREATE INDEX IF NOT EXISTS idx_packages_name ON packages(name);
                CREATE INDEX IF NOT EXISTS idx_packages_language ON packages(primary_language);
                CREATE INDEX IF NOT EXISTS idx_packages_keywords ON packages(keywords);
                CREATE INDEX IF NOT EXISTS idx_packages_published ON packages(published_at);
                
                CREATE TABLE IF NOT EXISTS downloads (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    package_name TEXT NOT NULL,
                    package_version TEXT NOT NULL,
                    client_ip TEXT,
                    user_agent TEXT,
                    downloaded_at TIMESTAMP NOT NULL,
                    success BOOLEAN NOT NULL
                );
                
                CREATE INDEX IF NOT EXISTS idx_downloads_package ON downloads(package_name, package_version);
                CREATE INDEX IF NOT EXISTS idx_downloads_time ON downloads(downloaded_at);
            ''')
    
    def create_user(self, username: str, email: str, password: str) -> int:
        """Create a new user account."""
        password_hash = RegistryUser.hash_password(password)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                INSERT INTO users (username, email, password_hash, created_at)
                VALUES (?, ?, ?, ?)
            ''', (username, email, password_hash, datetime.now()))
            return cursor.lastrowid
    
    def get_user(self, username: str) -> Optional[RegistryUser]:
        """Get user by username."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                SELECT username, email, password_hash, api_tokens, created_at, is_active, is_admin
                FROM users WHERE username = ?
            ''', (username,))
            
            row = cursor.fetchone()
            if row:
                return RegistryUser(
                    username=row[0],
                    email=row[1], 
                    password_hash=row[2],
                    api_tokens=json.loads(row[3]),
                    created_at=datetime.fromisoformat(row[4]),
                    is_active=bool(row[5]),
                    is_admin=bool(row[6])
                )
        return None
    
    def add_api_token(self, username: str, token: str):
        """Add API token for user."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('SELECT api_tokens FROM users WHERE username = ?', (username,))
            row = cursor.fetchone()
            if row:
                tokens = json.loads(row[0])
                tokens.append(token)
                conn.execute('UPDATE users SET api_tokens = ? WHERE username = ?', 
                           (json.dumps(tokens), username))
    
    def store_package(self, package: PackageRecord) -> int:
        """Store package metadata in database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                INSERT OR REPLACE INTO packages (
                    name, version, author, email, description, license,
                    homepage, repository, primary_language, supported_languages,
                    language_targets, dependencies, keywords, categories,
                    minimum_runa_version, checksum, size_bytes, download_count,
                    published_at, updated_at, file_path
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                package.name, package.version, package.author, package.email,
                package.description, package.license, package.homepage, package.repository,
                package.primary_language, json.dumps(package.supported_languages),
                json.dumps(package.language_targets), json.dumps(package.dependencies),
                json.dumps(package.keywords), json.dumps(package.categories),
                package.minimum_runa_version, package.checksum, package.size_bytes,
                package.download_count, package.published_at, package.updated_at,
                package.file_path
            ))
            return cursor.lastrowid
    
    def get_package(self, name: str, version: Optional[str] = None) -> Optional[PackageRecord]:
        """Get package by name and optionally version."""
        with sqlite3.connect(self.db_path) as conn:
            if version:
                cursor = conn.execute('''
                    SELECT * FROM packages WHERE name = ? AND version = ?
                ''', (name, version))
            else:
                cursor = conn.execute('''
                    SELECT * FROM packages WHERE name = ? 
                    ORDER BY published_at DESC LIMIT 1
                ''', (name,))
            
            row = cursor.fetchone()
            if row:
                return self._row_to_package_record(row)
        return None
    
    def get_package_versions(self, name: str) -> List[str]:
        """Get all versions of a package."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                SELECT version FROM packages WHERE name = ? ORDER BY published_at DESC
            ''', (name,))
            return [row[0] for row in cursor.fetchall()]
    
    def search_packages(self, query: str, language: Optional[str] = None,
                       category: Optional[str] = None, limit: int = 50) -> List[PackageRecord]:
        """Search packages by query, language, and category."""
        with sqlite3.connect(self.db_path) as conn:
            sql_parts = ['SELECT * FROM packages WHERE 1=1']
            params = []
            
            # Text search in name, description, keywords
            if query:
                sql_parts.append('''
                    AND (name LIKE ? OR description LIKE ? OR keywords LIKE ?)
                ''')
                search_term = f'%{query}%'
                params.extend([search_term, search_term, search_term])
            
            # Language filter
            if language:
                sql_parts.append('AND (primary_language = ? OR supported_languages LIKE ?)')
                params.extend([language, f'%{language}%'])
            
            # Category filter
            if category:
                sql_parts.append('AND categories LIKE ?')
                params.append(f'%{category}%')
            
            sql_parts.append('ORDER BY download_count DESC, published_at DESC LIMIT ?')
            params.append(limit)
            
            sql = ' '.join(sql_parts)
            cursor = conn.execute(sql, params)
            return [self._row_to_package_record(row) for row in cursor.fetchall()]
    
    def increment_download_count(self, name: str, version: str):
        """Increment download count for a package."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                UPDATE packages SET download_count = download_count + 1,
                updated_at = ? WHERE name = ? AND version = ?
            ''', (datetime.now(), name, version))
    
    def log_download(self, package_name: str, package_version: str, client_ip: str,
                    user_agent: str, success: bool):
        """Log a package download attempt."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT INTO downloads (package_name, package_version, client_ip,
                                     user_agent, downloaded_at, success)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (package_name, package_version, client_ip, user_agent, datetime.now(), success))
    
    def _row_to_package_record(self, row) -> PackageRecord:
        """Convert database row to PackageRecord."""
        return PackageRecord(
            name=row[1],
            version=row[2],
            author=row[3],
            email=row[4],
            description=row[5],
            license=row[6],
            homepage=row[7],
            repository=row[8],
            primary_language=row[9],
            supported_languages=json.loads(row[10]),
            language_targets=json.loads(row[11]),
            dependencies=json.loads(row[12]),
            keywords=json.loads(row[13]),
            categories=json.loads(row[14]),
            minimum_runa_version=row[15],
            checksum=row[16],
            size_bytes=row[17],
            download_count=row[18],
            published_at=datetime.fromisoformat(row[19]),
            updated_at=datetime.fromisoformat(row[20]),
            file_path=row[21]
        )


class PackageRegistryServer:
    """Multi-language package registry server with REST API."""
    
    def __init__(self, data_dir: str = "./registry_data", 
                 secret_key: Optional[str] = None):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # Storage directories
        self.packages_dir = self.data_dir / "packages"
        self.packages_dir.mkdir(exist_ok=True)
        
        # Database
        db_path = self.data_dir / "registry.db"
        self.db = PackageDatabase(str(db_path))
        
        # Flask app
        self.app = Flask(__name__)
        self.app.wsgi_app = ProxyFix(self.app.wsgi_app)
        self.app.config['SECRET_KEY'] = secret_key or secrets.token_hex(32)
        self.app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max
        
        # Language tier configuration
        self.language_tiers = {
            1: ["javascript", "typescript", "python", "cpp", "java", "csharp", "sql"],
            2: ["rust", "go", "swift", "kotlin", "php", "webassembly"], 
            3: ["html", "css", "shell", "hcl", "yaml", "json", "xml"],
            4: ["r", "matlab", "julia", "solidity", "graphql", "vyper", "move", "michelson", "scilla", "smartpy", "ligo", "plutus", "pact", "scrypto"],
            5: ["lisp", "haskell", "erlang", "elixir", "llvm_ir", "assembly"],
            6: ["objective_c", "visual_basic", "cobol", "ada", "perl", "fortran"]
        }
        
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup Flask routes."""
        
        @self.app.route('/api/v1/health', methods=['GET'])
        def health_check():
            """Health check endpoint."""
            return jsonify({
                "status": "healthy",
                "version": "0.3.0",
                "timestamp": datetime.now().isoformat()
            })
        
        @self.app.route('/api/v1/auth/register', methods=['POST'])
        def register_user():
            """Register a new user account."""
            data = request.get_json()
            
            required_fields = ['username', 'email', 'password']
            if not all(field in data for field in required_fields):
                return jsonify({"error": "Missing required fields"}), 400
            
            try:
                user_id = self.db.create_user(data['username'], data['email'], data['password'])
                return jsonify({
                    "message": "User created successfully",
                    "user_id": user_id
                }), 201
            except sqlite3.IntegrityError:
                return jsonify({"error": "Username or email already exists"}), 409
        
        @self.app.route('/api/v1/auth/login', methods=['POST'])
        def login_user():
            """Authenticate user and return API token."""
            data = request.get_json()
            
            if 'username' not in data or 'password' not in data:
                return jsonify({"error": "Username and password required"}), 400
            
            user = self.db.get_user(data['username'])
            if not user or not user.check_password(data['password']):
                return jsonify({"error": "Invalid credentials"}), 401
            
            if not user.is_active:
                return jsonify({"error": "Account is deactivated"}), 403
            
            # Generate API token (JWT)
            token_payload = {
                'username': user.username,
                'exp': datetime.now() + timedelta(days=30)
            }
            token = jwt.encode(token_payload, self.app.config['SECRET_KEY'], algorithm='HS256')
            
            # Store token in database
            self.db.add_api_token(user.username, token)
            
            return jsonify({
                "access_token": token,
                "token_type": "bearer",
                "expires_in": 30 * 24 * 3600  # 30 days
            })
        
        @self.app.route('/api/v1/packages/search', methods=['GET'])
        def search_packages():
            """Search for packages."""
            query = request.args.get('q', '')
            language = request.args.get('language')
            category = request.args.get('category')
            limit = min(int(request.args.get('limit', 50)), 100)
            
            packages = self.db.search_packages(query, language, category, limit)
            
            return jsonify({
                "query": query,
                "total": len(packages),
                "packages": [self._package_record_to_api(pkg) for pkg in packages]
            })
        
        @self.app.route('/api/v1/packages/<package_name>', methods=['GET'])
        def get_package_info(package_name):
            """Get package information."""
            version = request.args.get('version')
            package = self.db.get_package(package_name, version)
            
            if not package:
                return jsonify({"error": "Package not found"}), 404
            
            return jsonify(self._package_record_to_api(package))
        
        @self.app.route('/api/v1/packages/<package_name>/versions', methods=['GET'])
        def get_package_versions(package_name):
            """Get all versions of a package."""
            versions = self.db.get_package_versions(package_name)
            
            if not versions:
                return jsonify({"error": "Package not found"}), 404
            
            return jsonify({"versions": versions})
        
        @self.app.route('/api/v1/packages/<package_name>/<version>/download', methods=['GET'])
        def download_package(package_name, version):
            """Download a package archive."""
            package = self.db.get_package(package_name, version)
            
            if not package:
                return jsonify({"error": "Package not found"}), 404
            
            file_path = self.packages_dir / package.file_path
            if not file_path.exists():
                return jsonify({"error": "Package file not found"}), 404
            
            # Log download
            client_ip = request.environ.get('REMOTE_ADDR', 'unknown')
            user_agent = request.headers.get('User-Agent', 'unknown')
            
            try:
                # Increment download count
                self.db.increment_download_count(package_name, version)
                self.db.log_download(package_name, version, client_ip, user_agent, True)
                
                return send_file(file_path, as_attachment=True, 
                               download_name=f"{package_name}-{version}.tar.gz")
            except Exception as e:
                self.db.log_download(package_name, version, client_ip, user_agent, False)
                return jsonify({"error": "Download failed"}), 500
        
        @self.app.route('/api/v1/packages/publish', methods=['POST'])
        def publish_package():
            """Publish a new package."""
            # Authenticate user
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return jsonify({"error": "Authentication required"}), 401
            
            token = auth_header.split(' ')[1]
            try:
                payload = jwt.decode(token, self.app.config['SECRET_KEY'], algorithms=['HS256'])
                username = payload['username']
            except jwt.InvalidTokenError:
                return jsonify({"error": "Invalid token"}), 401
            
            user = self.db.get_user(username)
            if not user or not user.is_active:
                return jsonify({"error": "User not found or inactive"}), 401
            
            # Process package data
            data = request.get_json()
            if not data:
                return jsonify({"error": "No package data provided"}), 400
            
            # Validate required fields
            required_fields = ['name', 'version', 'description', 'author', 'email']
            if not all(field in data for field in required_fields):
                return jsonify({"error": "Missing required package fields"}), 400
            
            # Validate version format
            try:
                PackageVersion.from_string(data['version'])
            except ValueError:
                return jsonify({"error": "Invalid version format"}), 400
            
            # Check if package version already exists
            existing = self.db.get_package(data['name'], data['version'])
            if existing:
                return jsonify({"error": "Package version already exists"}), 409
            
            # Validate language targets
            for lang in data.get('supported_languages', []):
                if lang not in [l for tier_langs in self.language_tiers.values() for l in tier_langs] + ['runa']:
                    return jsonify({"error": f"Unsupported language: {lang}"}), 400
            
            # Create package record
            now = datetime.now()
            package_record = PackageRecord(
                name=data['name'],
                version=data['version'],
                author=data['author'],
                email=data['email'],
                description=data['description'],
                license=data.get('license', 'MIT'),
                homepage=data.get('homepage'),
                repository=data.get('repository'),
                primary_language=data.get('primary_language', 'runa'),
                supported_languages=data.get('supported_languages', ['runa']),
                language_targets=data.get('language_targets', {}),
                dependencies=data.get('dependencies', {}),
                keywords=data.get('keywords', []),
                categories=data.get('categories', []),
                minimum_runa_version=data.get('minimum_runa_version'),
                checksum=data.get('checksum', ''),
                size_bytes=data.get('size_bytes', 0),
                published_at=now,
                updated_at=now,
                file_path=f"{data['name']}/{data['version']}/{data['name']}-{data['version']}.tar.gz"
            )
            
            # Store in database
            package_id = self.db.store_package(package_record)
            
            # Create package directory structure
            package_dir = self.packages_dir / data['name'] / data['version']
            package_dir.mkdir(parents=True, exist_ok=True)
            
            return jsonify({
                "message": "Package published successfully",
                "package_id": package_id,
                "name": data['name'],
                "version": data['version'],
                "url": f"/api/v1/packages/{data['name']}/{data['version']}"
            }), 201
        
        @self.app.route('/api/v1/languages', methods=['GET'])
        def get_supported_languages():
            """Get list of supported languages by tier."""
            return jsonify({
                "language_tiers": self.language_tiers,
                "total_languages": sum(len(langs) for langs in self.language_tiers.values()) + 1,  # +1 for runa
                "core_language": "runa"
            })
        
        @self.app.route('/api/v1/stats', methods=['GET'])
        def get_registry_stats():
            """Get registry statistics."""
            with sqlite3.connect(self.db.db_path) as conn:
                # Package counts
                package_count = conn.execute('SELECT COUNT(*) FROM packages').fetchone()[0]
                user_count = conn.execute('SELECT COUNT(*) FROM users').fetchone()[0]
                
                # Language distribution
                lang_stats = conn.execute('''
                    SELECT primary_language, COUNT(*) as count
                    FROM packages GROUP BY primary_language
                    ORDER BY count DESC
                ''').fetchall()
                
                # Recent downloads
                recent_downloads = conn.execute('''
                    SELECT COUNT(*) FROM downloads
                    WHERE downloaded_at > datetime('now', '-7 days')
                ''').fetchone()[0]
                
                total_downloads = conn.execute('SELECT SUM(download_count) FROM packages').fetchone()[0] or 0
            
            return jsonify({
                "total_packages": package_count,
                "total_users": user_count,
                "total_downloads": total_downloads,
                "recent_downloads": recent_downloads,
                "language_distribution": [{"language": lang, "count": count} for lang, count in lang_stats],
                "supported_language_tiers": len(self.language_tiers)
            })
    
    def _package_record_to_api(self, package: PackageRecord) -> Dict[str, Any]:
        """Convert PackageRecord to API response format."""
        return {
            "name": package.name,
            "version": package.version,
            "description": package.description,
            "author": package.author,
            "email": package.email,
            "license": package.license,
            "homepage": package.homepage,
            "repository": package.repository,
            "primary_language": package.primary_language,
            "supported_languages": package.supported_languages,
            "language_targets": package.language_targets,
            "dependencies": package.dependencies,
            "keywords": package.keywords,
            "categories": package.categories,
            "minimum_runa_version": package.minimum_runa_version,
            "size_bytes": package.size_bytes,
            "download_count": package.download_count,
            "published_at": package.published_at.isoformat(),
            "updated_at": package.updated_at.isoformat(),
            "checksum": package.checksum
        }
    
    def run(self, host: str = '127.0.0.1', port: int = 5000, debug: bool = False):
        """Run the registry server."""
        print(f"Starting Runa Package Registry Server on {host}:{port}")
        print(f"Data directory: {self.data_dir}")
        print(f"Supported language tiers: {len(self.language_tiers)}")
        
        self.app.run(host=host, port=port, debug=debug)


def main():
    """CLI entry point for the registry server."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Runa Package Registry Server')
    parser.add_argument('--host', default='127.0.0.1', help='Host to bind to')
    parser.add_argument('--port', type=int, default=5000, help='Port to bind to')
    parser.add_argument('--data-dir', default='./registry_data', help='Data directory')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    args = parser.parse_args()
    
    # Create and run registry server
    registry = PackageRegistryServer(args.data_dir)
    registry.run(args.host, args.port, args.debug)


if __name__ == '__main__':
    main()