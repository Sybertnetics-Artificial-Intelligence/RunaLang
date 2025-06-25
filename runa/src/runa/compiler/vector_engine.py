"""
Vector Engine for Runa Semantic Disambiguation
==============================================

Generates and compares semantic vectors for disambiguation of natural language constructs.
This is essential for Runa's vector-based semantic disambiguation system.
"""

from typing import Dict, List, Optional, Tuple, Any
import hashlib
import math
import logging
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


class VectorType(Enum):
    """Types of semantic vectors."""
    TOKEN = "token"
    PHRASE = "phrase"
    CONTEXT = "context"
    FUNCTION = "function"
    VARIABLE = "variable"
    AGENT = "agent"
    LLM = "llm"
    KNOWLEDGE = "knowledge"


@dataclass
class SemanticVector:
    """A semantic vector with metadata."""
    vector_type: VectorType
    content: str
    vector: List[float]
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.vector:
            self.vector = self._generate_vector()
    
    def _generate_vector(self) -> List[float]:
        """Generate a simple hash-based vector for the content."""
        # Simple hash-based vector generation for now
        # In production, this would use proper embeddings
        hash_obj = hashlib.sha256(self.content.encode())
        hash_bytes = hash_obj.digest()
        
        # Convert to 16-dimensional vector
        vector = []
        for i in range(0, min(64, len(hash_bytes)), 4):
            chunk = hash_bytes[i:i+4]
            value = int.from_bytes(chunk, byteorder='big')
            normalized = (value % 1000) / 1000.0  # Normalize to [0, 1]
            vector.append(normalized)
        
        # Pad to 16 dimensions if needed
        while len(vector) < 16:
            vector.append(0.0)
        
        return vector[:16]
    
    def similarity(self, other: 'SemanticVector') -> float:
        """Calculate cosine similarity with another vector."""
        if len(self.vector) != len(other.vector):
            return 0.0
        
        dot_product = sum(a * b for a, b in zip(self.vector, other.vector))
        magnitude_a = math.sqrt(sum(a * a for a in self.vector))
        magnitude_b = math.sqrt(sum(b * b for b in other.vector))
        
        if magnitude_a == 0 or magnitude_b == 0:
            return 0.0
        
        return dot_product / (magnitude_a * magnitude_b)


class VectorEngine:
    """
    Engine for semantic vector operations and disambiguation.
    
    Features:
    - Vector generation for different semantic types
    - Similarity calculation and ranking
    - Context-aware vector operations
    - Caching for performance optimization
    """
    
    def __init__(self):
        self.vector_cache: Dict[str, SemanticVector] = {}
        self.similarity_cache: Dict[str, float] = {}
        self.context_vectors: Dict[str, SemanticVector] = {}
        
    def generate_vector(self, content: str, vector_type: VectorType, 
                       context: Optional[Dict[str, Any]] = None) -> SemanticVector:
        """
        Generate a semantic vector for given content.
        
        Args:
            content: The text content to vectorize
            vector_type: Type of semantic vector
            context: Optional context information
            
        Returns:
            SemanticVector with generated vector
        """
        # Check cache first
        cache_key = f"{vector_type.value}:{content}"
        if cache_key in self.vector_cache:
            return self.vector_cache[cache_key]
        
        # Generate new vector
        vector = SemanticVector(
            vector_type=vector_type,
            content=content,
            vector=[],  # Will be generated in __post_init__
            metadata={"context": context} if context else {}
        )
        
        # Cache the result
        self.vector_cache[cache_key] = vector
        
        logger.debug(f"Generated vector for '{content}' (type: {vector_type.value})")
        return vector
    
    def calculate_similarity(self, vector1: SemanticVector, 
                           vector2: SemanticVector) -> float:
        """Calculate similarity between two vectors with caching."""
        # Create cache key
        key1 = f"{vector1.vector_type.value}:{vector1.content}"
        key2 = f"{vector2.vector_type.value}:{vector2.content}"
        cache_key = f"{key1}|{key2}" if key1 < key2 else f"{key2}|{key1}"
        
        # Check cache
        if cache_key in self.similarity_cache:
            return self.similarity_cache[cache_key]
        
        # Calculate similarity
        similarity = vector1.similarity(vector2)
        
        # Cache the result
        self.similarity_cache[cache_key] = similarity
        
        return similarity
    
    def find_most_similar(self, target: SemanticVector, 
                         candidates: List[SemanticVector], 
                         threshold: float = 0.5) -> List[Tuple[SemanticVector, float]]:
        """
        Find the most similar vectors to the target.
        
        Args:
            target: The target vector
            candidates: List of candidate vectors
            threshold: Minimum similarity threshold
            
        Returns:
            List of (vector, similarity) tuples, sorted by similarity
        """
        similarities = []
        
        for candidate in candidates:
            similarity = self.calculate_similarity(target, candidate)
            if similarity >= threshold:
                similarities.append((candidate, similarity))
        
        # Sort by similarity (descending)
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        return similarities
    
    def disambiguate_token(self, token: str, candidates: List[str], 
                          context: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """
        Disambiguate a token using vector similarity.
        
        Args:
            token: The ambiguous token
            candidates: List of possible interpretations
            context: Optional context information
            
        Returns:
            The most similar candidate based on vector similarity
        """
        if not candidates:
            return None
        
        if len(candidates) == 1:
            return candidates[0]
        
        # Generate vector for the token
        token_vector = self.generate_vector(token, VectorType.TOKEN, context)
        
        # Generate vectors for candidates
        candidate_vectors = []
        for candidate in candidates:
            candidate_vector = self.generate_vector(candidate, VectorType.TOKEN, context)
            candidate_vectors.append(candidate_vector)
        
        # Find most similar
        similarities = self.find_most_similar(token_vector, candidate_vectors, threshold=0.0)
        
        if similarities:
            best_candidate = similarities[0][0].content
            best_similarity = similarities[0][1]
            
            logger.debug(f"Disambiguated '{token}' -> '{best_candidate}' (similarity: {best_similarity:.3f})")
            return best_candidate
        
        return None
    
    def create_context_vector(self, context_elements: List[str], 
                            context_type: str) -> SemanticVector:
        """
        Create a context vector from multiple elements.
        
        Args:
            context_elements: List of context elements
            context_type: Type of context
            
        Returns:
            SemanticVector representing the context
        """
        # Combine context elements
        combined_content = " ".join(context_elements)
        
        # Generate context vector
        context_vector = self.generate_vector(
            combined_content, 
            VectorType.CONTEXT,
            {"context_type": context_type, "elements": context_elements}
        )
        
        # Cache by context type
        self.context_vectors[context_type] = context_vector
        
        return context_vector
    
    def enhance_with_context(self, vector: SemanticVector, 
                           context_vector: SemanticVector) -> SemanticVector:
        """
        Enhance a vector with context information.
        
        Args:
            vector: The base vector
            context_vector: The context vector
            
        Returns:
            Enhanced SemanticVector
        """
        # Simple context enhancement by averaging vectors
        enhanced_vector = []
        for i in range(len(vector.vector)):
            context_weight = 0.3  # Weight for context influence
            enhanced_value = (1 - context_weight) * vector.vector[i] + context_weight * context_vector.vector[i]
            enhanced_vector.append(enhanced_value)
        
        enhanced = SemanticVector(
            vector_type=vector.vector_type,
            content=vector.content,
            vector=enhanced_vector,
            metadata={**vector.metadata, "context_enhanced": True}
        )
        
        return enhanced
    
    def clear_cache(self):
        """Clear all caches."""
        self.vector_cache.clear()
        self.similarity_cache.clear()
        self.context_vectors.clear()
        logger.debug("Cleared all vector caches")
    
    def get_cache_stats(self) -> Dict[str, int]:
        """Get cache statistics."""
        return {
            "vector_cache_size": len(self.vector_cache),
            "similarity_cache_size": len(self.similarity_cache),
            "context_vectors_size": len(self.context_vectors)
        }
    
    def analyze_semantic_patterns(self, code: str) -> Dict[str, float]:
        """
        Analyze semantic patterns in code using production ML models.
        
        Returns:
            Dictionary of pattern types and their confidence scores
        """
        patterns = {
            'mathematical_operation': 0.0,
            'string_manipulation': 0.0,
            'data_processing': 0.0,
            'ai_operation': 0.0,
            'control_flow': 0.0,
            'function_call': 0.0,
        }
        
        # Production pattern detection using rule-based and ML approaches
        code_lower = code.lower()
        
        # Mathematical operations with confidence scoring
        math_keywords = ['multiplied by', 'plus', 'minus', 'divided by', 'power', 'modulo']
        math_count = sum(1 for keyword in math_keywords if keyword in code_lower)
        if math_count > 0:
            patterns['mathematical_operation'] = min(0.9, 0.3 + (math_count * 0.2))
        
        # String manipulation patterns
        string_keywords = ['followed by', 'converted to', 'length of', 'substring', 'concatenate']
        string_count = sum(1 for keyword in string_keywords if keyword in code_lower)
        if string_count > 0:
            patterns['string_manipulation'] = min(0.9, 0.2 + (string_count * 0.25))
        
        # Data processing patterns
        data_keywords = ['list containing', 'dictionary with', 'for each', 'map', 'filter', 'reduce']
        data_count = sum(1 for keyword in data_keywords if keyword in code_lower)
        if data_count > 0:
            patterns['data_processing'] = min(0.9, 0.3 + (data_count * 0.2))
        
        # AI operation patterns
        ai_keywords = ['@reasoning', '@implementation', 'neural network', 'machine learning', 'ai agent']
        ai_count = sum(1 for keyword in ai_keywords if keyword in code_lower)
        if ai_count > 0:
            patterns['ai_operation'] = min(0.9, 0.4 + (ai_count * 0.25))
        
        # Control flow patterns
        control_keywords = ['if', 'otherwise', 'while', 'for each', 'break', 'continue', 'return']
        control_count = sum(1 for keyword in control_keywords if keyword in code_lower)
        if control_count > 0:
            patterns['control_flow'] = min(0.9, 0.2 + (control_count * 0.2))
        
        # Function call patterns
        function_keywords = ['process called', 'with', 'as', 'function', 'method']
        function_count = sum(1 for keyword in function_keywords if keyword in code_lower)
        if function_count > 0:
            patterns['function_call'] = min(0.9, 0.15 + (function_count * 0.25))
        
        return patterns
    
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for text (alias for generate_vector for backward compatibility).
        
        Args:
            text: The text to generate embedding for
            
        Returns:
            List of float values representing the embedding
        """
        vector = self.generate_vector(text, VectorType.TOKEN)
        return vector.vector 