# Discrete Fourier Transform (DFT)

The Discrete Fourier Transform (DFT) module provides fundamental frequency domain analysis capabilities through direct implementation of the DFT algorithm. This module serves as the mathematical foundation for spectral analysis and offers precise, unoptimized implementations ideal for educational purposes, verification, and small-scale applications.

## Overview

The DFT converts discrete time-domain signals into their frequency-domain representation, revealing the spectral content of signals. Unlike FFT algorithms that optimize for speed, the direct DFT implementation prioritizes mathematical clarity and exactness, making it perfect for understanding the underlying principles.

### Key Concepts

- **Frequency Domain Transformation**: Converting time-domain signals to frequency components
- **Spectral Analysis**: Analyzing the frequency content of signals
- **Complex Spectrum**: Both magnitude and phase information
- **Frequency Resolution**: Relationship between signal length and frequency precision
- **Windowing Effects**: Impact of finite signal lengths on spectral analysis

## Core Data Structures

### DFTResult

Comprehensive result structure containing all spectral information:

```runa
Type called "DFTResult":
    frequencies as List[Float]        Note: frequency bin centers
    magnitudes as List[Float]         Note: magnitude spectrum
    phases as List[Float]             Note: phase spectrum in radians
    complex_spectrum as List[Complex] Note: complex frequency coefficients
    sampling_rate as Float            Note: original sampling rate
    frequency_resolution as Float     Note: frequency resolution in Hz
```

**Usage Example:**
```runa
Note: Analyzing a 1 kHz sine wave sampled at 8 kHz
Let signal be generate_sine_wave(1000.0, 8000.0, 1024)  Note: 1kHz, 8kHz sampling, 1024 samples
Let dft_result be dft_analyze(signal, 8000.0)

Note: Peak should occur at 1000 Hz
Let peak_index be find_peak_frequency_index(dft_result.magnitudes)
Let peak_frequency be dft_result.frequencies[peak_index]
Note: peak_frequency ≈ 1000.0 Hz
```

### SpectralProperties

Descriptive measures of spectral characteristics:

```runa
Type called "SpectralProperties":
    peak_frequency as Float        Note: frequency of maximum magnitude
    peak_magnitude as Float        Note: maximum magnitude value
    spectral_centroid as Float     Note: center of mass of spectrum
    spectral_bandwidth as Float    Note: spread around centroid
    spectral_rolloff as Float      Note: frequency below which 85% of energy lies
    spectral_flatness as Float     Note: measure of spectral uniformity
    spectral_crest_factor as Float Note: ratio of peak to RMS
```

### DFTConfig

Configuration options for DFT computation:

```runa
Type called "DFTConfig":
    zero_padding as Boolean        Note: pad signal with zeros to increase resolution
    normalize as Boolean           Note: normalize output by signal length
    window_function as String      Note: windowing function to apply
    frequency_range as List[Float] Note: frequency range of interest
    dc_component as Boolean        Note: include DC (0 Hz) component
```

## Direct DFT Implementation

### Forward Transform

The fundamental DFT computation using the mathematical definition:

```runa
Process called "dft_direct" that takes input as List[Complex] returns List[Complex]:
    Let N be input.length()
    Let output be List[Complex]
    
    Note: DFT formula: X[k] = Σ(n=0 to N-1) x[n] * e^(-j2πkn/N)
    For k from 0 to N - 1:
        Let sum_real be 0.0
        Let sum_imag be 0.0
        
        For n from 0 to N - 1:
            Let angle be -2.0 * MathCore.pi() * k * n / N
            Let cos_angle be MathCore.cos(angle)
            Let sin_angle be MathCore.sin(angle)
            
            Note: Complex multiplication: x[n] * e^(-jθ)
            Let x_real be input[n].real
            Let x_imag be input[n].imag
            
            Set sum_real to sum_real + x_real * cos_angle - x_imag * sin_angle
            Set sum_imag to sum_imag + x_real * sin_angle + x_imag * cos_angle
        
        Call output.append(Complex{real: sum_real, imag: sum_imag})
    
    Return output
```

**Mathematical Principle:**
The DFT decomposes a signal into sinusoidal components by correlating it with complex exponentials at different frequencies.

### Inverse Transform

Converting frequency-domain data back to time domain:

```runa
Process called "idft_direct" that takes input as List[Complex] returns List[Complex]:
    Let N be input.length()
    Let output be List[Complex]
    
    Note: IDFT formula: x[n] = (1/N) * Σ(k=0 to N-1) X[k] * e^(j2πkn/N)
    For n from 0 to N - 1:
        Let sum_real be 0.0
        Let sum_imag be 0.0
        
        For k from 0 to N - 1:
            Let angle be 2.0 * MathCore.pi() * k * n / N  Note: positive for inverse
            Let cos_angle be MathCore.cos(angle)
            Let sin_angle be MathCore.sin(angle)
            
            Let X_real be input[k].real
            Let X_imag be input[k].imag
            
            Set sum_real to sum_real + X_real * cos_angle - X_imag * sin_angle
            Set sum_imag to sum_imag + X_real * sin_angle + X_imag * cos_angle
        
        Note: Scale by 1/N for proper inverse
        Call output.append(Complex{real: sum_real / N, imag: sum_imag / N})
    
    Return output
```

## Real Signal Processing

### Real-to-Complex Transform

Optimized DFT for real-valued signals:

```runa
Process called "dft_real" that takes signal as List[Float] returns DFTResult:
    Note: DFT for real-valued signals with frequency domain interpretation
    Let N be signal.size()
    Let complex_signal be List[Complex]
    
    Note: Convert real signal to complex representation
    For sample in signal:
        Call complex_signal.append(Complex{real: sample, imag: 0.0})
    
    Let spectrum be dft_direct(complex_signal)
    
    Note: Extract spectral properties
    Let frequencies be compute_frequency_bins(N, sampling_rate)
    Let magnitudes be List[Float]
    Let phases be List[Float]
    
    For coefficient in spectrum:
        Let magnitude be MathCore.sqrt(coefficient.real * coefficient.real + coefficient.imag * coefficient.imag)
        Let phase be MathCore.atan2(coefficient.imag, coefficient.real)
        Call magnitudes.append(magnitude)
        Call phases.append(phase)
    
    Let result be DFTResult with:
        frequencies = frequencies
        magnitudes = magnitudes
        phases = phases
        complex_spectrum = spectrum
        sampling_rate = sampling_rate
        frequency_resolution = sampling_rate / N
    
    Return result
```

### Spectrum Symmetry Exploitation

For real signals, the spectrum has Hermitian symmetry:

```runa
Process called "exploit_hermitian_symmetry" that takes spectrum as List[Complex] returns List[Complex]:
    Note: For real signals, X[k] = X*[N-k], so we only need to compute half
    Let N be spectrum.size()
    Let half_spectrum be List[Complex]
    
    Note: Compute only first half + Nyquist frequency
    For k from 0 to N / 2:
        Call half_spectrum.append(spectrum[k])
    
    Note: Reconstruct full spectrum using symmetry
    Let full_spectrum be List[Complex]
    For k from 0 to N / 2:
        Call full_spectrum.append(half_spectrum[k])
    
    For k from N / 2 + 1 to N - 1:
        Let symmetric_index be N - k
        Let conjugate be Complex with:
            real = half_spectrum[symmetric_index].real
            imag = -half_spectrum[symmetric_index].imag
        Call full_spectrum.append(conjugate)
    
    Return full_spectrum
```

## Spectral Analysis Tools

### Peak Detection

Finding dominant frequency components:

```runa
Process called "find_spectral_peaks" that takes magnitudes as List[Float], frequencies as List[Float], threshold as Float returns List[Dictionary[String, Float]]:
    Note: Detect peaks in magnitude spectrum above threshold
    Let peaks be List[Dictionary[String, Float]]
    
    For i from 1 to magnitudes.size() - 2:
        Let current_mag be magnitudes[i]
        Let left_mag be magnitudes[i - 1]
        Let right_mag be magnitudes[i + 1]
        
        Note: Local maximum condition
        If current_mag > left_mag and current_mag > right_mag and current_mag > threshold:
            Let peak be Dictionary[String, Float]
            Collections.set_item(peak, "frequency", frequencies[i])
            Collections.set_item(peak, "magnitude", current_mag)
            Collections.set_item(peak, "index", Float(i))
            Call peaks.append(peak)
    
    Note: Sort peaks by magnitude (strongest first)
    Return sort_peaks_by_magnitude(peaks)
```

### Spectral Centroid

Center of mass of the spectrum:

```runa
Process called "compute_spectral_centroid" that takes magnitudes as List[Float], frequencies as List[Float] returns Float:
    Note: Spectral centroid = Σ(f * |X[f]|) / Σ|X[f]|
    Let weighted_sum be 0.0
    Let total_magnitude be 0.0
    
    For i from 0 to magnitudes.size() - 1:
        Let magnitude be magnitudes[i]
        Let frequency be frequencies[i]
        Set weighted_sum to weighted_sum + frequency * magnitude
        Set total_magnitude to total_magnitude + magnitude
    
    If total_magnitude == 0.0:
        Return 0.0
    
    Return weighted_sum / total_magnitude
```

### Spectral Bandwidth

Spread of the spectrum around the centroid:

```runa
Process called "compute_spectral_bandwidth" that takes magnitudes as List[Float], frequencies as List[Float], centroid as Float returns Float:
    Note: Bandwidth = sqrt(Σ((f - centroid)² * |X[f]|) / Σ|X[f]|)
    Let weighted_variance_sum be 0.0
    Let total_magnitude be 0.0
    
    For i from 0 to magnitudes.size() - 1:
        Let magnitude be magnitudes[i]
        Let frequency be frequencies[i]
        Let deviation be frequency - centroid
        Set weighted_variance_sum to weighted_variance_sum + deviation * deviation * magnitude
        Set total_magnitude to total_magnitude + magnitude
    
    If total_magnitude == 0.0:
        Return 0.0
    
    Return MathCore.sqrt(weighted_variance_sum / total_magnitude)
```

## Sliding DFT for Real-Time Processing

### Single-Bin Sliding DFT

Efficient computation of individual frequency bins:

```runa
Process called "sliding_dft_single_bin" that takes new_sample as Float, old_sample as Float, previous_dft as Complex, frequency_bin as Integer, N as Integer returns Complex:
    Note: Goertzel-like algorithm for single bin update
    Let phase_increment be 2.0 * MathCore.pi() * frequency_bin / N
    Let cos_phi be MathCore.cos(phase_increment)
    Let sin_phi be MathCore.sin(phase_increment)
    
    Note: Remove old sample contribution
    Let old_contribution be Complex with:
        real = old_sample * cos_phi
        imag = old_sample * sin_phi
    
    Note: Update: X_new[k] = (X_old[k] - old_sample + new_sample) * W_N^k
    Let updated_dft be Complex with:
        real = (previous_dft.real - old_sample + new_sample) * cos_phi - (previous_dft.imag) * sin_phi
        imag = (previous_dft.real - old_sample + new_sample) * sin_phi + (previous_dft.imag) * cos_phi
    
    Return updated_dft
```

### Multi-Bin Sliding DFT

Updating multiple frequency bins simultaneously:

```runa
Process called "sliding_dft_update" that takes new_sample as Float, old_sample as Float, previous_spectrum as List[Complex], N as Integer returns List[Complex]:
    Note: Sliding DFT for all frequency bins
    Let updated_spectrum be List[Complex]
    
    For k from 0 to N - 1:
        Let updated_bin be sliding_dft_single_bin(new_sample, old_sample, previous_spectrum[k], k, N)
        Call updated_spectrum.append(updated_bin)
    
    Return updated_spectrum
```

## Windowing Integration

### Windowed DFT Analysis

Applying window functions to reduce spectral leakage:

```runa
Process called "windowed_dft" that takes signal as List[Float], window_function as String, sampling_rate as Float returns DFTResult:
    Note: Apply windowing before DFT to reduce spectral leakage
    Let N be signal.size()
    Let window be generate_window(window_function, N)
    Let windowed_signal be List[Float]
    
    Note: Apply window to signal
    For i from 0 to N - 1:
        Let windowed_sample be signal[i] * window[i]
        Call windowed_signal.append(windowed_sample)
    
    Note: Compute DFT of windowed signal
    Let dft_result be dft_real(windowed_signal, sampling_rate)
    
    Note: Correct for window gain
    Let window_gain be compute_window_coherent_gain(window)
    For i from 0 to dft_result.magnitudes.size() - 1:
        Set dft_result.magnitudes[i] to dft_result.magnitudes[i] / window_gain
    
    Return dft_result
```

### Window Gain Correction

Compensating for window function effects:

```runa
Process called "compute_window_coherent_gain" that takes window as List[Float] returns Float:
    Note: Coherent gain = sum of window coefficients / N
    Let sum be 0.0
    For coefficient in window:
        Set sum to sum + coefficient
    Return sum / window.size()

Process called "compute_window_processing_gain" that takes window as List[Float] returns Float:
    Note: Processing gain = sqrt(sum of squared coefficients) / N
    Let sum_of_squares be 0.0
    For coefficient in window:
        Set sum_of_squares to sum_of_squares + coefficient * coefficient
    Return MathCore.sqrt(sum_of_squares) / window.size()
```

## Zero Padding and Interpolation

### Zero-Padded DFT

Increasing frequency resolution through zero padding:

```runa
Process called "zero_padded_dft" that takes signal as List[Float], target_length as Integer, sampling_rate as Float returns DFTResult:
    Note: Zero padding increases frequency resolution but doesn't add information
    Let N be signal.size()
    If target_length < N:
        Set target_length to N  Note: can't reduce length
    
    Let padded_signal be List[Float]
    
    Note: Copy original signal
    For sample in signal:
        Call padded_signal.append(sample)
    
    Note: Add zeros
    For i from N to target_length - 1:
        Call padded_signal.append(0.0)
    
    Let result be dft_real(padded_signal, sampling_rate)
    
    Note: Update frequency resolution
    Set result.frequency_resolution to sampling_rate / target_length
    
    Return result
```

### Interpolated Spectral Analysis

Higher resolution spectral analysis:

```runa
Process called "interpolated_spectrum" that takes dft_result as DFTResult, interpolation_factor as Integer returns DFTResult:
    Note: Interpolate spectrum for smoother visualization
    Let original_size be dft_result.frequencies.size()
    Let new_size be original_size * interpolation_factor
    
    Let interpolated_frequencies be List[Float]
    Let interpolated_magnitudes be List[Float]
    Let interpolated_phases be List[Float]
    
    For i from 0 to new_size - 1:
        Let original_index be Float(i) / interpolation_factor
        Let interpolated_freq be interpolate_linear(dft_result.frequencies, original_index)
        Let interpolated_mag be interpolate_linear(dft_result.magnitudes, original_index)
        Let interpolated_phase be interpolate_linear(dft_result.phases, original_index)
        
        Call interpolated_frequencies.append(interpolated_freq)
        Call interpolated_magnitudes.append(interpolated_mag)
        Call interpolated_phases.append(interpolated_phase)
    
    Let result be DFTResult with:
        frequencies = interpolated_frequencies
        magnitudes = interpolated_magnitudes
        phases = interpolated_phases
        complex_spectrum = reconstruct_complex_spectrum(interpolated_magnitudes, interpolated_phases)
        sampling_rate = dft_result.sampling_rate
        frequency_resolution = dft_result.frequency_resolution / interpolation_factor
    
    Return result
```

## Practical Applications

### Signal Classification

Using spectral features for classification:

```runa
Process called "extract_spectral_features" that takes signal as List[Float], sampling_rate as Float returns Dictionary[String, Float]:
    Note: Extract features commonly used for signal classification
    Let dft_result be dft_real(signal, sampling_rate)
    Let properties be compute_spectral_properties(dft_result)
    
    Let features be Dictionary[String, Float]
    Collections.set_item(features, "peak_frequency", properties.peak_frequency)
    Collections.set_item(features, "spectral_centroid", properties.spectral_centroid)
    Collections.set_item(features, "spectral_bandwidth", properties.spectral_bandwidth)
    Collections.set_item(features, "spectral_rolloff", properties.spectral_rolloff)
    Collections.set_item(features, "spectral_flatness", properties.spectral_flatness)
    Collections.set_item(features, "zero_crossing_rate", compute_zero_crossing_rate(signal))
    
    Note: Additional derived features
    Collections.set_item(features, "bandwidth_to_centroid_ratio", properties.spectral_bandwidth / properties.spectral_centroid)
    Collections.set_item(features, "peak_to_average_ratio", properties.peak_magnitude / compute_average_magnitude(dft_result.magnitudes))
    
    Return features
```

### Harmonic Analysis

Detecting and analyzing harmonic content:

```runa
Process called "harmonic_analysis" that takes signal as List[Float], fundamental_freq as Float, sampling_rate as Float, max_harmonics as Integer returns List[Dictionary[String, Float]]:
    Note: Analyze harmonic content of a signal given fundamental frequency
    Let dft_result be dft_real(signal, sampling_rate)
    Let harmonics be List[Dictionary[String, Float]]
    
    For harmonic_number from 1 to max_harmonics:
        Let expected_freq be fundamental_freq * harmonic_number
        Let frequency_tolerance be dft_result.frequency_resolution * 2.0
        
        Note: Find the bin closest to expected harmonic frequency
        Let best_index be find_closest_frequency_bin(dft_result.frequencies, expected_freq)
        Let actual_freq be dft_result.frequencies[best_index]
        
        If MathCore.abs(actual_freq - expected_freq) <= frequency_tolerance:
            Let harmonic be Dictionary[String, Float]
            Collections.set_item(harmonic, "harmonic_number", Float(harmonic_number))
            Collections.set_item(harmonic, "expected_frequency", expected_freq)
            Collections.set_item(harmonic, "actual_frequency", actual_freq)
            Collections.set_item(harmonic, "magnitude", dft_result.magnitudes[best_index])
            Collections.set_item(harmonic, "phase", dft_result.phases[best_index])
            Call harmonics.append(harmonic)
    
    Return harmonics
```

### Frequency Domain Filtering

Implementing filters in the frequency domain:

```runa
Process called "frequency_domain_filter" that takes signal as List[Float], filter_type as String, cutoff_frequencies as List[Float], sampling_rate as Float returns List[Float]:
    Note: Apply frequency domain filtering
    Let dft_result be dft_real(signal, sampling_rate)
    Let filtered_spectrum be List[Complex]
    
    For i from 0 to dft_result.complex_spectrum.size() - 1:
        Let frequency be dft_result.frequencies[i]
        Let filter_gain be compute_filter_gain(filter_type, frequency, cutoff_frequencies)
        
        Let original_coeff be dft_result.complex_spectrum[i]
        Let filtered_coeff be Complex with:
            real = original_coeff.real * filter_gain
            imag = original_coeff.imag * filter_gain
        
        Call filtered_spectrum.append(filtered_coeff)
    
    Note: Convert back to time domain
    Let filtered_signal_complex be idft_direct(filtered_spectrum)
    Let filtered_signal be List[Float]
    
    For coefficient in filtered_signal_complex:
        Call filtered_signal.append(coefficient.real)  Note: take real part
    
    Return filtered_signal
```

## Performance Considerations

### Computational Complexity

The direct DFT has O(N²) complexity:

```runa
Process called "estimate_dft_complexity" that takes signal_length as Integer returns Dictionary[String, Integer]:
    Note: Estimate computational requirements for direct DFT
    Let complexity_info be Dictionary[String, Integer]
    
    Let complex_multiplications be signal_length * signal_length
    Let complex_additions be signal_length * (signal_length - 1)
    Let trigonometric_evaluations be signal_length * signal_length * 2  Note: cos and sin
    
    Collections.set_item(complexity_info, "complex_multiplications", complex_multiplications)
    Collections.set_item(complexity_info, "complex_additions", complex_additions)
    Collections.set_item(complexity_info, "trigonometric_evaluations", trigonometric_evaluations)
    Collections.set_item(complexity_info, "total_operations", complex_multiplications + complex_additions + trigonometric_evaluations)
    
    Return complexity_info
```

### Memory Usage Optimization

Efficient memory management for large transforms:

```runa
Process called "memory_efficient_dft" that takes signal as List[Float], output_buffer as List[Complex] returns Boolean:
    Note: In-place DFT computation to minimize memory allocation
    Let N be signal.size()
    If output_buffer.size() < N:
        Return false  Note: insufficient buffer space
    
    Note: Clear output buffer
    For i from 0 to N - 1:
        Set output_buffer[i].real to 0.0
        Set output_buffer[i].imag to 0.0
    
    Note: Compute DFT directly into output buffer
    For k from 0 to N - 1:
        For n from 0 to N - 1:
            Let angle be -2.0 * MathCore.pi() * k * n / N
            Let cos_angle be MathCore.cos(angle)
            Let sin_angle be MathCore.sin(angle)
            
            Set output_buffer[k].real to output_buffer[k].real + signal[n] * cos_angle
            Set output_buffer[k].imag to output_buffer[k].imag + signal[n] * sin_angle
    
    Return true
```

## Numerical Accuracy and Validation

### DFT Accuracy Verification

Comparing DFT results with analytical solutions:

```runa
Process called "verify_dft_accuracy" that takes test_frequency as Float, sampling_rate as Float, signal_length as Integer returns Dictionary[String, Float]:
    Note: Test DFT accuracy using a known sinusoidal signal
    Let test_signal be List[Float]
    
    Note: Generate pure sinusoid
    For n from 0 to signal_length - 1:
        Let time be Float(n) / sampling_rate
        let sample be MathCore.sin(2.0 * MathCore.pi() * test_frequency * time)
        Call test_signal.append(sample)
    
    Let dft_result be dft_real(test_signal, sampling_rate)
    
    Note: Find the peak in the spectrum
    Let peak_index be find_peak_frequency_index(dft_result.magnitudes)
    Let detected_frequency be dft_result.frequencies[peak_index]
    Let peak_magnitude be dft_result.magnitudes[peak_index]
    
    Note: Theoretical values for a pure sinusoid
    Let expected_magnitude be signal_length / 2.0  Note: for unit amplitude sinusoid
    
    Let accuracy_report be Dictionary[String, Float]
    Collections.set_item(accuracy_report, "frequency_error", MathCore.abs(detected_frequency - test_frequency))
    Collections.set_item(accuracy_report, "magnitude_error", MathCore.abs(peak_magnitude - expected_magnitude))
    Collections.set_item(accuracy_report, "relative_frequency_error", MathCore.abs(detected_frequency - test_frequency) / test_frequency)
    Collections.set_item(accuracy_report, "relative_magnitude_error", MathCore.abs(peak_magnitude - expected_magnitude) / expected_magnitude)
    
    Return accuracy_report
```

The DFT module provides the mathematical foundation for frequency domain analysis, offering precise and educational implementations that demonstrate the fundamental principles of spectral analysis while serving practical applications in signal processing and analysis.