Note: Category Theory Morphisms Module

## Overview

The `math/category/morphisms` module provides comprehensive morphism theory and categorical constructions, including morphism composition, universal properties, limits and colimits, pullbacks and pushouts, equalizers and coequalizers. This module forms the foundation for categorical reasoning and diagram-based mathematics in Runa.

## Key Features

- **Morphism Types**: Complete taxonomy of morphisms (iso-, epi-, mono-, endo-, auto-)
- **Universal Constructions**: Limits, colimits, pullbacks, pushouts, equalizers
- **Composition Operations**: Morphism composition with associativity verification
- **Diagram Chasing**: Tools for categorical proof techniques
- **Categorical Properties**: Preservation of structure and universal properties

## Data Types

### Morphism
Represents a morphism (arrow) between objects in a category:
```runa
Type called "Morphism":
    morphism_id as String                         Note: Unique identifier
    source_object as String                       Note: Domain object
    target_object as String                       Note: Codomain object
    morphism_type as String                       Note: Type classification
    composition_properties as Dictionary[String, Boolean] Note: Composition data
    invertible as Boolean                         Note: Invertibility property
    identity_morphism as Boolean                  Note: Identity morphism flag
```

### Isomorphism
Represents an invertible morphism:
```runa
Type called "Isomorphism":
    morphism_base as Morphism                     Note: Base morphism structure
    inverse_morphism as Morphism                  Note: Inverse morphism
    isomorphism_verified as Boolean               Note: Verification status
    bidirectional_composition as Dictionary[String, String] Note: Composition data
```

### Epimorphism
Represents a right-cancellative morphism:
```runa
Type called "Epimorphism":
    morphism_base as Morphism                     Note: Base morphism
    right_cancellative as Boolean                 Note: Right cancellation property
    surjective_property as Boolean                Note: Surjectivity (if applicable)
    epic_verification as Dictionary[String, Boolean] Note: Verification data
```

### Monomorphism
Represents a left-cancellative morphism:
```runa
Type called "Monomorphism":
    morphism_base as Morphism                     Note: Base morphism
    left_cancellative as Boolean                  Note: Left cancellation property
    injective_property as Boolean                 Note: Injectivity (if applicable)
    monic_verification as Dictionary[String, Boolean] Note: Verification data
```

### Limit
Represents a categorical limit construction:
```runa
Type called "Limit":
    limit_object as String                        Note: Limit object
    cone_morphisms as Dictionary[String, String]  Note: Cone to diagram
    diagram_category as String                    Note: Diagram being limited
    universal_property as Boolean                 Note: Universal property satisfied
    uniqueness_condition as Boolean               Note: Uniqueness of factorization
```

### Pullback
Represents a categorical pullback (fiber product):
```runa
Type called "Pullback":
    pullback_object as String                     Note: Pullback object
    projection_morphisms as Dictionary[String, String] Note: Projection morphisms
    original_morphisms as Dictionary[String, String] Note: Original span morphisms
    commutativity_condition as Boolean            Note: Square commutativity
    universal_property as Boolean                 Note: Universal property
```

## Basic Morphism Operations

### Creating and Composing Morphisms
```runa
Import "math/category/morphisms" as Morphisms

Note: Create basic morphisms
Let f = Morphism with:
    morphism_id: "f"
    source_object: "A"
    target_object: "B"
    morphism_type: "general"
    composition_properties: Dictionary[String, Boolean]()
    invertible: false
    identity_morphism: false

Let g = Morphism with:
    morphism_id: "g"
    source_object: "B"
    target_object: "C"
    morphism_type: "general"
    composition_properties: Dictionary[String, Boolean]()
    invertible: false
    identity_morphism: false

Note: Compose morphisms g ∘ f
Let composition_result = Morphisms.compose_morphisms(g, f)
Display "Composition g ∘ f: " joined with composition_result.composed_morphism.morphism_id
Display "Source: " joined with composition_result.composed_morphism.source_object
Display "Target: " joined with composition_result.composed_morphism.target_object
Display "Composition valid: " joined with String(composition_result.composition_valid)
```

### Identity Morphisms
```runa
Note: Create identity morphism
Let id_A = Morphisms.create_identity_morphism("A")
Display "Identity morphism: " joined with id_A.morphism_id
Display "Is identity: " joined with String(id_A.identity_morphism)
Display "Source equals target: " joined with String(id_A.source_object == id_A.target_object)

Note: Verify identity laws
Let left_identity = Morphisms.compose_morphisms(f, id_A)
Let right_identity = Morphisms.compose_morphisms(id_A, f)

Display "Left identity: id_A ∘ f = f: " joined with String(left_identity.equals_original)
Display "Right identity: f ∘ id_B = f: " joined with String(right_identity.equals_original)
```

### Morphism Classification
```runa
Note: Analyze morphism properties
Let morphism_analysis = Morphisms.analyze_morphism_properties(f)
Display "Morphism type: " joined with morphism_analysis.morphism_classification
Display "Is monomorphism: " joined with String(morphism_analysis.is_monomorphism)
Display "Is epimorphism: " joined with String(morphism_analysis.is_epimorphism)
Display "Is isomorphism: " joined with String(morphism_analysis.is_isomorphism)

If morphism_analysis.is_isomorphism:
    Let inverse_search = Morphisms.find_inverse_morphism(f)
    Display "Inverse exists: " joined with String(inverse_search.inverse_exists)
    Display "Inverse morphism: " joined with inverse_search.inverse_morphism.morphism_id
```

## Isomorphisms and Invertible Morphisms

### Creating Isomorphisms
```runa
Note: Create isomorphism with explicit inverse
Let h = Morphism with:
    morphism_id: "h"
    source_object: "X"
    target_object: "Y"
    morphism_type: "isomorphism"
    invertible: true

Let h_inv = Morphism with:
    morphism_id: "h_inv"
    source_object: "Y"
    target_object: "X"
    morphism_type: "isomorphism"
    invertible: true

Let isomorphism_h = Isomorphism with:
    morphism_base: h
    inverse_morphism: h_inv
    isomorphism_verified: false

Note: Verify isomorphism properties
Let iso_verification = Morphisms.verify_isomorphism(isomorphism_h)
Display "Isomorphism verified: " joined with String(iso_verification.verification_successful)
Display "h ∘ h⁻¹ = id_Y: " joined with String(iso_verification.right_inverse_check)
Display "h⁻¹ ∘ h = id_X: " joined with String(iso_verification.left_inverse_check)

Set isomorphism_h.isomorphism_verified to iso_verification.verification_successful
```

### Automorphisms
```runa
Note: Create automorphism (isomorphism from object to itself)
Let rotation = Morphism with:
    morphism_id: "rotation_90"
    source_object: "Square"
    target_object: "Square"
    morphism_type: "automorphism"
    invertible: true

Let rotation_inv = Morphism with:
    morphism_id: "rotation_270"
    source_object: "Square" 
    target_object: "Square"
    morphism_type: "automorphism"
    invertible: true

Let automorphism_rot = Automorphism with:
    isomorphism_base: Isomorphism with:
        morphism_base: rotation
        inverse_morphism: rotation_inv
    endomorphism_base: Endomorphism with:
        morphism_base: rotation
        fixed_points: ["center"]
    group_structure: Dictionary with: "order": "4"
    symmetry_properties: Dictionary with: "preserves_shape": "true"

Note: Analyze automorphism group
Let auto_group_analysis = Morphisms.analyze_automorphism_group(automorphism_rot)
Display "Group order: " joined with auto_group_analysis.group_order
Display "Abelian group: " joined with String(auto_group_analysis.is_abelian)
Display "Cyclic group: " joined with String(auto_group_analysis.is_cyclic)
```

## Monomorphisms and Epimorphisms

### Monomorphisms (Injective Morphisms)
```runa
Note: Create and verify monomorphism
Let embedding = Morphism with:
    morphism_id: "embedding"
    source_object: "SubObject"
    target_object: "Object"
    morphism_type: "monomorphism"

Let monomorphism_embed = Monomorphism with:
    morphism_base: embedding
    left_cancellative: false  Note: To be verified
    injective_property: true
    monic_verification: Dictionary[String, Boolean]()

Note: Test left cancellation property
Let test_morphisms = ["α", "β"]  Note: Two morphisms with same target
Let cancellation_test = Morphisms.test_left_cancellation(monomorphism_embed, test_morphisms)
Display "Left cancellative: " joined with String(cancellation_test.is_left_cancellative)
Display "Monomorphism verified: " joined with String(cancellation_test.monomorphism_verified)

Set monomorphism_embed.left_cancellative to cancellation_test.is_left_cancellative
Set monomorphism_embed.monic_verification to cancellation_test.verification_data
```

### Epimorphisms (Surjective Morphisms)  
```runa
Note: Create and verify epimorphism
Let projection = Morphism with:
    morphism_id: "projection"
    source_object: "Product"
    target_object: "Factor"
    morphism_type: "epimorphism"

Let epimorphism_proj = Epimorphism with:
    morphism_base: projection
    right_cancellative: false  Note: To be verified
    surjective_property: true
    epic_verification: Dictionary[String, Boolean]()

Note: Test right cancellation property
Let test_morphisms_epi = ["γ", "δ"]  Note: Two morphisms with same source
Let epi_cancellation_test = Morphisms.test_right_cancellation(epimorphism_proj, test_morphisms_epi)
Display "Right cancellative: " joined with String(epi_cancellation_test.is_right_cancellative)
Display "Epimorphism verified: " joined with String(epi_cancellation_test.epimorphism_verified)

Set epimorphism_proj.right_cancellative to epi_cancellation_test.is_right_cancellative
Set epimorphism_proj.epic_verification to epi_cancellation_test.verification_data
```

### Bimorphisms
```runa
Note: Morphisms that are both mono and epi
Let bimorphism_candidate = Morphism with:
    morphism_id: "bimorphism"
    source_object: "A"
    target_object: "B"

Let bimorphism_analysis = Morphisms.analyze_bimorphism(bimorphism_candidate)
Display "Is monomorphism: " joined with String(bimorphism_analysis.is_monomorphism)
Display "Is epimorphism: " joined with String(bimorphism_analysis.is_epimorphism)
Display "Is bimorphism: " joined with String(bimorphism_analysis.is_bimorphism)

Note: In Set category, bimorphisms are isomorphisms
If bimorphism_analysis.is_bimorphism and bimorphism_analysis.category_type == "Set":
    Display "In Set: bimorphism implies isomorphism"
    Let iso_construction = Morphisms.construct_isomorphism_from_bimorphism(bimorphism_candidate)
    Display "Isomorphism constructed: " joined with String(iso_construction.construction_successful)
```

## Universal Constructions

### Limits and Cones
```runa
Note: Construct limit of diagram
Let diagram_objects = ["X", "Y", "Z"]
Let diagram_morphisms = Dictionary[String, String]()
Set diagram_morphisms["f: X → Y"] to "f"
Set diagram_morphisms["g: X → Z"] to "g"

Let cone_morphisms = Dictionary[String, String]()
Set cone_morphisms["p_X: L → X"] to "p_X"  
Set cone_morphisms["p_Y: L → Y"] to "p_Y"
Set cone_morphisms["p_Z: L → Z"] to "p_Z"

Let limit_construction = Limit with:
    limit_object: "L"
    cone_morphisms: cone_morphisms
    diagram_category: "discrete_diagram"
    universal_property: false  Note: To be verified
    uniqueness_condition: false

Note: Verify universal property of limit
Let limit_verification = Morphisms.verify_limit_universal_property(limit_construction)
Display "Universal property satisfied: " joined with String(limit_verification.universal_property_satisfied)
Display "Unique factorization exists: " joined with String(limit_verification.unique_factorization)
Display "Cone commutativity: " joined with String(limit_verification.cone_commutes)

Set limit_construction.universal_property to limit_verification.universal_property_satisfied
Set limit_construction.uniqueness_condition to limit_verification.unique_factorization
```

### Colimits and Cocones
```runa
Note: Construct colimit (dual to limit)
Let colimit_construction = Colimit with:
    colimit_object: "C"
    cocone_morphisms: Dictionary with:
        "i_X: X → C": "i_X"
        "i_Y: Y → C": "i_Y"
        "i_Z: Z → C": "i_Z"
    diagram_category: "discrete_diagram"
    universal_property: false
    uniqueness_condition: false

Let colimit_verification = Morphisms.verify_colimit_universal_property(colimit_construction)
Display "Colimit universal property: " joined with String(colimit_verification.universal_property_satisfied)
Display "Cocone commutativity: " joined with String(colimit_verification.cocone_commutes)

Note: Limit-colimit duality
Let duality_relationship = Morphisms.analyze_limit_colimit_duality(limit_construction, colimit_construction)
Display "Dual constructions: " joined with String(duality_relationship.are_dual)
Display "Opposite category relationship: " joined with String(duality_relationship.opposite_category_correspondence)
```

### Products and Coproducts
```runa
Note: Product as special case of limit
Let product_objects = ["A", "B"]
Let product_limit = Morphisms.construct_product(product_objects)
Display "Product object: " joined with product_limit.product_object
Display "Projection morphisms: " joined with String(Length(product_limit.projections))

Note: Verify product universal property
For Each object in product_limit.projections:
    Display "Projection to " joined with object["target"] joined with ": " joined with object["morphism"]

Note: Coproduct as special case of colimit  
Let coproduct_colimit = Morphisms.construct_coproduct(product_objects)
Display "Coproduct object: " joined with coproduct_colimit.coproduct_object
Display "Injection morphisms: " joined with String(Length(coproduct_colimit.injections))

Note: Product-coproduct relationship
Let product_coproduct_analysis = Morphisms.compare_product_coproduct(product_limit, coproduct_colimit)
Display "Categorical duality: " joined with String(product_coproduct_analysis.categorical_duality)
Display "Distributive laws: " joined with String(product_coproduct_analysis.distributive_laws_hold)
```

## Pullbacks and Pushouts

### Pullback Construction
```runa
Note: Construct pullback (fiber product)
Let span_morphism_f = Morphism with:
    morphism_id: "f"
    source_object: "B"
    target_object: "C"

Let span_morphism_g = Morphism with:
    morphism_id: "g"
    source_object: "A"
    target_object: "C"

Let pullback_construction = Pullback with:
    pullback_object: "P"
    projection_morphisms: Dictionary with:
        "π₁: P → A": "π₁"
        "π₂: P → B": "π₂"
    original_morphisms: Dictionary with:
        "f: B → C": "f"
        "g: A → C": "g"
    commutativity_condition: false
    universal_property: false

Note: Verify pullback square commutativity
Let pullback_verification = Morphisms.verify_pullback_square(pullback_construction)
Display "Square commutes: g ∘ π₁ = f ∘ π₂: " joined with String(pullback_verification.square_commutes)
Display "Universal property: " joined with String(pullback_verification.universal_property_holds)

Set pullback_construction.commutativity_condition to pullback_verification.square_commutes
Set pullback_construction.universal_property to pullback_verification.universal_property_holds

Note: Applications of pullbacks
Let pullback_applications = Morphisms.analyze_pullback_applications(pullback_construction)
Display "Fiber over point: " joined with String(pullback_applications.fiber_interpretation)
Display "Base change: " joined with String(pullback_applications.base_change_interpretation)
Display "Inverse image: " joined with String(pullback_applications.inverse_image_interpretation)
```

### Pushout Construction  
```runa
Note: Construct pushout (cocartesian square)
Let cospan_morphism_f = Morphism with:
    morphism_id: "f"
    source_object: "A"
    target_object: "B"

Let cospan_morphism_g = Morphism with:
    morphism_id: "g"
    source_object: "A"
    target_object: "C"

Let pushout_construction = Pushout with:
    pushout_object: "Q"
    injection_morphisms: Dictionary with:
        "i₁: B → Q": "i₁"
        "i₂: C → Q": "i₂"
    original_morphisms: Dictionary with:
        "f: A → B": "f"
        "g: A → C": "g"
    commutativity_condition: false
    universal_property: false

Note: Verify pushout square
Let pushout_verification = Morphisms.verify_pushout_square(pushout_construction)
Display "Square commutes: i₁ ∘ f = i₂ ∘ g: " joined with String(pushout_verification.square_commutes)
Display "Universal property: " joined with String(pushout_verification.universal_property_holds)

Note: Pullback-pushout duality
Let pb_po_duality = Morphisms.analyze_pullback_pushout_duality(pullback_construction, pushout_construction)
Display "Dual constructions: " joined with String(pb_po_duality.are_dual)
Display "Opposite category correspondence: " joined with String(pb_po_duality.op_category_relationship)
```

## Equalizers and Coequalizers

### Equalizer Construction
```runa
Note: Construct equalizer of parallel morphisms
Let parallel_f = Morphism with:
    morphism_id: "f"
    source_object: "A"
    target_object: "B"

Let parallel_g = Morphism with:
    morphism_id: "g"  
    source_object: "A"
    target_object: "B"

Let equalizer_construction = Equalizer with:
    equalizer_object: "E"
    equalizer_morphism: "e: E → A"
    equalized_morphisms: ["f", "g"]
    equalizer_property: false
    universal_property: false

Note: Verify equalizer property
Let equalizer_verification = Morphisms.verify_equalizer_property(equalizer_construction)
Display "Equalizer property: f ∘ e = g ∘ e: " joined with String(equalizer_verification.equalizes_morphisms)
Display "Universal property: " joined with String(equalizer_verification.universal_property_satisfied)

Set equalizer_construction.equalizer_property to equalizer_verification.equalizes_morphisms
Set equalizer_construction.universal_property to equalizer_verification.universal_property_satisfied

Note: Equalizer as limit
Let equalizer_as_limit = Morphisms.interpret_equalizer_as_limit(equalizer_construction)
Display "Equalizer is limit of parallel pair: " joined with String(equalizer_as_limit.is_limit)
Display "Limiting cone structure: " joined with String(equalizer_as_limit.cone_structure_valid)
```

### Coequalizer Construction
```runa
Note: Construct coequalizer (dual to equalizer)
Let coequalizer_construction = Coequalizer with:
    coequalizer_object: "Q"
    coequalizer_morphism: "q: B → Q"
    coequalized_morphisms: ["f", "g"]
    coequalizer_property: false
    universal_property: false

Let coequalizer_verification = Morphisms.verify_coequalizer_property(coequalizer_construction)
Display "Coequalizer property: q ∘ f = q ∘ g: " joined with String(coequalizer_verification.coequalizes_morphisms)
Display "Universal property: " joined with String(coequalizer_verification.universal_property_satisfied)

Note: Quotient interpretation
Let quotient_analysis = Morphisms.analyze_coequalizer_as_quotient(coequalizer_construction)
Display "Quotient by equivalence relation: " joined with String(quotient_analysis.quotient_interpretation)
Display "Equivalence classes well-defined: " joined with String(quotient_analysis.well_defined_quotient)
```

## Advanced Constructions

### Kan Extensions
```runa
Note: Left and right Kan extensions
Let extension_data = Dictionary with:
    "functor": "F: C → D"
    "inclusion": "i: C → C'"
    "extension_type": "left"

Let kan_extension = Morphisms.compute_kan_extension(extension_data)
Display "Kan extension exists: " joined with String(kan_extension.extension_exists)
Display "Extension type: " joined with kan_extension.extension_type
Display "Universal property satisfied: " joined with String(kan_extension.universal_property)

If kan_extension.extension_exists:
    Let preservation_analysis = Morphisms.analyze_kan_extension_preservation(kan_extension)
    Display "Preserves colimits (left): " joined with String(preservation_analysis.preserves_colimits)
    Display "Preserves limits (right): " joined with String(preservation_analysis.preserves_limits)
```

### Adjunctions via Universal Properties
```runa
Note: Recognize adjunctions from universal constructions
Let adjunction_data = Dictionary with:
    "left_functor": "F: C → D"
    "right_functor": "G: D → C"
    "unit": "η: Id_C → GF"
    "counit": "ε: FG → Id_D"

Let adjunction_analysis = Morphisms.analyze_adjunction_via_universals(adjunction_data)
Display "Forms adjunction: F ⊣ G: " joined with String(adjunction_analysis.is_adjunction)
Display "Triangle identities satisfied: " joined with String(adjunction_analysis.triangle_identities)

Note: Universal property characterization
Let universal_characterization = Morphisms.characterize_adjunction_universally(adjunction_analysis)
Display "Universal property of adjunction: " joined with universal_characterization.universal_description
Display "Bijection Hom(F-, =) ≅ Hom(-, G=): " joined with String(universal_characterization.hom_bijection)
```

## Diagram Chasing and Proofs

### Snake Lemma
```runa
Note: Implement snake lemma for commutative diagrams
Let snake_diagram = Dictionary with:
    "rows": ["short exact sequence 1", "short exact sequence 2"]
    "vertical_morphisms": ["α", "β", "γ"]
    "commutativity": "all squares commute"

Let snake_lemma_result = Morphisms.apply_snake_lemma(snake_diagram)
Display "Snake lemma applies: " joined with String(snake_lemma_result.lemma_applicable)
Display "Connecting homomorphism exists: " joined with String(snake_lemma_result.connecting_morphism_exists)
Display "Long exact sequence: " joined with snake_lemma_result.exact_sequence

If snake_lemma_result.lemma_applicable:
    Let exactness_verification = Morphisms.verify_snake_lemma_exactness(snake_lemma_result)
    Display "Exactness at each object: " joined with String(exactness_verification.exact_at_all_objects)
```

### Five Lemma
```runa
Note: Five lemma for commutative diagrams
Let five_lemma_diagram = Dictionary with:
    "objects": ["A₁", "A₂", "A₃", "A₄", "A₅"]
    "horizontal_morphisms": ["f₁", "f₂", "f₃", "f₄"]
    "vertical_morphisms": ["α₁", "α₂", "α₃", "α₄", "α₅"]
    "commutativity": "diagram commutes"

Let five_lemma_conditions = Dictionary with:
    "α₁_epimorphism": "true"
    "α₂_monomorphism": "true"
    "α₄_epimorphism": "true"
    "α₅_monomorphism": "true"
    "rows_exact": "true"

Let five_lemma_result = Morphisms.apply_five_lemma(five_lemma_diagram, five_lemma_conditions)
Display "Five lemma conclusion: α₃ is isomorphism: " joined with String(five_lemma_result.middle_is_isomorphism)
Display "Proof technique: diagram chasing: " joined with String(five_lemma_result.proof_by_diagram_chase)
```

## Error Handling

### Morphism Composition Errors
```runa
Try:
    Note: Invalid composition (mismatched objects)
    Let invalid_f = Morphism with:
        source_object: "A"
        target_object: "B"
    
    Let invalid_g = Morphism with:
        source_object: "C"  Note: Should be "B" for composition
        target_object: "D"
    
    Let invalid_composition = Morphisms.compose_morphisms(invalid_g, invalid_f)
Catch Errors.CompositionError as error:
    Display "Composition error: " joined with error.message
    Display "Target of f must equal source of g for g ∘ f"

Try:
    Note: Non-existent inverse
    Let non_invertible = Morphism with:
        morphism_id: "non_iso"
        invertible: false
    
    Let inverse_attempt = Morphisms.find_inverse_morphism(non_invertible)
Catch Errors.InvertibilityError as error:
    Display "Invertibility error: " joined with error.message
    Display "Morphism is not an isomorphism"
```

### Universal Property Verification Errors
```runa
Try:
    Note: Invalid universal construction
    Let invalid_limit = Limit with:
        cone_morphisms: Dictionary[String, String]()  Note: Empty cone
        universal_property: true  Note: Claimed but not verified
    
    Let verification_attempt = Morphisms.verify_limit_universal_property(invalid_limit)
Catch Errors.UniversalPropertyError as error:
    Display "Universal property error: " joined with error.message
    Display "Cone is empty or doesn't commute with diagram"

Try:
    Note: Pullback with non-commuting square
    Let non_commuting_pullback = Pullback with:
        commutativity_condition: false
        universal_property: true  Note: Cannot be universal without commutativity
    
    Let pullback_check = Morphisms.verify_pullback_square(non_commuting_pullback)
Catch Errors.CommutativityError as error:
    Display "Commutativity error: " joined with error.message
    Display "Pullback square must commute"
```

## Performance Considerations

- **Composition Chains**: Cache associative compositions for repeated use
- **Universal Property Verification**: Use lazy evaluation for expensive checks
- **Diagram Construction**: Build diagrams incrementally to avoid redundant computations
- **Morphism Classification**: Store computed properties to avoid re-verification

## Best Practices

1. **Morphism Verification**: Always verify morphism properties before use in constructions
2. **Universal Properties**: Check universal properties hold before claiming categorical constructions
3. **Diagram Commutativity**: Verify all required squares and triangles commute
4. **Composition Validity**: Ensure source/target compatibility before composition
5. **Duality Principles**: Use categorical duality to derive constructions efficiently
6. **Proof Techniques**: Employ diagram chasing for categorical proofs

## Related Documentation

- **[Math Category Functors](functors.md)**: Functor theory and natural transformations
- **[Math Category Monads](monads.md)**: Monadic constructions and Kleisli categories
- **[Math Algebra Abstract](../algebra/abstract.md)**: Abstract algebraic structures
- **[Math Logic Formal](../logic/formal.md)**: Formal logic and proof systems