# Compress Module

The Compress module provides comprehensive data compression utilities including multiple compression algorithms, archive handling, and advanced compression features.

## Overview

The Compress module is designed to handle all data compression operations in Runa, from basic compression/decompression to advanced features like parallel processing, encryption, and adaptive compression. It supports multiple compression algorithms and archive formats.

## Core Features

- **Multiple Compression Algorithms**: Gzip, Bzip2, LZMA, LZ4, Zstd, Deflate, Brotli, LZOP
- **Archive Support**: ZIP, TAR, 7Z, RAR formats
- **Streaming Compression**: Real-time compression/decompression
- **Parallel Processing**: Multi-threaded compression
- **Encryption**: Compressed data encryption
- **Checksums**: Data integrity verification
- **Metadata**: Compression metadata handling
- **Deduplication**: Data deduplication
- **Adaptive Compression**: Automatic algorithm selection
- **Predictive Compression**: ML-based compression
- **Advanced Algorithms**: Wavelet, fractal, neural, quantum compression

## Basic Usage

### Simple Compression

```runa
Note: Compress data using different algorithms
:End Note

Let data be "Hello, World! This is a test string for compression."
Let compressed be compress data with algorithm as "gzip"
Let decompressed be decompress data compressed with algorithm as "gzip"

Assert decompressed equals data
```

### File Compression

```runa
Note: Compress and decompress files
:End Note

Let compressed be compress file "input.txt" to "output.gz" with algorithm as "gzip"
Let decompressed be decompress file "output.gz" to "decompressed.txt" with algorithm as "gzip"
```

### Directory Compression

```runa
Note: Compress entire directories
:End Note

Let compressed be compress directory "data_folder" to "archive.gz" with algorithm as "gzip"
Let extracted be decompress directory "archive.gz" to "extracted_folder" with algorithm as "gzip"
```

## API Reference

### Basic Compression Operations

#### `compress_data(data: String, algorithm: String) -> List[Integer]`
Compresses string data using specified algorithm.

**Parameters:**
- `data`: String data to compress
- `algorithm`: Compression algorithm (gzip, bzip2, lzma, lz4, zstd, deflate, brotli, lzop)

**Returns:** Compressed data as list of integers

**Example:**
```runa
Let data be "Hello, World!"
Let compressed be compress data with algorithm as "gzip"
```

#### `compress_bytes(data: List[Integer], algorithm: String) -> List[Integer]`
Compresses binary data using specified algorithm.

**Parameters:**
- `data`: Binary data as list of integers
- `algorithm`: Compression algorithm

**Returns:** Compressed data as list of integers

#### `decompress_data(compressed_data: List[Integer], algorithm: String) -> String`
Decompresses data to string using specified algorithm.

**Parameters:**
- `compressed_data`: Compressed data as list of integers
- `algorithm`: Compression algorithm

**Returns:** Decompressed string data

#### `decompress_bytes(compressed_data: List[Integer], algorithm: String) -> List[Integer]`
Decompresses data to binary using specified algorithm.

**Parameters:**
- `compressed_data`: Compressed data as list of integers
- `algorithm`: Compression algorithm

**Returns:** Decompressed binary data

### File Operations

#### `compress_file(input_file: String, output_file: String, algorithm: String) -> Boolean`
Compresses a file using specified algorithm.

**Parameters:**
- `input_file`: Path to input file
- `output_file`: Path to output file
- `algorithm`: Compression algorithm

**Returns:** True if compression successful

#### `decompress_file(input_file: String, output_file: String, algorithm: String) -> Boolean`
Decompresses a file using specified algorithm.

**Parameters:**
- `input_file`: Path to compressed file
- `output_file`: Path to output file
- `algorithm`: Compression algorithm

**Returns:** True if decompression successful

#### `compress_directory(input_dir: String, output_file: String, algorithm: String) -> Boolean`
Compresses a directory using specified algorithm.

**Parameters:**
- `input_dir`: Path to input directory
- `output_file`: Path to output file
- `algorithm`: Compression algorithm

**Returns:** True if compression successful

#### `decompress_directory(input_file: String, output_dir: String, algorithm: String) -> Boolean`
Decompresses a file to directory using specified algorithm.

**Parameters:**
- `input_file`: Path to compressed file
- `output_dir`: Path to output directory
- `algorithm`: Compression algorithm

**Returns:** True if decompression successful

### Compression Analysis

#### `get_compression_ratio(original_size: Integer, compressed_size: Integer) -> Number`
Calculates compression ratio.

**Parameters:**
- `original_size`: Original data size in bytes
- `compressed_size`: Compressed data size in bytes

**Returns:** Compression ratio (0.0 to 1.0)

#### `get_compression_speed(original_size: Integer, compression_time: Number) -> Number`
Calculates compression speed.

**Parameters:**
- `original_size`: Original data size in bytes
- `compression_time`: Compression time in seconds

**Returns:** Compression speed in bytes per second

#### `estimate_compressed_size(data: String, algorithm: String) -> Integer`
Estimates compressed data size.

**Parameters:**
- `data`: Data to estimate
- `algorithm`: Compression algorithm

**Returns:** Estimated compressed size in bytes

#### `is_compressed(data: List[Integer], algorithm: String) -> Boolean`
Checks if data is compressed with specified algorithm.

**Parameters:**
- `data`: Data to check
- `algorithm`: Compression algorithm

**Returns:** True if data is compressed

#### `get_compression_info(compressed_data: List[Integer]) -> Dictionary[String, Any]`
Gets compression information.

**Parameters:**
- `compressed_data`: Compressed data

**Returns:** Compression information dictionary

### Streaming Compression

#### `create_compression_stream(algorithm: String) -> Dictionary[String, Any]`
Creates compression stream.

**Parameters:**
- `algorithm`: Compression algorithm

**Returns:** Compression stream object

#### `compress_stream(stream: Dictionary[String, Any], data: String) -> List[Integer]`
Compresses data through stream.

**Parameters:**
- `stream`: Compression stream
- `data`: Data to compress

**Returns:** Compressed data

#### `compress_stream_bytes(stream: Dictionary[String, Any], data: List[Integer]) -> List[Integer]`
Compresses binary data through stream.

**Parameters:**
- `stream`: Compression stream
- `data`: Binary data to compress

**Returns:** Compressed data

#### `finish_compression_stream(stream: Dictionary[String, Any]) -> List[Integer]`
Finishes compression stream.

**Parameters:**
- `stream`: Compression stream

**Returns:** Final compressed data

#### `create_decompression_stream(algorithm: String) -> Dictionary[String, Any]`
Creates decompression stream.

**Parameters:**
- `algorithm`: Compression algorithm

**Returns:** Decompression stream object

#### `decompress_stream(stream: Dictionary[String, Any], data: List[Integer]) -> String`
Decompresses data through stream.

**Parameters:**
- `stream`: Decompression stream
- `data`: Compressed data

**Returns:** Decompressed string

#### `decompress_stream_bytes(stream: Dictionary[String, Any], data: List[Integer]) -> List[Integer]`
Decompresses binary data through stream.

**Parameters:**
- `stream`: Decompression stream
- `data`: Compressed data

**Returns:** Decompressed binary data

#### `finish_decompression_stream(stream: Dictionary[String, Any]) -> String`
Finishes decompression stream.

**Parameters:**
- `stream`: Decompression stream

**Returns:** Final decompressed data

### Algorithm-Specific Operations

#### Gzip Compression

#### `create_gzip_compressor() -> Dictionary[String, Any]`
Creates Gzip compressor.

#### `create_gzip_decompressor() -> Dictionary[String, Any]`
Creates Gzip decompressor.

#### `compress_gzip(data: String) -> List[Integer]`
Compresses data with Gzip.

#### `decompress_gzip(compressed_data: List[Integer]) -> String`
Decompresses data with Gzip.

#### `compress_gzip_file(input_file: String, output_file: String) -> Boolean`
Compresses file with Gzip.

#### `decompress_gzip_file(input_file: String, output_file: String) -> Boolean`
Decompresses file with Gzip.

#### Bzip2 Compression

#### `create_bzip2_compressor() -> Dictionary[String, Any]`
Creates Bzip2 compressor.

#### `create_bzip2_decompressor() -> Dictionary[String, Any]`
Creates Bzip2 decompressor.

#### `compress_bzip2(data: String) -> List[Integer]`
Compresses data with Bzip2.

#### `decompress_bzip2(compressed_data: List[Integer]) -> String`
Decompresses data with Bzip2.

#### `compress_bzip2_file(input_file: String, output_file: String) -> Boolean`
Compresses file with Bzip2.

#### `decompress_bzip2_file(input_file: String, output_file: String) -> Boolean`
Decompresses file with Bzip2.

#### LZMA Compression

#### `create_lzma_compressor() -> Dictionary[String, Any]`
Creates LZMA compressor.

#### `create_lzma_decompressor() -> Dictionary[String, Any]`
Creates LZMA decompressor.

#### `compress_lzma(data: String) -> List[Integer]`
Compresses data with LZMA.

#### `decompress_lzma(compressed_data: List[Integer]) -> String`
Decompresses data with LZMA.

#### `compress_lzma_file(input_file: String, output_file: String) -> Boolean`
Compresses file with LZMA.

#### `decompress_lzma_file(input_file: String, output_file: String) -> Boolean`
Decompresses file with LZMA.

#### LZ4 Compression

#### `create_lz4_compressor() -> Dictionary[String, Any]`
Creates LZ4 compressor.

#### `create_lz4_decompressor() -> Dictionary[String, Any]`
Creates LZ4 decompressor.

#### `compress_lz4(data: String) -> List[Integer]`
Compresses data with LZ4.

#### `decompress_lz4(compressed_data: List[Integer]) -> String`
Decompresses data with LZ4.

#### `compress_lz4_file(input_file: String, output_file: String) -> Boolean`
Compresses file with LZ4.

#### `decompress_lz4_file(input_file: String, output_file: String) -> Boolean`
Decompresses file with LZ4.

#### Zstd Compression

#### `create_zstd_compressor() -> Dictionary[String, Any]`
Creates Zstd compressor.

#### `create_zstd_decompressor() -> Dictionary[String, Any]`
Creates Zstd decompressor.

#### `compress_zstd(data: String) -> List[Integer]`
Compresses data with Zstd.

#### `decompress_zstd(compressed_data: List[Integer]) -> String`
Decompresses data with Zstd.

#### `compress_zstd_file(input_file: String, output_file: String) -> Boolean`
Compresses file with Zstd.

#### `decompress_zstd_file(input_file: String, output_file: String) -> Boolean`
Decompresses file with Zstd.

#### Deflate Compression

#### `create_deflate_compressor() -> Dictionary[String, Any]`
Creates Deflate compressor.

#### `create_deflate_decompressor() -> Dictionary[String, Any]`
Creates Deflate decompressor.

#### `compress_deflate(data: String) -> List[Integer]`
Compresses data with Deflate.

#### `decompress_deflate(compressed_data: List[Integer]) -> String`
Decompresses data with Deflate.

#### `compress_deflate_file(input_file: String, output_file: String) -> Boolean`
Compresses file with Deflate.

#### `decompress_deflate_file(input_file: String, output_file: String) -> Boolean`
Decompresses file with Deflate.

#### Brotli Compression

#### `create_brotli_compressor() -> Dictionary[String, Any]`
Creates Brotli compressor.

#### `create_brotli_decompressor() -> Dictionary[String, Any]`
Creates Brotli decompressor.

#### `compress_brotli(data: String) -> List[Integer]`
Compresses data with Brotli.

#### `decompress_brotli(compressed_data: List[Integer]) -> String`
Decompresses data with Brotli.

#### `compress_brotli_file(input_file: String, output_file: String) -> Boolean`
Compresses file with Brotli.

#### `decompress_brotli_file(input_file: String, output_file: String) -> Boolean`
Decompresses file with Brotli.

#### LZOP Compression

#### `create_lzop_compressor() -> Dictionary[String, Any]`
Creates LZOP compressor.

#### `create_lzop_decompressor() -> Dictionary[String, Any]`
Creates LZOP decompressor.

#### `compress_lzop(data: String) -> List[Integer]`
Compresses data with LZOP.

#### `decompress_lzop(compressed_data: List[Integer]) -> String`
Decompresses data with LZOP.

#### `compress_lzop_file(input_file: String, output_file: String) -> Boolean`
Compresses file with LZOP.

#### `decompress_lzop_file(input_file: String, output_file: String) -> Boolean`
Decompresses file with LZOP.

### Archive Operations

#### `create_archive(files: List[String], format: String) -> Dictionary[String, Any]`
Creates archive object.

**Parameters:**
- `files`: List of file paths to archive
- `format`: Archive format (zip, tar, 7z, rar)

**Returns:** Archive object

#### `add_file_to_archive(archive: Dictionary[String, Any], file_path: String, archive_path: String) -> Boolean`
Adds file to archive.

**Parameters:**
- `archive`: Archive object
- `file_path`: Path to file to add
- `archive_path`: Path within archive

**Returns:** True if file added successfully

#### `add_directory_to_archive(archive: Dictionary[String, Any], dir_path: String, archive_path: String) -> Boolean`
Adds directory to archive.

**Parameters:**
- `archive`: Archive object
- `dir_path`: Path to directory to add
- `archive_path`: Path within archive

**Returns:** True if directory added successfully

#### `extract_archive(archive: Dictionary[String, Any], output_dir: String) -> Boolean`
Extracts archive to directory.

**Parameters:**
- `archive`: Archive object
- `output_dir`: Output directory path

**Returns:** True if extraction successful

#### `list_archive_contents(archive: Dictionary[String, Any]) -> List[Dictionary[String, Any]]`
Lists archive contents.

**Parameters:**
- `archive`: Archive object

**Returns:** List of archive entries

#### `get_archive_info(archive: Dictionary[String, Any]) -> Dictionary[String, Any]`
Gets archive information.

**Parameters:**
- `archive`: Archive object

**Returns:** Archive information dictionary

### Archive Format-Specific Operations

#### ZIP Archives

#### `create_zip_archive(files: List[String]) -> Dictionary[String, Any]`
Creates ZIP archive.

#### `add_to_zip(zip_archive: Dictionary[String, Any], file_path: String, archive_path: String) -> Boolean`
Adds file to ZIP archive.

#### `extract_zip(zip_archive: Dictionary[String, Any], output_dir: String) -> Boolean`
Extracts ZIP archive.

#### `list_zip_contents(zip_archive: Dictionary[String, Any]) -> List[Dictionary[String, Any]]`
Lists ZIP archive contents.

#### TAR Archives

#### `create_tar_archive(files: List[String], compression: String) -> Dictionary[String, Any]`
Creates TAR archive.

#### `add_to_tar(tar_archive: Dictionary[String, Any], file_path: String, archive_path: String) -> Boolean`
Adds file to TAR archive.

#### `extract_tar(tar_archive: Dictionary[String, Any], output_dir: String) -> Boolean`
Extracts TAR archive.

#### `list_tar_contents(tar_archive: Dictionary[String, Any]) -> List[Dictionary[String, Any]]`
Lists TAR archive contents.

#### 7Z Archives

#### `create_7z_archive(files: List[String]) -> Dictionary[String, Any]`
Creates 7Z archive.

#### `add_to_7z(sevenz_archive: Dictionary[String, Any], file_path: String, archive_path: String) -> Boolean`
Adds file to 7Z archive.

#### `extract_7z(sevenz_archive: Dictionary[String, Any], output_dir: String) -> Boolean`
Extracts 7Z archive.

#### `list_7z_contents(sevenz_archive: Dictionary[String, Any]) -> List[Dictionary[String, Any]]`
Lists 7Z archive contents.

#### RAR Archives

#### `create_rar_archive(files: List[String]) -> Dictionary[String, Any]`
Creates RAR archive.

#### `add_to_rar(rar_archive: Dictionary[String, Any], file_path: String, archive_path: String) -> Boolean`
Adds file to RAR archive.

#### `extract_rar(rar_archive: Dictionary[String, Any], output_dir: String) -> Boolean`
Extracts RAR archive.

#### `list_rar_contents(rar_archive: Dictionary[String, Any]) -> List[Dictionary[String, Any]]`
Lists RAR archive contents.

### Advanced Compression Features

#### Compression Levels

#### `compress_with_level(data: String, algorithm: String, level: Integer) -> List[Integer]`
Compresses data with specified level.

**Parameters:**
- `data`: Data to compress
- `algorithm`: Compression algorithm
- `level`: Compression level (1-9, higher = better compression)

**Returns:** Compressed data

#### Dictionary-Based Compression

#### `compress_with_dict(data: String, algorithm: String, dictionary: List[Integer]) -> List[Integer]`
Compresses data using custom dictionary.

**Parameters:**
- `data`: Data to compress
- `algorithm`: Compression algorithm
- `dictionary`: Custom compression dictionary

**Returns:** Compressed data

#### `create_dictionary(training_data: List[String], algorithm: String) -> List[Integer]`
Creates compression dictionary from training data.

**Parameters:**
- `training_data`: List of training strings
- `algorithm`: Compression algorithm

**Returns:** Compression dictionary

#### Parallel Compression

#### `compress_with_parallel(data: String, algorithm: String, threads: Integer) -> List[Integer]`
Compresses data using multiple threads.

**Parameters:**
- `data`: Data to compress
- `algorithm`: Compression algorithm
- `threads`: Number of threads to use

**Returns:** Compressed data

#### `decompress_with_parallel(compressed_data: List[Integer], algorithm: String, threads: Integer) -> String`
Decompresses data using multiple threads.

**Parameters:**
- `compressed_data`: Compressed data
- `algorithm`: Compression algorithm
- `threads`: Number of threads to use

**Returns:** Decompressed data

#### Progress Tracking

#### `compress_with_progress(data: String, algorithm: String, callback: String) -> List[Integer]`
Compresses data with progress callback.

**Parameters:**
- `data`: Data to compress
- `algorithm`: Compression algorithm
- `callback`: Progress callback function name

**Returns:** Compressed data

#### `decompress_with_progress(compressed_data: List[Integer], algorithm: String, callback: String) -> String`
Decompresses data with progress callback.

**Parameters:**
- `compressed_data`: Compressed data
- `algorithm`: Compression algorithm
- `callback`: Progress callback function name

**Returns:** Decompressed data

#### Encryption

#### `compress_with_encryption(data: String, algorithm: String, password: String) -> List[Integer]`
Compresses data with encryption.

**Parameters:**
- `data`: Data to compress
- `algorithm`: Compression algorithm
- `password`: Encryption password

**Returns:** Encrypted compressed data

#### `decompress_with_decryption(compressed_data: List[Integer], algorithm: String, password: String) -> String`
Decompresses encrypted data.

**Parameters:**
- `compressed_data`: Encrypted compressed data
- `algorithm`: Compression algorithm
- `password`: Decryption password

**Returns:** Decompressed data

#### Checksums

#### `compress_with_checksum(data: String, algorithm: String) -> Dictionary[String, Any]`
Compresses data with checksum.

**Parameters:**
- `data`: Data to compress
- `algorithm`: Compression algorithm

**Returns:** Dictionary with compressed data and checksum

#### `decompress_with_checksum(compressed_data: List[Integer], algorithm: String) -> Dictionary[String, Any]`
Decompresses data with checksum verification.

**Parameters:**
- `compressed_data`: Compressed data
- `algorithm`: Compression algorithm

**Returns:** Dictionary with decompressed data and checksum

#### `verify_compression_checksum(compressed_data: List[Integer], checksum: String) -> Boolean`
Verifies compression checksum.

**Parameters:**
- `compressed_data`: Compressed data
- `checksum`: Expected checksum

**Returns:** True if checksum matches

#### Metadata

#### `compress_with_metadata(data: String, algorithm: String, metadata: Dictionary[String, Any]) -> List[Integer]`
Compresses data with metadata.

**Parameters:**
- `data`: Data to compress
- `algorithm`: Compression algorithm
- `metadata`: Metadata dictionary

**Returns:** Compressed data with metadata

#### `decompress_with_metadata(compressed_data: List[Integer], algorithm: String) -> Dictionary[String, Any]`
Decompresses data and extracts metadata.

**Parameters:**
- `compressed_data`: Compressed data
- `algorithm`: Compression algorithm

**Returns:** Dictionary with decompressed data and metadata

#### `get_compression_metadata(compressed_data: List[Integer]) -> Dictionary[String, Any]`
Gets compression metadata.

**Parameters:**
- `compressed_data`: Compressed data

**Returns:** Metadata dictionary

#### Deduplication

#### `compress_with_deduplication(data: String, algorithm: String) -> List[Integer]`
Compresses data with deduplication.

**Parameters:**
- `data`: Data to compress
- `algorithm`: Compression algorithm

**Returns:** Compressed data

#### `decompress_with_deduplication(compressed_data: List[Integer], algorithm: String) -> String`
Decompresses data with deduplication.

**Parameters:**
- `compressed_data`: Compressed data
- `algorithm`: Compression algorithm

**Returns:** Decompressed data

### Compression Profiles

#### `create_compression_profile(name: String, config: Dictionary[String, Any]) -> Dictionary[String, Any]`
Creates compression profile.

**Parameters:**
- `name`: Profile name
- `config`: Profile configuration

**Returns:** Compression profile object

#### `set_profile_algorithm(profile: Dictionary[String, Any], algorithm: String) -> None`
Sets profile algorithm.

#### `set_profile_level(profile: Dictionary[String, Any], level: Integer) -> None`
Sets profile compression level.

#### `set_profile_threads(profile: Dictionary[String, Any], threads: Integer) -> None`
Sets profile thread count.

#### `set_profile_encryption(profile: Dictionary[String, Any], encryption: Boolean) -> None`
Sets profile encryption.

#### `compress_with_profile(data: String, profile: Dictionary[String, Any]) -> List[Integer]`
Compresses data using profile.

#### `decompress_with_profile(compressed_data: List[Integer], profile: Dictionary[String, Any]) -> String`
Decompresses data using profile.

### Benchmarking and Optimization

#### `get_compression_benchmark(data: String, algorithms: List[String]) -> Dictionary[String, Any]`
Benchmarks compression algorithms.

**Parameters:**
- `data`: Data to benchmark
- `algorithms`: List of algorithms to test

**Returns:** Benchmark results

#### `get_decompression_benchmark(compressed_data: Dictionary[String, List[Integer]]) -> Dictionary[String, Any]`
Benchmarks decompression algorithms.

**Parameters:**
- `compressed_data`: Dictionary of compressed data by algorithm

**Returns:** Benchmark results

#### `get_compression_recommendation(data: String, criteria: Dictionary[String, Any]) -> String`
Recommends compression algorithm.

**Parameters:**
- `data`: Data to analyze
- `criteria`: Recommendation criteria

**Returns:** Recommended algorithm

#### `optimize_compression(data: String, target_size: Integer) -> Dictionary[String, Any]`
Optimizes compression parameters.

**Parameters:**
- `data`: Data to optimize
- `target_size`: Target compressed size

**Returns:** Optimization results

### Advanced Algorithms

#### Adaptive Compression

#### `compress_with_adaptive(data: String) -> List[Integer]`
Compresses data with adaptive algorithm selection.

#### `decompress_with_adaptive(compressed_data: List[Integer]) -> String`
Decompresses data with adaptive algorithm.

#### Predictive Compression

#### `compress_with_predictive(data: String, model: String) -> List[Integer]`
Compresses data using predictive model.

#### `decompress_with_predictive(compressed_data: List[Integer], model: String) -> String`
Decompresses data using predictive model.

#### `train_compression_model(training_data: List[String], model_type: String) -> Dictionary[String, Any]`
Trains compression model.

#### `save_compression_model(model: Dictionary[String, Any], file_path: String) -> Boolean`
Saves compression model.

#### `load_compression_model(file_path: String) -> Dictionary[String, Any]`
Loads compression model.

#### Context-Aware Compression

#### `compress_with_context(data: String, context: String) -> List[Integer]`
Compresses data with context.

#### `decompress_with_context(compressed_data: List[Integer], context: String) -> String`
Decompresses data with context.

#### Delta Compression

#### `compress_with_delta(data: String, base_data: String) -> List[Integer]`
Compresses data using delta encoding.

#### `decompress_with_delta(compressed_data: List[Integer], base_data: String) -> String`
Decompresses data using delta encoding.

#### Incremental Compression

#### `compress_with_incremental(data: String, previous_data: String) -> List[Integer]`
Compresses data using incremental encoding.

#### `decompress_with_incremental(compressed_data: List[Integer], previous_data: String) -> String`
Decompresses data using incremental encoding.

#### Hierarchical Compression

#### `compress_with_hierarchical(data: String, levels: Integer) -> List[Integer]`
Compresses data using hierarchical encoding.

#### `decompress_with_hierarchical(compressed_data: List[Integer], levels: Integer) -> String`
Decompresses data using hierarchical encoding.

#### Wavelet Compression

#### `compress_with_wavelet(data: String, wavelet_type: String) -> List[Integer]`
Compresses data using wavelet transform.

#### `decompress_with_wavelet(compressed_data: List[Integer], wavelet_type: String) -> String`
Decompresses data using wavelet transform.

#### Fractal Compression

#### `compress_with_fractal(data: String, iterations: Integer) -> List[Integer]`
Compresses data using fractal encoding.

#### `decompress_with_fractal(compressed_data: List[Integer], iterations: Integer) -> String`
Decompresses data using fractal encoding.

#### Neural Compression

#### `compress_with_neural(data: String, model_path: String) -> List[Integer]`
Compresses data using neural network.

#### `decompress_with_neural(compressed_data: List[Integer], model_path: String) -> String`
Decompresses data using neural network.

#### Quantum Compression

#### `compress_with_quantum(data: String, qubits: Integer) -> List[Integer]`
Compresses data using quantum algorithm.

#### `decompress_with_quantum(compressed_data: List[Integer], qubits: Integer) -> String`
Decompresses data using quantum algorithm.

## Advanced Examples

### Multi-Algorithm Compression

```runa
Note: Compare different compression algorithms
:End Note

Let data be repeat "Hello, World! " for 1000 times
Let algorithms be ["gzip", "bzip2", "lzma", "lz4", "zstd"]

For each algorithm in algorithms:
    Let start_time be get current time
    Let compressed be compress data with algorithm as algorithm
    Let end_time be get current time
    
    Let compression_time be end_time minus start_time
    Let ratio be get compression ratio length of data with length of compressed
    
    Note: Algorithm: algorithm, Ratio: ratio, Time: compression_time
End For
```

### Streaming Compression

```runa
Note: Compress large data in chunks
:End Note

Let stream be create compression stream with algorithm as "gzip"
Let chunks be ["Chunk 1", "Chunk 2", "Chunk 3", "Chunk 4"]
Let compressed be []

For each chunk in chunks:
    Let compressed_chunk be compress stream stream with chunk
    Add compressed_chunk to compressed
End For

Let final_data be finish compression stream stream
Add final_data to compressed
```

### Archive Creation

```runa
Note: Create a ZIP archive with multiple files
:End Note

Let files be ["file1.txt", "file2.txt", "file3.txt"]
Let archive be create archive files with format as "zip"

Add file to archive archive with "file1.txt" as "data/file1.txt"
Add file to archive archive with "file2.txt" as "data/file2.txt"
Add file to archive archive with "file3.txt" as "data/file3.txt"

Let contents be list archive contents archive
For each entry in contents:
    Note: Archive entry: entry["name"], Size: entry["size"]
End For
```

### Parallel Compression

```runa
Note: Compress large dataset in parallel
:End Note

Let data be repeat "Large dataset content " for 10000 times
Let compressed be compress with parallel data with algorithm as "zstd" and threads as 4

Note: Parallel compression completed
```

### Encrypted Compression

```runa
Note: Compress and encrypt sensitive data
:End Note

Let sensitive_data be "This is sensitive information that needs protection"
Let password be "my-secret-password"

Let encrypted_compressed be compress with encryption sensitive_data with algorithm as "gzip" and password as password
Let decrypted_decompressed be decompress with decryption encrypted_compressed with algorithm as "gzip" and password as password

Assert decrypted_decompressed equals sensitive_data
```

## Error Handling

The Compress module provides comprehensive error handling:

```runa
Note: Handle compression errors gracefully
:End Note

Try:
    Let compressed be compress data with algorithm as "invalid_algorithm"
    Note: Compression successful
Catch error:
    Note: Compression failed: error
End Try

Try:
    Let decompressed be decompress data invalid_data with algorithm as "gzip"
    Note: Decompression successful
Catch error:
    Note: Decompression failed: error
End Try
```

## Performance Considerations

- Choose appropriate compression algorithm for data type
- Use parallel compression for large datasets
- Consider compression level vs. speed trade-offs
- Use streaming for large files
- Implement proper error handling
- Monitor compression ratios and speeds
- Use checksums for data integrity
- Consider encryption for sensitive data

## Security Considerations

- Validate input data before compression
- Use strong passwords for encrypted compression
- Verify checksums after decompression
- Handle sensitive data securely
- Use secure random number generation
- Implement proper access controls
- Monitor for compression-based attacks

## Testing

The Compress module includes comprehensive tests covering:

- All compression algorithms
- File and directory operations
- Archive formats
- Streaming operations
- Parallel processing
- Encryption and security
- Error handling
- Performance testing
- Edge cases and stress testing

Run tests with:
```bash
runa test_compress.runa
```

## Dependencies

The Compress module depends on:
- Compression libraries (zlib, bzip2, lzma, lz4, zstd, brotli)
- Archive libraries (zip, tar, 7z, rar)
- Cryptographic libraries for encryption
- Threading libraries for parallel processing
- File system operations

## Future Enhancements

Planned features include:
- More compression algorithms
- Advanced archive formats
- Cloud storage integration
- Real-time compression
- Machine learning optimization
- Quantum-resistant encryption
- Advanced deduplication
- Compression analytics 