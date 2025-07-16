"""
Unit tests for Tier 1: Learning Systems.

Tests the supervised learning, reinforcement learning,
and learning system integration.
"""

import unittest
import numpy as np
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

from runa.ai.learning.core import (
    LearningSystem, LearningMethod, LearningExample, LearningSession,
    LearningType, LearningState, SupervisedLearning, ReinforcementLearning
)
from runa.ai.memory.episodic import (
    EpisodicMemory, MemoryType, MemoryPriority
)
from runa.ai.memory.semantic import (
    SemanticMemory, KnowledgeType, ConfidenceLevel, SourceType
)


class TestLearningExample(unittest.TestCase):
    """Test learning example functionality."""
    
    def test_example_creation(self):
        """Test creating learning examples."""
        input_data = {"feature1": 1.0, "feature2": 2.0}
        expected_output = {"prediction": "positive"}
        reward = 1.0
        
        example = LearningExample(
            id="test_example",
            input_data=input_data,
            expected_output=expected_output,
            reward=reward
        )
        
        self.assertEqual(example.id, "test_example")
        self.assertEqual(example.input_data, input_data)
        self.assertEqual(example.expected_output, expected_output)
        self.assertEqual(example.reward, reward)
        self.assertIsInstance(example.timestamp, datetime)
    
    def test_error_calculation(self):
        """Test error calculation between expected and actual output."""
        example = LearningExample(
            id="test_example",
            input_data={"feature1": 1.0},
            expected_output={"value": 5.0},
            actual_output={"value": 3.0}
        )
        
        error = example.calculate_error()
        self.assertEqual(error, 2.0)  # |5.0 - 3.0| = 2.0
    
    def test_error_calculation_no_outputs(self):
        """Test error calculation when outputs are missing."""
        example = LearningExample(
            id="test_example",
            input_data={"feature1": 1.0}
        )
        
        error = example.calculate_error()
        self.assertEqual(error, 0.0)


class TestLearningSession(unittest.TestCase):
    """Test learning session functionality."""
    
    def test_session_creation(self):
        """Test creating learning sessions."""
        session = LearningSession(
            id="test_session",
            learning_type=LearningType.SUPERVISED,
            agent_id="test_agent"
        )
        
        self.assertEqual(session.id, "test_session")
        self.assertEqual(session.learning_type, LearningType.SUPERVISED)
        self.assertEqual(session.agent_id, "test_agent")
        self.assertEqual(session.state, LearningState.IDLE)
        self.assertEqual(len(session.examples), 0)
    
    def test_add_example(self):
        """Test adding examples to sessions."""
        session = LearningSession(
            id="test_session",
            learning_type=LearningType.SUPERVISED,
            agent_id="test_agent"
        )
        
        example = LearningExample(
            id="example1",
            input_data={"feature": 1.0},
            expected_output={"prediction": "positive"}
        )
        
        session.add_example(example)
        self.assertEqual(len(session.examples), 1)
        self.assertEqual(session.examples[0].id, "example1")
    
    def test_session_duration(self):
        """Test session duration calculation."""
        session = LearningSession(
            id="test_session",
            learning_type=LearningType.SUPERVISED,
            agent_id="test_agent"
        )
        
        # Duration should be None before end_time is set
        self.assertIsNone(session.get_duration())
        
        # Set end time
        session.end_time = datetime.now()
        duration = session.get_duration()
        self.assertIsInstance(duration, timedelta)
        self.assertGreaterEqual(duration.total_seconds(), 0)
    
    def test_performance_calculation(self):
        """Test performance metrics calculation."""
        session = LearningSession(
            id="test_session",
            learning_type=LearningType.SUPERVISED,
            agent_id="test_agent"
        )
        
        # Add examples with different characteristics
        example1 = LearningExample(
            id="example1",
            input_data={"feature": 1.0},
            expected_output={"value": 5.0},
            actual_output={"value": 4.0},
            reward=1.0
        )
        example2 = LearningExample(
            id="example2",
            input_data={"feature": 2.0},
            expected_output={"value": 10.0},
            actual_output={"value": 12.0},
            reward=0.5
        )
        
        session.add_example(example1)
        session.add_example(example2)
        
        performance = session.calculate_performance()
        
        self.assertEqual(performance["total_examples"], 2)
        self.assertEqual(performance["successful_examples"], 2)
        self.assertEqual(performance["success_rate"], 1.0)
        self.assertEqual(performance["average_error"], 1.5)  # (1.0 + 2.0) / 2
        self.assertEqual(performance["average_reward"], 0.75)  # (1.0 + 0.5) / 2


class TestSupervisedLearning(unittest.TestCase):
    """Test supervised learning method."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.learner = SupervisedLearning()
    
    def test_learn_from_examples(self):
        """Test learning from supervised examples."""
        examples = [
            LearningExample(
                id="ex1",
                input_data={"color": "red", "size": "large"},
                expected_output={"category": "fruit"}
            ),
            LearningExample(
                id="ex2",
                input_data={"color": "red", "size": "small"},
                expected_output={"category": "berry"}
            ),
            LearningExample(
                id="ex3",
                input_data={"color": "red", "size": "large"},
                expected_output={"category": "fruit"}
            )
        ]
        
        result = self.learner.learn(examples)
        
        self.assertTrue(result["success"])
        self.assertEqual(result["learned_examples"], 3)
        self.assertGreater(result["total_patterns"], 0)
    
    def test_predict_with_learned_patterns(self):
        """Test making predictions with learned patterns."""
        # Learn from examples
        examples = [
            LearningExample(
                id="ex1",
                input_data={"color": "red", "size": "large"},
                expected_output={"category": "fruit"}
            ),
            LearningExample(
                id="ex2",
                input_data={"color": "red", "size": "large"},
                expected_output={"category": "fruit"}
            )
        ]
        self.learner.learn(examples)
        
        # Make prediction
        prediction = self.learner.predict({"color": "red", "size": "large"})
        
        self.assertIn("category", prediction)
        self.assertEqual(prediction["category"], "fruit")
    
    def test_predict_unknown_pattern(self):
        """Test prediction for unknown patterns."""
        prediction = self.learner.predict({"color": "blue", "size": "medium"})
        
        self.assertIn("prediction", prediction)
        self.assertEqual(prediction["prediction"], "unknown")
        self.assertEqual(prediction["confidence"], 0.0)
    
    def test_evaluate_performance(self):
        """Test performance evaluation."""
        # Train on some examples
        train_examples = [
            LearningExample(
                id="train1",
                input_data={"color": "red"},
                expected_output={"category": "fruit"}
            ),
            LearningExample(
                id="train2",
                input_data={"color": "green"},
                expected_output={"category": "vegetable"}
            )
        ]
        self.learner.learn(train_examples)
        
        # Test on similar examples
        test_examples = [
            LearningExample(
                id="test1",
                input_data={"color": "red"},
                expected_output={"category": "fruit"}
            ),
            LearningExample(
                id="test2",
                input_data={"color": "green"},
                expected_output={"category": "vegetable"}
            )
        ]
        
        performance = self.learner.evaluate(test_examples)
        
        self.assertIn("accuracy", performance)
        self.assertIn("error_rate", performance)
        self.assertIn("average_error", performance)
        self.assertGreaterEqual(performance["accuracy"], 0.0)
        self.assertLessEqual(performance["accuracy"], 1.0)


class TestReinforcementLearning(unittest.TestCase):
    """Test reinforcement learning method."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.learner = ReinforcementLearning()
    
    def test_learn_from_examples(self):
        """Test learning from reinforcement examples."""
        examples = [
            LearningExample(
                id="ex1",
                input_data={"state": "hungry", "action": "eat"},
                reward=1.0
            ),
            LearningExample(
                id="ex2",
                input_data={"state": "hungry", "action": "sleep"},
                reward=-0.5
            ),
            LearningExample(
                id="ex3",
                input_data={"state": "hungry", "action": "eat"},
                reward=1.0
            )
        ]
        
        result = self.learner.learn(examples)
        
        self.assertTrue(result["success"])
        self.assertEqual(result["updated_actions"], 3)
        self.assertGreater(result["total_states"], 0)
        self.assertGreater(result["average_reward"], 0)
    
    def test_predict_optimal_action(self):
        """Test predicting optimal actions."""
        # Learn from examples
        examples = [
            LearningExample(
                id="ex1",
                input_data={"state": "hungry", "action": "eat"},
                reward=1.0
            ),
            LearningExample(
                id="ex2",
                input_data={"state": "hungry", "action": "sleep"},
                reward=-0.5
            )
        ]
        self.learner.learn(examples)
        
        # Predict action for known state
        prediction = self.learner.predict({"state": "hungry"})
        
        self.assertIn("action", prediction)
        self.assertIn("value", prediction)
        self.assertIn("confidence", prediction)
    
    def test_predict_unknown_state(self):
        """Test prediction for unknown states."""
        prediction = self.learner.predict({"state": "unknown_state"})
        
        self.assertIn("action", prediction)
        self.assertEqual(prediction["action"], "explore")
        self.assertEqual(prediction["confidence"], 0.0)
    
    def test_evaluate_performance(self):
        """Test performance evaluation."""
        # Train on some examples
        train_examples = [
            LearningExample(
                id="train1",
                input_data={"state": "hungry", "action": "eat"},
                reward=1.0
            ),
            LearningExample(
                id="train2",
                input_data={"state": "tired", "action": "sleep"},
                reward=1.0
            )
        ]
        self.learner.learn(train_examples)
        
        # Test on similar examples
        test_examples = [
            LearningExample(
                id="test1",
                input_data={"state": "hungry", "action": "eat"},
                reward=1.0
            ),
            LearningExample(
                id="test2",
                input_data={"state": "tired", "action": "sleep"},
                reward=1.0
            )
        ]
        
        performance = self.learner.evaluate(test_examples)
        
        self.assertIn("total_reward", performance)
        self.assertIn("average_reward", performance)
        self.assertIn("optimality_rate", performance)
        self.assertGreaterEqual(performance["total_reward"], 0)
        self.assertGreaterEqual(performance["average_reward"], 0)


class TestLearningSystem(unittest.TestCase):
    """Test learning system integration."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.agent_id = "test_agent"
        self.learning_system = LearningSystem(agent_id=self.agent_id)
        
        # Create memory systems
        self.episodic_memory = EpisodicMemory(agent_id=self.agent_id)
        self.semantic_memory = SemanticMemory(agent_id=self.agent_id)
        
        # Register memory systems
        self.learning_system.register_memory_systems(
            self.episodic_memory,
            self.semantic_memory
        )
        
        # Create default learning methods
        self.learning_system.create_default_methods()
    
    def test_add_learning_methods(self):
        """Test adding learning methods to the system."""
        supervised_learner = SupervisedLearning()
        reinforcement_learner = ReinforcementLearning()
        
        self.learning_system.add_learning_method(supervised_learner)
        self.learning_system.add_learning_method(reinforcement_learner)
        
        stats = self.learning_system.get_learning_statistics()
        self.assertEqual(stats["total_methods"], 2)
        self.assertIn("supervised_learner", stats["methods"])
        self.assertIn("reinforcement_learner", stats["methods"])
    
    def test_learning_session_lifecycle(self):
        """Test complete learning session lifecycle."""
        # Start session
        session_id = self.learning_system.start_learning_session(
            LearningType.SUPERVISED
        )
        
        self.assertIsNotNone(session_id)
        self.assertEqual(len(self.learning_system.active_sessions), 1)
        
        # Add examples
        example_id1 = self.learning_system.add_example_to_session(
            session_id=session_id,
            input_data={"feature": 1.0},
            expected_output={"prediction": "positive"}
        )
        example_id2 = self.learning_system.add_example_to_session(
            session_id=session_id,
            input_data={"feature": 2.0},
            expected_output={"prediction": "negative"}
        )
        
        self.assertIsNotNone(example_id1)
        self.assertIsNotNone(example_id2)
        
        # Complete session
        result = self.learning_system.complete_learning_session(session_id)
        
        self.assertTrue(result["success"])
        self.assertEqual(len(self.learning_system.active_sessions), 0)
        self.assertEqual(len(self.learning_system.completed_sessions), 1)
    
    def test_learn_from_experience(self):
        """Test learning directly from experience data."""
        examples = [
            {
                "input": {"feature": 1.0},
                "output": {"prediction": "positive"},
                "reward": 1.0
            },
            {
                "input": {"feature": 2.0},
                "output": {"prediction": "negative"},
                "reward": 0.0
            }
        ]
        
        result = self.learning_system.learn_from_experience(
            LearningType.SUPERVISED,
            examples
        )
        
        self.assertTrue(result["success"])
        self.assertIn("learned_examples", result)
    
    def test_prediction_with_method(self):
        """Test making predictions using specific learning methods."""
        # Add supervised learner with unique name
        supervised_learner = SupervisedLearning(name="custom_learner")
        self.learning_system.add_learning_method(supervised_learner)
        
        # Train the learner
        examples = [
            LearningExample(
                id="ex1",
                input_data={"color": "red"},
                expected_output={"category": "fruit"}
            )
        ]
        supervised_learner.learn(examples)
        
        # Make prediction
        prediction = self.learning_system.predict(
            "custom_learner",
            {"color": "red"}
        )
        
        self.assertIn("category", prediction)
        self.assertEqual(prediction["category"], "fruit")
    
    def test_method_evaluation(self):
        """Test evaluating learning methods."""
        # Add supervised learner
        supervised_learner = SupervisedLearning()
        self.learning_system.add_learning_method(supervised_learner)
        
        # Train the learner
        train_examples = [
            LearningExample(
                id="train1",
                input_data={"feature": 1.0},
                expected_output={"prediction": "positive"}
            )
        ]
        supervised_learner.learn(train_examples)
        
        # Evaluate
        test_examples = [
            {
                "input": {"feature": 1.0},
                "output": {"prediction": "positive"}
            }
        ]
        
        evaluation = self.learning_system.evaluate_method(
            "supervised_learner",
            test_examples
        )
        
        self.assertIn("accuracy", evaluation)
        self.assertIn("error_rate", evaluation)
        self.assertIn("average_error", evaluation)
    
    def test_create_default_methods(self):
        """Test creation of default learning methods."""
        self.learning_system.create_default_methods()
        
        stats = self.learning_system.get_learning_statistics()
        self.assertEqual(stats["total_methods"], 2)
        self.assertIn("supervised_learner", stats["methods"])
        self.assertIn("reinforcement_learner", stats["methods"])
    
    def test_memory_integration(self):
        """Test integration with memory systems."""
        # Create default methods
        self.learning_system.create_default_methods()
        
        # Learn from experience
        examples = [
            {
                "input": {"feature": 1.0},
                "output": {"prediction": "positive"},
                "reward": 1.0
            }
        ]
        
        result = self.learning_system.learn_from_experience(
            LearningType.SUPERVISED,
            examples
        )
        
        self.assertTrue(result["success"])
        
        # Check that learning experience was stored in episodic memory
        experiences = self.episodic_memory.search_experiences(
            memory_type=MemoryType.LEARNING
        )
        self.assertGreater(len(experiences), 0)
        
        # Check that learned knowledge was stored in semantic memory
        knowledge_items = self.semantic_memory.search_knowledge(
            knowledge_type=KnowledgeType.PROCEDURE
        )
        self.assertGreater(len(knowledge_items), 0)


class TestLearningIntegration(unittest.TestCase):
    """Test integration between learning and memory systems."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.agent_id = "test_agent"
        self.learning_system = LearningSystem(agent_id=self.agent_id)
        self.episodic_memory = EpisodicMemory(agent_id=self.agent_id)
        self.semantic_memory = SemanticMemory(agent_id=self.agent_id)
        
        # Register memory systems
        self.learning_system.register_memory_systems(
            self.episodic_memory,
            self.semantic_memory
        )
        
        # Create default learning methods
        self.learning_system.create_default_methods()
    
    def test_end_to_end_learning(self):
        """Test complete end-to-end learning process."""
        # Start supervised learning session
        session_id = self.learning_system.start_learning_session(
            LearningType.SUPERVISED
        )
        
        # Add training examples
        for i in range(5):
            self.learning_system.add_example_to_session(
                session_id=session_id,
                input_data={"feature": i, "category": "A" if i < 3 else "B"},
                expected_output={"prediction": "positive" if i < 3 else "negative"}
            )
        
        # Complete learning session
        result = self.learning_system.complete_learning_session(session_id)
        
        self.assertTrue(result["success"])
        self.assertIn("learned_examples", result)
        self.assertGreater(result["learned_examples"], 0)
        
        # Test prediction
        prediction = self.learning_system.predict(
            "supervised_learner",
            {"feature": 1, "category": "A"}
        )
        
        self.assertIsNotNone(prediction)
        self.assertIn("prediction", prediction)
    
    def test_reinforcement_learning_cycle(self):
        """Test reinforcement learning cycle."""
        # Start reinforcement learning session
        session_id = self.learning_system.start_learning_session(
            LearningType.REINFORCEMENT
        )
        
        # Add reinforcement examples
        for i in range(3):
            self.learning_system.add_example_to_session(
                session_id=session_id,
                input_data={"state": f"state_{i}", "action": "action_A"},
                reward=1.0 if i < 2 else 0.0
            )
        
        # Complete learning session
        result = self.learning_system.complete_learning_session(session_id)
        
        self.assertTrue(result["success"])
        self.assertIn("updated_actions", result)
        self.assertGreater(result["updated_actions"], 0)
        
        # Test action prediction
        prediction = self.learning_system.predict(
            "reinforcement_learner",
            {"state": "state_0"}
        )
        
        self.assertIsNotNone(prediction)
        self.assertIn("action", prediction)
    
    def test_learning_statistics_tracking(self):
        """Test learning statistics tracking."""
        # Perform multiple learning sessions
        for i in range(3):
            session_id = self.learning_system.start_learning_session(
                LearningType.SUPERVISED
            )
            
            self.learning_system.add_example_to_session(
                session_id=session_id,
                input_data={"feature": i},
                expected_output={"prediction": "positive"}
            )
            
            self.learning_system.complete_learning_session(session_id)
        
        # Check statistics
        stats = self.learning_system.get_learning_statistics()
        
        self.assertEqual(stats["total_sessions"], 3)
        self.assertEqual(stats["completed_sessions"], 3)
        self.assertEqual(stats["active_sessions"], 0)
        self.assertGreater(stats["statistics"]["total_examples"], 0)
        self.assertGreater(stats["statistics"]["successful_learning"], 0)


if __name__ == "__main__":
    unittest.main() 