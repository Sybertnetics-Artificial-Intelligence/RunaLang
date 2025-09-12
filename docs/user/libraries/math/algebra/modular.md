# Modular Arithmetic Module

The `math/algebra/modular` module provides comprehensive modular arithmetic and algebraic structures over finite rings and fields. This module is essential for number theory, cryptography, coding theory, and discrete mathematics applications.

## Quick Start

```runa
Import "math/algebra/modular" as Modular

Note: Basic modular arithmetic operations
Let mod_ring be Modular.create_modular_ring(15)
Let a be mod_ring.create_element(7)
Let b be mod_ring.create_element(11)

Let sum be Modular.add(a, b)
Let product be Modular.multiply(a, b)
Let inverse_a be Modular.multiplicative_inverse(a)

Display "7 + 11 ≡ " joined with sum.value joined with " (mod 15)"
Display "7 × 11 ≡ " joined with product.value joined with " (mod 15)"
Display "7^(-1) ≡ " joined with inverse_a.value joined with " (mod 15)"
```

## Core Concepts

### Modular Arithmetic
Arithmetic performed with respect to a modulus, where numbers are considered equivalent if they differ by a multiple of the modulus.

### Rings of Integers Modulo n
The ring Z/nZ consisting of equivalence classes of integers modulo n.

### Finite Fields
Fields with finitely many elements, crucial for cryptography and error correction.

### Quadratic Residues
Study of which numbers are squares modulo a prime.

### Elliptic Curves
Algebraic curves with group structure, fundamental to modern cryptography.

## API Reference

### Modular Ring Construction

#### Basic Modular Rings
```runa
Type called "ModularRing":
    modulus as Integer
    elements as Set[ModularElement]
    is_field as Boolean
    characteristic as Integer
    units as Set[ModularElement]

Type called "ModularElement":
    value as Integer
    modulus as Integer
    ring as ModularRing

Process called "create_modular_ring" that takes modulus as Integer returns ModularRing:
    Note: Create ring Z/nZ of integers modulo n

Process called "create_element" that takes:
    value as Integer,
    ring as ModularRing
returns ModularElement:
    Note: Create element in modular ring
```

#### Modular Arithmetic Operations
```runa
Process called "add" that takes:
    a as ModularElement,
    b as ModularElement
returns ModularElement:
    Note: Add two elements in modular ring

Process called "multiply" that takes:
    a as ModularElement,
    b as ModularElement
returns ModularElement:
    Note: Multiply two elements in modular ring

Process called "power" that takes:
    element as ModularElement,
    exponent as Integer
returns ModularElement:
    Note: Compute element raised to power using fast exponentiation

Process called "multiplicative_inverse" that takes element as ModularElement returns ModularElement:
    Note: Compute multiplicative inverse (if it exists)
```

### Finite Fields

#### Prime Fields
```runa
Process called "create_prime_field" that takes prime as Integer returns ModularRing:
    Note: Create finite field F_p where p is prime

Process called "is_prime_field" that takes ring as ModularRing returns Boolean:
    Note: Check if modular ring is a prime field

Process called "primitive_root" that takes prime_field as ModularRing returns ModularElement:
    Note: Find primitive root (generator) of multiplicative group
```

#### Extension Fields
```runa
Type called "ExtensionField":
    base_field as ModularRing
    irreducible_polynomial as Polynomial
    degree as Integer
    elements as Set[PolynomialElement]

Process called "create_extension_field" that takes:
    base_field as ModularRing,
    irreducible_polynomial as Polynomial
returns ExtensionField:
    Note: Create extension field F_p^n

Process called "find_irreducible_polynomial" that takes:
    base_field as ModularRing,
    degree as Integer
returns Polynomial:
    Note: Find irreducible polynomial of given degree

Process called "primitive_element" that takes field as ExtensionField returns PolynomialElement:
    Note: Find primitive element (generator) of multiplicative group
```

### Chinese Remainder Theorem

#### System Solving
```runa
Process called "chinese_remainder_theorem" that takes:
    moduli as List[Integer],
    residues as List[Integer]
returns ModularElement:
    Note: Solve system of congruences using CRT

Process called "crt_reconstruction" that takes:
    partial_results as List[ModularElement],
    moduli as List[Integer]
returns Integer:
    Note: Reconstruct integer from modular representations

Process called "crt_interpolation" that takes:
    evaluation_points as List[ModularElement],
    function_values as List[ModularElement]
returns Polynomial:
    Note: Interpolate polynomial using CRT
```

### Quadratic Residues

#### Residue Testing
```runa
Process called "is_quadratic_residue" that takes:
    a as Integer,
    p as Integer
returns Boolean:
    Note: Test if a is quadratic residue modulo prime p

Process called "legendre_symbol" that takes:
    a as Integer,
    p as Integer
returns Integer:
    Note: Compute Legendre symbol (a/p)

Process called "jacobi_symbol" that takes:
    a as Integer,
    n as Integer
returns Integer:
    Note: Compute Jacobi symbol (a/n) for composite n

Process called "kronecker_symbol" that takes:
    a as Integer,
    n as Integer
returns Integer:
    Note: Compute Kronecker symbol (generalization of Jacobi)
```

#### Square Root Computation
```runa
Process called "tonelli_shanks_algorithm" that takes:
    a as Integer,
    p as Integer
returns List[Integer]:
    Note: Compute square roots modulo prime using Tonelli-Shanks

Process called "cipolla_algorithm" that takes:
    a as Integer,
    p as Integer
returns List[Integer]:
    Note: Compute square roots modulo prime using Cipolla's method

Process called "sqrt_mod_prime_power" that takes:
    a as Integer,
    p as Integer,
    k as Integer
returns List[Integer]:
    Note: Compute square roots modulo prime power p^k
```

### Elliptic Curves

#### Curve Definition
```runa
Type called "EllipticCurve":
    a as ModularElement
    b as ModularElement
    field as ModularRing
    discriminant as ModularElement
    j_invariant as ModularElement
    is_singular as Boolean

Type called "EllipticCurvePoint":
    x as ModularElement
    y as ModularElement
    curve as EllipticCurve
    is_point_at_infinity as Boolean

Process called "create_elliptic_curve" that takes:
    a as Integer,
    b as Integer,
    field as ModularRing
returns EllipticCurve:
    Note: Create elliptic curve y² = x³ + ax + b over finite field

Process called "is_on_curve" that takes:
    point as EllipticCurvePoint,
    curve as EllipticCurve
returns Boolean:
    Note: Check if point lies on elliptic curve
```

#### Point Operations
```runa
Process called "point_addition" that takes:
    P as EllipticCurvePoint,
    Q as EllipticCurvePoint
returns EllipticCurvePoint:
    Note: Add two points on elliptic curve

Process called "point_doubling" that takes point as EllipticCurvePoint returns EllipticCurvePoint:
    Note: Double a point on elliptic curve (efficient special case)

Process called "scalar_multiplication" that takes:
    k as Integer,
    point as EllipticCurvePoint
returns EllipticCurvePoint:
    Note: Compute k*P using efficient scalar multiplication

Process called "point_order" that takes point as EllipticCurvePoint returns Integer:
    Note: Compute order of point in elliptic curve group
```

#### Curve Properties
```runa
Process called "count_points" that takes curve as EllipticCurve returns Integer:
    Note: Count points on elliptic curve using Schoof's algorithm

Process called "compute_frobenius_trace" that takes curve as EllipticCurve returns Integer:
    Note: Compute trace of Frobenius endomorphism

Process called "is_supersingular" that takes curve as EllipticCurve returns Boolean:
    Note: Check if elliptic curve is supersingular

Process called "j_invariant" that takes curve as EllipticCurve returns ModularElement:
    Note: Compute j-invariant of elliptic curve
```

## Practical Examples

### Basic Modular Arithmetic
```runa
Import "math/algebra/modular" as Modular

Note: Solve linear congruence ax ≡ b (mod m)
Process called "solve_linear_congruence" that takes:
    a as Integer,
    b as Integer,
    m as Integer
returns List[Integer]:
    Let gcd_result be Modular.extended_gcd(a, m)
    Let g be gcd_result.gcd
    
    If b % g != 0:
        Return []  Note: No solution exists
    
    Let x0 be (gcd_result.x * (b / g)) % m
    Let solutions be []
    Let step be m / g
    
    For i from 0 to g - 1:
        solutions.append((x0 + i * step) % m)
    
    Return solutions

Let solutions be solve_linear_congruence(7, 3, 15)
Display "Solutions to 7x ≡ 3 (mod 15): " joined with solutions
```

### Chinese Remainder Theorem Application
```runa
Note: Solve system of congruences
Note: x ≡ 2 (mod 3), x ≡ 3 (mod 5), x ≡ 2 (mod 7)

Let moduli be [3, 5, 7]
Let residues be [2, 3, 2]

Let solution be Modular.chinese_remainder_theorem(moduli, residues)
Display "Solution: x ≡ " joined with solution.value joined with " (mod " joined with (3 * 5 * 7) joined with ")"

Note: Verify solution
For i from 0 to moduli.length() - 1:
    Let remainder be solution.value % moduli[i]
    Let expected be residues[i]
    Display "x ≡ " joined with remainder joined with " (mod " joined with moduli[i] joined with "), expected " joined with expected
```

### Quadratic Residue Analysis
```runa
Note: Analyze quadratic residues modulo prime
Let prime be 17
Let quadratic_residues be []
Let non_residues be []

For a from 1 to prime - 1:
    If Modular.is_quadratic_residue(a, prime):
        quadratic_residues.append(a)
    Otherwise:
        non_residues.append(a)

Display "Quadratic residues mod " joined with prime joined with ": " joined with quadratic_residues
Display "Non-residues mod " joined with prime joined with ": " joined with non_residues

Note: Verify using Legendre symbol
For Each a in quadratic_residues:
    Let legendre be Modular.legendre_symbol(a, prime)
    Display "(" joined with a joined with "/" joined with prime joined with ") = " joined with legendre

Note: Find square roots
Let a be 4
Let sqrt_results be Modular.tonelli_shanks_algorithm(a, prime)
Display "Square roots of " joined with a joined with " mod " joined with prime joined with ": " joined with sqrt_results
```

### Finite Field Arithmetic
```runa
Note: Work with extension field F_8 = F_2^3
Let base_field be Modular.create_prime_field(2)
Let irreducible_poly be base_field.create_polynomial("x^3 + x + 1")
Let F8 be Modular.create_extension_field(base_field, irreducible_poly)

Note: Find primitive element
Let primitive be Modular.primitive_element(F8)
Display "Primitive element found: " joined with primitive

Note: Generate all field elements using primitive element
Let elements be []
Let current be F8.one()
For i from 0 to 6:  Note: F_8* has order 7
    elements.append(current)
    current be Modular.multiply(current, primitive)

Display "All elements of F_8*:"
For Each element in elements:
    Display "  " joined with element
```

### Elliptic Curve Cryptography
```runa
Note: Set up elliptic curve for cryptography
Let prime be 97  Note: Small prime for demonstration
Let field be Modular.create_prime_field(prime)
Let curve be Modular.create_elliptic_curve(a: 2, b: 3, field: field)

Note: Find a base point
Let base_point be null
For x from 1 to prime - 1:
    For y from 1 to prime - 1:
        Let test_point be EllipticCurvePoint:
            x: field.create_element(x)
            y: field.create_element(y)
            curve: curve
            is_point_at_infinity: False
        
        If Modular.is_on_curve(test_point, curve):
            base_point be test_point
            Break
    If base_point != null:
        Break

Display "Base point found: (" joined with base_point.x.value joined with ", " joined with base_point.y.value joined with ")"

Note: Compute point order
Let point_order be Modular.point_order(base_point)
Display "Point order: " joined with point_order

Note: Perform scalar multiplication
Let private_key be 23
Let public_key be Modular.scalar_multiplication(private_key, base_point)
Display "Public key: (" joined with public_key.x.value joined with ", " joined with public_key.y.value joined with ")"
```

### Cryptographic Applications
```runa
Note: Implement basic ElGamal encryption over elliptic curve
Process called "elgamal_encrypt" that takes:
    message_point as EllipticCurvePoint,
    public_key as EllipticCurvePoint,
    base_point as EllipticCurvePoint,
    random_k as Integer
returns Dictionary[String, EllipticCurvePoint]:
    Let c1 be Modular.scalar_multiplication(random_k, base_point)
    Let shared_secret be Modular.scalar_multiplication(random_k, public_key)
    Let c2 be Modular.point_addition(message_point, shared_secret)
    
    Return Dictionary[String, EllipticCurvePoint]:
        "c1": c1
        "c2": c2

Process called "elgamal_decrypt" that takes:
    ciphertext as Dictionary[String, EllipticCurvePoint],
    private_key as Integer
returns EllipticCurvePoint:
    Let c1 be ciphertext["c1"]
    Let c2 be ciphertext["c2"]
    
    Let shared_secret be Modular.scalar_multiplication(private_key, c1)
    Let negative_shared be Modular.point_negate(shared_secret)
    
    Return Modular.point_addition(c2, negative_shared)

Note: Encrypt and decrypt a message
Let message_point be base_point  Note: Use base point as message
Let random_k be 17
Let ciphertext be elgamal_encrypt(message_point, public_key, base_point, random_k)
Let decrypted be elgamal_decrypt(ciphertext, private_key)

Display "Message encrypted and decrypted successfully: " joined with 
    (decrypted.x.value == message_point.x.value and decrypted.y.value == message_point.y.value)
```

## Advanced Features

### Discrete Logarithm Problem

#### Baby-Step Giant-Step
```runa
Process called "baby_step_giant_step" that takes:
    base as ModularElement,
    target as ModularElement,
    order_bound as Integer
returns Integer:
    Note: Solve discrete logarithm using baby-step giant-step algorithm
    
Let generator be Modular.primitive_root(field)
Let target be field.create_element(42)
Let discrete_log be baby_step_giant_step(generator, target, field.order() - 1)
Display "Discrete log of " joined with target.value joined with " is " joined with discrete_log
```

#### Pollard's Rho Algorithm
```runa
Process called "pollard_rho_discrete_log" that takes:
    base as ModularElement,
    target as ModularElement
returns Integer:
    Note: Solve discrete logarithm using Pollard's rho method
    
Let rho_result be pollard_rho_discrete_log(generator, target)
Display "Discrete log found using Pollard's rho: " joined with rho_result
```

### Isogeny-Based Cryptography
```runa
Type called "EllipticCurveIsogeny":
    domain as EllipticCurve
    codomain as EllipticCurve
    degree as Integer
    kernel_points as List[EllipticCurvePoint]

Process called "compute_isogeny" that takes:
    curve as EllipticCurve,
    kernel_points as List[EllipticCurvePoint]
returns EllipticCurveIsogeny:
    Note: Compute isogeny with given kernel

Process called "evaluate_isogeny" that takes:
    isogeny as EllipticCurveIsogeny,
    point as EllipticCurvePoint
returns EllipticCurvePoint:
    Note: Evaluate isogeny at given point
```

### Pairing-Based Cryptography
```runa
Process called "weil_pairing" that takes:
    P as EllipticCurvePoint,
    Q as EllipticCurvePoint,
    order as Integer
returns ModularElement:
    Note: Compute Weil pairing for points of given order

Process called "tate_pairing" that takes:
    P as EllipticCurvePoint,
    Q as EllipticCurvePoint,
    order as Integer
returns ModularElement:
    Note: Compute Tate pairing for points of given order
```

## Integration with Other Modules

### With Number Theory
```runa
Import "math/discrete/number_theory" as NumberTheory
Import "math/algebra/modular" as Modular

Note: Study structure of multiplicative group
Let n be 35
Let phi_n be NumberTheory.euler_totient(n)
Let units_mod_n be Modular.units(Modular.create_modular_ring(n))

Display "φ(" joined with n joined with ") = " joined with phi_n
Display "Number of units mod " joined with n joined with ": " joined with units_mod_n.size()

Note: Find primitive roots when they exist
Let prime be 13
Let prime_field be Modular.create_prime_field(prime)
Let primitive_roots be []

For a from 2 to prime - 1:
    Let element be prime_field.create_element(a)
    If Modular.multiplicative_order(element) == prime - 1:
        primitive_roots.append(a)

Display "Primitive roots mod " joined with prime joined with ": " joined with primitive_roots
```

### With Abstract Algebra
```runa
Import "math/algebra/abstract" as Abstract
Import "math/algebra/modular" as Modular

Note: Study modular ring as abstract ring
Let modular_ring be Modular.create_modular_ring(12)
Let abstract_ring be Abstract.create_ring_from_modular_ring(modular_ring)

Let is_integral_domain be Abstract.is_integral_domain(abstract_ring)
Let zero_divisors be Abstract.find_zero_divisors(abstract_ring)

Display "Z/12Z is integral domain: " joined with is_integral_domain
Display "Zero divisors in Z/12Z: " joined with zero_divisors
```

### With Polynomial Algebra
```runa
Import "math/algebra/polynomial" as Poly
Import "math/algebra/modular" as Modular

Note: Factor polynomials over finite fields
Let prime_field be Modular.create_prime_field(5)
Let poly_ring be Poly.create_polynomial_ring(["x"], prime_field)
Let polynomial be poly_ring.create_polynomial("x^4 + x + 1")

Let factors be Poly.factor_over_finite_field(polynomial, prime_field)
Display "Factorization over F_5:"
For Each factor in factors:
    Display "  " joined with Poly.to_string(factor)
```

## Coding Theory Applications

### Reed-Solomon Codes
```runa
Note: Implement Reed-Solomon encoding
Process called "reed_solomon_encode" that takes:
    message as List[Integer],
    field as ModularRing,
    num_parity as Integer
returns List[ModularElement]:
    Let generator_polynomial be Modular.rs_generator_polynomial(field, num_parity)
    Let message_poly be Poly.create_polynomial_from_coefficients(message, field)
    Let codeword_poly be Poly.polynomial_multiplication(message_poly, generator_polynomial)
    
    Return Poly.coefficients(codeword_poly)

Let F256 be Modular.create_extension_field(
    Modular.create_prime_field(2),
    irreducible_polynomial: "x^8 + x^4 + x^3 + x^2 + 1"
)

Let message be [1, 2, 3, 4]
Let encoded be reed_solomon_encode(message, F256, num_parity: 4)
Display "RS encoded message length: " joined with encoded.length()
```

### BCH Codes
```runa
Note: Generate BCH code
Process called "bch_generator_polynomial" that takes:
    field as ExtensionField,
    designed_distance as Integer
returns Polynomial:
    Note: Generate BCH generator polynomial for given distance
    
Let F16 be Modular.create_extension_field(
    Modular.create_prime_field(2),
    irreducible_polynomial: "x^4 + x + 1"
)

Let bch_generator be bch_generator_polynomial(F16, designed_distance: 5)
Display "BCH generator polynomial degree: " joined with bch_generator.degree
```

## Best Practices

### Efficient Modular Arithmetic
```runa
Note: Use Montgomery reduction for repeated operations
Process called "montgomery_setup" that takes modulus as Integer returns MontgomeryContext:
    Note: Set up Montgomery context for efficient modular arithmetic

Process called "montgomery_multiply" that takes:
    a as Integer,
    b as Integer,
    context as MontgomeryContext
returns Integer:
    Note: Multiply using Montgomery reduction
```

### Constant-Time Implementations
```runa
Note: Implement constant-time scalar multiplication for side-channel resistance
Process called "constant_time_scalar_mult" that takes:
    k as Integer,
    point as EllipticCurvePoint
returns EllipticCurvePoint:
    Note: Scalar multiplication resistant to timing attacks
```

### Parameter Validation
```runa
Note: Validate cryptographic parameters
Process called "validate_ec_parameters" that takes curve as EllipticCurve returns Boolean:
    Let discriminant be Modular.compute_discriminant(curve)
    If Modular.is_zero(discriminant):
        Return False  Note: Singular curve
    
    Let point_count be Modular.count_points(curve)
    Let is_secure be not Modular.is_anomalous_curve(curve)
    
    Return is_secure

Process called "validate_prime" that takes p as Integer returns Boolean:
    Return NumberTheory.is_prime(p) and p >= 2^160  Note: Minimum security level
```

This module provides comprehensive modular arithmetic functionality essential for cryptography, coding theory, and computational number theory, with both theoretical foundations and practical implementations optimized for security and efficiency.