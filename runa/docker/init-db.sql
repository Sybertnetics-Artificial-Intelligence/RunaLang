-- Runa Package Registry Database Schema
-- PostgreSQL initialization script for package metadata storage

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "btree_gin";

-- Create tables
CREATE TABLE IF NOT EXISTS packages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    author VARCHAR(255),
    homepage VARCHAR(500),
    repository VARCHAR(500),
    license VARCHAR(100),
    keywords TEXT[], -- Array of keywords for search
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    download_count BIGINT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS package_versions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    package_id UUID NOT NULL REFERENCES packages(id) ON DELETE CASCADE,
    version VARCHAR(50) NOT NULL,
    description TEXT,
    dependencies JSONB DEFAULT '{}', -- Store as JSON for flexible querying
    target_languages TEXT[], -- Array of supported target languages
    runa_version VARCHAR(50), -- Required Runa version
    file_path VARCHAR(500), -- Path to package file on disk
    file_size BIGINT,
    file_hash VARCHAR(128), -- SHA-256 hash of package file
    published_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_yanked BOOLEAN DEFAULT FALSE, -- Mark versions as yanked but keep them
    yank_reason TEXT,
    download_count BIGINT DEFAULT 0,
    UNIQUE(package_id, version)
);

CREATE TABLE IF NOT EXISTS package_tags (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    package_id UUID NOT NULL REFERENCES packages(id) ON DELETE CASCADE,
    tag VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(package_id, tag)
);

CREATE TABLE IF NOT EXISTS api_tokens (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    token_hash VARCHAR(128) NOT NULL UNIQUE, -- Hashed API token
    name VARCHAR(255) NOT NULL, -- Token name/description
    permissions JSONB DEFAULT '{}', -- Token permissions
    expires_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_used_at TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS download_stats (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    package_id UUID NOT NULL REFERENCES packages(id) ON DELETE CASCADE,
    version_id UUID REFERENCES package_versions(id) ON DELETE CASCADE,
    downloaded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ip_address INET,
    user_agent TEXT,
    country_code VARCHAR(2),
    INDEX(downloaded_at),
    INDEX(package_id, downloaded_at)
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_packages_name ON packages(name);
CREATE INDEX IF NOT EXISTS idx_packages_keywords ON packages USING GIN(keywords);
CREATE INDEX IF NOT EXISTS idx_packages_active ON packages(is_active);

CREATE INDEX IF NOT EXISTS idx_package_versions_package_id ON package_versions(package_id);
CREATE INDEX IF NOT EXISTS idx_package_versions_version ON package_versions(version);
CREATE INDEX IF NOT EXISTS idx_package_versions_published ON package_versions(published_at);
CREATE INDEX IF NOT EXISTS idx_package_versions_target_langs ON package_versions USING GIN(target_languages);
CREATE INDEX IF NOT EXISTS idx_package_versions_dependencies ON package_versions USING GIN(dependencies);

CREATE INDEX IF NOT EXISTS idx_package_tags_package_id ON package_tags(package_id);
CREATE INDEX IF NOT EXISTS idx_package_tags_tag ON package_tags(tag);

CREATE INDEX IF NOT EXISTS idx_api_tokens_hash ON api_tokens(token_hash);
CREATE INDEX IF NOT EXISTS idx_api_tokens_active ON api_tokens(is_active);

CREATE INDEX IF NOT EXISTS idx_download_stats_package_id ON download_stats(package_id);
CREATE INDEX IF NOT EXISTS idx_download_stats_downloaded_at ON download_stats(downloaded_at);

-- Create functions and triggers for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_packages_updated_at 
    BEFORE UPDATE ON packages 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Create function to increment download counts
CREATE OR REPLACE FUNCTION record_download(
    p_package_name VARCHAR(255),
    p_version VARCHAR(50) DEFAULT NULL,
    p_ip_address INET DEFAULT NULL,
    p_user_agent TEXT DEFAULT NULL
)
RETURNS VOID AS $$
DECLARE
    v_package_id UUID;
    v_version_id UUID;
BEGIN
    -- Get package ID
    SELECT id INTO v_package_id 
    FROM packages 
    WHERE name = p_package_name AND is_active = TRUE;
    
    IF v_package_id IS NULL THEN
        RAISE EXCEPTION 'Package not found: %', p_package_name;
    END IF;
    
    -- Update package download count
    UPDATE packages 
    SET download_count = download_count + 1 
    WHERE id = v_package_id;
    
    -- If version specified, update version download count
    IF p_version IS NOT NULL THEN
        SELECT id INTO v_version_id 
        FROM package_versions 
        WHERE package_id = v_package_id AND version = p_version AND is_yanked = FALSE;
        
        IF v_version_id IS NOT NULL THEN
            UPDATE package_versions 
            SET download_count = download_count + 1 
            WHERE id = v_version_id;
        END IF;
    END IF;
    
    -- Record download stat
    INSERT INTO download_stats (package_id, version_id, ip_address, user_agent)
    VALUES (v_package_id, v_version_id, p_ip_address, p_user_agent);
END;
$$ LANGUAGE plpgsql;

-- Create function for package search
CREATE OR REPLACE FUNCTION search_packages(
    p_query TEXT,
    p_limit INTEGER DEFAULT 20,
    p_offset INTEGER DEFAULT 0
)
RETURNS TABLE(
    package_name VARCHAR(255),
    description TEXT,
    author VARCHAR(255),
    latest_version VARCHAR(50),
    download_count BIGINT,
    updated_at TIMESTAMP WITH TIME ZONE
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        p.name,
        p.description,
        p.author,
        pv.version,
        p.download_count,
        p.updated_at
    FROM packages p
    LEFT JOIN LATERAL (
        SELECT version
        FROM package_versions pv2
        WHERE pv2.package_id = p.id AND pv2.is_yanked = FALSE
        ORDER BY pv2.published_at DESC
        LIMIT 1
    ) pv ON true
    WHERE 
        p.is_active = TRUE AND
        (
            p.name ILIKE '%' || p_query || '%' OR
            p.description ILIKE '%' || p_query || '%' OR
            p.keywords && ARRAY[p_query] OR
            EXISTS (
                SELECT 1 FROM package_tags pt 
                WHERE pt.package_id = p.id AND pt.tag ILIKE '%' || p_query || '%'
            )
        )
    ORDER BY 
        CASE 
            WHEN p.name ILIKE p_query || '%' THEN 1
            WHEN p.name ILIKE '%' || p_query || '%' THEN 2
            ELSE 3
        END,
        p.download_count DESC,
        p.updated_at DESC
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;

-- Insert some sample data for development
INSERT INTO packages (name, description, author, keywords) VALUES
    ('runa-stdlib', 'Runa Standard Library with common utilities', 'Sybertnetics Team', ARRAY['stdlib', 'utilities', 'core']),
    ('runa-web', 'Web development utilities for Runa', 'Sybertnetics Team', ARRAY['web', 'http', 'api']),
    ('runa-ml', 'Machine learning package for Runa', 'Sybertnetics Team', ARRAY['ml', 'machine-learning', 'ai'])
ON CONFLICT (name) DO NOTHING;

-- Insert sample versions
WITH pkg_data AS (
    SELECT id, name FROM packages WHERE name IN ('runa-stdlib', 'runa-web', 'runa-ml')
)
INSERT INTO package_versions (package_id, version, description, dependencies, target_languages, runa_version)
SELECT 
    id,
    '1.0.0',
    'Initial release of ' || name,
    '{}',
    ARRAY['python', 'javascript', 'typescript', 'java', 'cpp'],
    '1.0.0'
FROM pkg_data
ON CONFLICT (package_id, version) DO NOTHING;

-- Grant permissions to registry user (if exists)
DO $$
BEGIN
    IF EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'runa') THEN
        GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO runa;
        GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO runa;
        GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO runa;
    END IF;
END
$$;