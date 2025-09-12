# Fourier Transform Engine

The Fourier transform engine provides comprehensive implementations of Fourier analysis methods, spectral analysis techniques, and time-frequency domain transformations. This module forms the foundation for signal processing, frequency domain analysis, and spectral computation throughout the Runa standard library.

## Overview

The `math/engine/fourier` module implements a complete suite of Fourier analysis tools:

- **Discrete Fourier Transform (DFT)**: Foundation algorithms for frequency domain conversion
- **Fast Fourier Transform (FFT)**: Optimized implementations with O(N log N) complexity
- **Window Functions**: Spectral leakage mitigation and signal conditioning
- **Wavelet Transforms**: Multi-resolution analysis and time-frequency localization
- **Spectral Analysis**: Advanced power spectral density estimation and cross-spectral analysis

## Architecture

```
math/engine/fourier/
├── dft.runa          # Discrete Fourier Transform implementations
├── fft.runa          # Fast Fourier Transform algorithms
├── windowing.runa    # Window functions and spectral conditioning
├── wavelets.runa     # Wavelet transforms and multi-resolution analysis
└── spectral.runa     # Advanced spectral analysis methods
```

## Quick Start

### Basic FFT Analysis

```runa
Import "math/engine/fourier/fft" as FFT
Import "math/engine/fourier/windowing" as Windowing

Note: Analyze frequency content of a signal
Let signal be [1.0, 0.5, -0.3, 0.8, -0.2, 0.6, -0.4, 0.9]
Let windowed_signal be Windowing.apply_window(signal, "hann")
Let spectrum be FFT.fft(windowed_signal)

Note: Extract magnitude and phase information
Let magnitudes be FFT.magnitude(spectrum)
Let phases be FFT.phase(spectrum)
```

### Power Spectral Density Estimation

```runa
Import "math/engine/fourier/spectral" as Spectral

Note: Estimate power spectral density using Welch's method
Let long_signal be generate_test_signal(1024)
Let psd be Spectral.welch_psd(long_signal, "hann", 256, 128, 1000.0)

Note: Extract frequency bins and power values
Let frequencies be psd.frequencies
Let power_values be psd.power
```

### Wavelet Analysis

```runa
Import "math/engine/fourier/wavelets" as Wavelets

Note: Perform continuous wavelet transform
Let signal be load_physiological_data()
Let scales be Wavelets.generate_scales(1, 128, 64)
Let cwt_result be Wavelets.cwt(signal, "morlet", scales)

Note: Analyze time-frequency content
Let time_frequency_map be cwt_result.coefficients
Let ridge_lines be Wavelets.extract_ridges(cwt_result, 0.3)
```

## Module Components

### 1. Discrete Fourier Transform ([dft.runa](dft.md))

The DFT module provides the mathematical foundation for frequency domain analysis:

- **Forward/Inverse DFT**: Complete implementation of the discrete Fourier transform
- **Complex Number Support**: Full complex arithmetic for frequency domain operations
- **Multi-dimensional DFT**: Support for 2D and N-dimensional transforms
- **Normalization Options**: Multiple normalization conventions

**Key Types:**
- `ComplexNumber`: Complex number representation
- `DFTResult`: Transform results with metadata
- `DFTConfig`: Configuration for transform parameters

### 2. Fast Fourier Transform ([fft.runa](fft.md))

Optimized FFT implementations for high-performance spectral analysis:

- **Cooley-Tukey Algorithm**: Classic radix-2 decimation-in-time
- **Mixed-Radix FFT**: Support for non-power-of-2 lengths
- **Real-valued FFT**: Optimized transforms for real input signals
- **GPU Acceleration**: Hardware-accelerated computation paths

**Key Features:**
- O(N log N) complexity for all transform sizes
- In-place computation options for memory efficiency
- Vectorized operations using SIMD instructions
- Automatic algorithm selection based on input characteristics

### 3. Window Functions ([windowing.runa](windowing.md))

Comprehensive collection of window functions for spectral conditioning:

- **Classical Windows**: Hamming, Hanning, Blackman, Kaiser
- **Modern Windows**: Tukey, Gaussian, Flat-top, Bohman
- **Parametric Windows**: Customizable window shapes and parameters
- **Performance Analysis**: Window characteristics and spectral properties

**Applications:**
- Spectral leakage reduction
- Side-lobe suppression
- Signal conditioning for analysis
- Filter design and implementation

### 4. Wavelet Transforms ([wavelets.runa](wavelets.md))

Multi-resolution analysis and time-frequency localization:

- **Continuous Wavelet Transform (CWT)**: Time-scale analysis
- **Discrete Wavelet Transform (DWT)**: Efficient decomposition algorithms
- **Wavelet Families**: Morlet, Daubechies, Biorthogonal, Coiflets
- **Multi-resolution Analysis**: Hierarchical signal decomposition

**Advanced Features:**
- Ridge extraction for instantaneous frequency analysis
- Wavelet packet decomposition
- Denoising and compression applications
- Real-time processing capabilities

### 5. Spectral Analysis ([spectral.runa](spectral.md))

Advanced methods for power spectral density estimation and cross-spectral analysis:

- **Non-parametric Methods**: Periodogram, Welch's method, Bartlett's method
- **Parametric Methods**: AR modeling, Maximum Entropy Method
- **Cross-spectral Analysis**: Coherence, cross-correlation, transfer functions
- **Time-frequency Analysis**: Spectrograms, instantaneous frequency

**Research-Grade Features:**
- Higher-order spectral analysis (bispectrum, trispectrum)
- Multitaper spectral estimation
- Evolutionary spectral analysis
- Statistical significance testing

## Performance Characteristics

### Computational Complexity

| Operation | Time Complexity | Space Complexity | Notes |
|-----------|----------------|------------------|-------|
| DFT | O(N²) | O(N) | Direct computation |
| FFT | O(N log N) | O(N) | Optimized algorithms |
| Real FFT | O(N log N) | O(N/2) | Real-valued optimization |
| CWT | O(N × M) | O(N × M) | N samples, M scales |
| DWT | O(N) | O(N) | Fast wavelet transform |

### Memory Optimization

The module implements several memory optimization strategies:

```runa
Note: In-place FFT computation
Let signal be allocate_signal_buffer(1024)
FFT.fft_inplace(signal)  Note: No additional memory allocation

Note: Streaming spectral analysis
Let analyzer be Spectral.create_streaming_analyzer(512, "welch")
For chunk in signal_stream:
    Let partial_result be analyzer.process_chunk(chunk)
```

### Hardware Acceleration

Automatic detection and utilization of hardware acceleration:

- **SIMD Instructions**: Vectorized operations on x86_64 and ARM64
- **GPU Compute**: CUDA and OpenCL implementations for large transforms
- **Multi-threading**: Parallel processing for independent operations
- **Cache Optimization**: Memory access patterns optimized for modern CPUs

## Integration Examples

### Digital Signal Processing Pipeline

```runa
Process called "analyze_audio_signal" that takes audio_data as List[Float], sample_rate as Float returns SpectralAnalysis:
    Note: Complete audio analysis pipeline
    
    Note: Pre-processing with windowing
    Let windowed_signal be Windowing.apply_window(audio_data, "kaiser", 8.6)
    
    Note: Frequency domain analysis
    Let spectrum be FFT.fft(windowed_signal)
    Let magnitude_spectrum be FFT.magnitude(spectrum)
    
    Note: Power spectral density estimation
    Let psd be Spectral.welch_psd(audio_data, "hann", 1024, 512, sample_rate)
    
    Note: Time-frequency analysis
    Let spectrogram be Spectral.spectrogram(audio_data, "hann", 256, 128, sample_rate)
    
    Note: Feature extraction
    Let spectral_centroid be compute_spectral_centroid(magnitude_spectrum)
    Let spectral_rolloff be compute_spectral_rolloff(magnitude_spectrum, 0.85)
    
    Let analysis be SpectralAnalysis with:
        spectrum = spectrum
        psd = psd
        spectrogram = spectrogram
        features = SpectralFeatures with:
            centroid = spectral_centroid
            rolloff = spectral_rolloff
    
    Return analysis
```

### Biomedical Signal Analysis

```runa
Process called "analyze_eeg_signal" that takes eeg_data as List[Float], channels as Integer returns EEGAnalysis:
    Note: Multi-channel EEG analysis with wavelets
    
    Let channel_analyses be []
    
    For channel_index in range(channels):
        Let channel_data be extract_channel(eeg_data, channel_index)
        
        Note: Artifact removal with wavelet denoising
        Let denoised_signal be Wavelets.denoise(channel_data, "db4", 0.1)
        
        Note: Time-frequency decomposition
        Let scales be Wavelets.generate_scales(1, 256, 64)
        Let cwt_result be Wavelets.cwt(denoised_signal, "morlet", scales)
        
        Note: Extract frequency bands
        Let alpha_band be extract_frequency_band(cwt_result, 8.0, 13.0)
        Let beta_band be extract_frequency_band(cwt_result, 13.0, 30.0)
        Let gamma_band be extract_frequency_band(cwt_result, 30.0, 100.0)
        
        Let channel_analysis be ChannelAnalysis with:
            raw_signal = channel_data
            denoised_signal = denoised_signal
            cwt_coefficients = cwt_result
            frequency_bands = FrequencyBands with:
                alpha = alpha_band
                beta = beta_band
                gamma = gamma_band
        
        channel_analyses.append(channel_analysis)
    
    Note: Cross-channel coherence analysis
    Let coherence_matrix be compute_coherence_matrix(channel_analyses)
    
    Let analysis be EEGAnalysis with:
        channels = channel_analyses
        coherence = coherence_matrix
        
    Return analysis
```

## Best Practices

### 1. Algorithm Selection

Choose the appropriate algorithm based on your requirements:

```runa
Process called "select_transform_algorithm" that takes signal_length as Integer, precision_required as Boolean returns String:
    Note: Algorithm selection based on signal characteristics
    
    If signal_length <= 1024 and precision_required:
        Return "dft"  Note: Exact computation for small signals
    Otherwise if signal_length is power_of_two(signal_length):
        Return "radix2_fft"  Note: Optimal for power-of-2 lengths
    Otherwise if signal_length < 10000:
        Return "mixed_radix_fft"  Note: Good for arbitrary lengths
    Otherwise:
        Return "chirp_z_transform"  Note: Flexible for very large transforms
```

### 2. Memory Management

Efficient memory usage for large-scale processing:

```runa
Process called "process_large_signal" that takes signal_stream as SignalStream returns ProcessedStream:
    Note: Memory-efficient processing of large signals
    
    Let block_size be 4096
    Let overlap_size be 512
    
    Let processor be create_streaming_processor(block_size, overlap_size)
    Let output_stream be create_output_stream()
    
    For block in signal_stream.blocks(block_size, overlap_size):
        Let processed_block be processor.process(block)
        output_stream.write(processed_block)
    
    Return output_stream
```

### 3. Error Handling

Robust error handling for numerical computations:

```runa
Process called "safe_spectral_analysis" that takes signal as List[Float] returns Result[SpectralResult, AnalysisError]:
    Note: Safe spectral analysis with comprehensive error checking
    
    If signal.is_empty():
        Return error(AnalysisError.EmptySignal)
    
    If signal.length() < 4:
        Return error(AnalysisError.InsufficientSamples)
    
    Note: Check for numerical issues
    If contains_infinite_values(signal):
        Return error(AnalysisError.InfiniteValues)
    
    If contains_nan_values(signal):
        Return error(AnalysisError.NaNValues)
    
    Note: Perform analysis with error recovery
    Try:
        Let result be perform_spectral_analysis(signal)
        Return success(result)
    Catch numerical_error as NumericError:
        Note: Attempt analysis with extended precision
        Let extended_result be perform_extended_precision_analysis(signal)
        Return success(extended_result)
    Catch memory_error as MemoryError:
        Note: Fall back to streaming analysis
        Let streaming_result be perform_streaming_analysis(signal)
        Return success(streaming_result)
```

## Research Applications

The Fourier engine supports advanced research applications:

### 1. Gravitational Wave Detection

```runa
Note: Template matching for gravitational wave detection
Let strain_data be load_ligo_data()
Let template_bank be load_waveform_templates()

For template in template_bank:
    Let matched_filter be compute_matched_filter(strain_data, template)
    Let snr_timeseries be FFT.correlate(strain_data, template)
    
    If max(snr_timeseries) > detection_threshold:
        Log "Potential gravitational wave detected"
```

### 2. Seismic Data Analysis

```runa
Note: Multi-station seismic event detection
Let seismic_stations be load_seismic_network()
Let coherence_threshold be 0.8

Let cross_station_coherence be Spectral.compute_coherence_matrix(seismic_stations)
Let event_candidates be detect_coherent_events(cross_station_coherence, coherence_threshold)
```

### 3. Radio Astronomy

```runa
Note: Pulsar timing analysis with advanced spectral methods
Let telescope_data be load_radio_observations()
Let folded_profile be fold_at_predicted_period(telescope_data)
Let timing_residuals be compute_timing_residuals(folded_profile)

Let noise_analysis be Spectral.multitaper_psd(timing_residuals)
Let red_noise_model be fit_power_law_noise(noise_analysis)
```

## Performance Benchmarks

Typical performance characteristics on modern hardware:

| Operation | Input Size | Time (ms) | Memory (MB) |
|-----------|------------|-----------|-------------|
| FFT | 1024 | 0.1 | 0.008 |
| FFT | 1M | 45 | 8 |
| FFT | 16M | 780 | 128 |
| Welch PSD | 1M samples | 120 | 16 |
| CWT | 4096 samples, 64 scales | 85 | 2 |
| Spectrogram | 1M samples | 95 | 24 |

*Benchmarks performed on Intel i9-12900K with 32GB DDR4-3200*

## Advanced Configuration

### Custom Window Functions

```runa
Process called "create_custom_window" that takes length as Integer, parameters as WindowParameters returns List[Float]:
    Note: Design custom window function
    
    Let window be []
    Let center be (length - 1) / 2.0
    
    For i in range(length):
        Let x be (i - center) / center
        Let value be evaluate_window_function(x, parameters)
        window.append(value)
    
    Note: Normalize window energy
    Let window_energy be sum(w * w for w in window)
    Let normalization_factor be sqrt(length / window_energy)
    
    For i in range(length):
        window[i] = window[i] * normalization_factor
    
    Return window
```

### Adaptive Spectral Analysis

```runa
Type called "AdaptiveAnalyzer":
    window_size as Integer
    overlap_ratio as Float
    adaptation_rate as Float
    noise_floor_estimate as Float

Process called "adaptive_spectral_analysis" that takes signal as List[Float], analyzer as AdaptiveAnalyzer returns AdaptiveSpectrum:
    Note: Spectral analysis with adaptive parameters
    
    Let local_statistics be compute_local_statistics(signal)
    
    Note: Adapt window size based on signal characteristics
    If local_statistics.stationarity_index < 0.5:
        analyzer.window_size = min(analyzer.window_size * 0.8, 128)
    Otherwise:
        analyzer.window_size = min(analyzer.window_size * 1.2, 2048)
    
    Note: Adapt overlap based on signal dynamics
    analyzer.overlap_ratio = 0.5 + 0.3 * local_statistics.variability_index
    
    Let spectrum be Spectral.welch_psd(signal, "adaptive", analyzer.window_size, 
                                      analyzer.window_size * analyzer.overlap_ratio, 1.0)
    
    Return AdaptiveSpectrum with:
        spectrum = spectrum
        parameters = analyzer
        adaptation_metrics = local_statistics
```

## Related Modules

The Fourier engine integrates with other mathematical components:

- **[Linear Algebra](../linalg/README.md)**: Matrix operations for multi-dimensional transforms
- **[Statistics](../stats/README.md)**: Statistical analysis of spectral estimates
- **[Optimization](../optimization/README.md)**: Parameter estimation for spectral models
- **[Numerical Methods](../numerical/README.md)**: Root finding and numerical integration
- **[Random](../random/README.md)**: Monte Carlo methods for spectral analysis

## References

1. Cooley, J.W. and Tukey, J.W. (1965). "An algorithm for the machine calculation of complex Fourier series"
2. Welch, P. (1967). "The use of fast Fourier transform for the estimation of power spectra"
3. Mallat, S. (1989). "A theory for multiresolution signal decomposition: the wavelet representation"
4. Thomson, D.J. (1982). "Spectrum estimation and harmonic analysis"
5. Daubechies, I. (1992). "Ten Lectures on Wavelets"

## Contributing

When contributing to the Fourier engine:

1. **Algorithm Implementation**: Follow the established patterns for numerical stability
2. **Performance Testing**: Include benchmarks for new algorithms
3. **Documentation**: Provide mathematical background and practical examples
4. **Error Handling**: Implement comprehensive error checking and recovery
5. **Testing**: Include unit tests with known reference solutions

For detailed implementation guidelines, see the [Runa Mathematical Library Development Guide](../../contributing/math_library.md).