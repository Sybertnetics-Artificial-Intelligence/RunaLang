Note: Math Core Conversion Module

## Overview

The `math/core/conversion` module provides comprehensive mathematical unit and format conversion operations. It handles angular units, numerical bases, coordinate systems, temperature scales, scientific notation, and various other mathematical representations with high precision and error handling.

## Key Features

- **Angular Conversions**: Degrees, radians, gradians, and turns
- **Base Conversions**: Binary, octal, decimal, hexadecimal, and arbitrary bases
- **Scientific Notation**: Engineering and scientific format conversions
- **Coordinate Systems**: Cartesian, polar, spherical, and cylindrical
- **Temperature Scales**: Celsius, Fahrenheit, Kelvin, and Rankine
- **Precision Control**: Arbitrary precision support for all conversions

## Data Types

### ConversionResult
Represents the result of a conversion operation:
```runa
Type called "ConversionResult":
    conversion_type as String       Note: Type of conversion performed
    original_value as String        Note: Input value
    converted_value as String       Note: Output value
    original_unit as String         Note: Source unit
    target_unit as String          Note: Destination unit
    conversion_factor as String     Note: Conversion multiplier
    precision_used as Integer       Note: Precision level
    error_occurred as Boolean       Note: Error flag
    unsupported_unit_error as Boolean # Unit support error
```

### CoordinateSystem
Represents coordinate system conversion parameters:
```runa
Type called "CoordinateSystem":
    system_type as String          Note: cartesian/polar/spherical/cylindrical
    coordinates as List[String]    Note: Coordinate values
    unit_system as String         Note: Unit specification
    precision as Integer          Note: Calculation precision
```

## Angular Unit Conversions

### Basic Angular Conversions
```runa
Note: Convert between common angle units
Let angle_degrees be "180"
Let precision be 50

Note: Degrees to radians
Let to_radians be Conversion.angle_to_radians(angle_degrees, precision)
Display "180° = " joined with to_radians.converted_value joined with " radians"

Note: Radians to degrees
Let pi_radians be "3.14159265358979323846"
Let to_degrees be Conversion.angle_to_degrees(pi_radians, precision)
Display "π radians = " joined with to_degrees.converted_value joined with "°"
```

### Comprehensive Angular Conversion
```runa
Note: Convert between all angle units
Let angle be "90"  Note: degrees
Let precision be 30

Let conversions be Conversion.convert_angle_units(angle, "degrees", precision)
Display "90 degrees equals:"
Display "  Radians: " joined with conversions["radians"]
Display "  Gradians: " joined with conversions["gradians"]
Display "  Turns: " joined with conversions["turns"]
Display "  Mils: " joined with conversions["mils"]
```

### Angular Arithmetic with Units
```runa
Note: Perform arithmetic operations with angle units
Let angle1 be "45"   Note: degrees
Let angle2 be "60"   Note: degrees

Let sum_angles be Conversion.add_angles(angle1, angle2, "degrees", 30)
Let diff_angles be Conversion.subtract_angles(angle2, angle1, "degrees", 30)

Display "45° joined with 60° = " joined with sum_angles.converted_value joined with "°"
Display "60° - 45° = " joined with diff_angles.converted_value joined with "°"

Note: Convert result to radians
Let sum_in_radians be Conversion.angle_to_radians(sum_angles.converted_value, 30)
Display "105° = " joined with sum_in_radians.converted_value joined with " radians"
```

## Numerical Base Conversions

### Common Base Conversions
```runa
Note: Convert between common number bases
Let decimal_num be "255"

Let binary be Conversion.decimal_to_binary(decimal_num)
Let octal be Conversion.decimal_to_octal(decimal_num)
Let hexadecimal be Conversion.decimal_to_hexadecimal(decimal_num)

Display "255₁₀ = " joined with binary.converted_value joined with "₂"     Note: 11111111
Display "255₁₀ = " joined with octal.converted_value joined with "₈"      Note: 377
Display "255₁₀ = " joined with hexadecimal.converted_value joined with "₁₆" # FF
```

### Arbitrary Base Conversion
```runa
Note: Convert to any base from 2 to 36
Let number be "1000"
Let target_base be 7

Let base7_result be Conversion.convert_to_base(number, 10, target_base)
Display "1000₁₀ = " joined with base7_result.converted_value joined with "₇"

Note: Convert back to decimal
Let back_to_decimal be Conversion.convert_to_base(base7_result.converted_value, target_base, 10)
Display base7_result.converted_value joined with "₇ = " joined with back_to_decimal.converted_value joined with "₁₀"
```

### Fractional Base Conversion
```runa
Note: Convert fractional numbers between bases
Let fractional_decimal be "123.456"

Let fractional_binary be Conversion.convert_fractional_base(fractional_decimal, 10, 2, 20)
Let fractional_hex be Conversion.convert_fractional_base(fractional_decimal, 10, 16, 10)

Display "123.456₁₀ = " joined with fractional_binary.converted_value joined with "₂"
Display "123.456₁₀ = " joined with fractional_hex.converted_value joined with "₁₆"
```

## Scientific and Engineering Notation

### Scientific Notation
```runa
Note: Convert to scientific notation
Let large_number be "123456789.123456789"
Let small_number be "0.000000123456789"

Let large_scientific be Conversion.to_scientific_notation(large_number, 6)
Let small_scientific be Conversion.to_scientific_notation(small_number, 6)

Display "Large number: " joined with large_scientific.converted_value  Note: 1.23457E+8
Display "Small number: " joined with small_scientific.converted_value  Note: 1.23457E-7
```

### Engineering Notation
```runa
Note: Convert to engineering notation (powers of 3)
Let number be "12345"

Let engineering be Conversion.to_engineering_notation(number, 4)
Display "Engineering notation: " joined with engineering.converted_value  Note: 12.35E+3

Note: From scientific back to decimal
Let scientific_input be "1.234E+5"
Let back_to_decimal be Conversion.from_scientific_notation(scientific_input)
Display "Back to decimal: " joined with back_to_decimal.converted_value  Note: 123400
```

### Significant Figures
```runa
Note: Control significant figures in conversions
Let measurement be "123.456789"

Let sig_fig_3 be Conversion.to_significant_figures(measurement, 3)
Let sig_fig_5 be Conversion.to_significant_figures(measurement, 5)

Display "3 significant figures: " joined with sig_fig_3.converted_value  Note: 123
Display "5 significant figures: " joined with sig_fig_5.converted_value  Note: 123.46
```

## Coordinate System Conversions

### Cartesian to Polar
```runa
Note: Convert 2D Cartesian coordinates to polar
Let x be "3.0"
Let y be "4.0"
Let precision be 30

Let cartesian_coords be CoordinateSystem with:
    system_type: "cartesian"
    coordinates: [x, y]
    precision: precision

Let polar_result be Conversion.cartesian_to_polar(cartesian_coords)
Display "Cartesian (3, 4 = Polar (r=" joined with polar_result.coordinates[0] joined with ", θ=" joined with polar_result.coordinates[1] joined with ")")
```

### Polar to Cartesian
```runa
Note: Convert polar coordinates back to Cartesian
Let radius be "5.0"
Let angle be "0.927295218"  Note: arctan(4/3)

Let polar_coords be CoordinateSystem with:
    system_type: "polar"
    coordinates: [radius, angle]
    precision: 30

Let cartesian_result be Conversion.polar_to_cartesian(polar_coords)
Display "Polar (5, 0.927 = Cartesian (x=" joined with cartesian_result.coordinates[0] joined with ", y=" joined with cartesian_result.coordinates[1] joined with ")")
```

### 3D Coordinate Conversions
```runa
Note: Spherical to Cartesian conversion
Let spherical_coords be CoordinateSystem with:
    system_type: "spherical"
    coordinates: ["10.0", "1.047", "0.785"]  Note: r, θ, φ (radius, azimuth, elevation)
    precision: 30

Let cartesian_3d be Conversion.spherical_to_cartesian(spherical_coords)
Display "Spherical (10, 60°, 45° = Cartesian:")
Display "  x = " joined with cartesian_3d.coordinates[0]
Display "  y = " joined with cartesian_3d.coordinates[1]
Display "  z = " joined with cartesian_3d.coordinates[2]

Note: Cylindrical to Cartesian conversion
Let cylindrical_coords be CoordinateSystem with:
    system_type: "cylindrical"
    coordinates: ["5.0", "1.047", "3.0"]  Note: ρ, φ, z
    precision: 30

Let cartesian_from_cyl be Conversion.cylindrical_to_cartesian(cylindrical_coords)
Display "Cylindrical (5, 60°, 3 = Cartesian:")
Display "  x = " joined with cartesian_from_cyl.coordinates[0]
Display "  y = " joined with cartesian_from_cyl.coordinates[1]
Display "  z = " joined with cartesian_from_cyl.coordinates[2]
```

## Temperature Conversions

### Basic Temperature Scales
```runa
Note: Convert between temperature scales
Let celsius be "25.0"
Let fahrenheit be "77.0"
Let kelvin be "298.15"

Note: Celsius conversions
Let c_to_f be Conversion.celsius_to_fahrenheit(celsius, 10)
Let c_to_k be Conversion.celsius_to_kelvin(celsius, 10)

Display "25°C = " joined with c_to_f.converted_value joined with "°F"
Display "25°C = " joined with c_to_k.converted_value joined with " K"

Note: Fahrenheit conversions
Let f_to_c be Conversion.fahrenheit_to_celsius(fahrenheit, 10)
Let f_to_k be Conversion.fahrenheit_to_kelvin(fahrenheit, 10)

Display "77°F = " joined with f_to_c.converted_value joined with "°C"
Display "77°F = " joined with f_to_k.converted_value joined with " K"
```

### Absolute Temperature Scales
```runa
Note: Work with absolute temperature scales
Let kelvin_temp be "273.15"
Let rankine_temp be "491.67"

Let k_to_c be Conversion.kelvin_to_celsius(kelvin_temp, 10)
Let k_to_r be Conversion.kelvin_to_rankine(kelvin_temp, 10)

Display "273.15 K = " joined with k_to_c.converted_value joined with "°C"  Note: 0°C
Display "273.15 K = " joined with k_to_r.converted_value joined with "°R"  Note: 491.67°R

Let r_to_f be Conversion.rankine_to_fahrenheit(rankine_temp, 10)
Display "491.67°R = " joined with r_to_f.converted_value joined with "°F"  Note: 32°F
```

### Temperature Difference Conversions
```runa
Note: Convert temperature differences (not absolute temperatures)
Let temp_diff_c be "10.0"  Note: 10°C difference

Let diff_to_f be Conversion.celsius_diff_to_fahrenheit_diff(temp_diff_c)
Let diff_to_k be Conversion.celsius_diff_to_kelvin_diff(temp_diff_c)

Display "Temperature difference:"
Display "10°C = " joined with diff_to_f.converted_value joined with "°F"  Note: 18°F
Display "10°C = " joined with diff_to_k.converted_value joined with " K"  Note: 10 K
```

## Physical Unit Conversions

### Length Conversions
```runa
Note: Convert between length units
Let meters be "100"

Let length_conversions be Conversion.convert_length_units(meters, "meters", 30)
Display "100 meters equals:"
Display "  Kilometers: " joined with length_conversions["kilometers"]
Display "  Centimeters: " joined with length_conversions["centimeters"]
Display "  Inches: " joined with length_conversions["inches"]
Display "  Feet: " joined with length_conversions["feet"]
Display "  Yards: " joined with length_conversions["yards"]
Display "  Miles: " joined with length_conversions["miles"]
```

### Mass Conversions
```runa
Note: Convert between mass units
Let kilograms be "50"

Let mass_conversions be Conversion.convert_mass_units(kilograms, "kilograms", 30)
Display "50 kilograms equals:"
Display "  Grams: " joined with mass_conversions["grams"]
Display "  Pounds: " joined with mass_conversions["pounds"]
Display "  Ounces: " joined with mass_conversions["ounces"]
Display "  Stones: " joined with mass_conversions["stones"]
```

### Volume Conversions
```runa
Note: Convert between volume units
Let liters be "10"

Let volume_conversions be Conversion.convert_volume_units(liters, "liters", 30)
Display "10 liters equals:"
Display "  Milliliters: " joined with volume_conversions["milliliters"]
Display "  Gallons (US: " joined with volume_conversions["gallons_us"])
Display "  Gallons (UK: " joined with volume_conversions["gallons_uk"])
Display "  Quarts: " joined with volume_conversions["quarts"]
Display "  Pints: " joined with volume_conversions["pints"]
```

## Time Unit Conversions

### Standard Time Units
```runa
Note: Convert between time units
Let seconds be "3661"  Note: 1 hour, 1 minute, 1 second

Let time_conversions be Conversion.convert_time_units(seconds, "seconds", 30)
Display "3661 seconds equals:"
Display "  Minutes: " joined with time_conversions["minutes"]
Display "  Hours: " joined with time_conversions["hours"]
Display "  Days: " joined with time_conversions["days"]

Note: Format as time string
Let time_formatted be Conversion.seconds_to_time_string(seconds)
Display "Formatted: " joined with time_formatted.converted_value  Note: "01:01:01"
```

### Astronomical Time Units
```runa
Note: Convert to astronomical time units
Let earth_days be "365.25"

Let astro_conversions be Conversion.convert_astronomical_time(earth_days, "days", 30)
Display "365.25 days equals:"
Display "  Sidereal days: " joined with astro_conversions["sidereal_days"]
Display "  Julian years: " joined with astro_conversions["julian_years"]
Display "  Tropical years: " joined with astro_conversions["tropical_years"]
```

## Energy and Power Conversions

### Energy Units
```runa
Note: Convert between energy units
Let joules be "1000"

Let energy_conversions be Conversion.convert_energy_units(joules, "joules", 30)
Display "1000 joules equals:"
Display "  Calories: " joined with energy_conversions["calories"]
Display "  Kilocalories: " joined with energy_conversions["kilocalories"]
Display "  BTU: " joined with energy_conversions["btu"]
Display "  Kilowatt-hours: " joined with energy_conversions["kwh"]
Display "  Electron volts: " joined with energy_conversions["ev"]
```

### Power Units
```runa
Note: Convert between power units
Let watts be "1000"

Let power_conversions be Conversion.convert_power_units(watts, "watts", 30)
Display "1000 watts equals:"
Display "  Kilowatts: " joined with power_conversions["kilowatts"]
Display "  Horsepower: " joined with power_conversions["horsepower"]
Display "  BTU/hour: " joined with power_conversions["btu_per_hour"]
```

## Pressure and Force Conversions

### Pressure Units
```runa
Note: Convert between pressure units
Let pascals be "101325"  Note: Standard atmospheric pressure

Let pressure_conversions be Conversion.convert_pressure_units(pascals, "pascals", 30)
Display "101325 pascals (1 atm equals:")
Display "  Atmospheres: " joined with pressure_conversions["atmospheres"]
Display "  mmHg: " joined with pressure_conversions["mmhg"]
Display "  PSI: " joined with pressure_conversions["psi"]
Display "  Bar: " joined with pressure_conversions["bar"]
```

### Force Units
```runa
Note: Convert between force units
Let newtons be "100"

Let force_conversions be Conversion.convert_force_units(newtons, "newtons", 30)
Display "100 newtons equals:"
Display "  Pounds-force: " joined with force_conversions["pounds_force"]
Display "  Dynes: " joined with force_conversions["dynes"]
Display "  Kilograms-force: " joined with force_conversions["kilograms_force"]
```

## Data Storage Conversions

### Binary and Decimal Storage Units
```runa
Note: Convert between storage units
Let bytes be "1048576"  Note: 1 MiB

Let storage_conversions be Conversion.convert_storage_units(bytes, "bytes", 30)
Display "1048576 bytes equals:"
Display "  Kilobytes (decimal: " joined with storage_conversions["kb_decimal"])    Note: 1000^1
Display "  Kibibytes (binary: " joined with storage_conversions["kib_binary"])     Note: 1024^1
Display "  Megabytes (decimal: " joined with storage_conversions["mb_decimal"])    Note: 1000^2
Display "  Mebibytes (binary: " joined with storage_conversions["mib_binary"])     Note: 1024^2
```

### Bit and Byte Conversions
```runa
Note: Convert between bits and bytes
Let bits be "8192"

Let bit_conversions be Conversion.convert_bit_byte_units(bits, "bits", 30)
Display "8192 bits equals:"
Display "  Bytes: " joined with bit_conversions["bytes"]
Display "  Kilobits: " joined with bit_conversions["kilobits"]
Display "  Kilobytes: " joined with bit_conversions["kilobytes"]
```

## Frequency and Wavelength Conversions

### Electromagnetic Spectrum
```runa
Note: Convert between frequency and wavelength
Let frequency_hz be "299792458"  Note: 1 meter wavelength in Hz

Let wave_conversions be Conversion.frequency_to_wavelength(frequency_hz, "vacuum", 30)
Display "299,792,458 Hz in vacuum:"
Display "  Wavelength (m: " joined with wave_conversions.converted_value)
Display "  Wavelength (mm: " joined with Conversion.convert_length_units(wave_conversions.converted_value, "meters", 30)["millimeters"])

Note: Convert back
Let wavelength_m be "1.0"
Let back_to_freq be Conversion.wavelength_to_frequency(wavelength_m, "vacuum", 30)
Display "1 meter wavelength = " joined with back_to_freq.converted_value joined with " Hz"
```

### Audio Frequencies
```runa
Note: Audio frequency conversions
Let frequency be "440"  Note: A4 note

Let audio_conversions be Conversion.convert_audio_frequencies(frequency, "Hz", 30)
Display "440 Hz (A4 equals:")
Display "  Period: " joined with audio_conversions["period"] joined with " seconds"
Display "  Wavelength in air: " joined with audio_conversions["wavelength_air"] joined with " meters"
Display "  MIDI note number: " joined with audio_conversions["midi_note"]
```

## Mathematical Format Conversions

### Fraction and Decimal Conversions
```runa
Note: Convert between fractions and decimals
Let decimal be "0.75"
Let precision be 30

Let to_fraction be Conversion.decimal_to_fraction(decimal, 1000)  Note: Max denominator
Display "0.75 = " joined with to_fraction.converted_value  Note: "3/4"

Let fraction be "22/7"
Let to_decimal be Conversion.fraction_to_decimal(fraction, precision)
Display "22/7 = " joined with to_decimal.converted_value
```

### Percentage Conversions
```runa
Note: Convert between decimals and percentages
Let decimal_value be "0.25"
Let percentage_value be "75"

Let to_percentage be Conversion.decimal_to_percentage(decimal_value, 2)
Let to_decimal be Conversion.percentage_to_decimal(percentage_value, 10)

Display "0.25 = " joined with to_percentage.converted_value joined with "%"
Display "75% = " joined with to_decimal.converted_value
```

### Complex Number Format Conversions
```runa
Note: Convert between rectangular and polar forms
Let complex_rectangular be "3+4i"
Let precision be 30

Let to_polar be Conversion.rectangular_to_polar_complex(complex_rectangular, precision)
Display "3+4i = " joined with to_polar.converted_value joined with " (polar form")

Let complex_polar be "5∠0.927"
Let to_rectangular be Conversion.polar_to_rectangular_complex(complex_polar, precision)
Display "5∠0.927 = " joined with to_rectangular.converted_value joined with " (rectangular form")
```

## Statistical Distribution Parameter Conversions

### Normal Distribution Parameters
```runa
Note: Convert between different parameterizations
Let mean be "100"
Let std_dev be "15"

Note: Convert to standardized form
Let standardized be Conversion.normalize_distribution_parameters(mean, std_dev, "normal")
Display "N(100, 15² standardized parameters:")
Display "  Location: " joined with standardized["location"]
Display "  Scale: " joined with standardized["scale"]

Note: Convert variance to standard deviation
Let variance be "225"  Note: 15²
Let std_from_var be Conversion.variance_to_standard_deviation(variance, 30)
Display "Variance 225 = Standard deviation " joined with std_from_var.converted_value
```

## Currency and Financial Conversions

### Currency Exchange
```runa
Note: Currency conversion with exchange rates
Let amount_usd be "100"
Let exchange_rates be Dictionary with:
    "USD_to_EUR": "0.85"
    "USD_to_GBP": "0.75"
    "USD_to_JPY": "110.0"

Let eur_amount be Conversion.convert_currency(amount_usd, "USD", "EUR", exchange_rates, 10)
Let gbp_amount be Conversion.convert_currency(amount_usd, "USD", "GBP", exchange_rates, 10)

Display "$100 USD equals:"
Display "  €" joined with eur_amount.converted_value joined with " EUR"
Display "  £" joined with gbp_amount.converted_value joined with " GBP"
```

### Financial Calculations
```runa
Note: Interest rate conversions
Let annual_rate be "0.05"  Note: 5% annual

Let monthly_rate be Conversion.annual_to_monthly_interest_rate(annual_rate, 10)
Let daily_rate be Conversion.annual_to_daily_interest_rate(annual_rate, 10)

Display "5% annual interest rate equals:"
Display "  Monthly: " joined with String(Parse monthly_rate.converted_value as Float * 100 joined with "%"))
Display "  Daily: " joined with String(Parse daily_rate.converted_value as Float * 100 joined with "%"))
```

## Advanced Conversion Features

### Batch Conversions
```runa
Note: Convert multiple values at once
Let values be ["10", "20", "30", "40", "50"]
Let from_unit be "celsius"
Let to_unit be "fahrenheit"

Let batch_results be Conversion.batch_convert_temperature(values, from_unit, to_unit, 10)
Display "Batch temperature conversion (°C to °F:")
For i from 0 to Length(values) - 1:
    Display "  " joined with values[i] joined with "°C = " joined with batch_results[i] joined with "°F"
```

### Custom Unit Definitions
```runa
Note: Define custom conversion factors
Let custom_units be Dictionary with:
    "furlong_to_meter": "201.168"
    "fortnight_to_second": "1209600"

Let distance_furlongs be "5"
Let custom_distance be Conversion.convert_with_custom_factor(
    distance_furlongs, 
    custom_units["furlong_to_meter"], 
    30
)
Display "5 furlongs = " joined with custom_distance.converted_value joined with " meters"
```

### Conversion Chains
```runa
Note: Chain multiple conversions
Let conversion_chain be [
    Dictionary with: "from": "fahrenheit", "to": "celsius", "value": "212",
    Dictionary with: "from": "celsius", "to": "kelvin", "value": "result_of_previous"
]

Let chained_result be Conversion.execute_conversion_chain(conversion_chain, 30)
Display "212°F → °C → K = " joined with chained_result.converted_value joined with " K"
```

## Error Handling

The conversion module provides comprehensive error handling:

```runa
Note: Unsupported unit conversion
Try:
    Let invalid_conversion be Conversion.convert_length_units("100", "invalid_unit", 30)
Catch Errors.ConversionError as error:
    Display "Conversion error: " joined with error.message
    If error.unsupported_unit_error:
        Display "Supported units: meters, kilometers, feet, inches, yards, miles"

Note: Division by zero in custom conversions
Try:
    Let zero_factor be Conversion.convert_with_custom_factor("100", "0", 30)
Catch Errors.MathematicalError as error:
    Display "Mathematical error: " joined with error.message

Note: Domain errors for temperature conversions
Try:
    Let below_absolute_zero be Conversion.celsius_to_kelvin("-300", 30)
Catch Errors.MathematicalError as error:
    Display "Temperature below absolute zero: " joined with error.message
```

## Performance Considerations

- **Precision Settings**: Higher precision increases computation time
- **Batch Operations**: Use batch conversions for multiple values
- **Caching**: Conversion factors are cached for repeated operations
- **Custom Units**: Define custom factors for specialized applications

## Best Practices

1. **Specify Precision**: Always specify appropriate precision for your use case
2. **Validate Inputs**: Check for valid ranges, especially for temperature conversions
3. **Use Appropriate Units**: Choose the most suitable unit system for your application
4. **Handle Errors**: Always wrap conversions in error handling blocks
5. **Document Units**: Clearly document the units used in your calculations
6. **Test Conversions**: Verify conversion results with known reference values