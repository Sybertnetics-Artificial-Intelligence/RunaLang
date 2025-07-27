# Runa Compression Ecosystem Documentation

## Overview

The Runa Standard Library provides a comprehensive compression ecosystem that supports multiple compression algorithms and archive formats. This production-ready system offers a unified interface for all compression operations while providing direct access to individual compression modules for specialized use cases.

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Unified Compression Interface](#unified-compression-interface)
3. [Individual Compression Modules](#individual-compression-modules)
4. [Archive Format Support](#archive-format-support)
5. [Configuration and Error Handling](#configuration-and-error-handling)
6. [Performance and Memory Management](#performance-and-memory-management)
7. [Cross-Platform Compatibility](#cross-platform-compatibility)
8. [Usage Examples](#usage-examples)
9. [Best Practices](#best-practices)
10. [API Reference](#api-reference)

## Architecture Overview

The compression ecosystem follows a modular design with the following components:

```
compress.runa           # Unified interface for all compression algorithms
├── bz2.runa           # BZIP2 compression implementation
├── gzip.runa          # GZIP/DEFLATE compression with RFC compliance
├── lzma.runa          # LZMA/XZ compression for high efficiency
├── tar.runa           # TAR archive format with compression integration
└── zip.runa           # ZIP archive format with encryption support
```

### Design Principles

- **Unified Interface**: Single API for all compression algorithms
- **Modular Design**: Individual modules for specialized requirements
- **Production Ready**: Comprehensive error handling and validation
- **Performance Optimized**: Memory-efficient streaming operations
- **Standards Compliant**: Full adherence to RFC specifications
- **Cross-Platform**: Consistent behavior across all platforms

## Unified Compression Interface

The `compress.runa` module provides a unified API for all compression operations.

### Basic Usage

```runa
Import "stdlib/compress/compress" as compress

Note:Compress data using any algorithm
Let compression_result be compress.compress_data with:
    data as "Hello, World! This is test data for compression."
    algorithm as "gzip"
    config as None

Match compression_result:
    When "success":
        Display "Compressed " plus compression_result.original_size as String plus 
                " bytes to " plus compression_result.compressed_size as String plus " bytes"
        Display "Compression ratio: " plus compression_result.compression_ratio as String
    When "error":
        Display "Compression failed: " plus compression_result.error_message
```

### Supported Algorithms

| Algorithm | Description | Best Use Cases |
|-----------|-------------|----------------|
| `gzip` | GZIP/DEFLATE compression | Web content, HTTP responses, general purpose |
| `bzip2` | BZIP2 compression | High compression ratio, archival storage |
| `lzma` | LZMA/XZ compression | Maximum compression efficiency, long-term storage |

### Configuration Options

```runa
Note:Create custom compression configuration
Let config be compress.create_compression_config with:
    compression_level as 6              Note:1-9, higher = better compression
    enable_verification as true         Note:Verify compressed data integrity
    buffer_size as 65536               Note:Memory buffer size in bytes
    memory_limit as 8388608            Note:Maximum memory usage (8MB)
    enable_streaming as false          Note:Enable streaming compression
    normalize_line_endings as false   Note:Normalize line endings for text
    preserve_file_attributes as true  Note:Preserve file metadata
```

## Individual Compression Modules

### BZ2 Module (`bz2.runa`)

BZIP2 compression using the Burrows-Wheeler transform algorithm.

**Characteristics:**
- High compression ratio
- Slower compression/decompression speed
- Good for archival and backup applications
- Block-based compression (typically 900KB blocks)

**Usage:**
```runa
Import "stdlib/compress/bz2" as bz2

Let bz2_config be bz2.create_bz2_config with:
    compression_level as 9
    enable_verification as true
    block_size as 900000  Note:900KB blocks

Let result be bz2.bz2_compress with:
    data as text_data
    config as bz2_config
```

**Configuration Options:**
- `compression_level`: 1-9 (default: 6)
- `block_size`: 100KB-900KB (default: 900KB)
- `enable_verification`: CRC32 verification (default: true)
- `memory_limit`: Maximum memory usage
- `enable_streaming`: Streaming compression support

### GZIP Module (`gzip.runa`)

GZIP/DEFLATE compression with full RFC 1952 compliance.

**Characteristics:**
- Fast compression and decompression
- Wide compatibility (web standards)
- RFC 1952 GZIP header support
- DEFLATE algorithm (RFC 1951)

**Usage:**
```runa
Import "stdlib/compress/gzip" as gzip

Let gzip_config be gzip.create_gzip_config with:
    compression_level as 6
    use_gzip_headers as true
    include_filename as true
    filename as "data.txt"
    include_comment as true
    comment as "Compressed with Runa GZIP"

Let result be gzip.gzip_compress with:
    data as web_content
    config as gzip_config
```

**Configuration Options:**
- `compression_level`: 1-9 (default: 6)
- `window_size`: 8-15 (default: 15)
- `use_gzip_headers`: Include GZIP headers (default: true)
- `include_filename`: Include original filename
- `include_comment`: Include file comment
- `include_modification_time`: Include timestamp

**DEFLATE-Only Compression:**
```runa
Note:For HTTP Content-Encoding: deflate
Let deflate_result be gzip.deflate_compress with:
    data as http_response_body
    config as None
```

### LZMA Module (`lzma.runa`)

LZMA/XZ compression for maximum compression efficiency.

**Characteristics:**
- Highest compression ratios
- Slower compression (faster decompression)
- XZ format support
- Dictionary-based compression

**Usage:**
```runa
Import "stdlib/compress/lzma" as lzma

Let lzma_config be lzma.create_lzma_config with:
    compression_level as 6
    enable_extreme_mode as false
    dictionary_size as 16777216  Note:16MB
    enable_integrity_check as true

Let result be lzma.lzma_compress with:
    data as large_dataset
    config as lzma_config
```

**Configuration Options:**
- `compression_level`: 0-9 (default: 6)
- `enable_extreme_mode`: Maximum compression (slower)
- `dictionary_size`: 4KB-1.5GB (default: 16MB)
- `enable_integrity_check`: SHA-256 checksum
- `match_finder`: Algorithm for finding matches

## Archive Format Support

### TAR Module (`tar.runa`)

TAR archive format with compression integration.

**Supported Formats:**
- POSIX ustar format
- GNU tar extensions
- pax (POSIX.1-2001) format

**Usage:**
```runa
Import "stdlib/compress/tar" as tar

Let tar_config be tar.create_tar_config with:
    compression_algorithm as "gzip"
    compression_level as 6
    archive_format as "ustar"
    preserve_permissions as true
    preserve_timestamps as true

Note:Create compressed TAR archive
Let files_to_archive be list containing "file1.txt", "file2.txt", "directory/"
Let result be tar.create_tar_archive with:
    files as files_to_archive
    archive_path as "backup.tar.gz"
    config as tar_config
```

**Features:**
- Recursive directory archiving
- Metadata preservation (permissions, timestamps, ownership)
- Symbolic link handling
- Large file support (>8GB)
- Incremental archiving support

### ZIP Module (`zip.runa`)

ZIP archive format with compression and encryption.

**Supported Features:**
- ZIP32 and ZIP64 formats
- Multiple compression methods (Store, Deflate, BZIP2, LZMA)
- Password-based encryption (Traditional, AES-128/192/256)
- Unicode filename support

**Usage:**
```runa
Import "stdlib/compress/zip" as zip

Let zip_config be zip.create_zip_config with:
    compression_method as "deflate"
    compression_level as 6
    enable_zip64 as true
    enable_encryption as false

Note:Create ZIP archive
Let files_to_zip be list containing "document.pdf", "images/", "data.csv"
Let result be zip.create_zip_archive with:
    files as files_to_zip
    archive_path as "package.zip"
    config as zip_config
```

**Encryption Support:**
```runa
Note:Create encrypted ZIP archive
Let encrypted_config be zip.create_zip_config with:
    compression_method as "lzma"
    enable_encryption as true
    encryption_method as "aes256"
    password as "secure_password_123"

Let result be zip.create_zip_archive with:
    files as sensitive_files
    archive_path as "secure.zip"
    config as encrypted_config
```

## Configuration and Error Handling

### Validation

All configuration objects are validated before use:

```runa
Let config be compress.create_compression_config with:
    compression_level as 15  Note:Invalid level

Let validation_result be compress.validate_compression_config with config as config
If not validation_result.is_valid:
    Display "Configuration error: " plus validation_result.error_message
    For each suggestion in validation_result.suggestions:
        Display "Suggestion: " plus suggestion
```

### Error Codes

| Error Code | Description | Suggested Action |
|------------|-------------|------------------|
| `COMPRESS_EMPTY_INPUT` | Empty or null data provided | Provide non-empty data |
| `COMPRESS_INVALID_CONFIG` | Invalid configuration parameters | Check configuration values |
| `COMPRESS_UNSUPPORTED_ALGORITHM` | Algorithm not supported | Use supported algorithm |
| `COMPRESS_MEMORY_LIMIT_EXCEEDED` | Memory usage exceeded limit | Increase limit or reduce data |
| `COMPRESS_CORRUPTED_DATA` | Data corruption detected | Check data integrity |

### Error Recovery

```runa
Let compression_result be compress.compress_data with:
    data as large_data
    algorithm as "gzip"
    config as None

Match compression_result:
    When "error":
        If compression_result.error_code is equal to "COMPRESS_MEMORY_LIMIT_EXCEEDED":
            Note:Retry with streaming compression
            Let streaming_config be compress.create_compression_config with:
                enable_streaming as true
                buffer_size as 32768
            
            Let retry_result be compress.compress_data with:
                data as large_data
                algorithm as "gzip"
                config as streaming_config
```

## Performance and Memory Management

### Memory Efficiency

```runa
Note:Configure memory limits for large files
Let memory_config be compress.create_compression_config with:
    memory_limit as 67108864      Note:64MB limit
    buffer_size as 16384          Note:16KB buffers
    enable_streaming as true      Note:Stream processing

Note:Monitor memory usage
Let result be compress.compress_data with:
    data as very_large_file
    algorithm as "lzma"
    config as memory_config

If result.memory_used is greater than 50000000:  Note:50MB
    Display "Warning: High memory usage detected"
```

### Streaming Operations

For large files or real-time compression:

```runa
Note:Streaming compression for web responses
Let streaming_config be gzip.create_gzip_config with:
    compression_level as 6
    enable_streaming as true
    flush_mode as "sync_flush"

Let data_chunks be list containing chunk1, chunk2, chunk3
Let result be gzip.gzip_compress_streaming with:
    data_chunks as data_chunks
    config as streaming_config
```

### Performance Benchmarks

Typical performance characteristics (1MB text file):

| Algorithm | Compression Ratio | Compression Speed | Decompression Speed |
|-----------|------------------|-------------------|-------------------|
| GZIP (level 1) | 3.2:1 | Very Fast | Very Fast |
| GZIP (level 6) | 4.1:1 | Fast | Fast |
| GZIP (level 9) | 4.3:1 | Medium | Fast |
| BZIP2 (level 6) | 4.8:1 | Slow | Medium |
| LZMA (level 6) | 5.2:1 | Very Slow | Fast |

## Cross-Platform Compatibility

### Line Ending Normalization

```runa
Note:Handle cross-platform text files
Let cross_platform_config be compress.create_compression_config with:
    normalize_line_endings as true
    target_line_ending as "LF"  Note:Unix-style

Let result be compress.compress_data with:
    data as text_with_mixed_endings
    algorithm as "gzip"
    config as cross_platform_config
```

### Character Encoding

The compression ecosystem handles UTF-8 encoding automatically:

```runa
Note:Unicode text compression
Let unicode_text be "Hello 世界 🌍 Здравствуй мир"
Let result be compress.compress_data with:
    data as unicode_text
    algorithm as "gzip"
    config as None

Note:Unicode is preserved exactly
Match result:
    When "success":
        Let decompressed be compress.decompress_data with:
            compressed_data as result.compressed_data
            algorithm as "gzip"
            config as None
        Note:decompressed.decompressed_data equals original unicode_text
```

## Usage Examples

### Web Content Compression

```runa
Note:HTTP response compression
Import "stdlib/compress/gzip" as gzip

Process called "compress_http_response" that takes content as String returns String:
    Let web_config be gzip.create_gzip_config with:
        compression_level as 6
        use_gzip_headers as true
        include_modification_time as false
    
    Let result be gzip.gzip_compress with:
        data as content
        config as web_config
    
    Match result:
        When "success":
            Return result.compressed_data
        When "error":
            Return content  Note:Return uncompressed if compression fails
```

### Backup and Archival

```runa
Note:Create compressed backup
Import "stdlib/compress/tar" as tar

Process called "create_backup" that takes source_files as List[String] and backup_path as String returns Boolean:
    Let backup_config be tar.create_tar_config with:
        compression_algorithm as "lzma"
        compression_level as 9
        preserve_permissions as true
        preserve_timestamps as true
        enable_verification as true
    
    Let result be tar.create_tar_archive with:
        files as source_files
        archive_path as backup_path
        config as backup_config
    
    Match result:
        When "success":
            Display "Backup created: " plus backup_path
            Display "Files archived: " plus result.files_processed as String
            Display "Compression ratio: " plus result.compression_ratio as String
            Return true
        When "error":
            Display "Backup failed: " plus result.error_message
            Return false
```

### Data Distribution

```runa
Note:Package files for distribution
Import "stdlib/compress/zip" as zip

Process called "package_for_distribution" that takes files as List[String] and output_path as String returns Boolean:
    Let distribution_config be zip.create_zip_config with:
        compression_method as "deflate"
        compression_level as 6
        enable_unicode_filenames as true
        archive_comment as "Package created with Runa compression"
    
    Let result be zip.create_zip_archive with:
        files as files
        archive_path as output_path
        config as distribution_config
    
    Match result:
        When "success":
            Note:Verify archive integrity
            Let verification_result be zip.verify_zip_archive with:
                archive_path as output_path
                config as distribution_config
            
            If verification_result.success and verification_result.is_valid:
                Display "Package created and verified: " plus output_path
                Return true
            Otherwise:
                Display "Package verification failed"
                Return false
        When "error":
            Display "Packaging failed: " plus result.error_message
            Return false
```

## Best Practices

### Algorithm Selection

1. **GZIP**: Choose for web content, HTTP responses, and general-purpose compression
2. **BZIP2**: Use for archival storage where compression ratio is more important than speed
3. **LZMA**: Select for maximum compression efficiency and long-term storage

### Configuration Guidelines

1. **Compression Level**: Start with level 6 for balanced performance
2. **Memory Limits**: Set appropriate limits based on system resources
3. **Streaming**: Enable for large files or real-time applications
4. **Verification**: Always enable for critical data

### Error Handling

1. **Validate Configurations**: Always validate before compression
2. **Handle Failures Gracefully**: Provide fallback mechanisms
3. **Log Errors**: Capture detailed error information for debugging
4. **Monitor Resources**: Track memory and processing time

### Performance Optimization

1. **Choose Appropriate Buffer Sizes**: 16KB-64KB for most applications
2. **Use Streaming for Large Files**: Prevents memory exhaustion
3. **Cache Configurations**: Reuse configuration objects
4. **Monitor Compression Ratios**: Adjust algorithms based on data characteristics

## API Reference

### Unified Interface (`compress.runa`)

#### Functions

- `compress_data(data: String, algorithm: String, config: Optional[CompressionConfig]) -> CompressionResult`
- `decompress_data(compressed_data: String, algorithm: String, config: Optional[CompressionConfig]) -> DecompressionResult`
- `create_compression_config(...) -> CompressionConfig`
- `validate_compression_config(config: CompressionConfig) -> ValidationResult`

### BZ2 Module (`bz2.runa`)

#### Functions

- `bz2_compress(data: String, config: Optional[BZ2Config]) -> BZ2CompressResult`
- `bz2_decompress(compressed_data: String, config: Optional[BZ2Config]) -> BZ2DecompressResult`
- `create_bz2_config(...) -> BZ2Config`

### GZIP Module (`gzip.runa`)

#### Functions

- `gzip_compress(data: String, config: Optional[GZIPConfig]) -> GZIPCompressResult`
- `gzip_decompress(compressed_data: String, config: Optional[GZIPConfig]) -> GZIPDecompressResult`
- `deflate_compress(data: String, config: Optional[GZIPConfig]) -> DeflateCompressResult`
- `deflate_decompress(compressed_data: String, config: Optional[GZIPConfig]) -> DeflateDecompressResult`

### LZMA Module (`lzma.runa`)

#### Functions

- `lzma_compress(data: String, config: Optional[LZMAConfig]) -> LZMACompressResult`
- `lzma_decompress(compressed_data: String, config: Optional[LZMAConfig]) -> LZMADecompressResult`
- `create_lzma_config(...) -> LZMAConfig`

### TAR Module (`tar.runa`)

#### Functions

- `create_tar_archive(files: List[String], archive_path: String, config: Optional[TARConfig]) -> TARResult`
- `extract_tar_archive(archive_path: String, output_directory: String, config: Optional[TARConfig]) -> TARResult`
- `list_tar_contents(archive_path: String, config: Optional[TARConfig]) -> Dictionary[String, Any]`

### ZIP Module (`zip.runa`)

#### Functions

- `create_zip_archive(files: List[String], archive_path: String, config: Optional[ZIPConfig]) -> ZIPResult`
- `extract_zip_archive(archive_path: String, output_directory: String, config: Optional[ZIPConfig]) -> ZIPResult`
- `list_zip_contents(archive_path: String, config: Optional[ZIPConfig]) -> Dictionary[String, Any]`
- `add_to_zip_archive(archive_path: String, files: List[String], config: Optional[ZIPConfig]) -> ZIPResult`

---

*This documentation covers the complete Runa compression ecosystem. For additional examples and advanced usage patterns, refer to the test suite in `tests/unit/stdlib/test_compress.runa`.*