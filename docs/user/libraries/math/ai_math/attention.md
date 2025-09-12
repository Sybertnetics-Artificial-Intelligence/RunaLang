# Attention Mechanisms and Transformer Operations

The Attention Mechanisms module (`math/ai_math/attention`) implements comprehensive attention mechanisms including self-attention, multi-head attention, scaled dot-product attention, and transformer architectures. Based on "Attention Is All You Need" and subsequent improvements, this module provides the mathematical foundations for modern natural language processing and sequence modeling.

## Overview

This module implements state-of-the-art attention mechanisms used in modern deep learning:

- **Self-Attention**: Query, key, and value from the same sequence
- **Multi-Head Attention**: Parallel attention mechanisms with different learned projections
- **Cross-Attention**: Attention between different sequences (encoder-decoder)
- **Positional Encoding**: Sinusoidal and learnable position embeddings
- **Transformer Blocks**: Complete transformer encoder/decoder implementations
- **Attention Variants**: Sparse attention, local attention, relative position attention

## Key Features

### Efficient Implementations
- **Batch Processing**: Optimized for batch computation
- **Memory Efficient**: Reduced memory usage for long sequences
- **Numerical Stability**: Stable softmax computation and gradient flow

### Flexible Architecture
- **Configurable Heads**: Variable number of attention heads
- **Multiple Attention Types**: Self, cross, and causal attention
- **Position Encodings**: Sinusoidal, learned, and relative encodings

### Advanced Features
- **Attention Visualization**: Built-in attention pattern analysis
- **Gradient Checkpointing**: Memory-efficient training for large models
- **Layer Normalization**: Pre-norm and post-norm configurations

## Core Types

### Attention Configuration
```runa
Type called "AttentionConfig":
    d_model as Integer                  Note: Model dimensionality
    num_heads as Integer               Note: Number of attention heads
    d_k as Integer                     Note: Key dimension (d_model / num_heads)
    d_v as Integer                     Note: Value dimension
    dropout as Float                   Note: Attention dropout probability
    temperature as Float               Note: Scaling temperature
    causal as Boolean                  Note: Whether to apply causal masking

Type called "AttentionWeights":
    query_weights as Matrix[Float]     Note: W_Q projection matrix
    key_weights as Matrix[Float]       Note: W_K projection matrix
    value_weights as Matrix[Float]     Note: W_V projection matrix
    output_weights as Matrix[Float]    Note: W_O output projection
```

### Positional Encoding Types
```runa
Type called "PositionalEncoding":
    encoding_type as String           Note: sinusoidal, learned, relative
    max_sequence_length as Integer
    d_model as Integer
    encoding_matrix as Matrix[Float]
    dropout as Float

Type called "RelativePositionEncoding":
    max_relative_distance as Integer
    num_buckets as Integer
    bidirectional as Boolean
    embeddings as Matrix[Float]
```

## Scaled Dot-Product Attention

### Basic Attention Mechanism
```runa
Import "math/ai_math/attention" as Attention

Note: Scaled dot-product attention implementation
Let query_matrix be LinAlg.create_matrix([
    ["0.1", "0.5", "0.3"],    Note: Query vectors for each position
    ["0.2", "0.4", "0.6"],
    ["0.3", "0.2", "0.8"]
], "float")

Let key_matrix be LinAlg.create_matrix([
    ["0.4", "0.1", "0.2"],    Note: Key vectors for each position  
    ["0.3", "0.6", "0.1"],
    ["0.2", "0.3", "0.7"]
], "float")

Let value_matrix be LinAlg.create_matrix([
    ["1.0", "0.5", "0.2"],    Note: Value vectors for each position
    ["0.8", "0.6", "0.4"], 
    ["0.3", "0.9", "0.7"]
], "float")

Let attention_config be AttentionConfig with:
    d_model: 3
    num_heads: 1
    d_k: 3
    d_v: 3
    dropout: 0.0
    temperature: 1.0
    causal: false

Let attention_output be Attention.scaled_dot_product_attention(
    query_matrix, 
    key_matrix, 
    value_matrix, 
    attention_config
)

Display "Attention output computed with shape: " joined with String(attention_output.attention_values.rows) joined with "x" joined with String(attention_output.attention_values.columns)
```

**Mathematical Formula**: Attention(Q,K,V) = softmax(QK^T/√d_k)V

**Properties**:
- Captures relationships between all sequence positions
- Scaling by √d_k prevents softmax saturation
- Permutation invariant (except for positional encoding)

### Attention with Masking
```runa
Note: Causal (autoregressive) attention masking
Let causal_mask be AttentionMask with:
    mask_type: "causal"
    mask_values: create_causal_mask(sequence_length: 3)
    padding_value: -1e9

Let masked_attention be Attention.masked_scaled_attention(
    query_matrix,
    key_matrix,
    value_matrix,
    causal_mask,
    attention_config
)

Display "Masked attention computed"
```

**Causal Mask**: Prevents attention to future positions in autoregressive generation

### Temperature-Scaled Attention
```runa
Note: Temperature scaling for attention sharpness control
Let temp_config be AttentionConfig with:
    d_model: 3
    num_heads: 1
    d_k: 3
    d_v: 3
    dropout: 0.0
    temperature: 0.5      Note: Lower temperature = sharper attention
    causal: false

Let sharp_attention be Attention.scaled_dot_product_attention(
    query_matrix,
    key_matrix, 
    value_matrix,
    temp_config
)

Display "Temperature-scaled attention computed"
```

## Multi-Head Attention

### Multi-Head Self-Attention
```runa
Note: Multi-head attention for richer representations
Let mha_config be AttentionConfig with:
    d_model: 512
    num_heads: 8          Note: Typical number for transformers
    d_k: 64              Note: d_model / num_heads
    d_v: 64
    dropout: 0.1
    temperature: 1.0
    causal: false

Let mha_weights be AttentionWeights with:
    query_weights: xavier_init(512, 512)
    key_weights: xavier_init(512, 512)
    value_weights: xavier_init(512, 512)
    output_weights: xavier_init(512, 512)

Let input_sequence be create_random_matrix(10, 512)  Note: [seq_len, d_model]

Let mha_output be Attention.multi_head_attention(
    input_sequence,   Note: Self-attention: Q=K=V
    input_sequence,
    input_sequence,
    mha_weights,
    mha_config
)

Display "Multi-head attention output shape: " joined with String(mha_output.output.shape)
Display "Attention weights shape: " joined with String(mha_output.attention_weights.shape)
```

**Mathematical Formula**: MultiHead(Q,K,V) = Concat(head_1,...,head_h)W^O

Where head_i = Attention(QW_i^Q, KW_i^K, VW_i^V)

**Benefits**:
- Multiple representation subspaces
- Capture different types of relationships
- Improved model expressiveness

### Cross-Attention (Encoder-Decoder)
```runa
Note: Cross-attention between encoder and decoder
Let encoder_output be create_random_matrix(15, 512)  Note: Encoder sequence
Let decoder_input be create_random_matrix(10, 512)   Note: Decoder sequence

Let cross_attention_output be Attention.multi_head_attention(
    decoder_input,    Note: Queries from decoder
    encoder_output,   Note: Keys from encoder
    encoder_output,   Note: Values from encoder
    mha_weights,
    mha_config
)

Display "Cross-attention computed between encoder and decoder"
```

**Use Cases**:
- Machine translation
- Text summarization  
- Image captioning
- Any encoder-decoder architecture

### Attention Head Analysis
```runa
Note: Analyze individual attention heads
Let head_analysis be Attention.analyze_attention_heads(mha_output.attention_weights, mha_config)

For Each head_id, analysis in head_analysis.head_statistics:
    Display "Head " joined with String(head_id) joined with " focuses on: " joined with analysis.attention_pattern
    Display "  Average attention entropy: " joined with String(analysis.entropy)
    Display "  Max attention weight: " joined with String(analysis.max_weight)
```

## Positional Encoding

### Sinusoidal Positional Encoding
```runa
Note: Sinusoidal position embeddings
Let pos_encoding_config be PositionalEncoding with:
    encoding_type: "sinusoidal"
    max_sequence_length: 1000
    d_model: 512
    dropout: 0.1

Let pos_encodings be Attention.create_positional_encoding(pos_encoding_config)

Note: Add positional encoding to input embeddings
Let input_with_pos be Attention.add_positional_encoding(input_sequence, pos_encodings)

Display "Added sinusoidal positional encoding"
```

**Mathematical Formulas**:
- PE(pos, 2i) = sin(pos / 10000^(2i/d_model))
- PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))

**Properties**:
- No learnable parameters
- Allows extrapolation to longer sequences
- Captures relative position information

### Learned Positional Encoding
```runa
Note: Learnable position embeddings
Let learned_pos_config be PositionalEncoding with:
    encoding_type: "learned"
    max_sequence_length: 512
    d_model: 512
    dropout: 0.1

Let learned_positions be Attention.create_positional_encoding(learned_pos_config)
Display "Created learnable positional embeddings"
```

**Benefits**:
- Can adapt to specific tasks
- May learn better patterns for specific domains
- Limited to maximum training sequence length

### Relative Positional Encoding
```runa
Note: Relative position attention (T5-style)
Let relative_config be RelativePositionEncoding with:
    max_relative_distance: 128
    num_buckets: 32
    bidirectional: true
    embeddings: xavier_init(32, 64)

Let relative_attention be Attention.relative_position_attention(
    query_matrix,
    key_matrix,
    value_matrix,
    relative_config
)

Display "Relative positional attention computed"
```

**Benefits**:
- Better length generalization
- Focuses on relative rather than absolute positions
- Used in T5, DeBERTa, and other models

## Transformer Blocks

### Transformer Encoder Layer
```runa
Note: Complete transformer encoder layer
Let encoder_config be TransformerBlock with:
    self_attention: mha_config
    feed_forward: FeedForwardNetwork with:
        d_model: 512
        d_ff: 2048         Note: Typically 4x d_model
        activation: "relu"
        dropout: 0.1
    layer_norm_1: LayerNorm with:
        normalized_shape: [512]
        epsilon: 1e-6
        elementwise_affine: true
    layer_norm_2: LayerNorm with:
        normalized_shape: [512] 
        epsilon: 1e-6
        elementwise_affine: true
    residual_connection: true
    dropout: 0.1

Let encoder_output be Attention.transformer_encoder_layer(input_sequence, encoder_config)
Display "Transformer encoder layer output computed"
```

**Architecture**:
1. Multi-head self-attention
2. Add & Norm (residual connection + layer normalization)
3. Feed-forward network
4. Add & Norm

### Transformer Decoder Layer
```runa
Note: Transformer decoder layer with cross-attention
Let decoder_config be TransformerBlock with:
    self_attention: causal_mha_config     Note: Causal self-attention
    cross_attention: cross_mha_config     Note: Cross-attention to encoder
    feed_forward: feed_forward_config
    layer_norm_1: layer_norm_config
    layer_norm_2: layer_norm_config
    layer_norm_3: layer_norm_config       Note: Additional layer norm for cross-attention
    residual_connection: true
    dropout: 0.1

Let decoder_output be Attention.transformer_decoder_layer(
    decoder_input,
    encoder_output,
    decoder_config
)

Display "Transformer decoder layer output computed"
```

**Architecture**:
1. Causal multi-head self-attention
2. Add & Norm
3. Multi-head cross-attention (to encoder)
4. Add & Norm  
5. Feed-forward network
6. Add & Norm

### Stacked Transformer
```runa
Note: Multiple transformer layers
Let num_layers be 6
Let transformer_stack be Attention.create_transformer_stack(encoder_config, num_layers)

Let final_output be input_sequence
Let layer_idx be 0
While layer_idx < num_layers:
    Set final_output to Attention.transformer_encoder_layer(final_output, encoder_config)
    Set layer_idx to layer_idx + 1

Display "Processed through " joined with String(num_layers) joined with " transformer layers"
```

## Advanced Attention Variants

### Sparse Attention
```runa
Note: Sparse attention for long sequences
Let sparse_config be SparseAttentionConfig with:
    attention_pattern: "local_window"     Note: local_window, strided, or custom
    window_size: 64                       Note: Local attention window
    stride: 32                           Note: Stride for strided attention
    sparsity_ratio: 0.1                  Note: Fraction of connections to keep

Let sparse_attention be Attention.sparse_attention(
    query_matrix,
    key_matrix,
    value_matrix,
    sparse_config
)

Display "Sparse attention computed with reduced complexity"
```

**Benefits**:
- Linear complexity instead of quadratic
- Handles very long sequences
- Maintains most important attention connections

### Local Attention
```runa
Note: Local attention with fixed window
Let local_config be LocalAttentionConfig with:
    window_size: 128                     Note: Attention window size
    stride: 64                          Note: Window stride
    causal: true                        Note: Causal masking within windows

Let local_attention be Attention.local_attention(
    query_matrix,
    key_matrix, 
    value_matrix,
    local_config
)

Display "Local attention with window size " joined with String(local_config.window_size)
```

### Flash Attention (Memory Efficient)
```runa
Note: Memory-efficient attention computation
Let flash_config be FlashAttentionConfig with:
    block_size: 128                     Note: Block size for tiling
    causal: false
    dropout: 0.1

Let flash_output be Attention.flash_attention(
    query_matrix,
    key_matrix,
    value_matrix,
    flash_config
)

Display "Flash attention computed with reduced memory usage"
```

**Benefits**:
- Significantly reduced memory usage
- Same computational complexity
- Enables training larger models

## Attention Analysis and Visualization

### Attention Pattern Analysis
```runa
Note: Analyze attention patterns
Let attention_analysis be Attention.analyze_attention_patterns(
    mha_output.attention_weights,
    input_tokens,
    analysis_config
)

Display "Attention Analysis Results:"
Display "  Entropy: " joined with String(attention_analysis.entropy)
Display "  Sparsity: " joined with String(attention_analysis.sparsity)
Display "  Head diversity: " joined with String(attention_analysis.head_diversity)

For Each pattern in attention_analysis.dominant_patterns:
    Display "  Pattern: " joined with pattern.pattern_type joined with " (strength: " joined with String(pattern.strength) joined with ")"
```

### Attention Visualization
```runa
Note: Generate attention visualization data
Let viz_config be AttentionVisualizationConfig with:
    head_id: 0                          Note: Which attention head to visualize
    layer_id: 3                         Note: Which layer to visualize
    token_labels: ["The", "cat", "sat", "on", "the", "mat"]
    normalization: "row"                Note: Row or column normalization

Let attention_viz be Attention.create_attention_visualization(
    mha_output.attention_weights,
    viz_config
)

Display "Attention visualization created for head " joined with String(viz_config.head_id)
```

### Head Importance Analysis
```runa
Note: Measure importance of different attention heads
Let importance_analysis be Attention.compute_head_importance(
    model_outputs,
    attention_weights,
    targets,
    importance_config
)

Display "Head Importance Ranking:"
For Each head_info in importance_analysis.ranked_heads:
    Display "  Head " joined with String(head_info.layer) joined with "-" joined with String(head_info.head) joined with ": " joined with String(head_info.importance_score)
```

## Training and Optimization

### Attention Dropout
```runa
Note: Apply dropout to attention weights
Let dropout_config be AttentionDropoutConfig with:
    attention_dropout: 0.1              Note: Dropout on attention weights
    output_dropout: 0.1                 Note: Dropout on output
    training_mode: true

Let attention_with_dropout be Attention.attention_with_dropout(
    attention_output,
    dropout_config
)

Display "Applied dropout to attention computation"
```

### Gradient Accumulation for Large Models
```runa
Note: Gradient accumulation for memory efficiency
Let accumulation_config be GradientAccumulationConfig with:
    accumulation_steps: 4               Note: Accumulate over 4 micro-batches
    clip_grad_norm: 5.0                Note: Gradient clipping threshold

Let accumulated_grads be Attention.compute_accumulated_attention_gradients(
    micro_batches,
    model_parameters,
    accumulation_config
)

Display "Accumulated gradients over " joined with String(accumulation_config.accumulation_steps) joined with " steps"
```

### Mixed Precision Training
```runa
Note: Mixed precision for attention computation
Let precision_config be MixedPrecisionConfig with:
    use_fp16: true                      Note: Use half precision
    loss_scale: 1024.0                  Note: Loss scaling factor
    max_loss_scale: 65536.0
    loss_scale_window: 2000

Let fp16_attention be Attention.mixed_precision_attention(
    query_matrix,
    key_matrix,
    value_matrix,
    attention_config,
    precision_config
)

Display "Mixed precision attention computed"
```

## Performance Optimization

### Batch Attention Computation
```runa
Note: Efficient batch processing
Let batched_queries be create_batched_tensor([batch_size, seq_len, d_model])
Let batched_keys be create_batched_tensor([batch_size, seq_len, d_model])  
Let batched_values be create_batched_tensor([batch_size, seq_len, d_model])

Let batch_config be BatchAttentionConfig with:
    batch_size: 32
    max_seq_len: 512
    padding_token: 0                    Note: Token ID for padding
    attention_mask: create_padding_mask(batched_queries)

Let batch_attention_output be Attention.batch_attention(
    batched_queries,
    batched_keys,
    batched_values,
    batch_config
)

Display "Batch attention computed for " joined with String(batch_config.batch_size) joined with " sequences"
```

### Attention Caching for Inference
```runa
Note: Key-value caching for autoregressive generation
Let kv_cache be Attention.initialize_kv_cache(
    max_batch_size: 1,
    max_seq_len: 1024,
    num_heads: 8,
    head_dim: 64
)

Let generation_step be 0
While generation_step < max_generation_length:
    Let current_token_embedding be get_next_token_embedding(generation_step)
    
    Let cached_output be Attention.attention_with_kv_cache(
        current_token_embedding,
        kv_cache,
        generation_step,
        attention_config
    )
    
    Note: Update cache for next step
    Set kv_cache to cached_output.updated_cache
    
    Set generation_step to generation_step + 1

Display "Generated sequence using KV cache"
```

**Benefits**:
- Avoids recomputing keys/values for previous tokens
- Significant speedup for autoregressive generation
- Reduced memory bandwidth requirements

## Common Patterns and Use Cases

### BERT-style Bidirectional Attention
```runa
Note: Bidirectional attention for BERT-like models
Let bert_config be AttentionConfig with:
    d_model: 768
    num_heads: 12
    d_k: 64
    d_v: 64
    dropout: 0.1
    temperature: 1.0
    causal: false                       Note: Bidirectional attention

Let bert_attention be Attention.multi_head_attention(
    input_embeddings,
    input_embeddings, 
    input_embeddings,
    bert_weights,
    bert_config
)

Display "BERT-style bidirectional attention computed"
```

### GPT-style Causal Attention
```runa
Note: Causal attention for autoregressive models  
Let gpt_config be AttentionConfig with:
    d_model: 1024
    num_heads: 16
    d_k: 64
    d_v: 64
    dropout: 0.1
    temperature: 1.0
    causal: true                        Note: Causal masking for autoregression

Let causal_mask be create_causal_mask(sequence_length)
Let gpt_attention be Attention.causal_multi_head_attention(
    input_embeddings,
    gpt_weights,
    gpt_config,
    causal_mask
)

Display "GPT-style causal attention computed"
```

### T5-style Encoder-Decoder
```runa
Note: T5-style relative position attention
Let t5_encoder_config be AttentionConfig with:
    d_model: 512
    num_heads: 8
    d_k: 64
    d_v: 64
    dropout: 0.1
    temperature: 1.0
    causal: false

Let t5_decoder_config be AttentionConfig with:
    d_model: 512
    num_heads: 8
    d_k: 64
    d_v: 64
    dropout: 0.1
    temperature: 1.0
    causal: true

Let t5_output be Attention.t5_encoder_decoder_attention(
    encoder_input,
    decoder_input,
    t5_encoder_config,
    t5_decoder_config,
    relative_position_config
)

Display "T5-style encoder-decoder attention computed"
```

## Testing and Validation

### Attention Mechanism Tests
```runa
Note: Test attention properties
Process called "test_attention_properties":
    Let identity_query be create_identity_matrix(4)
    Let identity_key be create_identity_matrix(4)
    Let identity_value be create_identity_matrix(4)
    
    Let identity_attention be Attention.scaled_dot_product_attention(
        identity_query,
        identity_key, 
        identity_value,
        basic_attention_config
    )
    
    Note: For identity matrices, attention should approximate identity
    Let attention_weights be identity_attention.attention_weights
    
    Note: Check that diagonal elements are highest
    Let i be 0
    While i < attention_weights.rows:
        Let diagonal_val be attention_weights.entries.get(i).get(i)
        Let max_off_diagonal be find_max_off_diagonal(attention_weights, i)
        Assert diagonal_val > max_off_diagonal
        Set i to i + 1
    
    Display "Attention mechanism tests passed"
```

### Gradient Flow Verification
```runa
Note: Verify gradients flow properly through attention
Process called "test_attention_gradients":
    Let test_query be create_random_matrix(5, 8)
    Let test_key be create_random_matrix(5, 8)
    Let test_value be create_random_matrix(5, 8)
    
    Let attention_output be Attention.scaled_dot_product_attention(
        test_query,
        test_key,
        test_value,
        test_attention_config
    )
    
    Note: Compute gradients
    Let gradients be compute_attention_gradients(attention_output)
    
    Note: Check gradient magnitudes
    Let q_grad_norm be compute_norm(gradients.query_gradients)
    Let k_grad_norm be compute_norm(gradients.key_gradients)  
    Let v_grad_norm be compute_norm(gradients.value_gradients)
    
    Assert q_grad_norm > 1e-8
    Assert k_grad_norm > 1e-8
    Assert v_grad_norm > 1e-8
    
    Display "Attention gradient flow verified"
```

## Troubleshooting Common Issues

### Attention Collapse
```runa
Note: Detect and handle attention collapse
Process called "detect_attention_collapse" that takes attention_weights as Matrix[Float] returns Boolean:
    Let max_attention be find_maximum_attention(attention_weights)
    Let attention_entropy be compute_attention_entropy(attention_weights)
    
    If max_attention > 0.95 or attention_entropy < 0.1:
        Display "Warning: Attention collapse detected"
        Display "Consider: lower temperature, attention dropout, label smoothing"
        Return true
    
    Return false
```

### Memory Issues with Long Sequences
```runa
Note: Handle memory issues with long sequences
Process called "handle_long_sequence_attention" that takes sequence_length as Integer:
    If sequence_length > 1024:
        Display "Using sparse attention for sequence length " joined with String(sequence_length)
        Return "sparse"
    Otherwise if sequence_length > 512:
        Display "Using gradient checkpointing for sequence length " joined with String(sequence_length)
        Return "checkpoint"
    Otherwise:
        Return "standard"
```

### Numerical Instability in Softmax
```runa
Note: Handle numerical issues in attention softmax
Process called "stable_attention_softmax" that takes logits as Matrix[Float] returns Matrix[Float]:
    Note: Apply temperature and clipping for stability
    Let clipped_logits be clip_logits(logits, min_val: -50.0, max_val: 50.0)
    Let stable_softmax be compute_stable_softmax(clipped_logits)
    
    Return stable_softmax
```

## Related Documentation

- **[AI Math Neural Ops](neural_ops.md)**: Neural network operations and activations
- **[AI Math Loss Functions](loss_functions.md)**: Loss functions for transformer training
- **[AI Math Optimization](optimization.md)**: Optimization techniques for attention models
- **[Math Engine Linear Algebra](../engine/linalg/core.md)**: Matrix operations underlying attention
- **[Math Core Operations](../core/operations.md)**: Basic mathematical operations

The Attention Mechanisms module provides the mathematical foundations for modern transformer architectures, enabling state-of-the-art performance in natural language processing, computer vision, and other sequence modeling tasks.