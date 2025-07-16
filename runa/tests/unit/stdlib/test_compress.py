"""
Unit tests for Runa compression module.

Tests all compression algorithms, file operations, and utility functions.
"""

import unittest
import tempfile
import os
from runa.stdlib.compress import (
    # Compression algorithms
    gzip_compress, gzip_decompress,
    bzip2_compress, bzip2_decompress,
    lzma_compress, lzma_decompress,
    zlib_compress, zlib_decompress,
    
    # Utility functions
    compress_file, decompress_file,
    get_compression_ratio, is_compressed,
    detect_compression_algorithm, get_compression_stats
)


class TestGzipCompression(unittest.TestCase):
    """Test gzip compression and decompression."""
    
    def test_gzip_compress_string(self):
        """Test gzip compression with string input."""
        data = "Hello, world! This is a test string for compression."
        compressed = gzip_compress(data)
        self.assertIsInstance(compressed, bytes)
        self.assertLess(len(compressed), len(data.encode('utf-8')))
    
    def test_gzip_compress_bytes(self):
        """Test gzip compression with bytes input."""
        data = b"Hello, world! This is a test string for compression."
        compressed = gzip_compress(data)
        self.assertIsInstance(compressed, bytes)
        self.assertLess(len(compressed), len(data))
    
    def test_gzip_decompress(self):
        """Test gzip decompression."""
        original = "Hello, world! This is a test string for compression."
        compressed = gzip_compress(original)
        decompressed = gzip_decompress(compressed)
        self.assertEqual(decompressed.decode('utf-8'), original)
    
    def test_gzip_compression_levels(self):
        """Test gzip compression with different levels."""
        data = "Hello, world! " * 100  # Repeat to make compression more effective
        
        # Test different compression levels
        for level in [1, 6, 9]:
            compressed = gzip_compress(data, level)
            decompressed = gzip_decompress(compressed)
            self.assertEqual(decompressed.decode('utf-8'), data)


class TestBzip2Compression(unittest.TestCase):
    """Test bzip2 compression and decompression."""
    
    def test_bzip2_compress_string(self):
        """Test bzip2 compression with string input."""
        data = "Hello, world! This is a test string for compression."
        compressed = bzip2_compress(data)
        self.assertIsInstance(compressed, bytes)
        self.assertLess(len(compressed), len(data.encode('utf-8')))
    
    def test_bzip2_compress_bytes(self):
        """Test bzip2 compression with bytes input."""
        data = b"Hello, world! This is a test string for compression."
        compressed = bzip2_compress(data)
        self.assertIsInstance(compressed, bytes)
        self.assertLess(len(compressed), len(data))
    
    def test_bzip2_decompress(self):
        """Test bzip2 decompression."""
        original = "Hello, world! This is a test string for compression."
        compressed = bzip2_compress(original)
        decompressed = bzip2_decompress(compressed)
        self.assertEqual(decompressed.decode('utf-8'), original)
    
    def test_bzip2_compression_levels(self):
        """Test bzip2 compression with different levels."""
        data = "Hello, world! " * 100  # Repeat to make compression more effective
        
        # Test different compression levels
        for level in [1, 6, 9]:
            compressed = bzip2_compress(data, level)
            decompressed = bzip2_decompress(compressed)
            self.assertEqual(decompressed.decode('utf-8'), data)


class TestLZMACompression(unittest.TestCase):
    """Test LZMA compression and decompression."""
    
    def test_lzma_compress_string(self):
        """Test LZMA compression with string input."""
        data = "Hello, world! This is a test string for compression."
        compressed = lzma_compress(data)
        self.assertIsInstance(compressed, bytes)
        self.assertLess(len(compressed), len(data.encode('utf-8')))
    
    def test_lzma_compress_bytes(self):
        """Test LZMA compression with bytes input."""
        data = b"Hello, world! This is a test string for compression."
        compressed = lzma_compress(data)
        self.assertIsInstance(compressed, bytes)
        self.assertLess(len(compressed), len(data))
    
    def test_lzma_decompress(self):
        """Test LZMA decompression."""
        original = "Hello, world! This is a test string for compression."
        compressed = lzma_compress(original)
        decompressed = lzma_decompress(compressed)
        self.assertEqual(decompressed.decode('utf-8'), original)
    
    def test_lzma_compression_levels(self):
        """Test LZMA compression with different levels."""
        data = "Hello, world! " * 100  # Repeat to make compression more effective
        
        # Test different compression levels
        for level in [0, 3, 6, 9]:
            compressed = lzma_compress(data, level)
            decompressed = lzma_decompress(compressed)
            self.assertEqual(decompressed.decode('utf-8'), data)


class TestZlibCompression(unittest.TestCase):
    """Test zlib compression and decompression."""
    
    def test_zlib_compress_string(self):
        """Test zlib compression with string input."""
        data = "Hello, world! This is a test string for compression."
        compressed = zlib_compress(data)
        self.assertIsInstance(compressed, bytes)
        self.assertLess(len(compressed), len(data.encode('utf-8')))
    
    def test_zlib_compress_bytes(self):
        """Test zlib compression with bytes input."""
        data = b"Hello, world! This is a test string for compression."
        compressed = zlib_compress(data)
        self.assertIsInstance(compressed, bytes)
        self.assertLess(len(compressed), len(data))
    
    def test_zlib_decompress(self):
        """Test zlib decompression."""
        original = "Hello, world! This is a test string for compression."
        compressed = zlib_compress(original)
        decompressed = zlib_decompress(compressed)
        self.assertEqual(decompressed.decode('utf-8'), original)
    
    def test_zlib_compression_levels(self):
        """Test zlib compression with different levels."""
        data = "Hello, world! " * 100  # Repeat to make compression more effective
        
        # Test different compression levels
        for level in [0, 3, 6, 9]:
            compressed = zlib_compress(data, level)
            decompressed = zlib_decompress(compressed)
            self.assertEqual(decompressed.decode('utf-8'), data)


class TestFileCompression(unittest.TestCase):
    """Test file compression and decompression."""
    
    def setUp(self):
        """Set up test files."""
        self.test_data = "Hello, world! This is a test file for compression.\n" * 100
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test files."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_compress_file_gzip(self):
        """Test file compression with gzip."""
        input_path = os.path.join(self.temp_dir, "input.txt")
        output_path = os.path.join(self.temp_dir, "output.gz")
        
        # Create test file
        with open(input_path, 'w') as f:
            f.write(self.test_data)
        
        # Compress file
        result = compress_file(input_path, output_path, 'gzip')
        self.assertTrue(bool(result))
        self.assertTrue(os.path.exists(output_path))
        self.assertLess(os.path.getsize(output_path), os.path.getsize(input_path))
    
    def test_compress_file_bzip2(self):
        """Test file compression with bzip2."""
        input_path = os.path.join(self.temp_dir, "input.txt")
        output_path = os.path.join(self.temp_dir, "output.bz2")
        
        # Create test file
        with open(input_path, 'w') as f:
            f.write(self.test_data)
        
        # Compress file
        result = compress_file(input_path, output_path, 'bzip2')
        self.assertTrue(bool(result))
        self.assertTrue(os.path.exists(output_path))
        self.assertLess(os.path.getsize(output_path), os.path.getsize(input_path))
    
    def test_compress_file_lzma(self):
        """Test file compression with LZMA."""
        input_path = os.path.join(self.temp_dir, "input.txt")
        output_path = os.path.join(self.temp_dir, "output.xz")
        
        # Create test file
        with open(input_path, 'w') as f:
            f.write(self.test_data)
        
        # Compress file
        result = compress_file(input_path, output_path, 'lzma')
        self.assertTrue(bool(result))
        self.assertTrue(os.path.exists(output_path))
        self.assertLess(os.path.getsize(output_path), os.path.getsize(input_path))
    
    def test_compress_file_zlib(self):
        """Test file compression with zlib."""
        input_path = os.path.join(self.temp_dir, "input.txt")
        output_path = os.path.join(self.temp_dir, "output.zlib")
        
        # Create test file
        with open(input_path, 'w') as f:
            f.write(self.test_data)
        
        # Compress file
        result = compress_file(input_path, output_path, 'zlib')
        self.assertTrue(bool(result))
        self.assertTrue(os.path.exists(output_path))
        self.assertLess(os.path.getsize(output_path), os.path.getsize(input_path))
    
    def test_decompress_file_gzip(self):
        """Test file decompression with gzip."""
        input_path = os.path.join(self.temp_dir, "input.txt")
        compressed_path = os.path.join(self.temp_dir, "compressed.gz")
        decompressed_path = os.path.join(self.temp_dir, "decompressed.txt")
        
        # Create test file
        with open(input_path, 'w') as f:
            f.write(self.test_data)
        
        # Compress and decompress
        compress_file(input_path, compressed_path, 'gzip')
        result = decompress_file(compressed_path, decompressed_path, 'gzip')
        self.assertTrue(bool(result))
        
        # Check content
        with open(decompressed_path, 'r') as f:
            decompressed_content = f.read()
        self.assertEqual(decompressed_content, self.test_data)
    
    def test_compress_file_remove_original(self):
        """Test file compression with original file removal."""
        input_path = os.path.join(self.temp_dir, "input.txt")
        output_path = os.path.join(self.temp_dir, "output.gz")
        
        # Create test file
        with open(input_path, 'w') as f:
            f.write(self.test_data)
        
        original_size = os.path.getsize(input_path)
        
        # Compress file and remove original
        result = compress_file(input_path, output_path, 'gzip', remove_original=True)
        self.assertTrue(bool(result))
        self.assertFalse(os.path.exists(input_path))  # Original should be removed
        self.assertTrue(os.path.exists(output_path))
        self.assertLess(os.path.getsize(output_path), original_size)
    
    def test_compress_file_nonexistent(self):
        """Test file compression with nonexistent file."""
        input_path = os.path.join(self.temp_dir, "nonexistent.txt")
        output_path = os.path.join(self.temp_dir, "output.gz")
        
        with self.assertRaises(FileNotFoundError):
            compress_file(input_path, output_path, 'gzip')
    
    def test_compress_file_invalid_algorithm(self):
        """Test file compression with invalid algorithm."""
        input_path = os.path.join(self.temp_dir, "input.txt")
        output_path = os.path.join(self.temp_dir, "output.gz")
        
        # Create test file
        with open(input_path, 'w') as f:
            f.write(self.test_data)
        
        with self.assertRaises(ValueError):
            compress_file(input_path, output_path, 'invalid_algorithm')


class TestCompressionUtilities(unittest.TestCase):
    """Test compression utility functions."""
    
    def test_get_compression_ratio(self):
        """Test get_compression_ratio function."""
        original_size = 1000
        compressed_size = 500
        ratio = get_compression_ratio(original_size, compressed_size)
        self.assertEqual(float(ratio), 2.0)
        
        # Test with zero compressed size
        ratio = get_compression_ratio(original_size, 0)
        self.assertEqual(float(ratio), 0.0)
    
    def test_is_compressed_auto(self):
        """Test is_compressed function with auto detection."""
        # Test gzip signature
        gzip_data = b'\x1f\x8b' + b'data'
        self.assertTrue(bool(is_compressed(gzip_data, 'auto')))
        
        # Test bzip2 signature
        bzip2_data = b'BZ' + b'data'
        self.assertTrue(bool(is_compressed(bzip2_data, 'auto')))
        
        # Test LZMA signature
        lzma_data = b'\xfd7zXZ\x00' + b'data'
        self.assertTrue(bool(is_compressed(lzma_data, 'auto')))
        
        # Test zlib signature
        zlib_data = b'\x78' + b'data'
        self.assertTrue(bool(is_compressed(zlib_data, 'auto')))
        
        # Test uncompressed data
        uncompressed_data = b'Hello, world!'
        self.assertFalse(bool(is_compressed(uncompressed_data, 'auto')))
    
    def test_is_compressed_specific(self):
        """Test is_compressed function with specific algorithms."""
        # Test gzip
        gzip_data = b'\x1f\x8b' + b'data'
        self.assertTrue(bool(is_compressed(gzip_data, 'gzip')))
        self.assertFalse(bool(is_compressed(gzip_data, 'bzip2')))
        
        # Test bzip2
        bzip2_data = b'BZ' + b'data'
        self.assertTrue(bool(is_compressed(bzip2_data, 'bzip2')))
        self.assertFalse(bool(is_compressed(bzip2_data, 'gzip')))
    
    def test_is_compressed_invalid_algorithm(self):
        """Test is_compressed function with invalid algorithm."""
        data = b'Hello, world!'
        with self.assertRaises(ValueError):
            is_compressed(data, 'invalid_algorithm')
    
    def test_detect_compression_algorithm(self):
        """Test detect_compression_algorithm function."""
        # Test gzip
        gzip_data = b'\x1f\x8b' + b'data'
        algorithm = detect_compression_algorithm(gzip_data)
        self.assertEqual(str(algorithm), 'gzip')
        
        # Test bzip2
        bzip2_data = b'BZ' + b'data'
        algorithm = detect_compression_algorithm(bzip2_data)
        self.assertEqual(str(algorithm), 'bzip2')
        
        # Test LZMA
        lzma_data = b'\xfd7zXZ\x00' + b'data'
        algorithm = detect_compression_algorithm(lzma_data)
        self.assertEqual(str(algorithm), 'lzma')
        
        # Test zlib
        zlib_data = b'\x78' + b'data'
        algorithm = detect_compression_algorithm(zlib_data)
        self.assertEqual(str(algorithm), 'zlib')
        
        # Test unknown
        unknown_data = b'Hello, world!'
        algorithm = detect_compression_algorithm(unknown_data)
        self.assertEqual(str(algorithm), 'unknown')
    
    def test_get_compression_stats(self):
        """Test get_compression_stats function."""
        original_data = b"Hello, world! " * 100
        compressed_data = gzip_compress(original_data)
        
        stats = get_compression_stats(original_data, compressed_data)
        
        self.assertIn('original_size', stats)
        self.assertIn('compressed_size', stats)
        self.assertIn('compression_ratio', stats)
        self.assertIn('compression_percentage', stats)
        self.assertIn('space_saved', stats)
        self.assertIn('algorithm', stats)
        
        self.assertEqual(stats['original_size'], len(original_data))
        self.assertEqual(stats['compressed_size'], len(compressed_data))
        self.assertGreater(float(stats['compression_ratio']), 1.0)
        self.assertGreater(float(stats['compression_percentage']), 0.0)
        self.assertEqual(stats['space_saved'], len(original_data) - len(compressed_data))
        self.assertEqual(str(stats['algorithm']), 'gzip')


class TestCompressionEdgeCases(unittest.TestCase):
    """Test compression functions with edge cases."""
    
    def test_compress_empty_data(self):
        """Test compression with empty data."""
        # Test all algorithms with empty data
        empty_data = ""
        empty_bytes = b""
        
        for compress_func in [gzip_compress, bzip2_compress, lzma_compress, zlib_compress]:
            compressed = compress_func(empty_data)
            self.assertIsInstance(compressed, bytes)
            self.assertGreater(len(compressed), 0)  # Should still have header
    
    def test_compress_small_data(self):
        """Test compression with very small data."""
        small_data = "a"
        
        for compress_func in [gzip_compress, bzip2_compress, lzma_compress, zlib_compress]:
            compressed = compress_func(small_data)
            decompressed = self._get_decompress_func(compress_func)(compressed)
            self.assertEqual(decompressed.decode('utf-8'), small_data)
    
    def test_compress_large_data(self):
        """Test compression with large data."""
        large_data = "Hello, world! " * 10000
        
        for compress_func in [gzip_compress, bzip2_compress, lzma_compress, zlib_compress]:
            compressed = compress_func(large_data)
            decompressed = self._get_decompress_func(compress_func)(compressed)
            self.assertEqual(decompressed.decode('utf-8'), large_data)
    
    def _get_decompress_func(self, compress_func):
        """Get corresponding decompress function."""
        decompress_map = {
            gzip_compress: gzip_decompress,
            bzip2_compress: bzip2_decompress,
            lzma_compress: lzma_decompress,
            zlib_compress: zlib_decompress
        }
        return decompress_map[compress_func]
    
    def test_decompress_invalid_data(self):
        """Test decompression with invalid data."""
        invalid_data = b"Invalid compressed data"
        
        with self.assertRaises(Exception):
            gzip_decompress(invalid_data)
        
        with self.assertRaises(Exception):
            bzip2_decompress(invalid_data)
        
        with self.assertRaises(Exception):
            lzma_decompress(invalid_data)
        
        with self.assertRaises(Exception):
            zlib_decompress(invalid_data)


if __name__ == '__main__':
    unittest.main() 