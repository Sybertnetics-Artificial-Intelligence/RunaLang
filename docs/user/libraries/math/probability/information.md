# Information Theory - Runa Standard Library

The `math/probability/information` module provides comprehensive support for information theory, coding theory, and statistical information measures. This module enables analysis of information content, communication systems, and data compression algorithms.

## Overview

Information theory quantifies the amount of information in data and the fundamental limits of data compression and communication. This module provides tools for:

- **Entropy measures** including Shannon entropy, conditional entropy, and cross-entropy
- **Mutual information** and conditional mutual information for dependency analysis
- **Divergence measures** including KL-divergence, JS-divergence, and f-divergences
- **Channel coding** with capacity calculations and error correction
- **Data compression** algorithms and theoretical limits
- **Information geometry** and statistical manifolds

## Key Features

### Entropy and Information Content
- Shannon entropy for discrete and continuous distributions
- Conditional and joint entropy calculations
- Differential entropy for continuous random variables
- Rényi entropy and generalized entropy measures

### Mutual Information Analysis
- Mutual information between random variables
- Conditional mutual information for multivariate analysis
- Transfer entropy for causal information flow
- Integrated information for complex systems

### Divergence and Distance Measures  
- Kullback-Leibler divergence and Jensen-Shannon divergence
- Wasserstein distance and optimal transport
- f-divergences and φ-divergences
- Information-theoretic clustering and classification

### Coding and Communication
- Source coding with Huffman and arithmetic codes
- Channel capacity for various noise models
- Error-correcting codes and decoding algorithms
- Rate-distortion theory and lossy compression

## Quick Start

```runa
Use math/probability/information

Note: Analyze information content of a text
Let text_data be "the quick brown fox jumps over the lazy dog"
Let char_frequencies be frequency_analysis(text_data)

Note: Compute Shannon entropy
Let text_entropy be shannon_entropy(char_frequencies)
Print("Text entropy: {text_entropy:.4f} bits per character")

Note: Optimal encoding length
Let optimal_length be text_entropy * text_data.length
Print("Minimum encoding length: {optimal_length:.2f} bits")

Note: Compare with uniform distribution
Let uniform_entropy be Real::log2(26.0)  Note: 26 letters
Print("Uniform entropy: {uniform_entropy:.4f} bits per character")
Print("Compression ratio: {text_entropy / uniform_entropy:.4f}")

Note: Build Huffman code
Let huffman_code be HuffmanCoder::build(char_frequencies)
Let encoded_text be huffman_code.encode(text_data)
Print("Huffman encoded length: {encoded_text.length} bits")
Print("Actual compression: {encoded_text.length / (text_data.length * 8.0):.4f}")
```

## Entropy Calculations

### Shannon Entropy

```runa
Note: Discrete Shannon entropy
Process shannon_entropy(probabilities as List[Real]) returns Real:
    Let entropy be 0.0
    For Each p In probabilities:
        If p > 0.0:
            entropy -= p * Real::log2(p)
    Return entropy

Note: Entropy of a die roll
Let fair_die be [1.0/6.0; 6]  Note: Fair six-sided die
Let loaded_die be [0.1, 0.1, 0.1, 0.1, 0.1, 0.5]  Note: Loaded die

Print("Fair die entropy: {shannon_entropy(fair_die):.4f} bits")
Print("Loaded die entropy: {shannon_entropy(loaded_die):.4f} bits")

Note: Maximum entropy is achieved by uniform distribution
Let max_entropy be Real::log2(6.0)
Print("Maximum possible entropy: {max_entropy:.4f} bits")
```

### Conditional Entropy

```runa
Note: Weather prediction example
Let weather_states be ["Sunny", "Rainy", "Cloudy"]
Let tomorrow_given_today be Matrix([
    [0.7, 0.2, 0.1],  Note: Tomorrow given Sunny today
    [0.3, 0.4, 0.3],  Note: Tomorrow given Rainy today
    [0.4, 0.3, 0.3]   Note: Tomorrow given Cloudy today
])

Let today_distribution be [0.5, 0.3, 0.2]  Note: Prior for today's weather

Note: Compute conditional entropy H(Tomorrow|Today)
Let conditional_entropy be conditional_shannon_entropy(tomorrow_given_today, today_distribution)
Print("Conditional entropy H(Tomorrow|Today): {conditional_entropy:.4f} bits")

Note: Compute joint and marginal entropies
Let joint_distribution be compute_joint_distribution(today_distribution, tomorrow_given_today)
Let joint_entropy be shannon_entropy(joint_distribution.flatten())
let tomorrow_distribution be compute_marginal_distribution(joint_distribution, axis: 1)
Let tomorrow_entropy be shannon_entropy(tomorrow_distribution)

Print("Joint entropy H(Today,Tomorrow): {joint_entropy:.4f} bits")
Print("Tomorrow entropy H(Tomorrow): {tomorrow_entropy:.4f} bits")
Print("Mutual information I(Today;Tomorrow): {tomorrow_entropy - conditional_entropy:.4f} bits")
```

### Differential Entropy

```runa
Note: Continuous distributions
Let normal_dist be Normal::new(mean: 0.0, std_dev: 1.0)
Let uniform_dist be Uniform::new(lower: -Real::sqrt(3.0), upper: Real::sqrt(3.0))  Note: Same variance

Note: Differential entropy (in nats, using natural log)
Let normal_diff_entropy be differential_entropy(normal_dist)
Let uniform_diff_entropy be differential_entropy(uniform_dist)

Print("Normal differential entropy: {normal_diff_entropy:.4f} nats")
Print("Uniform differential entropy: {uniform_diff_entropy:.4f} nats")

Note: Convert to bits
Print("Normal differential entropy: {normal_diff_entropy / Real::ln(2.0):.4f} bits")
Print("Uniform differential entropy: {uniform_diff_entropy / Real::ln(2.0):.4f} bits")

Note: Maximum entropy principle
Print("Normal has maximum entropy among distributions with fixed variance")
```

## Mutual Information and Dependencies

### Bivariate Mutual Information

```runa
Note: Gene expression correlation analysis
Let gene_a_levels be [1.2, 2.1, 0.8, 3.2, 1.5, 2.8, 0.9, 2.3]
Let gene_b_levels be [2.1, 3.8, 1.2, 5.1, 2.3, 4.2, 1.4, 3.9]

Note: Discretize continuous data for MI calculation
Let discretizer be EqualWidthDiscretizer::new(bins: 4)
Let gene_a_discrete be discretizer.fit_transform(gene_a_levels)
Let gene_b_discrete be discretizer.fit_transform(gene_b_levels)

Note: Compute mutual information
Let joint_counts be contingency_table(gene_a_discrete, gene_b_discrete)
Let mutual_info be mutual_information_from_counts(joint_counts)

Print("Mutual information between genes: {mutual_info:.4f} bits")

Note: Normalized mutual information (0 to 1 scale)
Let gene_a_entropy be shannon_entropy_from_counts(gene_a_discrete.value_counts())
Let gene_b_entropy be shannon_entropy_from_counts(gene_b_discrete.value_counts())
Let normalized_mi be mutual_info / Real::sqrt(gene_a_entropy * gene_b_entropy)

Print("Normalized mutual information: {normalized_mi:.4f}")
```

### Conditional Mutual Information

```runa
Note: Three-way interaction analysis
Let X be [0, 1, 0, 1, 0, 1, 0, 1]  Note: Binary variable X
Let Y be [0, 0, 1, 1, 0, 0, 1, 1]  Note: Binary variable Y  
Let Z be [0, 1, 1, 0, 1, 0, 0, 1]  Note: Confounding variable Z

Note: Compute I(X;Y|Z) - mutual information between X and Y given Z
Let conditional_mi be conditional_mutual_information(X, Y, Z)
Print("Conditional mutual information I(X;Y|Z): {conditional_mi:.4f} bits")

Note: Compare with unconditional mutual information
Let unconditional_mi be mutual_information(X, Y)
Print("Unconditional mutual information I(X;Y): {unconditional_mi:.4f} bits")

Note: Information decomposition
Let redundancy be min(mutual_information(X, Z), mutual_information(Y, Z))
Let unique_x be mutual_information(X, Y) - conditional_mi - redundancy
Let unique_y be mutual_information(Y, Z) - conditional_mi - redundancy
Let synergy be conditional_mi

Print("Redundant information: {redundancy:.4f} bits")
Print("Unique to X: {unique_x:.4f} bits")
Print("Unique to Y: {unique_y:.4f} bits")
Print("Synergistic information: {synergy:.4f} bits")
```

### Transfer Entropy

```runa
Note: Causal information flow between time series
Let time_series_x be generate_ar_process(length: 100, coefficients: [0.7])
Let time_series_y be generate_coupled_process(time_series_x, coupling: 0.3, noise: 0.2)

Note: Compute transfer entropy from X to Y
Let embedding_dim be 2
Let prediction_horizon be 1
Let transfer_entropy_x_to_y be transfer_entropy(
    source: time_series_x,
    target: time_series_y, 
    embedding_dimension: embedding_dim,
    prediction_horizon: prediction_horizon
)

Note: Compute transfer entropy from Y to X
Let transfer_entropy_y_to_x be transfer_entropy(
    source: time_series_y,
    target: time_series_x,
    embedding_dimension: embedding_dim,
    prediction_horizon: prediction_horizon  
)

Print("Transfer entropy X → Y: {transfer_entropy_x_to_y:.4f} bits")
Print("Transfer entropy Y → X: {transfer_entropy_y_to_x:.4f} bits")

Note: Net information flow
Let net_flow be transfer_entropy_x_to_y - transfer_entropy_y_to_x
Print("Net information flow (X → Y): {net_flow:.4f} bits")
```

## Divergence Measures

### Kullback-Leibler Divergence

```runa
Note: Compare probability distributions
Let p_distribution be [0.5, 0.3, 0.2]  Note: True distribution
Let q_distribution be [0.4, 0.4, 0.2]  Note: Approximate distribution

Let kl_divergence_pq be kullback_leibler_divergence(p_distribution, q_distribution)
Let kl_divergence_qp be kullback_leibler_divergence(q_distribution, p_distribution)

Print("KL(P||Q): {kl_divergence_pq:.4f} bits")
Print("KL(Q||P): {kl_divergence_qp:.4f} bits")

Note: KL divergence is not symmetric
Print("Asymmetry: |KL(P||Q) - KL(Q||P)| = {Real::abs(kl_divergence_pq - kl_divergence_qp):.4f}")

Note: Jensen-Shannon divergence (symmetric)
Let js_divergence be jensen_shannon_divergence(p_distribution, q_distribution)
Print("Jensen-Shannon divergence: {js_divergence:.4f} bits")

Note: Relationship to mutual information
Let mixture be [(p_distribution[i] + q_distribution[i]) / 2.0 For i In Range(3)]
Let expected_kl be 0.5 * kl_divergence_pq + 0.5 * kl_divergence_qp
Print("JS divergence as expected KL: {js_divergence:.4f} ≈ {expected_kl:.4f}")
```

### f-Divergences

```runa
Note: General f-divergence framework
Process f_divergence(p as List[Real], q as List[Real], f_function as Function) returns Real:
    Let divergence be 0.0
    For i In Range(p.length):
        If q[i] > 0.0:
            Let ratio be p[i] / q[i]
            divergence += q[i] * f_function(ratio)
    Return divergence

Note: Define different f-functions
Let kl_f_function be |t| t * Real::ln(t) - t + 1.0
Let chi_squared_f_function be |t| (t - 1.0) * (t - 1.0)
Let hellinger_f_function be |t| (Real::sqrt(t) - 1.0) * (Real::sqrt(t) - 1.0)

Let test_p be [0.6, 0.3, 0.1]
Let test_q be [0.4, 0.4, 0.2]

Let kl_div be f_divergence(test_p, test_q, kl_f_function)
Let chi_squared_div be f_divergence(test_p, test_q, chi_squared_f_function)
Let hellinger_div be f_divergence(test_p, test_q, hellinger_f_function)

Print("KL f-divergence: {kl_div:.4f}")
Print("Chi-squared divergence: {chi_squared_div:.4f}")
Print("Hellinger divergence: {hellinger_div:.4f}")
```

### Wasserstein Distance

```runa
Note: Optimal transport distance between distributions
Let distribution_1 be [0.3, 0.4, 0.2, 0.1]
Let distribution_2 be [0.1, 0.3, 0.4, 0.2]
Let ground_distances be Matrix([
    [0.0, 1.0, 2.0, 3.0],
    [1.0, 0.0, 1.0, 2.0],
    [2.0, 1.0, 0.0, 1.0],
    [3.0, 2.0, 1.0, 0.0]
])

Let wasserstein_dist be wasserstein_distance(distribution_1, distribution_2, ground_distances)
Print("Wasserstein distance: {wasserstein_dist:.4f}")

Note: Earth Mover's Distance for 1D case
Let samples_1 be [1.0, 2.0, 3.0, 4.0]
Let samples_2 be [1.5, 2.5, 3.5, 4.5]
Let weights_1 be [0.3, 0.4, 0.2, 0.1]
Let weights_2 be [0.1, 0.3, 0.4, 0.2]

Let emd_1d be earth_movers_distance_1d(samples_1, samples_2, weights_1, weights_2)
Print("Earth Mover's Distance (1D): {emd_1d:.4f}")
```

## Channel Coding and Communication

### Channel Capacity

```runa
Note: Binary symmetric channel
Let error_probability be 0.1
Let bsc_capacity be binary_symmetric_channel_capacity(error_probability)
Print("Binary symmetric channel capacity (p={error_probability}): {bsc_capacity:.4f} bits per use")

Note: Additive white Gaussian noise channel
Let signal_power be 1.0
Let noise_power be 0.1
Let snr_db be 10.0 * Real::log10(signal_power / noise_power)
Let awgn_capacity be awgn_channel_capacity(signal_power, noise_power)
Print("AWGN channel capacity (SNR={snr_db:.1f} dB): {awgn_capacity:.4f} bits per use")

Note: Discrete memoryless channel
Let channel_matrix be Matrix([
    [0.9, 0.05, 0.05],  Note: Input 0
    [0.1, 0.8,  0.1 ],  Note: Input 1  
    [0.05, 0.05, 0.9]   Note: Input 2
])

Let dmc_capacity be discrete_memoryless_channel_capacity(channel_matrix)
Print("DMC capacity: {dmc_capacity:.4f} bits per use")
```

### Error Correcting Codes

```runa
Note: Hamming code implementation
Let hamming_7_4 be HammingCode::new(data_bits: 4, parity_bits: 3)

Note: Encode data
Let data_word be [1, 0, 1, 1]
Let code_word be hamming_7_4.encode(data_word)
Print("Data: {data_word}")
Print("Encoded: {code_word}")

Note: Simulate channel errors
Let received_word be code_word.clone()
received_word[2] = 1 - received_word[2]  Note: Flip one bit
Print("Received (with error): {received_word}")

Note: Decode and correct
Let (decoded_data, error_position) be hamming_7_4.decode(received_word)
Print("Decoded data: {decoded_data}")
Print("Error detected at position: {error_position}")

Note: Verify correction
If decoded_data == data_word:
    Print("Error successfully corrected!")
Otherwise:
    Print("Decoding failed")
```

### Huffman Coding

```runa
Note: Optimal prefix-free coding
Let symbol_frequencies be Dictionary::new()
symbol_frequencies["A"] = 5
symbol_frequencies["B"] = 2
symbol_frequencies["C"] = 1
symbol_frequencies["D"] = 1
symbol_frequencies["E"] = 1

Let huffman_tree be HuffmanTree::build(symbol_frequencies)
Let huffman_codes be huffman_tree.generate_codes()

Print("Huffman codes:")
For Each symbol, code In huffman_codes:
    Print("  {symbol}: {code}")

Note: Compute average code length
Let total_frequency be symbol_frequencies.values().sum()
Let average_length be 0.0
For Each symbol, frequency In symbol_frequencies:
    Let probability be frequency / total_frequency
    Let code_length be huffman_codes[symbol].length
    average_length += probability * code_length

Print("Average code length: {average_length:.4f} bits per symbol")

Note: Compare with entropy
Let probabilities be [symbol_frequencies[s] / total_frequency For s In symbol_frequencies.keys()]
Let source_entropy be shannon_entropy(probabilities)
Print("Source entropy: {source_entropy:.4f} bits per symbol")
Print("Coding efficiency: {source_entropy / average_length:.4f}")
```

## Data Compression Analysis

### Lempel-Ziv Complexity

```runa
Note: Algorithmic information content approximation
Process lempel_ziv_complexity(sequence as String) returns Integer:
    Let complexity be 0
    Let i be 0
    
    While i < sequence.length:
        Let max_match_length be 0
        Let match_position be -1
        
        Note: Find longest match in previous portion
        For start In Range(i):
            Let match_length be 0
            While (start + match_length < i) And 
                  (i + match_length < sequence.length) And
                  (sequence[start + match_length] == sequence[i + match_length]):
                match_length += 1
            
            If match_length > max_match_length:
                max_match_length = match_length
                match_position = start
        
        Note: Move to next unmatched position
        i += If max_match_length > 0 Then max_match_length + 1 Else 1
        complexity += 1
    
    Return complexity

Let test_strings be [
    "0101010101",     Note: Periodic
    "0110100110010110", Note: Fibonacci-like  
    "1100100100001111", Note: Random-ish
    "0000000000"      Note: Constant
]

For Each string In test_strings:
    Let lz_complexity be lempel_ziv_complexity(string)
    Let max_complexity be string.length  Note: Upper bound
    Let relative_complexity be lz_complexity / max_complexity
    Print("String: {string}")
    Print("  LZ complexity: {lz_complexity}/{max_complexity} = {relative_complexity:.3f}")
```

### Rate-Distortion Theory

```runa
Note: Rate-distortion function for Gaussian source
Process gaussian_rate_distortion(variance as Real, distortion as Real) returns Real:
    If distortion >= variance:
        Return 0.0  Note: No coding needed
    Otherwise:
        Return 0.5 * Real::log2(variance / distortion)

Let source_variance be 1.0
Let distortions be [0.1, 0.25, 0.5, 0.75, 1.0, 2.0]

Print("Rate-Distortion function for Gaussian source (σ² = {source_variance}):")
For Each D In distortions:
    Let rate be gaussian_rate_distortion(source_variance, D)
    Print("  D = {D:.2f}: R(D) = {rate:.4f} bits per sample")
```

## Advanced Applications

### Information Bottleneck

```runa
Note: Information bottleneck method for representation learning
Type InformationBottleneckResult:
    representation_size as Integer
    mutual_info_x_t as Real
    mutual_info_t_y as Real
    beta as Real
    objective as Real

Process information_bottleneck(
    X as Matrix[Real], 
    Y as List[Integer], 
    beta as Real,
    representation_dim as Integer
) returns InformationBottleneckResult:
    
    Note: Initialize random representation
    Let encoder be NeuralNetwork::new()
        .add_layer(DenseLayer::new(X.columns, 128))
        .add_layer(ActivationLayer::relu())
        .add_layer(DenseLayer::new(128, representation_dim))
        .add_layer(ActivationLayer::sigmoid())
    
    Note: Decoder for reconstruction
    Let decoder be NeuralNetwork::new()
        .add_layer(DenseLayer::new(representation_dim, 128))
        .add_layer(ActivationLayer::relu())
        .add_layer(DenseLayer::new(128, Y.unique().length))
        .add_layer(ActivationLayer::softmax())
    
    Note: Training loop with information bottleneck objective
    For epoch In Range(1000):
        Let T be encoder.forward(X)  Note: Representation
        Let Y_pred be decoder.forward(T)
        
        Note: Estimate mutual information
        Let I_X_T be estimate_mutual_information(X, T)
        Let I_T_Y be estimate_mutual_information(T, Y_pred)
        
        Note: Information bottleneck objective
        Let objective be I_T_Y - beta * I_X_T
        Let loss be -objective + cross_entropy_loss(Y_pred, Y)
        
        encoder.backward(loss)
        decoder.backward(loss)
        
        If epoch % 100 == 0:
            Print("Epoch {epoch}: I(X;T)={I_X_T:.3f}, I(T;Y)={I_T_Y:.3f}, Obj={objective:.3f}")
    
    Return InformationBottleneckResult {
        representation_size: representation_dim,
        mutual_info_x_t: I_X_T,
        mutual_info_t_y: I_T_Y,
        beta: beta,
        objective: objective
    }
```

### Integrated Information

```runa
Note: Integrated Information Theory (IIT) analysis
Process integrated_information(network as NetworkSystem, partition as Partition) returns Real:
    Note: Compute phi (integrated information) for a partition
    Let full_system_entropy be compute_system_entropy(network)
    
    Let partition_entropy be 0.0
    For Each subset In partition.subsets:
        Let subset_network be network.extract_subset(subset)
        partition_entropy += compute_system_entropy(subset_network)
    
    Let phi be full_system_entropy - partition_entropy
    Return Real::max(0.0, phi)

Note: Example neural network analysis  
Let neural_network be NeuralNetworkSystem::new()
    .add_nodes([0, 1, 2, 3])  Note: 4 neurons
    .add_connections([
        (0, 1, strength: 0.8),
        (1, 2, strength: 0.6),
        (2, 3, strength: 0.7),
        (3, 0, strength: 0.4)  Note: Feedback loop
    ])

Note: Find minimum information partition (MIP)
Let all_partitions be generate_all_partitions(neural_network.nodes)
Let min_phi be Real::INFINITY
Let mip be None

For Each partition In all_partitions:
    Let phi be integrated_information(neural_network, partition)
    If phi < min_phi:
        min_phi = phi
        mip = Some(partition)

Print("Minimum Information Partition: {mip}")
Print("Integrated Information (Φ): {min_phi:.4f}")
```

### Network Information Theory

```runa
Note: Information flow in networks
Type NetworkInformation:
    nodes as List[Integer]
    edges as List[(Integer, Integer)]
    information_flows as Dictionary[(Integer, Integer), Real]
    centrality_measures as Dictionary[Integer, Real]

Process analyze_network_information(graph as Graph, node_activities as Dictionary[Integer, List[Real]]) returns NetworkInformation:
    Let information_flows be Dictionary::new()
    Let centrality_measures be Dictionary::new()
    
    Note: Compute pairwise transfer entropies
    For Each (source, target) In graph.edges:
        Let source_activity be node_activities[source]
        Let target_activity be node_activities[target]
        
        Let te be transfer_entropy(source_activity, target_activity, embedding_dim: 2)
        information_flows[(source, target)] = te
    
    Note: Compute information centrality for each node
    For Each node In graph.nodes:
        Let total_outflow be 0.0
        Let total_inflow be 0.0
        
        For Each (source, target, flow) In information_flows:
            If source == node:
                total_outflow += flow
            If target == node:
                total_inflow += flow
        
        centrality_measures[node] = total_outflow + total_inflow
    
    Return NetworkInformation {
        nodes: graph.nodes,
        edges: graph.edges,
        information_flows: information_flows,
        centrality_measures: centrality_measures
    }

Note: Analyze brain network
Let brain_graph be load_brain_connectome("connectome.csv")
Let fmri_data be load_fmri_timeseries("fmri_data.csv")

Let network_info be analyze_network_information(brain_graph, fmri_data)

Note: Find most central information hubs
Let sorted_centrality be network_info.centrality_measures
    .to_list()
    .sort_by(|(node, centrality)| -centrality)

Print("Top information hubs:")
For i In Range(5):
    Let (node, centrality) be sorted_centrality[i]
    Print("  Node {node}: centrality = {centrality:.4f}")
```

## Performance Optimization

### Efficient Entropy Computation

```runa
Note: Vectorized entropy calculation for large datasets
Process fast_batch_entropy(data_matrix as Matrix[Integer]) returns List[Real]:
    Note: Compute entropy for each row in parallel
    Let entropies be List::with_capacity(data_matrix.rows)
    
    Let thread_pool be ThreadPool::new(num_threads: 8)
    Let chunk_size be data_matrix.rows / 8
    
    Let futures be List::new()
    For chunk_start In Range(0, data_matrix.rows, chunk_size):
        Let chunk_end be min(chunk_start + chunk_size, data_matrix.rows)
        
        Let future be thread_pool.spawn(move || {
            Let chunk_entropies be List::new()
            For row In Range(chunk_start, chunk_end):
                Let row_data be data_matrix.row(row)
                Let frequencies be count_frequencies(row_data)
                Let probabilities be frequencies.map(|f| f / row_data.length)
                chunk_entropies.push(shannon_entropy(probabilities))
            Return chunk_entropies
        })
        
        futures.push(future)
    
    Note: Collect results
    For future In futures:
        entropies.extend(future.get())
    
    Return entropies
```

### Streaming Mutual Information

```runa
Note: Online mutual information estimation for streaming data
Type StreamingMIEstimator:
    window_size as Integer
    x_buffer as RingBuffer[Real]
    y_buffer as RingBuffer[Real]
    joint_histogram as SparseMatrix[Integer]
    marginal_x as Dictionary[Integer, Integer]
    marginal_y as Dictionary[Integer, Integer]

Process StreamingMIEstimator::update(self, x_value as Real, y_value as Real):
    Note: Discretize values
    Let x_bin be discretize(x_value, self.bins)
    Let y_bin be discretize(y_value, self.bins)
    
    Note: Remove old values if buffer is full
    If self.x_buffer.is_full():
        Let old_x_bin be discretize(self.x_buffer.front(), self.bins)
        Let old_y_bin be discretize(self.y_buffer.front(), self.bins)
        
        self.joint_histogram[(old_x_bin, old_y_bin)] -= 1
        self.marginal_x[old_x_bin] -= 1
        self.marginal_y[old_y_bin] -= 1
    
    Note: Add new values
    self.x_buffer.push_back(x_value)
    self.y_buffer.push_back(y_value)
    
    self.joint_histogram[(x_bin, y_bin)] += 1
    self.marginal_x[x_bin] += 1
    self.marginal_y[y_bin] += 1

Process StreamingMIEstimator::current_mutual_information(self) returns Real:
    Let mi be 0.0
    Let total_samples be self.x_buffer.size()
    
    For Each ((x_bin, y_bin), joint_count) In self.joint_histogram:
        If joint_count > 0:
            Let p_xy be joint_count / total_samples
            Let p_x be self.marginal_x[x_bin] / total_samples
            Let p_y be self.marginal_y[y_bin] / total_samples
            
            mi += p_xy * Real::log2(p_xy / (p_x * p_y))
    
    Return mi
```

## Error Handling and Validation

### Numerical Stability

```runa
Note: Numerically stable entropy computation
Process stable_entropy(probabilities as List[Real]) returns Result[Real, String]:
    Note: Input validation
    If probabilities.is_empty():
        Return Err("Empty probability vector")
    
    Let sum_probs be probabilities.sum()
    If Real::abs(sum_probs - 1.0) > 1e-10:
        Return Err("Probabilities do not sum to 1: {sum_probs}")
    
    Let entropy be 0.0
    For Each p In probabilities:
        If p < 0.0:
            Return Err("Negative probability: {p}")
        If p > 0.0:
            Note: Use log1p for better numerical stability when p is small
            If p < 1e-10:
                entropy -= p * Real::ln(p)  Note: Direct computation for tiny values
            Otherwise:
                entropy -= p * Real::ln(p)
    
    Note: Convert to bits
    entropy /= Real::ln(2.0)
    
    If entropy < 0.0 Or entropy.is_nan():
        Return Err("Invalid entropy value: {entropy}")
    
    Return Ok(entropy)
```

### Information Measure Validation

```runa
Process validate_mutual_information(X as List[Integer], Y as List[Integer]) returns Result[Real, String]:
    If X.length != Y.length:
        Return Err("X and Y must have same length")
    
    If X.is_empty():
        Return Err("Empty data vectors")
    
    Note: Compute mutual information
    Let joint_counts be contingency_table(X, Y)
    Let mi_result be mutual_information_from_counts(joint_counts)
    
    Match mi_result:
        Ok(mi) => {
            Note: Validate MI properties
            If mi < -1e-10:  Note: Allow small numerical errors
                Return Err("Negative mutual information: {mi}")
            
            Note: MI should not exceed individual entropies
            Let h_x be shannon_entropy_from_counts(X.value_counts())
            Let h_y be shannon_entropy_from_counts(Y.value_counts())
            
            If mi > h_x + 1e-10:
                Return Err("MI exceeds H(X): {mi} > {h_x}")
            If mi > h_y + 1e-10:
                Return Err("MI exceeds H(Y): {mi} > {h_y}")
            
            Return Ok(mi)
        }
        Err(error) => Return Err(error)
```

## Best Practices

### Information-Theoretic Model Selection

```runa
Note: Use information criteria for model comparison
Process compare_models_aic(models as List[StatisticalModel], data as Dataset) returns ModelRanking:
    Let model_scores be List::new()
    
    For Each model In models:
        Let fitted_model be model.fit(data)
        Let log_likelihood be fitted_model.log_likelihood(data)
        Let num_parameters be fitted_model.parameter_count()
        
        Let aic be -2.0 * log_likelihood + 2.0 * num_parameters
        Let bic be -2.0 * log_likelihood + num_parameters * Real::ln(data.size())
        
        model_scores.push(ModelScore {
            model: model,
            aic: aic,
            bic: bic,
            log_likelihood: log_likelihood
        })
    
    Note: Sort by AIC (lower is better)
    model_scores.sort_by(|score| score.aic)
    
    Return ModelRanking {
        best_model: model_scores[0].model,
        all_scores: model_scores
    }
```

### Information-Theoretic Feature Selection

```runa
Note: Select features based on mutual information
Process mutual_information_feature_selection(
    X as Matrix[Real], 
    y as List[Integer], 
    k as Integer
) returns List[Integer]:
    
    Let feature_scores be List::new()
    
    For feature_idx In Range(X.columns):
        Let feature_data be X.column(feature_idx)
        Let mi_score be mutual_information(feature_data, y)
        feature_scores.push((feature_idx, mi_score))
    
    Note: Sort by MI score (descending)
    feature_scores.sort_by(|(idx, score)| -score)
    
    Note: Return top k feature indices
    Return feature_scores[0..k].map(|(idx, score)| idx)
```

### Memory-Efficient Information Processing

```runa
Note: Process large datasets without loading everything into memory
Process streaming_entropy_analysis(data_stream as DataStream) returns EntropyAnalysis:
    Let frequency_counter be FrequencyCounter::new()
    let total_count be 0
    
    Note: Process data in chunks
    While Let Some(chunk) be data_stream.next_chunk():
        For Each value In chunk:
            frequency_counter.increment(value)
            total_count += 1
        
        Note: Periodic memory cleanup
        If total_count % 1000000 == 0:
            frequency_counter.compact()  Note: Remove zero-count entries
            Print("Processed {total_count} samples...")
    
    Note: Compute final entropy
    Let probabilities be frequency_counter.to_probabilities()
    Let entropy be shannon_entropy(probabilities)
    
    Return EntropyAnalysis {
        entropy: entropy,
        total_samples: total_count,
        unique_values: frequency_counter.unique_count(),
        most_common: frequency_counter.most_common(10)
    }
```

The information theory module provides comprehensive tools for analyzing information content, dependencies, and communication systems. From basic entropy calculations to advanced network information analysis, it supports both theoretical investigations and practical applications in data science, machine learning, and communication engineering.