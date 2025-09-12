use anyhow::Result;
use std::path::Path;
use std::fs;

pub fn read_file_to_string<P: AsRef<Path>>(path: P) -> Result<String> {
    let content = fs::read_to_string(&path)
        .map_err(|e| anyhow::anyhow!("Failed to read file {}: {}", path.as_ref().display(), e))?;
    Ok(content)
}

pub fn write_string_to_file<P: AsRef<Path>>(path: P, content: &str) -> Result<()> {
    fs::write(&path, content)
        .map_err(|e| anyhow::anyhow!("Failed to write file {}: {}", path.as_ref().display(), e))?;
    Ok(())
}

pub fn ensure_directory_exists<P: AsRef<Path>>(path: P) -> Result<()> {
    fs::create_dir_all(&path)
        .map_err(|e| anyhow::anyhow!("Failed to create directory {}: {}", path.as_ref().display(), e))?;
    Ok(())
}

pub fn file_exists<P: AsRef<Path>>(path: P) -> bool {
    path.as_ref().exists()
}

pub fn get_file_extension<P: AsRef<Path>>(path: P) -> Option<String> {
    path.as_ref()
        .extension()
        .and_then(|ext| ext.to_str())
        .map(|s| s.to_string())
}