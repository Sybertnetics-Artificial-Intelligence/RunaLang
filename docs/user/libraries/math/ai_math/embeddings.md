# Embedding Operations and Representation Learning

The Embedding Operations module (`math/ai_math/embeddings`) provides comprehensive embedding operations including word embeddings (Word2Vec, GloVe, FastText), sentence embeddings, positional embeddings, and various embedding manipulation techniques. This module supports both learned and pre-trained embeddings with efficient lookup and similarity computation.

## Overview

This module implements state-of-the-art embedding techniques for representation learning:

- **Word Embeddings**: Word2Vec (Skip-gram, CBOW), GloVe, FastText
- **Sentence Embeddings**: Mean pooling, weighted pooling, transformer-based
- **Positional Embeddings**: Sinusoidal, learned, rotary position encoding
- **Similarity Operations**: Cosine similarity, dot product, Euclidean distance
- **Embedding Manipulations**: Normalization, dimensionality reduction, clustering
- **Subword Embeddings**: Character n-grams, byte-pair encoding

## Key Features

### Efficient Implementation
- **Fast Lookup**: O(1) embedding retrieval from vocabulary
- **Batch Operations**: Vectorized similarity computations
- **Memory Optimization**: Sparse gradient updates for large vocabularies

### Flexible Architecture
- **Multiple Algorithms**: Support for various embedding methods
- **Configurable Dimensions**: Adjustable embedding sizes
- **Custom Vocabularies**: User-defined word mappings

### Advanced Techniques
- **Subword Information**: Character-level representations
- **Hierarchical Softmax**: Efficient training for large vocabularies
- **Negative Sampling**: Scalable training approach

## Core Types

### Embedding Configuration
```runa
Type called "EmbeddingConfig":
    vocab_size as Integer             Note: Size of vocabulary
    embedding_dim as Integer          Note: Dimension of embedding vectors
    padding_idx as Optional[Integer]  Note: Index for padding token
    max_norm as Optional[Float]       Note: Maximum norm for renormalization
    norm_type as Float               Note: Type of norm for clipping
    scale_grad_by_freq as Boolean    Note: Scale gradients by word frequency
    sparse as Boolean                Note: Whether to use sparse gradients

Type called "EmbeddingMatrix":
    embeddings as Matrix[Float]       Note: The embedding weight matrix
    vocab as Dictionary[String, Integer]  Note: Word to index mapping
    index_to_word as Dictionary[Integer, String]  Note: Index to word mapping
    frozen as Boolean                 Note: Whether embeddings are frozen
```

### Word Embedding Types
```runa
Type called "Word2VecConfig":
    model_type as String             Note: skip_gram or cbow
    vector_size as Integer           Note: Dimensionality of embeddings
    window as Integer                Note: Context window size
    min_count as Integer             Note: Minimum word frequency
    negative_samples as Integer       Note: Number of negative samples
    learning_rate as Float           Note: Initial learning rate
    epochs as Integer                Note: Number of training epochs
```

## Basic Embedding Operations

### Creating Embedding Matrices
```runa
Import "math/ai_math/embeddings" as Embeddings

Note: Initialize embedding matrix
Let vocab_size be 10000
Let embedding_dim be 300

Let embedding_config be EmbeddingConfig with:
    vocab_size: vocab_size
    embedding_dim: embedding_dim
    padding_idx: 0                   Note: Index 0 for padding token
    max_norm: 1.0                    Note: L2 norm clipping
    norm_type: 2.0                   Note: L2 norm
    scale_grad_by_freq: false
    sparse: false

Let embedding_matrix be Embeddings.create_embedding_matrix(vocab_size, embedding_dim, embedding_config)

Display "Created embedding matrix of size: " joined with String(embedding_matrix.embeddings.rows) joined with "x" joined with String(embedding_matrix.embeddings.columns)
```

### Vocabulary Management
```runa
Note: Build vocabulary from text corpus
Let text_corpus be ["hello world", "world of embeddings", "hello embeddings"]
Let vocab_config be VocabularyConfig with:
    min_frequency: 1                 Note: Minimum word frequency
    max_vocab_size: 50000           Note: Maximum vocabulary size
    special_tokens: ["<PAD>", "<UNK>", "<START>", "<END>"]

Let vocabulary be Embeddings.build_vocabulary(text_corpus, vocab_config)

Display "Vocabulary size: " joined with String(vocabulary.vocab_size)
Display "Word to index mappings:"
For Each word, index in vocabulary.word_to_index:
    Display "  " joined with word joined with " -> " joined with String(index)

Note: Convert text to indices
Let sentence be "hello world"
Let token_indices be Embeddings.text_to_indices(sentence, vocabulary)
Display "Token indices for '" joined with sentence joined with "': " joined with String(token_indices.components)
```

### Embedding Lookup
```runa
Note: Look up embeddings for tokens
Let input_indices be Vector with components: ["1", "2", "3"], dimension: 3
Let embeddings be Embeddings.lookup_embeddings(embedding_matrix, input_indices)

Display "Retrieved embeddings shape: " joined with String(embeddings.rows) joined with "x" joined with String(embeddings.columns)

Note: Batch embedding lookup
Let batch_indices be Matrix with entries: [
    ["1", "2", "3"],         Note: First sentence
    ["4", "5", "0"]          Note: Second sentence (with padding)
]

Let batch_embeddings be Embeddings.batch_lookup_embeddings(embedding_matrix, batch_indices)
Display "Batch embeddings shape: " joined with String(batch_embeddings.batch_size) joined with "x" joined with String(batch_embeddings.seq_len) joined with "x" joined with String(batch_embeddings.embedding_dim)
```

## Word2Vec Implementation

### Skip-gram Model
```runa
Note: Skip-gram Word2Vec implementation
Let word2vec_config be Word2VecConfig with:
    model_type: "skip_gram"
    vector_size: 100
    window: 5                        Note: Context window size
    min_count: 5                     Note: Minimum word frequency
    negative_samples: 5              Note: Number of negative samples
    learning_rate: 0.025            Note: Initial learning rate
    epochs: 5

Let training_corpus be [
    ["the", "quick", "brown", "fox", "jumps"],
    ["over", "the", "lazy", "dog"],
    ["the", "dog", "runs", "quickly"]
]

Let word2vec_model be Embeddings.train_word2vec(training_corpus, word2vec_config)

Display "Word2Vec training completed"
Display "Vocabulary size: " joined with String(word2vec_model.vocabulary.vocab_size)
```

### Skip-gram Training Step
```runa
Note: Single training step for skip-gram
Process called "skipgram_training_step" that takes center_word as String, context_words as List[String], model as Word2VecModel:
    Let center_idx be model.vocabulary.word_to_index.get(center_word)
    Let center_embedding be Embeddings.get_embedding(model.input_embeddings, center_idx)
    
    Note: Positive samples (actual context words)
    For Each context_word in context_words:
        Let context_idx be model.vocabulary.word_to_index.get(context_word)
        Let context_embedding be Embeddings.get_embedding(model.output_embeddings, context_idx)
        
        Note: Compute sigmoid(center · context)
        Let dot_product be LinAlg.dot_product(center_embedding, context_embedding)
        Let sigmoid_score be sigmoid(dot_product)
        
        Note: Positive sample loss: -log(sigmoid(score))
        Let positive_loss be MathOps.multiply("-1.0", MathOps.natural_logarithm(sigmoid_score.to_string(), 15).result_value, 15)
        
        Note: Update embeddings based on positive sample gradient
        Call Embeddings.update_skipgram_embeddings(model, center_idx, context_idx, positive_loss.result_value, true)
    
    Note: Negative samples
    Let negative_samples be Embeddings.sample_negative_words(model.vocabulary, word2vec_config.negative_samples)
    For Each negative_word in negative_samples:
        Let negative_idx be model.vocabulary.word_to_index.get(negative_word)
        Let negative_embedding be Embeddings.get_embedding(model.output_embeddings, negative_idx)
        
        Let negative_dot_product be LinAlg.dot_product(center_embedding, negative_embedding)
        Let negative_sigmoid be sigmoid(negative_dot_product)
        
        Note: Negative sample loss: -log(1 - sigmoid(score))
        Let negative_loss be MathOps.multiply("-1.0", 
            MathOps.natural_logarithm(
                MathOps.subtract("1.0", negative_sigmoid.to_string(), 15).result_value, 
                15
            ).result_value, 
            15
        )
        
        Note: Update embeddings based on negative sample gradient
        Call Embeddings.update_skipgram_embeddings(model, center_idx, negative_idx, negative_loss.result_value, false)

Display "Skip-gram training step completed"
```

### Continuous Bag of Words (CBOW)
```runa
Note: CBOW model implementation
Let cbow_config be Word2VecConfig with:
    model_type: "cbow"
    vector_size: 100
    window: 5
    min_count: 5
    negative_samples: 5
    learning_rate: 0.025
    epochs: 5

Process called "cbow_training_step" that takes context_words as List[String], target_word as String, model as Word2VecModel:
    Note: Average context word embeddings
    Let context_sum be Vector with components: zeros(model.vector_size), dimension: model.vector_size
    Let context_count be 0
    
    For Each context_word in context_words:
        If model.vocabulary.word_to_index.has_key(context_word):
            Let context_idx be model.vocabulary.word_to_index.get(context_word)
            Let context_embedding be Embeddings.get_embedding(model.input_embeddings, context_idx)
            
            Set context_sum to LinAlg.add_vectors(context_sum, context_embedding)
            Set context_count to context_count + 1
    
    If context_count > 0:
        Let context_average be LinAlg.scalar_divide_vector(context_sum, context_count.to_string())
        
        Note: Predict target word from context average
        Let target_idx be model.vocabulary.word_to_index.get(target_word)
        Let target_embedding be Embeddings.get_embedding(model.output_embeddings, target_idx)
        
        Let prediction_score be LinAlg.dot_product(context_average, target_embedding)
        Let prediction_prob be sigmoid(prediction_score)
        
        Note: Update embeddings based on prediction error
        Let error be MathOps.subtract("1.0", prediction_prob.to_string(), 15)
        Call Embeddings.update_cbow_embeddings(model, context_words, target_idx, error.result_value)

Display "CBOW training step completed"
```

## GloVe (Global Vectors) Implementation

### Co-occurrence Matrix Construction
```runa
Note: Build word co-occurrence matrix for GloVe
Let glove_config be GloVeConfig with:
    vector_size: 100
    max_vocab: 50000
    min_count: 5
    x_max: 100.0                     Note: Cutoff for weighting function
    alpha: 0.75                      Note: Exponent for weighting function
    learning_rate: 0.05

Let cooccurrence_matrix be Embeddings.build_cooccurrence_matrix(training_corpus, glove_config)

Display "Co-occurrence matrix built"
Display "Matrix size: " joined with String(cooccurrence_matrix.rows) joined with "x" joined with String(cooccurrence_matrix.columns)
Display "Non-zero entries: " joined with String(cooccurrence_matrix.nnz)
```

### GloVe Training
```runa
Note: Train GloVe embeddings using co-occurrence statistics
Process called "train_glove" that takes cooccurrence_matrix as SparseMatrix[Float], config as GloVeConfig returns GloVeModel:
    Note: Initialize word and context vectors randomly
    Let vocab_size be cooccurrence_matrix.rows
    Let word_vectors be Embeddings.initialize_random_matrix(vocab_size, config.vector_size, 0.5)
    Let context_vectors be Embeddings.initialize_random_matrix(vocab_size, config.vector_size, 0.5)
    Let word_biases be Embeddings.initialize_zero_vector(vocab_size)
    Let context_biases be Embeddings.initialize_zero_vector(vocab_size)
    
    Let epoch be 0
    While epoch < config.epochs:
        Let total_loss be 0.0
        
        Note: Iterate through non-zero co-occurrence entries
        For Each i, j, x_ij in cooccurrence_matrix.non_zero_entries:
            Note: Compute weighting function f(x_ij)
            Let weight be Embeddings.compute_glove_weight(x_ij, config.x_max, config.alpha)
            
            Note: Compute prediction: w_i · w_j + b_i + b_j
            Let word_i be Embeddings.get_vector_row(word_vectors, i)
            Let context_j be Embeddings.get_vector_row(context_vectors, j)
            Let dot_product be LinAlg.dot_product(word_i, context_j)
            
            Let prediction be MathOps.add(
                MathOps.add(dot_product.to_string(), word_biases.components.get(i), 15).result_value,
                context_biases.components.get(j),
                15
            )
            
            Note: Compute weighted loss: f(x_ij) * (prediction - log(x_ij))²
            Let log_cooccurrence be MathOps.natural_logarithm(x_ij.to_string(), 15)
            Let error be MathOps.subtract(prediction.result_value, log_cooccurrence.result_value, 15)
            Let squared_error be MathOps.multiply(error.result_value, error.result_value, 15)
            Let weighted_loss be MathOps.multiply(weight.to_string(), squared_error.result_value, 15)
            
            Set total_loss to total_loss + Parse weighted_loss.result_value as Float
            
            Note: Compute gradients and update parameters
            Call Embeddings.update_glove_parameters(
                word_vectors, context_vectors, word_biases, context_biases,
                i, j, error.result_value, weight, config.learning_rate
            )
        
        Display "Epoch " joined with String(epoch) joined with " loss: " joined with String(total_loss)
        Set epoch to epoch + 1
    
    Note: Combine word and context vectors
    Let final_embeddings be Embeddings.combine_glove_vectors(word_vectors, context_vectors)
    
    Return GloVeModel with:
        embeddings: final_embeddings
        vocabulary: vocabulary
        config: config

Display "GloVe training completed"
```

## FastText Implementation

### Subword Information
```runa
Note: FastText with character n-gram features
Let fasttext_config be FastTextConfig with:
    vector_size: 100
    window: 5
    min_n: 3                         Note: Minimum n-gram length
    max_n: 6                         Note: Maximum n-gram length
    bucket: 2000000                  Note: Number of hash buckets for n-grams

Process called "extract_subword_features" that takes word as String, config as FastTextConfig returns List[Integer]:
    Let ngram_hashes be List[Integer]()
    
    Note: Add start and end markers
    Let padded_word be "<" joined with word joined with ">"
    
    Note: Extract character n-grams
    Let n be config.min_n
    While n <= config.max_n:
        Let pos be 0
        While pos + n <= padded_word.length:
            Let ngram be padded_word.substring(pos, pos + n)
            Let hash_value be Embeddings.fnv_hash(ngram) % config.bucket
            Call ngram_hashes.add(hash_value)
            Set pos to pos + 1
        Set n to n + 1
    
    Return ngram_hashes
```

### FastText Training
```runa
Note: Train FastText embeddings with subword information
Process called "train_fasttext" that takes corpus as List[List[String]], config as FastTextConfig returns FastTextModel:
    Note: Build vocabulary including subword features
    Let vocabulary be Embeddings.build_fasttext_vocabulary(corpus, config)
    
    Note: Initialize embeddings for words and n-grams
    Let word_embeddings be Embeddings.initialize_random_matrix(vocabulary.word_count, config.vector_size, 0.5)
    Let ngram_embeddings be Embeddings.initialize_random_matrix(config.bucket, config.vector_size, 0.5)
    
    For Each sentence in corpus:
        For Each center_word in sentence:
            Let context_words be Embeddings.get_context_words(sentence, center_word, config.window)
            
            Note: Get subword features for center word
            Let center_subwords be extract_subword_features(center_word, config)
            
            Note: Compute center word representation as sum of word + subword embeddings
            Let center_embedding be Embeddings.get_word_embedding(word_embeddings, center_word, vocabulary)
            For Each subword_hash in center_subwords:
                Let subword_embedding be Embeddings.get_vector_row(ngram_embeddings, subword_hash)
                Set center_embedding to LinAlg.add_vectors(center_embedding, subword_embedding)
            
            Note: Skip-gram training with subword-enhanced representations
            For Each context_word in context_words:
                Let context_embedding be Embeddings.get_word_embedding(word_embeddings, context_word, vocabulary)
                
                Note: Compute similarity and update embeddings
                Let similarity be LinAlg.dot_product(center_embedding, context_embedding)
                Let probability be sigmoid(similarity)
                
                Note: Update both word and subword embeddings
                Call Embeddings.update_fasttext_embeddings(
                    word_embeddings, ngram_embeddings,
                    center_word, center_subwords, context_word,
                    probability, config.learning_rate
                )
    
    Return FastTextModel with:
        word_embeddings: word_embeddings
        ngram_embeddings: ngram_embeddings
        vocabulary: vocabulary
        config: config

Display "FastText training completed"
```

## Sentence and Document Embeddings

### Mean Pooling
```runa
Note: Simple mean pooling for sentence embeddings
Process called "mean_pooling_embedding" that takes word_embeddings as Matrix[Float], attention_mask as Vector[Boolean] returns Vector[Float]:
    Note: Compute mean of word embeddings, excluding padding tokens
    Let embedding_sum be Vector with components: zeros(word_embeddings.columns), dimension: word_embeddings.columns
    Let valid_count be 0
    
    Let token_idx be 0
    While token_idx < word_embeddings.rows:
        Let is_valid be attention_mask.components.get(token_idx)
        If is_valid:
            Let token_embedding be LinAlg.get_matrix_row(word_embeddings, token_idx)
            Set embedding_sum to LinAlg.add_vectors(embedding_sum, token_embedding)
            Set valid_count to valid_count + 1
        Set token_idx to token_idx + 1
    
    If valid_count > 0:
        Return LinAlg.scalar_divide_vector(embedding_sum, valid_count.to_string())
    Otherwise:
        Return embedding_sum  Note: Return zeros if no valid tokens
```

### Weighted Pooling
```runa
Note: Weighted pooling using TF-IDF or attention weights
Process called "weighted_pooling_embedding" that takes word_embeddings as Matrix[Float], weights as Vector[Float] returns Vector[Float]:
    Let weighted_sum be Vector with components: zeros(word_embeddings.columns), dimension: word_embeddings.columns
    Let total_weight be 0.0
    
    Let token_idx be 0
    While token_idx < word_embeddings.rows:
        Let token_weight be Parse weights.components.get(token_idx) as Float
        Let token_embedding be LinAlg.get_matrix_row(word_embeddings, token_idx)
        
        Let weighted_embedding be LinAlg.scalar_multiply_vector(token_embedding, token_weight.to_string())
        Set weighted_sum to LinAlg.add_vectors(weighted_sum, weighted_embedding)
        Set total_weight to total_weight + token_weight
        Set token_idx to token_idx + 1
    
    If total_weight > 0.0:
        Return LinAlg.scalar_divide_vector(weighted_sum, total_weight.to_string())
    Otherwise:
        Return weighted_sum
```

### TF-IDF Weighted Embeddings
```runa
Note: Combine embeddings with TF-IDF weights
Let tfidf_config be TFIDFConfig with:
    max_features: 10000
    min_df: 1
    max_df: 0.95
    smooth_idf: true

Let documents be ["the quick brown fox", "jumps over lazy dog", "the dog runs quickly"]
Let tfidf_weights be Embeddings.compute_tfidf_weights(documents, vocabulary, tfidf_config)

Process called "tfidf_sentence_embedding" that takes document as String, embeddings as EmbeddingMatrix returns Vector[Float]:
    Let tokens be tokenize(document)
    Let token_embeddings be List[Vector[Float]]()
    Let token_weights be List[Float]()
    
    For Each token in tokens:
        If embeddings.vocab.has_key(token):
            Let token_idx be embeddings.vocab.get(token)
            Let token_embedding be Embeddings.get_embedding(embeddings, token_idx)
            Let tfidf_weight be tfidf_weights.get(token, 0.0)
            
            Call token_embeddings.add(token_embedding)
            Call token_weights.add(tfidf_weight)
    
    Note: Compute weighted average
    Return weighted_pooling_embedding(
        LinAlg.stack_vectors(token_embeddings),
        Vector with components: token_weights.map(x -> x.to_string())
    )
```

## Positional Embeddings

### Sinusoidal Positional Encoding
```runa
Note: Transformer-style sinusoidal position embeddings
Process called "sinusoidal_positional_encoding" that takes max_length as Integer, d_model as Integer returns Matrix[Float]:
    Let position_encodings be List[List[String]]()
    
    Let pos be 0
    While pos < max_length:
        Let encoding_row be List[String]()
        
        Let i be 0
        While i < d_model:
            Let angle_rate be 1.0 / MathOps.power("10000", MathOps.divide(String(i), String(d_model), 15).result_value, 15).result_value
            
            If i % 2 == 0:
                Note: Even indices use sine
                Let angle be pos.to_string() * angle_rate
                Let encoding_value be Trig.sine(angle.to_string(), "radians", 15)
                Call encoding_row.add(encoding_value.function_value)
            Otherwise:
                Note: Odd indices use cosine  
                Let angle be pos.to_string() * angle_rate
                Let encoding_value be Trig.cosine(angle.to_string(), "radians", 15)
                Call encoding_row.add(encoding_value.function_value)
            
            Set i to i + 1
        
        Call position_encodings.add(encoding_row)
        Set pos to pos + 1
    
    Return LinAlg.create_matrix(position_encodings, "float")
```

### Learnable Positional Embeddings
```runa
Note: Learnable position embeddings
Let max_seq_length be 512
Let d_model be 768

Let learned_positions be Embeddings.create_embedding_matrix(max_seq_length, d_model, embedding_config)

Process called "add_positional_embeddings" that takes input_embeddings as Matrix[Float], position_embeddings as EmbeddingMatrix returns Matrix[Float]:
    Let seq_length be input_embeddings.rows
    Let result_embeddings be List[List[String]]()
    
    Let pos be 0
    While pos < seq_length:
        Let input_row be LinAlg.get_matrix_row(input_embeddings, pos)
        Let position_row be Embeddings.get_embedding(position_embeddings, pos)
        Let combined_row be LinAlg.add_vectors(input_row, position_row)
        
        Call result_embeddings.add(combined_row.components)
        Set pos to pos + 1
    
    Return LinAlg.create_matrix(result_embeddings, "float")
```

### Rotary Position Encoding (RoPE)
```runa
Note: RoPE for relative position encoding
Process called "apply_rotary_position_encoding" that takes embeddings as Matrix[Float], position_ids as Vector[Integer], theta as Float returns Matrix[Float]:
    Let seq_length be embeddings.rows
    Let d_model be embeddings.columns
    Let rotated_embeddings be List[List[String]]()
    
    Let pos be 0
    While pos < seq_length:
        Let position_id be Parse position_ids.components.get(pos) as Integer
        Let embedding_row be LinAlg.get_matrix_row(embeddings, pos)
        Let rotated_row be List[String]()
        
        Note: Apply rotation to pairs of dimensions
        Let dim be 0
        While dim < d_model - 1:
            Let x1 be Parse embedding_row.components.get(dim) as Float
            Let x2 be Parse embedding_row.components.get(dim + 1) as Float
            
            Note: Compute rotation angle
            Let inv_freq be 1.0 / MathOps.power(theta.to_string(), MathOps.divide(dim.to_string(), d_model.to_string(), 15).result_value, 15).result_value
            Let angle be position_id.to_string() * inv_freq.to_string()
            
            Let cos_angle be Trig.cosine(angle, "radians", 15)
            Let sin_angle be Trig.sine(angle, "radians", 15)
            
            Note: Apply rotation matrix
            Let rotated_x1 be x1 * Parse cos_angle.function_value as Float - x2 * Parse sin_angle.function_value as Float
            Let rotated_x2 be x1 * Parse sin_angle.function_value as Float + x2 * Parse cos_angle.function_value as Float
            
            Call rotated_row.add(rotated_x1.to_string())
            Call rotated_row.add(rotated_x2.to_string())
            
            Set dim to dim + 2
        
        Call rotated_embeddings.add(rotated_row)
        Set pos to pos + 1
    
    Return LinAlg.create_matrix(rotated_embeddings, "float")
```

## Similarity and Distance Metrics

### Cosine Similarity
```runa
Note: Compute cosine similarity between embeddings
Process called "cosine_similarity" that takes embedding_a as Vector[Float], embedding_b as Vector[Float] returns Float:
    Let dot_product be LinAlg.dot_product(embedding_a, embedding_b)
    Let norm_a be LinAlg.vector_norm(embedding_a, 2.0)
    Let norm_b be LinAlg.vector_norm(embedding_b, 2.0)
    
    Let denominator be MathOps.multiply(norm_a.to_string(), norm_b.to_string(), 15)
    If Parse denominator.result_value as Float > 1e-10:
        Let similarity be MathOps.divide(dot_product.to_string(), denominator.result_value, 15)
        Return Parse similarity.result_value as Float
    Otherwise:
        Return 0.0
```

### Batch Similarity Computation
```runa
Note: Efficient batch cosine similarity
Process called "batch_cosine_similarity" that takes embeddings_a as Matrix[Float], embeddings_b as Matrix[Float] returns Matrix[Float]:
    Note: Normalize embeddings for efficient cosine similarity
    Let normalized_a be LinAlg.normalize_matrix_rows(embeddings_a, 2.0)
    Let normalized_b be LinAlg.normalize_matrix_rows(embeddings_b, 2.0)
    
    Note: Cosine similarity = normalized_a @ normalized_b^T
    Let similarity_matrix be LinAlg.matrix_multiply(normalized_a, LinAlg.transpose(normalized_b))
    
    Return similarity_matrix
```

### K-Nearest Neighbors Search
```runa
Note: Find most similar embeddings
Process called "find_nearest_neighbors" that takes query_embedding as Vector[Float], embedding_matrix as Matrix[Float], k as Integer returns List[Tuple[Integer, Float]]:
    Let similarities be List[Tuple[Integer, Float]]()
    
    Let i be 0
    While i < embedding_matrix.rows:
        Let candidate_embedding be LinAlg.get_matrix_row(embedding_matrix, i)
        Let similarity be cosine_similarity(query_embedding, candidate_embedding)
        Call similarities.add(Tuple with first: i, second: similarity)
        Set i to i + 1
    
    Note: Sort by similarity (descending) and return top k
    Let sorted_similarities be Sorting.sort_tuples_by_second(similarities, "descending")
    Return sorted_similarities.slice(0, k)
```

## Advanced Embedding Techniques

### Embedding Alignment and Mapping
```runa
Note: Align embeddings from different languages/domains
Process called "procrustes_alignment" that takes source_embeddings as Matrix[Float], target_embeddings as Matrix[Float] returns Matrix[Float]:
    Note: Procrustes analysis: find optimal rotation matrix W
    Note: min ||XW - Y||_F s.t. W^T W = I
    
    Let covariance_matrix be LinAlg.matrix_multiply(LinAlg.transpose(source_embeddings), target_embeddings)
    Let svd_result be LinAlg.singular_value_decomposition(covariance_matrix)
    
    Note: Optimal rotation: W = U V^T
    Let rotation_matrix be LinAlg.matrix_multiply(svd_result.u_matrix, LinAlg.transpose(svd_result.v_matrix))
    
    Return rotation_matrix
```

### Embedding Visualization
```runa
Note: Reduce dimensionality for visualization using PCA
Process called "pca_visualization" that takes embeddings as Matrix[Float], target_dimensions as Integer returns Matrix[Float]:
    Note: Center the data
    Let mean_vector be LinAlg.compute_column_means(embeddings)
    Let centered_embeddings be LinAlg.subtract_row_means(embeddings, mean_vector)
    
    Note: Compute covariance matrix
    Let covariance be LinAlg.matrix_multiply(LinAlg.transpose(centered_embeddings), centered_embeddings)
    Set covariance to LinAlg.scalar_multiply_matrix(covariance, (1.0 / (embeddings.rows - 1)).to_string())
    
    Note: Eigendecomposition for principal components
    Let eigen_result be LinAlg.eigendecomposition(covariance)
    
    Note: Select top components
    Let principal_components be LinAlg.get_matrix_columns(eigen_result.eigenvectors, 0, target_dimensions)
    
    Note: Project data
    Return LinAlg.matrix_multiply(centered_embeddings, principal_components)
```

### Embedding Clustering
```runa
Note: Cluster embeddings using K-means
Process called "cluster_embeddings" that takes embeddings as Matrix[Float], num_clusters as Integer returns Vector[Integer]:
    Note: Initialize cluster centroids randomly
    Let centroids be Embeddings.initialize_random_centroids(embeddings, num_clusters)
    Let assignments be Vector with components: zeros(embeddings.rows), dimension: embeddings.rows
    Let max_iterations be 100
    
    Let iteration be 0
    While iteration < max_iterations:
        Let converged be true
        
        Note: Assign points to nearest centroids
        Let point_idx be 0
        While point_idx < embeddings.rows:
            Let point_embedding be LinAlg.get_matrix_row(embeddings, point_idx)
            Let nearest_centroid be find_nearest_centroid(point_embedding, centroids)
            
            If Parse assignments.components.get(point_idx) as Integer != nearest_centroid:
                Set converged to false
                Set assignments.components[point_idx] to nearest_centroid.to_string()
            
            Set point_idx to point_idx + 1
        
        If converged:
            Break
        
        Note: Update centroids
        Set centroids to compute_new_centroids(embeddings, assignments, num_clusters)
        Set iteration to iteration + 1
    
    Return assignments
```

## Pre-trained Embedding Integration

### Loading Pre-trained Embeddings
```runa
Note: Load pre-trained embeddings (e.g., GloVe, Word2Vec)
Process called "load_pretrained_embeddings" that takes file_path as String, vocab as Vocabulary returns EmbeddingMatrix:
    Let pretrained_embeddings be Dictionary[String, Vector[Float]]()
    Let embedding_dim be 0
    
    Note: Parse embedding file (word vector format)
    Let lines be read_file_lines(file_path)
    For Each line in lines:
        Let tokens be split(line, " ")
        If tokens.length > 1:
            Let word be tokens.get(0)
            Let vector_components be tokens.slice(1)
            
            If embedding_dim == 0:
                Set embedding_dim to vector_components.length
            
            If vector_components.length == embedding_dim:
                Let embedding_vector be Vector with components: vector_components, dimension: embedding_dim
                Set pretrained_embeddings[word] to embedding_vector
    
    Note: Create embedding matrix from vocabulary
    Let embedding_matrix be Embeddings.initialize_embedding_matrix(vocab.vocab_size, embedding_dim)
    
    For Each word, index in vocab.word_to_index:
        If pretrained_embeddings.has_key(word):
            Let pretrained_vector be pretrained_embeddings.get(word)
            Call Embeddings.set_embedding(embedding_matrix, index, pretrained_vector)
    
    Return embedding_matrix
```

### Fine-tuning Pre-trained Embeddings
```runa
Note: Fine-tune embeddings on domain-specific data
Process called "finetune_embeddings" that takes pretrained_model as EmbeddingMatrix, domain_corpus as List[List[String]], config as FinetuningConfig:
    Note: Initialize with pretrained weights
    Let model be pretrained_model
    
    Note: Optionally freeze common words and only update rare words
    Let update_mask be create_update_mask(model.vocab, domain_corpus, config.freeze_common_words)
    
    For Each sentence in domain_corpus:
        For Each center_word in sentence:
            Let center_idx be model.vocab.get(center_word)
            
            Note: Only update if not frozen
            If update_mask.get(center_idx):
                Let context_words be get_context_words(sentence, center_word, config.window)
                
                Note: Apply skip-gram updates with lower learning rate
                Call skipgram_training_step_with_mask(center_word, context_words, model, update_mask, config.learning_rate)
    
    Display "Embedding fine-tuning completed"
```

## Performance Optimization

### Hierarchical Softmax
```runa
Note: Efficient training with hierarchical softmax
Process called "hierarchical_softmax" that takes input_embedding as Vector[Float], target_word_path as List[Tuple[Integer, Boolean]], model as Word2VecModel returns Float:
    Let log_probability be 0.0
    
    For Each node_id, direction in target_word_path:
        Let node_embedding be Embeddings.get_embedding(model.tree_embeddings, node_id)
        Let dot_product be LinAlg.dot_product(input_embedding, node_embedding)
        
        Let probability as Float
        If direction:  Note: Go right in binary tree
            Set probability to sigmoid(dot_product)
        Otherwise:     Note: Go left in binary tree
            Set probability to sigmoid(-dot_product)
        
        Set log_probability to log_probability + MathOps.natural_logarithm(probability.to_string(), 15).result_value
    
    Return log_probability
```

### Embedding Quantization
```runa
Note: Reduce memory usage through quantization
Process called "quantize_embeddings" that takes embeddings as Matrix[Float], num_bits as Integer returns QuantizedEmbeddings:
    Note: Compute quantization parameters
    Let min_val be LinAlg.matrix_minimum(embeddings)
    Let max_val be LinAlg.matrix_maximum(embeddings)
    Let scale be (max_val - min_val) / (2^num_bits - 1)
    
    Let quantized_values be List[List[Integer]]()
    
    Let i be 0
    While i < embeddings.rows:
        Let quantized_row be List[Integer]()
        Let j be 0
        While j < embeddings.columns:
            Let original_value be Parse embeddings.entries.get(i).get(j) as Float
            Let quantized_value be Integer((original_value - min_val) / scale)
            Call quantized_row.add(quantized_value)
            Set j to j + 1
        Call quantized_values.add(quantized_row)
        Set i to i + 1
    
    Return QuantizedEmbeddings with:
        quantized_matrix: quantized_values
        scale: scale
        offset: min_val
        num_bits: num_bits
```

## Testing and Evaluation

### Embedding Quality Tests
```runa
Note: Evaluate embedding quality using analogy tasks
Process called "analogy_test" that takes embeddings as EmbeddingMatrix, analogies as List[AnalogyQuadruplet] returns Float:
    Let correct_predictions be 0
    Let total_analogies be analogies.length
    
    For Each analogy in analogies:
        Note: Analogy: A is to B as C is to ?
        Let a_embedding be Embeddings.lookup_word_embedding(embeddings, analogy.word_a)
        Let b_embedding be Embeddings.lookup_word_embedding(embeddings, analogy.word_b)
        Let c_embedding be Embeddings.lookup_word_embedding(embeddings, analogy.word_c)
        
        Note: Compute analogy vector: B - A + C
        Let analogy_vector be LinAlg.add_vectors(
            LinAlg.subtract_vectors(b_embedding, a_embedding),
            c_embedding
        )
        
        Note: Find nearest neighbor (excluding A, B, C)
        Let exclude_words be [analogy.word_a, analogy.word_b, analogy.word_c]
        Let predicted_word be find_nearest_word_excluding(embeddings, analogy_vector, exclude_words)
        
        If predicted_word == analogy.word_d:
            Set correct_predictions to correct_predictions + 1
    
    Return correct_predictions / total_analogies
```

### Similarity Benchmark
```runa
Note: Evaluate on word similarity benchmarks
Process called "similarity_benchmark" that takes embeddings as EmbeddingMatrix, word_pairs as List[WordPair] returns Float:
    Let predicted_similarities be List[Float]()
    Let human_similarities be List[Float]()
    
    For Each word_pair in word_pairs:
        Let embedding_1 be Embeddings.lookup_word_embedding(embeddings, word_pair.word_1)
        Let embedding_2 be Embeddings.lookup_word_embedding(embeddings, word_pair.word_2)
        
        Let predicted_sim be cosine_similarity(embedding_1, embedding_2)
        
        Call predicted_similarities.add(predicted_sim)
        Call human_similarities.add(word_pair.human_similarity)
    
    Note: Compute Spearman correlation
    Let spearman_correlation be Stats.spearman_correlation(predicted_similarities, human_similarities)
    Return spearman_correlation
```

### Clustering Evaluation
```runa
Note: Evaluate embedding clustering quality
Process called "evaluate_embedding_clustering" that takes embeddings as Matrix[Float], true_labels as Vector[Integer], predicted_labels as Vector[Integer] returns ClusteringMetrics:
    Let ari_score be Metrics.adjusted_rand_index(true_labels, predicted_labels)
    Let nmi_score be Metrics.normalized_mutual_info_score(true_labels, predicted_labels)
    Let silhouette_score be Metrics.silhouette_score(embeddings, predicted_labels)
    
    Return ClusteringMetrics with:
        adjusted_rand_index: ari_score
        normalized_mutual_info: nmi_score
        silhouette_score: silhouette_score
```

## Related Documentation

- **[AI Math Neural Ops](neural_ops.md)**: Neural network operations for embedding layers
- **[AI Math Attention](attention.md)**: Attention mechanisms using embeddings
- **[Math Engine Linear Algebra](../engine/linalg/core.md)**: Matrix operations for embeddings
- **[Math Statistics](../statistics/README.md)**: Statistical methods for evaluation
- **[Math Core Operations](../core/operations.md)**: Basic mathematical operations

The Embedding Operations module provides comprehensive tools for learning and manipulating vector representations of discrete objects, enabling semantic understanding and similarity computation across various domains.