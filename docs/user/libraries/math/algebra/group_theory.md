# Group Theory Module

The `math/algebra/group_theory` module provides comprehensive group theory functionality including finite groups, Lie groups, representation theory, and advanced group-theoretic computations. This module is essential for symmetry analysis, physics applications, and abstract mathematical research.

## Quick Start

```runa
Import "math/algebra/group_theory" as Groups

Note: Create and analyze finite groups
Let cyclic_group be Groups.create_cyclic_group(order: 8)
Let dihedral_group be Groups.create_dihedral_group(sides: 4)
Let symmetric_group be Groups.create_symmetric_group(degree: 4)

Display "C8 is abelian: " joined with Groups.is_abelian(cyclic_group)
Display "D4 order: " joined with dihedral_group.order
Display "S4 has subgroup of order 12: " joined with Groups.has_subgroup_of_order(symmetric_group, 12)

Note: Compute group properties
Let sylow_subgroups be Groups.compute_sylow_subgroups(symmetric_group, prime: 2)
Display "Number of Sylow 2-subgroups in S4: " joined with sylow_subgroups.length()
```

## Core Concepts

### Group Classifications
Groups are classified by their structure, size, and properties:

- **Finite Groups**: Groups with finitely many elements
- **Infinite Groups**: Groups with infinitely many elements  
- **Abelian Groups**: Commutative groups
- **Simple Groups**: Groups with no proper normal subgroups
- **Lie Groups**: Groups that are smooth manifolds

### Group Actions
Ways groups can act on sets, providing connections between abstract groups and geometric/combinatorial structures.

### Representation Theory
Study of how groups can be realized as linear transformations of vector spaces.

## API Reference

### Basic Group Construction

#### Standard Groups
```runa
Type called "Group":
    elements as Set[Any]
    operation as Process that takes Any, Any returns Any
    identity as Any
    inverse as Process that takes Any returns Any
    order as Integer
    is_finite as Boolean
    is_abelian as Boolean

Process called "create_cyclic_group" that takes order as Integer returns Group:
    Note: Create cyclic group Z/nZ or Z

Process called "create_dihedral_group" that takes sides as Integer returns Group:
    Note: Create dihedral group D_n (symmetries of regular n-gon)

Process called "create_symmetric_group" that takes degree as Integer returns Group:
    Note: Create symmetric group S_n (permutations of n elements)

Process called "create_alternating_group" that takes degree as Integer returns Group:
    Note: Create alternating group A_n (even permutations)
```

#### Matrix Groups
```runa
Process called "create_general_linear_group" that takes:
    dimension as Integer,
    field as Field
returns Group:
    Note: Create GL(n, F) - invertible n×n matrices

Process called "create_special_linear_group" that takes:
    dimension as Integer,
    field as Field
returns Group:
    Note: Create SL(n, F) - matrices with determinant 1

Process called "create_orthogonal_group" that takes:
    dimension as Integer,
    field as Field
returns Group:
    Note: Create O(n, F) - orthogonal matrices

Process called "create_unitary_group" that takes dimension as Integer returns Group:
    Note: Create U(n) - unitary matrices
```

### Group Operations

#### Basic Operations
```runa
Process called "group_multiply" that takes:
    group as Group,
    element1 as Any,
    element2 as Any
returns Any:
    Note: Multiply two group elements

Process called "group_inverse" that takes:
    group as Group,
    element as Any
returns Any:
    Note: Compute inverse of group element

Process called "group_power" that takes:
    group as Group,
    element as Any,
    exponent as Integer
returns Any:
    Note: Compute element raised to power

Process called "element_order" that takes:
    group as Group,
    element as Any
returns Integer:
    Note: Compute order of group element
```

#### Group Properties
```runa
Process called "is_abelian" that takes group as Group returns Boolean:
    Note: Check if group is commutative

Process called "is_cyclic" that takes group as Group returns Boolean:
    Note: Check if group is cyclic

Process called "is_simple" that takes group as Group returns Boolean:
    Note: Check if group is simple (no proper normal subgroups)

Process called "compute_center" that takes group as Group returns Group:
    Note: Compute center Z(G) = {g ∈ G : gx = xg for all x ∈ G}

Process called "compute_commutator_subgroup" that takes group as Group returns Group:
    Note: Compute derived subgroup [G,G]
```

### Subgroups and Quotients

#### Subgroup Operations
```runa
Process called "generate_subgroup" that takes:
    group as Group,
    generators as List[Any]
returns Group:
    Note: Generate subgroup from given elements

Process called "find_all_subgroups" that takes group as Group returns List[Group]:
    Note: Find all subgroups of finite group

Process called "is_subgroup" that takes:
    subgroup as Group,
    parent_group as Group
returns Boolean:
    Note: Check if one group is subgroup of another

Process called "subgroup_index" that takes:
    subgroup as Group,
    parent_group as Group
returns Integer:
    Note: Compute index [G:H] = |G|/|H|
```

#### Normal Subgroups and Quotients
```runa
Process called "is_normal_subgroup" that takes:
    subgroup as Group,
    parent_group as Group
returns Boolean:
    Note: Check if subgroup is normal

Process called "compute_quotient_group" that takes:
    group as Group,
    normal_subgroup as Group
returns Group:
    Note: Compute quotient group G/N

Process called "find_normal_subgroups" that takes group as Group returns List[Group]:
    Note: Find all normal subgroups

Process called "compute_cosets" that takes:
    subgroup as Group,
    parent_group as Group,
    side as String
returns List[Set[Any]]:
    Note: Compute left or right cosets
```

### Sylow Theory

#### Sylow Subgroups
```runa
Process called "compute_sylow_subgroups" that takes:
    group as Group,
    prime as Integer
returns List[Group]:
    Note: Compute all Sylow p-subgroups

Process called "sylow_number" that takes:
    group as Group,
    prime as Integer
returns Integer:
    Note: Count number of Sylow p-subgroups

Process called "is_p_group" that takes:
    group as Group,
    prime as Integer
returns Boolean:
    Note: Check if group order is power of prime
```

#### p-Group Analysis
```runa
Process called "compute_p_rank" that takes:
    group as Group,
    prime as Integer
returns Integer:
    Note: Compute p-rank of abelian group

Process called "find_maximal_p_subgroups" that takes:
    group as Group,
    prime as Integer
returns List[Group]:
    Note: Find maximal p-subgroups
```

### Group Homomorphisms

#### Morphism Construction
```runa
Type called "GroupHomomorphism":
    domain as Group
    codomain as Group
    mapping as Process that takes Any returns Any
    kernel as Group
    image as Group
    is_isomorphism as Boolean

Process called "create_homomorphism" that takes:
    domain as Group,
    codomain as Group,
    mapping as Process
returns GroupHomomorphism:
    Note: Create group homomorphism with automatic kernel/image computation

Process called "composition" that takes:
    f as GroupHomomorphism,
    g as GroupHomomorphism
returns GroupHomomorphism:
    Note: Compose two homomorphisms
```

#### Isomorphism Testing
```runa
Process called "are_isomorphic" that takes:
    group1 as Group,
    group2 as Group
returns Boolean:
    Note: Check if two groups are isomorphic

Process called "find_isomorphism" that takes:
    group1 as Group,
    group2 as Group
returns GroupHomomorphism:
    Note: Find isomorphism between groups (if it exists)

Process called "compute_automorphism_group" that takes group as Group returns Group:
    Note: Compute group of automorphisms Aut(G)
```

## Practical Examples

### Finite Group Analysis
```runa
Import "math/algebra/group_theory" as Groups

Note: Analyze structure of S4 (symmetric group on 4 elements)
Let S4 be Groups.create_symmetric_group(4)
Display "S4 order: " joined with S4.order
Display "S4 is abelian: " joined with Groups.is_abelian(S4)

Note: Find normal subgroups
Let normal_subgroups be Groups.find_normal_subgroups(S4)
Display "Number of normal subgroups: " joined with normal_subgroups.length()

For Each N in normal_subgroups:
    Let quotient be Groups.compute_quotient_group(S4, N)
    Display "Quotient S4/N has order: " joined with quotient.order

Note: Analyze Sylow subgroups
Let sylow_2_subgroups be Groups.compute_sylow_subgroups(S4, prime: 2)
Let sylow_3_subgroups be Groups.compute_sylow_subgroups(S4, prime: 3)

Display "Number of Sylow 2-subgroups: " joined with sylow_2_subgroups.length()
Display "Number of Sylow 3-subgroups: " joined with sylow_3_subgroups.length()
```

### Group Actions and Orbits
```runa
Note: Study group action of S3 on set {1,2,3}
Let S3 be Groups.create_symmetric_group(3)
Let action_set be Set[Integer]: [1, 2, 3]

Type called "GroupAction":
    group as Group
    set as Set[Any]
    action as Process that takes Any, Any returns Any

Process called "create_natural_action" that takes:
    group as Group,
    set as Set[Any]
returns GroupAction:
    Note: Create natural action of symmetric group

Let natural_action be create_natural_action(S3, action_set)

Note: Compute orbits and stabilizers
Process called "compute_orbit" that takes:
    action as GroupAction,
    element as Any
returns Set[Any]:
    Note: Compute orbit of element under group action

Process called "compute_stabilizer" that takes:
    action as GroupAction,
    element as Any
returns Group:
    Note: Compute stabilizer subgroup

Let orbit_1 be compute_orbit(natural_action, 1)
Let stabilizer_1 be compute_stabilizer(natural_action, 1)

Display "Orbit of 1: " joined with orbit_1
Display "Stabilizer of 1 has order: " joined with stabilizer_1.order

Note: Verify orbit-stabilizer theorem: |Orbit| × |Stabilizer| = |Group|
Let product be orbit_1.size() * stabilizer_1.order
Display "Orbit-Stabilizer theorem verified: " joined with (product == S3.order)
```

### Classification of Small Groups
```runa
Note: Classify all groups of order 12
Process called "classify_groups_of_order" that takes n as Integer returns List[Group]:
    Let groups be []
    
    Note: Direct approach for small orders
    If n == 12:
        groups.append(Groups.create_cyclic_group(12))
        groups.append(Groups.create_dihedral_group(6))
        
        Note: A4 (alternating group) has order 12
        groups.append(Groups.create_alternating_group(4))
        
        Note: Z/2Z × Z/6Z
        Let Z2 be Groups.create_cyclic_group(2)
        Let Z6 be Groups.create_cyclic_group(6)
        groups.append(Groups.direct_product(Z2, Z6))
        
        Note: Z/3Z ⋊ Z/4Z (semidirect product)
        Let Z3 be Groups.create_cyclic_group(3)
        Let Z4 be Groups.create_cyclic_group(4)
        groups.append(Groups.semidirect_product(Z3, Z4))
    
    Return groups

Let groups_order_12 be classify_groups_of_order(12)
Display "Number of groups of order 12: " joined with groups_order_12.length()

For i from 0 to groups_order_12.length() - 1:
    Let G be groups_order_12[i]
    Display "Group " joined with (i + 1) joined with ": " joined with Groups.describe_structure(G)
```

### Representation Theory
```runa
Note: Compute irreducible representations of D4
Let D4 be Groups.create_dihedral_group(4)
Let complex_field be Abstract.create_complex_field()

Type called "Representation":
    group as Group
    vector_space as VectorSpace
    representation_map as Dictionary[Any, Matrix]
    dimension as Integer
    is_irreducible as Boolean

Process called "compute_irreducible_representations" that takes:
    group as Group,
    field as Field
returns List[Representation]:
    Note: Compute all irreducible representations over given field

Let irreducible_reps be compute_irreducible_representations(D4, complex_field)
Display "D4 has " joined with irreducible_reps.length() joined with " irreducible representations"

For Each rep in irreducible_reps:
    Display "Representation of dimension " joined with rep.dimension

Note: Compute character table
Process called "compute_character_table" that takes group as Group returns Matrix:
    Note: Compute character table for finite group

Let character_table be compute_character_table(D4)
Display "Character table for D4:"
Groups.display_character_table(character_table)
```

### Galois Theory Connection
```runa
Import "math/algebra/abstract" as Abstract
Import "math/algebra/polynomial" as Poly

Note: Compute Galois group of polynomial
Let rational_field be Abstract.create_rational_field()
Let polynomial_ring be Poly.create_polynomial_ring(["x"], rational_field)
Let polynomial be polynomial_ring.create_polynomial("x^4 - 2")

Process called "compute_galois_group" that takes:
    polynomial as Polynomial,
    base_field as Field
returns Group:
    Note: Compute Galois group of polynomial's splitting field

Let galois_group be compute_galois_group(polynomial, rational_field)
Display "Galois group of x^4 - 2 over Q:"
Display "  Order: " joined with galois_group.order
Display "  Structure: " joined with Groups.describe_structure(galois_group)

Note: Analyze subfield correspondence
Let splitting_field be Poly.compute_splitting_field(polynomial, rational_field)
Let subgroups be Groups.find_all_subgroups(galois_group)

Display "Galois correspondence:"
For Each H in subgroups:
    Let fixed_field be compute_fixed_field(splitting_field, H)
    Display "  Subgroup of order " joined with H.order joined with " fixes field of degree " joined with fixed_field.degree
```

## Advanced Features

### Lie Groups and Lie Algebras

#### Lie Group Construction
```runa
Type called "LieGroup":
    manifold as Manifold
    group_structure as Group
    dimension as Integer
    is_compact as Boolean
    is_connected as Boolean

Process called "create_matrix_lie_group" that takes:
    defining_equations as List[Polynomial],
    dimension as Integer
returns LieGroup:
    Note: Create Lie group as solution set of polynomial equations

Process called "create_special_orthogonal_group" that takes dimension as Integer returns LieGroup:
    Note: Create SO(n) - special orthogonal group

Process called "create_special_unitary_group" that takes dimension as Integer returns LieGroup:
    Note: Create SU(n) - special unitary group
```

#### Lie Algebra Operations
```runa
Type called "LieAlgebra":
    vector_space as VectorSpace
    lie_bracket as Process that takes Vector, Vector returns Vector
    dimension as Integer

Process called "compute_lie_algebra" that takes lie_group as LieGroup returns LieAlgebra:
    Note: Compute Lie algebra of Lie group

Process called "exponential_map" that takes:
    lie_algebra_element as Vector,
    lie_group as LieGroup
returns Any:
    Note: Compute exponential map from Lie algebra to Lie group

Process called "compute_root_system" that takes lie_algebra as LieAlgebra returns RootSystem:
    Note: Compute root system for semisimple Lie algebra
```

### Computational Group Theory

#### Algorithms for Large Groups
```runa
Process called "schreier_sims_algorithm" that takes group as Group returns StabiliserChain:
    Note: Compute stabilizer chain for permutation group

Process called "todd_coxeter_enumeration" that takes:
    presentation as GroupPresentation,
    subgroup_generators as List[Any]
returns Integer:
    Note: Enumerate cosets using Todd-Coxeter algorithm

Process called "knuth_bendix_completion" that takes presentation as GroupPresentation returns RewritingSystem:
    Note: Complete rewriting system for group presentation
```

#### Group Extensions
```runa
Process called "compute_group_extensions" that takes:
    normal_subgroup as Group,
    quotient_group as Group
returns List[Group]:
    Note: Classify extensions of N by Q

Process called "compute_cohomology_groups" that takes:
    group as Group,
    module as Module,
    degree as Integer
returns Module:
    Note: Compute group cohomology H^n(G,M)
```

## Integration with Other Modules

### With Linear Algebra
```runa
Import "math/algebra/linear" as Linear
Import "math/algebra/group_theory" as Groups

Note: Represent finite group as permutation matrices
Let S3 be Groups.create_symmetric_group(3)
Let permutation_representation be Dictionary[Any, Matrix]: {}

For Each element in S3.elements:
    Let permutation_matrix be Linear.create_permutation_matrix(element)
    permutation_representation[element] be permutation_matrix

Note: Verify representation property
Let g1 be S3.elements[1]
Let g2 be S3.elements[2]
Let product be Groups.group_multiply(S3, g1, g2)

Let matrix_product be Linear.matrix_multiplication(
    permutation_representation[g1],
    permutation_representation[g2]
)

Let representation_preserves be Linear.matrix_equals(
    matrix_product,
    permutation_representation[product]
)

Display "Permutation representation is valid: " joined with representation_preserves
```

### With Number Theory
```runa
Import "math/discrete/number_theory" as NumberTheory
Import "math/algebra/group_theory" as Groups

Note: Study multiplicative group of integers modulo n
Process called "create_multiplicative_group_mod_n" that takes n as Integer returns Group:
    Let units be NumberTheory.units_modulo_n(n)
    Let multiplication be Process that takes a as Integer, b as Integer returns Integer:
        Return (a * b) % n
    
    Return Groups.create_group(
        elements: units,
        operation: multiplication,
        identity: 1
    )

Let Z15_star be create_multiplicative_group_mod_n(15)
Display "(Z/15Z)* order: " joined with Z15_star.order
Display "φ(15) = " joined with NumberTheory.euler_totient(15)

Let is_cyclic be Groups.is_cyclic(Z15_star)
Display "(Z/15Z)* is cyclic: " joined with is_cyclic
```

### With Algebraic Geometry
```runa
Import "math/algebra/polynomial" as Poly
Import "math/algebra/group_theory" as Groups

Note: Study automorphism group of algebraic variety
Let polynomial_ring be Poly.create_polynomial_ring(["x", "y"], "complex")
Let defining_polynomial be polynomial_ring.create_polynomial("x^3 + y^3 - 1")
Let variety_ideal be Poly.create_ideal([defining_polynomial], polynomial_ring)

Process called "compute_variety_automorphisms" that takes ideal as PolynomialIdeal returns Group:
    Note: Compute automorphism group of algebraic variety
    
Let automorphism_group be compute_variety_automorphisms(variety_ideal)
Display "Automorphism group of curve x^3 + y^3 = 1:"
Display "  Order: " joined with automorphism_group.order
Display "  Structure: " joined with Groups.describe_structure(automorphism_group)
```

## Applications in Physics

### Crystallographic Groups
```runa
Note: Create space group for crystal structure
Type called "SpaceGroup":
    point_group as Group
    translations as List[Vector]
    dimension as Integer

Process called "create_space_group" that takes:
    point_operations as List[Matrix],
    translations as List[Vector]
returns SpaceGroup:
    Note: Create crystallographic space group

Let cubic_point_group be Groups.create_cubic_point_group()
Let translation_vectors be [
    Linear.create_vector([0.5, 0, 0]),
    Linear.create_vector([0, 0.5, 0]),
    Linear.create_vector([0, 0, 0.5])
]

Let space_group be create_space_group(
    cubic_point_group.elements,
    translation_vectors
)

Display "Space group created with " joined with space_group.point_group.order joined with " point operations"
```

### Particle Physics Symmetries
```runa
Note: SU(3) symmetry for quark flavor
Let SU3 be Groups.create_special_unitary_group(3)
Let fundamental_rep be Groups.compute_fundamental_representation(SU3)
Let adjoint_rep be Groups.compute_adjoint_representation(SU3)

Display "SU(3) fundamental representation dimension: " joined with fundamental_rep.dimension
Display "SU(3) adjoint representation dimension: " joined with adjoint_rep.dimension

Note: Decompose tensor products
Let tensor_product be Groups.tensor_product_representation(
    fundamental_rep,
    fundamental_rep
)
Let decomposition be Groups.decompose_representation(tensor_product)

Display "3 ⊗ 3 decomposition:"
For Each irrep in decomposition:
    Display "  " joined with irrep.dimension joined with "-dimensional representation"
```

## Best Practices

### Efficient Computation
```runa
Note: Choose appropriate representation for group
Process called "optimize_group_representation" that takes group as Group returns Group:
    If Groups.is_cyclic(group):
        Return Groups.convert_to_cyclic_representation(group)
    Otherwise If Groups.is_abelian(group):
        Return Groups.convert_to_abelian_representation(group)
    Otherwise If group.order <= 1000:
        Return Groups.convert_to_multiplication_table(group)
    Otherwise:
        Return Groups.convert_to_generator_representation(group)
```

### Memory Management
```runa
Note: Handle large groups efficiently
Process called "lazy_subgroup_computation" that takes group as Group returns Iterator[Group]:
    Note: Generate subgroups on-demand rather than computing all at once
    
Process called "streaming_coset_enumeration" that takes:
    group as Group,
    subgroup as Group
returns Iterator[Set[Any]]:
    Note: Enumerate cosets without storing all in memory
```

### Verification and Testing
```runa
Note: Verify group axioms for constructed groups
Process called "verify_group_structure" that takes group as Group returns Boolean:
    Let associativity be Groups.check_associativity(group)
    Let identity_property be Groups.check_identity_property(group)
    Let inverse_property be Groups.check_inverse_property(group)
    
    Return associativity and identity_property and inverse_property
```

This module provides comprehensive group theory functionality for both finite and infinite groups, supporting applications from pure mathematics to physics and computer science, making it an essential tool for symmetry analysis and abstract algebraic computation in Runa.