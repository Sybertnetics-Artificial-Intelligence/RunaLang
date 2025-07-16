"""
Unit tests for Tier 1: Memory & Learning Systems.

Tests the episodic memory, semantic memory, vector memory,
and memory policies systems.
"""

import unittest
import numpy as np
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

from runa.ai.memory.episodic import (
    EpisodicMemory, Experience, MemoryType, MemoryPriority
)
from runa.ai.memory.semantic import (
    SemanticMemory, Knowledge, KnowledgeType, ConfidenceLevel, SourceType, Concept
)
from runa.ai.memory.vector import (
    VectorMemory, Embedding, VectorType, SimilarityMetric
)
from runa.ai.memory.policies import (
    MemoryPolicyManager, ConsolidationPolicy, ForgettingPolicy,
    PolicyConfig, PolicyType, PolicyTrigger
)


class TestEpisodicMemory(unittest.TestCase):
    """Test episodic memory system."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.agent_id = "test_agent"
        self.memory = EpisodicMemory(agent_id=self.agent_id)
    
    def test_store_experience(self):
        """Test storing experiences in episodic memory."""
        context = {"location": "office", "time": "morning"}
        
        memory_id = self.memory.store_experience(
            memory_type=MemoryType.EXPERIENCE,
            context=context,
            action="started_work",
            priority=MemoryPriority.HIGH,
            tags={"work", "morning"}
        )
        
        self.assertIsNotNone(memory_id)
        self.assertEqual(len(self.memory.memories), 1)
        
        # Retrieve and verify
        experience = self.memory.retrieve_experience(memory_id)
        self.assertIsNotNone(experience)
        self.assertEqual(experience.agent_id, self.agent_id)
        self.assertEqual(experience.memory_type, MemoryType.EXPERIENCE)
        self.assertEqual(experience.context, context)
        self.assertEqual(experience.action, "started_work")
        self.assertEqual(experience.priority, MemoryPriority.HIGH)
        self.assertEqual(experience.tags, {"work", "morning"})
    
    def test_search_experiences(self):
        """Test searching experiences with filters."""
        # Store multiple experiences
        self.memory.store_experience(
            memory_type=MemoryType.EXPERIENCE,
            context={"location": "office"},
            tags={"work"}
        )
        self.memory.store_experience(
            memory_type=MemoryType.INTERACTION,
            context={"location": "home"},
            tags={"personal"}
        )
        self.memory.store_experience(
            memory_type=MemoryType.EXPERIENCE,
            context={"location": "office"},
            tags={"work", "meeting"}
        )
        
        # Search by type
        experiences = self.memory.search_experiences(memory_type=MemoryType.EXPERIENCE)
        self.assertEqual(len(experiences), 2)
        
        # Search by tags
        experiences = self.memory.search_experiences(tags={"work"})
        self.assertEqual(len(experiences), 2)
        
        # Search by priority
        experiences = self.memory.search_experiences(priority=MemoryPriority.MEDIUM)
        self.assertEqual(len(experiences), 3)  # All default to MEDIUM
    
    def test_experience_importance(self):
        """Test experience importance calculation."""
        # Create experience with high priority and emotional valence
        memory_id = self.memory.store_experience(
            memory_type=MemoryType.EXPERIENCE,
            context={"event": "important"},
            priority=MemoryPriority.HIGH,
            emotional_valence=0.8,
            confidence=0.9
        )
        
        experience = self.memory.retrieve_experience(memory_id)
        importance = experience.calculate_importance()
        
        self.assertGreater(importance, 0.5)  # Should be high importance
    
    def test_experience_associations(self):
        """Test experience associations."""
        # Store two related experiences
        memory_id1 = self.memory.store_experience(
            memory_type=MemoryType.EXPERIENCE,
            context={"event": "meeting"}
        )
        memory_id2 = self.memory.store_experience(
            memory_type=MemoryType.EXPERIENCE,
            context={"event": "followup"}
        )
        
        # Add association
        experience1 = self.memory.retrieve_experience(memory_id1)
        experience1.add_association(memory_id2)
        
        # Get related experiences
        related = self.memory.get_related_experiences(memory_id1)
        self.assertEqual(len(related), 1)
        self.assertEqual(related[0].id, memory_id2)
    
    def test_memory_summary(self):
        """Test memory summary generation."""
        # Store various types of memories
        self.memory.store_experience(
            memory_type=MemoryType.EXPERIENCE,
            context={"test": "data"},
            tags={"test"}
        )
        self.memory.store_experience(
            memory_type=MemoryType.INTERACTION,
            context={"test": "data2"},
            tags={"test", "interaction"}
        )
        
        summary = self.memory.get_memory_summary()
        
        self.assertEqual(summary["agent_id"], self.agent_id)
        self.assertEqual(summary["total_memories"], 2)
        self.assertIn("experience", summary["type_distribution"])
        self.assertIn("interaction", summary["type_distribution"])


class TestSemanticMemory(unittest.TestCase):
    """Test semantic memory system."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.agent_id = "test_agent"
        self.memory = SemanticMemory(agent_id=self.agent_id)
    
    def test_store_knowledge(self):
        """Test storing knowledge in semantic memory."""
        content = {"fact": "The sky is blue", "source": "observation"}
        
        knowledge_id = self.memory.store_knowledge(
            knowledge_type=KnowledgeType.FACT,
            content=content,
            confidence=ConfidenceLevel.HIGH,
            source=SourceType.EXPERIENCE,
            tags={"color", "sky"}
        )
        
        self.assertIsNotNone(knowledge_id)
        self.assertEqual(len(self.memory.knowledge), 1)
        
        # Retrieve and verify
        knowledge = self.memory.retrieve_knowledge(knowledge_id)
        self.assertIsNotNone(knowledge)
        self.assertEqual(knowledge.agent_id, self.agent_id)
        self.assertEqual(knowledge.knowledge_type, KnowledgeType.FACT)
        self.assertEqual(knowledge.content, content)
        self.assertEqual(knowledge.confidence, ConfidenceLevel.HIGH)
        self.assertEqual(knowledge.source, SourceType.EXPERIENCE)
        self.assertEqual(knowledge.tags, {"color", "sky"})
    
    def test_create_concept(self):
        """Test concept creation."""
        concept_id = self.memory.create_concept(
            name="Vehicle",
            description="A means of transportation",
            attributes={"wheels": "usually 4", "engine": "optional"},
            metadata={"category": "transport"}
        )
        
        self.assertIsNotNone(concept_id)
        self.assertEqual(len(self.memory.concepts), 1)
        
        # Retrieve and verify
        concept = self.memory.get_concept(concept_id)
        self.assertIsNotNone(concept)
        self.assertEqual(concept.name, "Vehicle")
        self.assertEqual(concept.description, "A means of transportation")
        self.assertEqual(concept.attributes["wheels"], "usually 4")
    
    def test_search_knowledge(self):
        """Test knowledge search functionality."""
        # Store various knowledge items
        self.memory.store_knowledge(
            knowledge_type=KnowledgeType.FACT,
            content={"topic": "math", "fact": "2+2=4"},
            tags={"math", "arithmetic"}
        )
        self.memory.store_knowledge(
            knowledge_type=KnowledgeType.RULE,
            content={"topic": "math", "rule": "commutative property"},
            tags={"math", "algebra"}
        )
        self.memory.store_knowledge(
            knowledge_type=KnowledgeType.FACT,
            content={"topic": "science", "fact": "water boils at 100C"},
            tags={"science", "chemistry"}
        )
        
        # Search by type
        knowledge_items = self.memory.search_knowledge(knowledge_type=KnowledgeType.FACT)
        self.assertEqual(len(knowledge_items), 2)
        
        # Search by tags
        knowledge_items = self.memory.search_knowledge(tags={"math"})
        self.assertEqual(len(knowledge_items), 2)
        
        # Search by content query
        knowledge_items = self.memory.search_knowledge(
            content_query={"topic": "math"}
        )
        self.assertEqual(len(knowledge_items), 2)
    
    def test_knowledge_relevance(self):
        """Test knowledge relevance calculation."""
        # Store knowledge
        knowledge_id = self.memory.store_knowledge(
            knowledge_type=KnowledgeType.FACT,
            content={"animal": "dog", "sound": "bark", "legs": 4}
        )
        
        knowledge = self.memory.retrieve_knowledge(knowledge_id)
        
        # Test relevance calculation
        query = {"animal": "dog", "sound": "bark"}
        relevance = knowledge.calculate_relevance(query)
        
        self.assertGreater(relevance, 0.5)  # Should be relevant
    
    def test_infer_knowledge(self):
        """Test knowledge inference."""
        # Store premise knowledge
        premise1 = self.memory.store_knowledge(
            knowledge_type=KnowledgeType.FACT,
            content={"mammal": "dog", "has_fur": True}
        )
        premise2 = self.memory.store_knowledge(
            knowledge_type=KnowledgeType.FACT,
            content={"mammal": "cat", "has_fur": True}
        )
        
        # Infer new knowledge
        inferred_id = self.memory.infer_knowledge(
            premises=[premise1, premise2],
            inference_type="deduction"
        )
        
        self.assertIsNotNone(inferred_id)
        
        # Verify inferred knowledge
        inferred = self.memory.retrieve_knowledge(inferred_id)
        self.assertEqual(inferred.knowledge_type, KnowledgeType.FACT)
        self.assertEqual(inferred.source, SourceType.INFERENCE)
        self.assertEqual(inferred.confidence, ConfidenceLevel.LOW)


class TestVectorMemory(unittest.TestCase):
    """Test vector memory system."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.agent_id = "test_agent"
        self.memory = VectorMemory(agent_id=self.agent_id)
    
    def test_store_embedding(self):
        """Test storing embeddings in vector memory."""
        vector = np.array([0.1, 0.2, 0.3, 0.4])
        content = "This is a test document"
        
        embedding_id = self.memory.store_embedding(
            vector_type=VectorType.TEXT,
            vector=vector,
            content=content,
            tags={"test", "document"},
            metadata={"length": len(content)}
        )
        
        self.assertIsNotNone(embedding_id)
        self.assertEqual(len(self.memory.embeddings), 1)
        
        # Retrieve and verify
        embedding = self.memory.retrieve_embedding(embedding_id)
        self.assertIsNotNone(embedding)
        self.assertEqual(embedding.agent_id, self.agent_id)
        self.assertEqual(embedding.vector_type, VectorType.TEXT)
        np.testing.assert_array_equal(embedding.vector, vector)
        self.assertEqual(embedding.content, content)
        self.assertEqual(embedding.tags, {"test", "document"})
    
    def test_find_similar(self):
        """Test similarity search."""
        # Store multiple embeddings
        vector1 = np.array([1.0, 0.0, 0.0])
        vector2 = np.array([0.9, 0.1, 0.0])
        vector3 = np.array([0.0, 1.0, 0.0])
        
        self.memory.store_embedding(
            vector_type=VectorType.TEXT,
            vector=vector1,
            content="First document",
            tags={"doc1"}
        )
        self.memory.store_embedding(
            vector_type=VectorType.TEXT,
            vector=vector2,
            content="Similar document",
            tags={"doc2"}
        )
        self.memory.store_embedding(
            vector_type=VectorType.TEXT,
            vector=vector3,
            content="Different document",
            tags={"doc3"}
        )
        
        # Find similar to vector1
        query_vector = np.array([0.95, 0.05, 0.0])
        similar = self.memory.find_similar(
            query_vector=query_vector,
            limit=2
        )
        
        self.assertEqual(len(similar), 2)
        # Should find vector1 and vector2 as most similar
        self.assertIn("First document", [s[0].content for s in similar])
        self.assertIn("Similar document", [s[0].content for s in similar])
    
    def test_find_similar_content(self):
        """Test content-based similarity search."""
        # Store embeddings with different content
        vector = np.array([0.1, 0.2, 0.3])
        
        self.memory.store_embedding(
            vector_type=VectorType.TEXT,
            vector=vector,
            content="The quick brown fox jumps over the lazy dog",
            tags={"fox"}
        )
        self.memory.store_embedding(
            vector_type=VectorType.TEXT,
            vector=vector,
            content="A lazy dog sleeps in the sun",
            tags={"dog"}
        )
        self.memory.store_embedding(
            vector_type=VectorType.TEXT,
            vector=vector,
            content="The weather is sunny today",
            tags={"weather"}
        )
        
        # Search for content similar to "fox"
        similar = self.memory.find_similar_content(
            content="fox brown quick",
            limit=2
        )
        
        self.assertEqual(len(similar), 1)
        self.assertIn("fox", similar[0][0].content)
    
    def test_embedding_normalization(self):
        """Test embedding normalization."""
        vector = np.array([3.0, 4.0, 0.0])  # Magnitude 5
        content = "Test content"
        
        embedding_id = self.memory.store_embedding(
            vector_type=VectorType.TEXT,
            vector=vector,
            content=content
        )
        
        embedding = self.memory.retrieve_embedding(embedding_id)
        normalized = embedding.normalize()
        
        # Check magnitude is 1
        self.assertAlmostEqual(normalized.get_magnitude(), 1.0, places=5)
        
        # Check direction is preserved
        original_unit = vector / np.linalg.norm(vector)
        np.testing.assert_array_almost_equal(normalized.vector, original_unit)
    
    def test_embedding_statistics(self):
        """Test embedding statistics generation."""
        # Store embeddings with different types
        vector = np.array([0.1, 0.2, 0.3])
        
        self.memory.store_embedding(
            vector_type=VectorType.TEXT,
            vector=vector,
            content="Text document",
            tags={"text"}
        )
        self.memory.store_embedding(
            vector_type=VectorType.IMAGE,
            vector=vector,
            content="Image description",
            tags={"image"}
        )
        
        stats = self.memory.get_embedding_statistics()
        
        self.assertEqual(stats["agent_id"], self.agent_id)
        self.assertEqual(stats["total_embeddings"], 2)
        self.assertIn("text", stats["type_distribution"])
        self.assertIn("image", stats["type_distribution"])


class TestMemoryPolicies(unittest.TestCase):
    """Test memory policy system."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.agent_id = "test_agent"
        self.policy_manager = MemoryPolicyManager(agent_id=self.agent_id)
        
        # Create memory systems
        self.episodic_memory = EpisodicMemory(agent_id=self.agent_id)
        self.semantic_memory = SemanticMemory(agent_id=self.agent_id)
        
        # Register memory systems
        self.policy_manager.register_memory_system("episodic", self.episodic_memory)
        self.policy_manager.register_memory_system("semantic", self.semantic_memory)
    
    def test_consolidation_policy(self):
        """Test memory consolidation policy."""
        # Create consolidation policy
        config = PolicyConfig(
            policy_type=PolicyType.CONSOLIDATION,
            trigger=PolicyTrigger.MANUAL,
            parameters={
                "similarity_threshold": 0.8,
                "max_consolidation_size": 5,
                "consolidation_strategy": "merge"
            }
        )
        policy = ConsolidationPolicy(config)
        
        # Add policy to manager
        self.policy_manager.add_policy("test_consolidation", policy)
        
        # Store similar memories
        for i in range(3):
            self.episodic_memory.store_experience(
                memory_type=MemoryType.EXPERIENCE,
                context={"location": "office", "activity": "meeting"},
                tags={"work", "meeting"}
            )
        
        # Execute policy
        results = self.policy_manager.execute_policies(["test_consolidation"])
        
        self.assertTrue(results["total_policies_executed"] > 0)
        self.assertIn("test_consolidation", results["results"])
    
    def test_forgetting_policy(self):
        """Test memory forgetting policy."""
        # Create forgetting policy
        config = PolicyConfig(
            policy_type=PolicyType.FORGETTING,
            trigger=PolicyTrigger.MANUAL,
            parameters={
                "forgetting_strategy": "importance_based",
                "retention_threshold": 0.3,
                "max_forget_percentage": 0.5
            }
        )
        policy = ForgettingPolicy(config)
        
        # Add policy to manager
        self.policy_manager.add_policy("test_forgetting", policy)
        
        # Store memories with different priorities
        for i in range(5):
            priority = MemoryPriority.LOW if i < 3 else MemoryPriority.HIGH
            self.episodic_memory.store_experience(
                memory_type=MemoryType.EXPERIENCE,
                context={"test": f"memory_{i}"},
                priority=priority
            )
        
        # Execute policy
        results = self.policy_manager.execute_policies(["test_forgetting"])
        
        self.assertTrue(results["total_policies_executed"] > 0)
        self.assertIn("test_forgetting", results["results"])
    
    def test_policy_manager_statistics(self):
        """Test policy manager statistics."""
        # Create and add policies
        consolidation_config = PolicyConfig(
            policy_type=PolicyType.CONSOLIDATION,
            trigger=PolicyTrigger.MANUAL
        )
        consolidation_policy = ConsolidationPolicy(consolidation_config)
        self.policy_manager.add_policy("consolidation", consolidation_policy)
        
        forgetting_config = PolicyConfig(
            policy_type=PolicyType.FORGETTING,
            trigger=PolicyTrigger.MANUAL
        )
        forgetting_policy = ForgettingPolicy(forgetting_config)
        self.policy_manager.add_policy("forgetting", forgetting_policy)
        
        # Get statistics
        stats = self.policy_manager.get_policy_statistics()
        
        self.assertEqual(stats["agent_id"], self.agent_id)
        self.assertEqual(stats["total_policies"], 2)
        self.assertIn("consolidation", stats["policies"])
        self.assertIn("forgetting", stats["policies"])
    
    def test_default_policies(self):
        """Test creation of default policies."""
        self.policy_manager.create_default_policies()
        
        stats = self.policy_manager.get_policy_statistics()
        self.assertEqual(stats["total_policies"], 2)
        self.assertIn("default_consolidation", stats["policies"])
        self.assertIn("default_forgetting", stats["policies"])


class TestMemoryIntegration(unittest.TestCase):
    """Test integration between memory systems."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.agent_id = "test_agent"
        self.episodic_memory = EpisodicMemory(agent_id=self.agent_id)
        self.semantic_memory = SemanticMemory(agent_id=self.agent_id)
        self.vector_memory = VectorMemory(agent_id=self.agent_id)
        self.policy_manager = MemoryPolicyManager(agent_id=self.agent_id)
        
        # Register all memory systems
        self.policy_manager.register_memory_system("episodic", self.episodic_memory)
        self.policy_manager.register_memory_system("semantic", self.semantic_memory)
        self.policy_manager.register_memory_system("vector", self.vector_memory)
    
    def test_cross_memory_operations(self):
        """Test operations that span multiple memory systems."""
        # Store experience in episodic memory
        experience_id = self.episodic_memory.store_experience(
            memory_type=MemoryType.LEARNING,
            context={"subject": "math", "topic": "algebra"},
            action="learned_equation",
            outcome={"success": True, "time_taken": 30}
        )
        
        # Store related knowledge in semantic memory
        knowledge_id = self.semantic_memory.store_knowledge(
            knowledge_type=KnowledgeType.FACT,
            content={"equation": "x + y = z", "subject": "math"},
            tags={"math", "algebra", "equation"}
        )
        
        # Store vector embedding
        vector = np.array([0.1, 0.2, 0.3])
        embedding_id = self.vector_memory.store_embedding(
            vector_type=VectorType.TEXT,
            vector=vector,
            content="Algebraic equations involve variables and constants",
            tags={"math", "algebra"}
        )
        
        # Verify all memories are stored
        self.assertIsNotNone(self.episodic_memory.retrieve_experience(experience_id))
        self.assertIsNotNone(self.semantic_memory.retrieve_knowledge(knowledge_id))
        self.assertIsNotNone(self.vector_memory.retrieve_embedding(embedding_id))
    
    def test_memory_policy_integration(self):
        """Test memory policies with all memory systems."""
        # Create default policies
        self.policy_manager.create_default_policies()
        
        # Populate memory systems
        for i in range(10):
            self.episodic_memory.store_experience(
                memory_type=MemoryType.EXPERIENCE,
                context={"test": f"memory_{i}"},
                priority=MemoryPriority.LOW if i < 5 else MemoryPriority.HIGH
            )
        
        # Execute policies
        results = self.policy_manager.execute_policies()
        
        self.assertTrue(results["total_policies_executed"] > 0)
        self.assertIn("default_consolidation", results["results"])
        self.assertIn("default_forgetting", results["results"])


if __name__ == "__main__":
    unittest.main() 