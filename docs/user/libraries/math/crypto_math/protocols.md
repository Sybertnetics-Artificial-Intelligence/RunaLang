# Protocols Module

The protocols module provides comprehensive mathematical foundations for advanced cryptographic protocols, including zero-knowledge proofs, multi-party computation, secret sharing schemes, and interactive proof systems. This module is essential for implementing sophisticated cryptographic systems with enhanced privacy and security properties.

## Overview

Cryptographic protocols enable secure communication and computation between multiple parties with various security guarantees such as privacy, authenticity, and correctness. This module provides the mathematical tools and theoretical foundations for implementing complex cryptographic protocols.

## Mathematical Foundation

### Protocol Security Models

- **Semi-Honest Model**: Parties follow protocol but may try to learn extra information
- **Malicious Model**: Parties may deviate arbitrarily from the protocol
- **Covert Model**: Parties may deviate but prefer not to be caught
- **Universal Composability**: Security guarantees under arbitrary composition

### Cryptographic Assumptions

- **Computational Assumptions**: Based on computational hardness (RSA, DLP, etc.)
- **Information-Theoretic Security**: Unconditional security regardless of computational power
- **Random Oracle Model**: Idealized hash functions for security proofs

## Core Data Structures

### CryptoProtocol

Represents a cryptographic protocol with its properties:

```runa
Type called "CryptoProtocol":
    protocol_id as String                 Note: Unique protocol identifier
    protocol_name as String              Note: Common name of the protocol
    protocol_type as String              Note: "zkp", "mpc", "secret_sharing", etc.
    security_model as String             Note: "semi_honest", "malicious", "covert"
    participants as List[String]         Note: List of participant identifiers
    rounds as Integer                    Note: Number of communication rounds
    computational_assumptions as List[String]  Note: Required hardness assumptions
    security_properties as Dictionary[String, Boolean]  Note: Security guarantees
```

### ZeroKnowledgeProof

Represents a zero-knowledge proof system:

```runa
Type called "ZeroKnowledgeProof":
    proof_id as String                   Note: Unique proof identifier
    statement as String                  Note: Statement being proved
    witness as String                    Note: Secret witness (prover side)
    proof_system as String               Note: "interactive", "non_interactive"
    completeness_parameter as Float     Note: Probability honest prover convinces verifier
    soundness_parameter as Float        Note: Probability cheating prover fails
    zero_knowledge_simulator as String  Note: Simulator algorithm description
    verification_algorithm as String    Note: Verification procedure
```

## Basic Usage

### Zero-Knowledge Proof Construction

```runa
Use math.crypto_math.protocols as Protocols

Note: Create a simple discrete logarithm zero-knowledge proof
Let dlog_zkp be Protocols.create_schnorr_proof()
dlog_zkp.statement = "I know x such that g^x = y"
dlog_zkp.proof_system = "interactive"

Note: Generate proof components
Let proof_transcript be Protocols.generate_schnorr_proof(dlog_zkp, witness, public_parameters)
Let verification_result be Protocols.verify_schnorr_proof(proof_transcript)
```

### Secret Sharing Setup

```runa
Note: Create Shamir secret sharing scheme
Let secret_sharing be Protocols.create_shamir_secret_sharing()
secret_sharing.threshold = 3
secret_sharing.total_participants = 5
secret_sharing.secret_domain = "finite_field_p"

Let shares be Protocols.generate_shamir_shares(secret, secret_sharing)
Let reconstructed_secret be Protocols.reconstruct_shamir_secret(shares.take(3))
```

## Zero-Knowledge Proof Systems

### Schnorr Proof of Knowledge

```runa
Note: Interactive Schnorr proof for discrete logarithm knowledge
Process called "schnorr_proof_interactive" that takes witness as String, generator as String, public_value as String, modulus as String returns Dictionary[String, String]:
    Let proof_transcript be Dictionary[String, String].create()
    
    Note: Prover's commitment phase
    Let r be Protocols.generate_random_scalar(modulus)
    Let commitment be Protocols.modular_exponentiation(generator, r, modulus)
    proof_transcript["commitment"] = commitment
    
    Note: Verifier's challenge (simulated)
    Let challenge be Protocols.generate_random_challenge(modulus)
    proof_transcript["challenge"] = challenge
    
    Note: Prover's response
    Let witness_int be Protocols.parse_big_integer(witness)
    Let challenge_int be Protocols.parse_big_integer(challenge)
    Let r_int be Protocols.parse_big_integer(r)
    
    Let response be Protocols.modular_arithmetic(
        Protocols.add_big_integer(r_int, Protocols.multiply_big_integer(witness_int, challenge_int)),
        modulus
    )
    proof_transcript["response"] = response
    
    Note: Store verification parameters
    proof_transcript["generator"] = generator
    proof_transcript["public_value"] = public_value
    proof_transcript["modulus"] = modulus
    proof_transcript["proof_type"] = "schnorr_interactive"
    
    Return proof_transcript
```

### Fiat-Shamir Transformation

```runa
Note: Convert interactive proof to non-interactive using Fiat-Shamir heuristic
Process called "fiat_shamir_transform" that takes interactive_proof as Dictionary[String, String], hash_function as String returns Dictionary[String, String]:
    Let non_interactive_proof be Dictionary[String, String].create()
    
    Note: Construct challenge input from commitment and public parameters
    Let challenge_input be interactive_proof["commitment"] + "|" + 
                           interactive_proof["generator"] + "|" + 
                           interactive_proof["public_value"] + "|" + 
                           interactive_proof["modulus"]
    
    Note: Generate challenge using hash function
    Let challenge_hash be Protocols.compute_hash(challenge_input, hash_function)
    let challenge be Protocols.hash_to_field_element(challenge_hash, interactive_proof["modulus"])
    
    Note: Recompute response with the derived challenge
    Let witness_challenge be Protocols.modular_multiply(
        interactive_proof["witness"],  Note: Would need to be passed separately
        challenge,
        interactive_proof["modulus"]
    )
    
    Let response be Protocols.modular_add(
        interactive_proof["randomness"],  Note: Would need to be stored
        witness_challenge,
        interactive_proof["modulus"]
    )
    
    non_interactive_proof["commitment"] = interactive_proof["commitment"]
    non_interactive_proof["challenge"] = challenge
    non_interactive_proof["response"] = response
    non_interactive_proof["proof_type"] = "schnorr_non_interactive"
    non_interactive_proof["hash_function"] = hash_function
    
    Note: Copy verification parameters
    non_interactive_proof["generator"] = interactive_proof["generator"]
    non_interactive_proof["public_value"] = interactive_proof["public_value"]
    non_interactive_proof["modulus"] = interactive_proof["modulus"]
    
    Return non_interactive_proof
```

## Multi-Party Computation

### BGW Protocol for Arithmetic Circuits

```runa
Note: BGW protocol for secure multi-party computation over finite fields
Process called "bgw_secure_computation" that takes circuit as String, inputs as List[String], threshold as Integer returns List[String]:
    Let participant_count be inputs.size
    let field_prime be Protocols.get_computation_prime()
    
    Note: Secret share all inputs using Shamir secret sharing
    Let shared_inputs be List[List[String]].create()
    
    For input_value in inputs:
        Let shares be Protocols.shamir_share_secret(input_value, threshold, participant_count, field_prime)
        shared_inputs.add(shares)
    
    Note: Parse and evaluate arithmetic circuit
    Let circuit_gates be Protocols.parse_arithmetic_circuit(circuit)
    Let intermediate_shares be Dictionary[String, List[String]].create()
    
    Note: Process gates in topological order
    For gate in circuit_gates:
        Match gate.operation:
            Case "add":
                Note: Addition is local - add shares pointwise
                Let left_shares be intermediate_shares[gate.left_input]
                let right_shares be intermediate_shares[gate.right_input]
                Let sum_shares be List[String].create()
                
                For i from 0 to participant_count:
                    let sum_share be Protocols.modular_add(left_shares[i], right_shares[i], field_prime)
                    sum_shares.add(sum_share)
                
                intermediate_shares[gate.output] = sum_shares
                
            Case "multiply":
                Note: Multiplication requires interaction and degree reduction
                Let left_shares be intermediate_shares[gate.left_input]
                Let right_shares be intermediate_shares[gate.right_input]
                
                Note: Local multiplication creates degree-2t shares
                Let product_shares_2t be List[String].create()
                For i from 0 to participant_count:
                    Let product_share be Protocols.modular_multiply(left_shares[i], right_shares[i], field_prime)
                    product_shares_2t.add(product_share)
                
                Note: Degree reduction using BGW multiplication protocol
                Let reduced_shares be Protocols.bgw_degree_reduction(product_shares_2t, threshold, participant_count, field_prime)
                intermediate_shares[gate.output] = reduced_shares
                
            Case "constant":
                Note: Public constant shared as (constant, 0, 0, ...)
                Let constant_shares be List[String].create()
                constant_shares.add(gate.constant_value)
                For i from 1 to participant_count:
                    constant_shares.add("0")
                intermediate_shares[gate.output] = constant_shares
    
    Note: Collect output shares
    Let output_gate_id be Protocols.get_circuit_output_gate(circuit)
    Let output_shares be intermediate_shares[output_gate_id]
    
    Note: Reconstruct final result (would be done by designated parties in practice)
    Let reconstruction_shares be output_shares.take(threshold + 1)
    Let final_result be Protocols.shamir_reconstruct_secret(reconstruction_shares, field_prime)
    
    Return [final_result]
```

### GMW Protocol for Boolean Circuits

```runa
Note: GMW protocol for secure computation of boolean circuits
Process called "gmw_boolean_computation" that takes circuit as String, inputs as List[String] returns String:
    Let participant_count be inputs.size
    
    Note: Secret share inputs using XOR sharing
    Let shared_inputs be List[List[String]].create()
    
    For input_bit in inputs:
        Let xor_shares be Protocols.generate_xor_shares(input_bit, participant_count)
        shared_inputs.add(xor_shares)
    
    Note: Parse boolean circuit
    Let boolean_gates be Protocols.parse_boolean_circuit(circuit)
    Let gate_shares be Dictionary[String, List[String]].create()
    
    For gate in boolean_gates:
        Match gate.operation:
            Case "xor":
                Note: XOR is local operation
                Let left_shares be gate_shares[gate.left_input]
                Let right_shares be gate_shares[gate.right_input]
                Let xor_result_shares be List[String].create()
                
                For i from 0 to participant_count:
                    Let xor_result be Protocols.xor_bits(left_shares[i], right_shares[i])
                    xor_result_shares.add(xor_result)
                
                gate_shares[gate.output] = xor_result_shares
                
            Case "and":
                Note: AND requires oblivious transfer protocol
                Let left_shares be gate_shares[gate.left_input]
                Let right_shares be gate_shares[gate.right_input]
                
                Note: Execute GMW AND protocol using OT
                Let and_result_shares be Protocols.gmw_and_gate(left_shares, right_shares)
                gate_shares[gate.output] = and_result_shares
                
            Case "not":
                Note: NOT on first share only (others remain 0)
                Let input_shares be gate_shares[gate.input]
                Let not_shares be List[String].create()
                not_shares.add(Protocols.not_bit(input_shares[0]))
                
                For i from 1 to participant_count:
                    not_shares.add(input_shares[i])  Note: Keep other shares unchanged
                
                gate_shares[gate.output] = not_shares
    
    Note: Reconstruct output
    Let output_gate_id be Protocols.get_circuit_output_gate(circuit)
    let output_shares be gate_shares[output_gate_id]
    
    Let final_result be "0"
    For share in output_shares:
        final_result = Protocols.xor_bits(final_result, share)
    
    Return final_result
```

## Secret Sharing Schemes

### Shamir Secret Sharing

```runa
Note: Shamir's threshold secret sharing scheme
Process called "shamir_secret_sharing" that takes secret as String, threshold as Integer, total_shares as Integer, field_prime as String returns List[String]:
    Let shares be List[String].create()
    
    Note: Generate random polynomial coefficients
    Let coefficients be List[String].create()
    coefficients.add(secret)  Note: a_0 = secret
    
    For i from 1 to threshold:
        Let random_coeff be Protocols.generate_random_field_element(field_prime)
        coefficients.add(random_coeff)
    
    Note: Evaluate polynomial at points 1, 2, ..., total_shares
    For share_index from 1 to total_shares:
        Let x_value be String.from_integer(share_index)
        Let y_value be Protocols.evaluate_polynomial(coefficients, x_value, field_prime)
        
        Let share be x_value + ":" + y_value  Note: (x, y) pair
        shares.add(share)
    
    Return shares
```

### Verifiable Secret Sharing

```runa
Note: Pedersen verifiable secret sharing with commitment
Process called "pedersen_vss" that takes secret as String, threshold as Integer, total_shares as Integer, generator_g as String, generator_h as String, field_prime as String returns Dictionary[String, List[String]]:
    Let vss_result be Dictionary[String, List[String]].create()
    
    Note: Generate random polynomial coefficients
    let secret_coefficients be List[String].create()
    Let commitment_coefficients be List[String].create()
    
    secret_coefficients.add(secret)
    Let random_commitment_coeff be Protocols.generate_random_field_element(field_prime)
    commitment_coefficients.add(random_commitment_coeff)
    
    For i from 1 to threshold:
        Let secret_coeff be Protocols.generate_random_field_element(field_prime)
        Let commit_coeff be Protocols.generate_random_field_element(field_prime)
        secret_coefficients.add(secret_coeff)
        commitment_coefficients.add(commit_coeff)
    
    Note: Compute polynomial commitments
    Let commitments be List[String].create()
    For i from 0 to threshold:
        Let g_to_ai be Protocols.modular_exponentiation(generator_g, secret_coefficients[i], field_prime)
        Let h_to_bi be Protocols.modular_exponentiation(generator_h, commitment_coefficients[i], field_prime)
        Let commitment_i be Protocols.modular_multiply(g_to_ai, h_to_bi, field_prime)
        commitments.add(commitment_i)
    
    Note: Generate shares
    let secret_shares be List[String].create()
    Let commitment_shares be List[String].create()
    
    For share_index from 1 to total_shares:
        Let x_value be String.from_integer(share_index)
        
        Let secret_share be Protocols.evaluate_polynomial(secret_coefficients, x_value, field_prime)
        Let commitment_share be Protocols.evaluate_polynomial(commitment_coefficients, x_value, field_prime)
        
        secret_shares.add(x_value + ":" + secret_share)
        commitment_shares.add(x_value + ":" + commitment_share)
    
    vss_result["secret_shares"] = secret_shares
    vss_result["commitment_shares"] = commitment_shares
    vss_result["polynomial_commitments"] = commitments
    
    Return vss_result
```

## Commitment Schemes

### Pedersen Commitment

```runa
Note: Pedersen commitment scheme with perfect hiding and computational binding
Process called "pedersen_commit" that takes message as String, randomness as String, generator_g as String, generator_h as String, modulus as String returns String:
    Note: Compute commitment C = g^m * h^r mod p
    Let g_to_m be Protocols.modular_exponentiation(generator_g, message, modulus)
    Let h_to_r be Protocols.modular_exponentiation(generator_h, randomness, modulus)
    
    Let commitment be Protocols.modular_multiply(g_to_m, h_to_r, modulus)
    Return commitment
```

### Vector Commitments

```runa
Note: Merkle tree-based vector commitment scheme
Process called "merkle_vector_commit" that takes vector as List[String], hash_function as String returns Dictionary[String, String]:
    Let commitment_data be Dictionary[String, String].create()
    
    Note: Pad vector to power of 2 if necessary
    Let padded_vector be Protocols.pad_to_power_of_2(vector)
    Let tree_height be Protocols.log2_integer(padded_vector.size)
    
    Note: Build Merkle tree bottom-up
    Let current_level be padded_vector
    Let tree_levels be List[List[String]].create()
    tree_levels.add(current_level)
    
    For level from 1 to tree_height:
        Let next_level be List[String].create()
        
        For i from 0 to (current_level.size / 2):
            Let left_hash be current_level[i * 2]
            Let right_hash be current_level[i * 2 + 1]
            Let parent_hash be Protocols.compute_hash(left_hash + right_hash, hash_function)
            next_level.add(parent_hash)
        
        tree_levels.add(next_level)
        current_level = next_level
    
    Note: Root is the commitment
    let root_commitment be tree_levels[tree_height][0]
    
    commitment_data["commitment"] = root_commitment
    commitment_data["tree_height"] = String.from_integer(tree_height)
    commitment_data["vector_size"] = String.from_integer(vector.size)
    
    Note: Store tree for opening proofs (in practice, would be stored separately)
    Protocols.store_merkle_tree(commitment_data["commitment"], tree_levels)
    
    Return commitment_data
```

## Oblivious Transfer

### 1-out-of-2 OT Protocol

```runa
Note: 1-out-of-2 oblivious transfer using RSA assumption
Process called "rsa_ot_1_of_2" that takes messages as List[String], choice_bit as String, rsa_modulus as String, rsa_exponent as String returns String:
    Note: Receiver's choice bit determines which message to receive
    
    Note: Receiver generates random values
    Let x0 be Protocols.generate_random_field_element(rsa_modulus)
    Let x1 be Protocols.generate_random_field_element(rsa_modulus)
    
    Note: Receiver computes v = x_c + r^e mod N where c is choice bit
    Let r be Protocols.generate_random_field_element(rsa_modulus)
    Let r_to_e be Protocols.modular_exponentiation(r, rsa_exponent, rsa_modulus)
    
    Let v be x0
    If choice_bit == "1":
        v = x1
    
    v = Protocols.modular_add(v, r_to_e, rsa_modulus)
    
    Note: Sender receives v and computes k0, k1
    Let k0 be Protocols.rsa_encrypt(Protocols.modular_subtract(v, x0, rsa_modulus), rsa_exponent, rsa_modulus)
    Let k1 be Protocols.rsa_encrypt(Protocols.modular_subtract(v, x1, rsa_modulus), rsa_exponent, rsa_modulus)
    
    Note: Sender encrypts messages
    Let encrypted_m0 be Protocols.xor_strings(messages[0], k0)
    Let encrypted_m1 be Protocols.xor_strings(messages[1], k1)
    
    Note: Receiver can decrypt only chosen message
    Let chosen_key be Protocols.big_integer_to_string(r)
    Let chosen_encrypted_message be encrypted_m0
    If choice_bit == "1":
        chosen_encrypted_message = encrypted_m1
    
    Let received_message be Protocols.xor_strings(chosen_encrypted_message, chosen_key)
    
    Return received_message
```

## Error Handling and Protocol Validation

### Protocol Security Validation

```runa
Note: Validate cryptographic protocol security properties
Process called "validate_protocol_security" that takes protocol as CryptoProtocol returns Dictionary[String, Boolean]:
    Let security_validation be Dictionary[String, Boolean].create()
    
    Note: Check participant requirements
    security_validation["sufficient_participants"] = (protocol.participants.size >= 2)
    
    Note: Validate computational assumptions
    For assumption in protocol.computational_assumptions:
        Let assumption_valid be Protocols.validate_cryptographic_assumption(assumption)
        security_validation["assumption_" + assumption] = assumption_valid
    
    Note: Check protocol type specific requirements
    Match protocol.protocol_type:
        Case "secret_sharing":
            Let threshold_property be protocol.security_properties["threshold_security"]
            security_validation["threshold_valid"] = threshold_property
            
        Case "zero_knowledge":
            let completeness be protocol.security_properties["completeness"]
            let soundness be protocol.security_properties["soundness"]
            Let zero_knowledge be protocol.security_properties["zero_knowledge"]
            
            security_validation["completeness"] = completeness
            security_validation["soundness"] = soundness
            security_validation["zero_knowledge"] = zero_knowledge
            
        Case "multi_party_computation":
            Let privacy_property be protocol.security_properties["privacy"]
            Let correctness_property be protocol.security_properties["correctness"]
            
            security_validation["privacy"] = privacy_property
            security_validation["correctness"] = correctness_property
    
    Note: Overall security assessment
    Let all_properties_valid be true
    For property_name in security_validation.keys():
        If not security_validation[property_name]:
            all_properties_valid = false
            Break
    
    security_validation["overall_security"] = all_properties_valid
    
    Return security_validation
```

### Zero-Knowledge Proof Verification

```runa
Note: Verify zero-knowledge proof transcript
Process called "verify_zkp_transcript" that takes proof as ZeroKnowledgeProof, transcript as Dictionary[String, String] returns Boolean:
    Match proof.proof_system:
        Case "schnorr_interactive":
            Note: Verify Schnorr proof: g^response = commitment * public_value^challenge
            Let generator be transcript["generator"]
            Let public_value be transcript["public_value"]
            Let modulus be transcript["modulus"]
            Let commitment be transcript["commitment"]
            Let challenge be transcript["challenge"]
            Let response be transcript["response"]
            
            Let left_side be Protocols.modular_exponentiation(generator, response, modulus)
            
            Let public_to_challenge be Protocols.modular_exponentiation(public_value, challenge, modulus)
            Let right_side be Protocols.modular_multiply(commitment, public_to_challenge, modulus)
            
            Return Protocols.big_integer_equal(left_side, right_side)
            
        Case "schnorr_non_interactive":
            Note: Recompute challenge and verify
            Let challenge_input be transcript["commitment"] + "|" + 
                                   transcript["generator"] + "|" + 
                                   transcript["public_value"] + "|" + 
                                   transcript["modulus"]
            
            Let expected_challenge be Protocols.fiat_shamir_challenge(challenge_input, transcript["hash_function"])
            
            If transcript["challenge"] != expected_challenge:
                Return false
            
            Note: Then verify as interactive proof
            Return Protocols.verify_schnorr_interactive_part(transcript)
            
        Otherwise:
            Return false  Note: Unsupported proof system
```

## Related Documentation

- **[Hash Theory](hash_theory.md)** - Hash functions in cryptographic protocols
- **[Prime Generation](prime_gen.md)** - Prime generation for protocol parameters
- **[Finite Fields](finite_fields.md)** - Finite field arithmetic in protocols
- **[Elliptic Curves](elliptic_curves.md)** - Elliptic curve-based protocols
- **[Lattice](lattice.md)** - Lattice-based protocol constructions