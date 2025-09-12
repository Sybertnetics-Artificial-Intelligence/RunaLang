# Runa Package Registry Server
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV REGISTRY_HOME=/opt/runa-registry
ENV REGISTRY_PORT=8080
ENV REGISTRY_HOST=0.0.0.0

# Create registry user and directories
RUN groupadd -r registry && useradd -r -g registry registry && \
    mkdir -p $REGISTRY_HOME && \
    mkdir -p /var/lib/runa-registry && \
    mkdir -p /var/log/runa-registry && \
    mkdir -p /etc/runa-registry && \
    chown -R registry:registry $REGISTRY_HOME && \
    chown -R registry:registry /var/lib/runa-registry && \
    chown -R registry:registry /var/log/runa-registry && \
    chown -R registry:registry /etc/runa-registry

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR $REGISTRY_HOME

# Copy registry-specific files
COPY --chown=registry:registry src/runa/tools/package/ ./package/
COPY --chown=registry:registry runa.toml .
COPY --chown=registry:registry requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir fastapi uvicorn gunicorn

# Create registry server script
COPY --chown=registry:registry <<'EOF' ./registry_server.py
#!/usr/bin/env python3
"""
Runa Package Registry Server

A FastAPI-based package registry for Runa packages that provides:
- Package upload/download
- Version management
- Dependency resolution
- Authentication
- Package search and discovery
"""

import os
import json
import logging
from typing import List, Dict, Optional
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, HTTPException, UploadFile, File, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import uvicorn

from package.registry import RunaPackageRegistry
from package.manager import PackageMetadata

# Configuration
REGISTRY_DATA_DIR = Path(os.getenv("REGISTRY_DATA_DIR", "/var/lib/runa-registry"))
REGISTRY_LOG_DIR = Path(os.getenv("REGISTRY_LOG_DIR", "/var/log/runa-registry"))
REGISTRY_HOST = os.getenv("REGISTRY_HOST", "0.0.0.0")
REGISTRY_PORT = int(os.getenv("REGISTRY_PORT", "8080"))
REGISTRY_TOKEN = os.getenv("REGISTRY_TOKEN", "runa-dev-token")

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(REGISTRY_LOG_DIR / "registry.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Runa Package Registry",
    description="Universal package registry for Runa translation platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Initialize registry
registry = RunaPackageRegistry(str(REGISTRY_DATA_DIR))

# Pydantic models
class PackageInfo(BaseModel):
    name: str
    version: str
    description: str
    author: str
    dependencies: Dict[str, str] = {}
    target_languages: List[str] = []

class RegistryStatus(BaseModel):
    status: str
    version: str
    packages_count: int
    uptime: str

# Authentication
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != REGISTRY_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )
    return credentials.credentials

# Routes
@app.get("/", response_model=RegistryStatus)
async def get_status():
    """Get registry status."""
    packages = registry.list_packages()
    return RegistryStatus(
        status="healthy",
        version="1.0.0",
        packages_count=len(packages),
        uptime="active"
    )

@app.get("/packages", response_model=List[str])
async def list_packages():
    """List all available packages."""
    return registry.list_packages()

@app.get("/packages/{package_name}")
async def get_package_info(package_name: str):
    """Get package information and available versions."""
    try:
        versions = registry.get_package_versions(package_name)
        if not versions:
            raise HTTPException(status_code=404, detail="Package not found")
        
        # Get metadata for latest version
        latest_version = max(versions)
        metadata = registry.get_package_metadata(package_name, latest_version)
        
        return {
            "name": package_name,
            "versions": versions,
            "latest": latest_version,
            "metadata": metadata.__dict__ if metadata else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/packages/{package_name}/{version}")
async def download_package(package_name: str, version: str):
    """Download a specific package version."""
    try:
        package_path = registry.get_package_path(package_name, version)
        if not package_path or not os.path.exists(package_path):
            raise HTTPException(status_code=404, detail="Package version not found")
        
        return FileResponse(
            package_path,
            media_type='application/octet-stream',
            filename=f"{package_name}-{version}.runa"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/packages/{package_name}")
async def upload_package(
    package_name: str,
    package_file: UploadFile = File(...),
    metadata: str = None,
    token: str = Depends(verify_token)
):
    """Upload a new package version."""
    try:
        # Parse metadata
        if metadata:
            metadata_dict = json.loads(metadata)
            package_metadata = PackageMetadata(**metadata_dict)
        else:
            # Extract metadata from package file
            package_metadata = PackageMetadata(
                name=package_name,
                version="1.0.0",
                description="Uploaded package",
                author="unknown"
            )
        
        # Save package file
        package_content = await package_file.read()
        success = registry.publish_package(package_metadata, package_content)
        
        if success:
            logger.info(f"Published package {package_name} v{package_metadata.version}")
            return {"message": "Package uploaded successfully", "version": package_metadata.version}
        else:
            raise HTTPException(status_code=500, detail="Failed to publish package")
            
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid metadata JSON")
    except Exception as e:
        logger.error(f"Upload failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/packages/{package_name}/{version}")
async def delete_package(package_name: str, version: str, token: str = Depends(verify_token)):
    """Delete a specific package version."""
    try:
        success = registry.delete_package(package_name, version)
        if success:
            logger.info(f"Deleted package {package_name} v{version}")
            return {"message": "Package deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Package version not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/search")
async def search_packages(q: str):
    """Search packages by name or description."""
    try:
        packages = registry.list_packages()
        results = [pkg for pkg in packages if q.lower() in pkg.lower()]
        return {"query": q, "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    # Ensure directories exist
    REGISTRY_DATA_DIR.mkdir(parents=True, exist_ok=True)
    REGISTRY_LOG_DIR.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Starting Runa Registry Server on {REGISTRY_HOST}:{REGISTRY_PORT}")
    logger.info(f"Data directory: {REGISTRY_DATA_DIR}")
    logger.info(f"Log directory: {REGISTRY_LOG_DIR}")
    
    uvicorn.run(
        "registry_server:app",
        host=REGISTRY_HOST,
        port=REGISTRY_PORT,
        reload=False,
        workers=1
    )
EOF

# Create entrypoint script
COPY --chown=registry:registry <<'EOF' ./entrypoint.sh
#!/bin/bash
set -e

# Initialize directories
mkdir -p /var/lib/runa-registry
mkdir -p /var/log/runa-registry
mkdir -p /etc/runa-registry

# Set permissions
chown -R registry:registry /var/lib/runa-registry
chown -R registry:registry /var/log/runa-registry
chown -R registry:registry /etc/runa-registry

# Start registry server
echo "Starting Runa Package Registry Server..."
exec python registry_server.py
EOF

# Make scripts executable
RUN chmod +x ./registry_server.py && \
    chmod +x ./entrypoint.sh

# Switch to registry user
USER registry

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:$REGISTRY_PORT/health || exit 1

# Expose registry port
EXPOSE $REGISTRY_PORT

# Default command
ENTRYPOINT ["./entrypoint.sh"]

# Labels
LABEL maintainer="Sybertnetics AI Solutions <dev@sybertnetics.com>"
LABEL version="1.0.0"
LABEL description="Runa Package Registry Server - Universal package management"
LABEL org.opencontainers.image.source="https://github.com/sybertnetics/runa"
LABEL org.opencontainers.image.documentation="https://docs.runa.dev/registry"
LABEL org.opencontainers.image.licenses="MIT"