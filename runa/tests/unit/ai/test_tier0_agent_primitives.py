"""
Unit tests for Tier 0: Agent & Cognitive Primitives.

Tests the core agent primitives including Agent, Skill, Task, Goal,
Intention, and related management systems.
"""

import unittest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta
import logging
import threading
import time

from runa.ai.agent.core import (
    Agent, SimpleAgent, Skill, Task, Goal, AgentStatus, SkillLevel
)
from runa.ai.agent.registry import (
    AgentRegistry, AgentGroup, AgentGroupManager, RegistryEvent
)
from runa.ai.agent.lifecycle import (
    AgentLifecycleManager, LifecyclePhase, LifecycleEvent, GracefulShutdown
)
from runa.ai.intention.core import (
    Intention, IntentionManager, IntentionState, RetryStrategy, SimpleIntentionPlanner
)
from runa.ai.intention.retry import (
    RetryPolicy, RetryManager, CircuitBreaker, RetryExecutor,
    FailureType, RecoveryAction, CircuitState, CircuitBreakerOpenError, FailureInfo
)


class TestSkill(unittest.TestCase):
    """Test cases for Skill functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.skill = Skill(
            name="test_skill",
            description="A test skill",
            level=SkillLevel.INTERMEDIATE
        )
    
    def test_skill_creation(self):
        """Test skill creation with valid parameters."""
        self.assertEqual(self.skill.name, "test_skill")
        self.assertEqual(self.skill.description, "A test skill")
        self.assertEqual(self.skill.level, SkillLevel.INTERMEDIATE)
        self.assertEqual(self.skill.usage_count, 0)
        self.assertIsNone(self.skill.last_used)
    
    def test_skill_use(self):
        """Test using a skill updates statistics."""
        initial_count = self.skill.usage_count
        self.skill.use()
        
        self.assertEqual(self.skill.usage_count, initial_count + 1)
        self.assertIsNotNone(self.skill.last_used)
        self.assertIsInstance(self.skill.last_used, datetime)
    
    def test_skill_serialization(self):
        """Test skill serialization and deserialization."""
        self.skill.use()
        skill_dict = self.skill.to_dict()
        
        restored_skill = Skill.from_dict(skill_dict)
        
        self.assertEqual(restored_skill.name, self.skill.name)
        self.assertEqual(restored_skill.description, self.skill.description)
        self.assertEqual(restored_skill.level, self.skill.level)
        self.assertEqual(restored_skill.usage_count, self.skill.usage_count)
        self.assertEqual(restored_skill.last_used, self.skill.last_used)


class TestTask(unittest.TestCase):
    """Test cases for Task functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.task = Task(
            id="task_001",
            name="Test Task",
            description="A test task",
            priority=7,
            estimated_duration=timedelta(minutes=30)
        )
    
    def test_task_creation(self):
        """Test task creation with valid parameters."""
        self.assertEqual(self.task.id, "task_001")
        self.assertEqual(self.task.name, "Test Task")
        self.assertEqual(self.task.priority, 7)
        self.assertEqual(self.task.status, "pending")
        self.assertEqual(self.task.estimated_duration, timedelta(minutes=30))
    
    def test_task_validation(self):
        """Test task validation with invalid parameters."""
        with self.assertRaises(ValueError):
            Task(
                id="invalid",
                name="Invalid",
                description="Invalid task",
                priority=15  # Invalid priority
            )
    
    def test_task_dependencies(self):
        """Test task dependency checking."""
        task1 = Task(id="task1", name="Task 1", description="First task")
        task2 = Task(
            id="task2",
            name="Task 2",
            description="Second task",
            dependencies=["task1"]
        )
        
        # Task2 cannot start without task1 completed
        self.assertFalse(task2.can_start(set()))
        self.assertTrue(task2.can_start({"task1"}))
    
    def test_task_overdue(self):
        """Test task overdue checking."""
        # Create a task with a past deadline by bypassing validation
        overdue_task = Task.__new__(Task)
        overdue_task.id = "overdue"
        overdue_task.name = "Overdue Task"
        overdue_task.description = "Overdue task"
        overdue_task.priority = 5
        overdue_task.status = "pending"
        overdue_task.estimated_duration = timedelta(hours=1)
        overdue_task.dependencies = []
        overdue_task.required_skills = []
        overdue_task.parameters = {}
        overdue_task.deadline = datetime.now() - timedelta(hours=1)
        overdue_task.created_at = datetime.now()
        
        self.assertTrue(overdue_task.is_overdue())
    
    def test_task_serialization(self):
        """Test task serialization and deserialization."""
        task_dict = self.task.to_dict()
        restored_task = Task.from_dict(task_dict)
        
        self.assertEqual(restored_task.id, self.task.id)
        self.assertEqual(restored_task.name, self.task.name)
        self.assertEqual(restored_task.priority, self.task.priority)
        self.assertEqual(restored_task.status, self.task.status)


class TestGoal(unittest.TestCase):
    """Test cases for Goal functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.goal = Goal(
            id="goal_001",
            name="Test Goal",
            description="A test goal",
            priority=8,
            target_date=datetime.now() + timedelta(days=7)
        )
    
    def test_goal_creation(self):
        """Test goal creation with valid parameters."""
        self.assertEqual(self.goal.id, "goal_001")
        self.assertEqual(self.goal.name, "Test Goal")
        self.assertEqual(self.goal.priority, 8)
        self.assertEqual(self.goal.progress, 0.0)
        self.assertEqual(self.goal.status, "active")
    
    def test_goal_progress_update(self):
        """Test goal progress updating."""
        self.goal.update_progress(0.5)
        self.assertEqual(self.goal.progress, 0.5)
        
        self.goal.update_progress(1.0)
        self.assertEqual(self.goal.progress, 1.0)
        self.assertEqual(self.goal.status, "completed")
    
    def test_goal_progress_validation(self):
        """Test goal progress validation."""
        with self.assertRaises(ValueError):
            self.goal.update_progress(1.5)  # Invalid progress
        
        with self.assertRaises(ValueError):
            self.goal.update_progress(-0.1)  # Invalid progress
    
    def test_goal_completion(self):
        """Test goal completion checking."""
        self.assertFalse(self.goal.is_completed())
        
        self.goal.update_progress(1.0)
        self.assertTrue(self.goal.is_completed())
    
    def test_goal_serialization(self):
        """Test goal serialization and deserialization."""
        goal_dict = self.goal.to_dict()
        restored_goal = Goal.from_dict(goal_dict)
        
        self.assertEqual(restored_goal.id, self.goal.id)
        self.assertEqual(restored_goal.name, self.goal.name)
        self.assertEqual(restored_goal.priority, self.goal.priority)
        self.assertEqual(restored_goal.progress, self.goal.progress)


class TestAgent(unittest.TestCase):
    """Test cases for Agent functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.skill = Skill(name="reasoning", description="Logical reasoning")
        self.goal = Goal(id="goal1", name="Complete Task", description="Complete a task")
        self.task = Task(id="task1", name="Test Task", description="A test task")
        
        self.agent = SimpleAgent(
            name="TestAgent",
            description="A test agent",
            skills=[self.skill],
            goals=[self.goal]
        )
    
    def test_agent_creation(self):
        """Test agent creation with valid parameters."""
        self.assertEqual(self.agent.name, "TestAgent")
        self.assertEqual(self.agent.description, "A test agent")
        self.assertEqual(len(self.agent.skills), 1)
        self.assertEqual(len(self.agent.goals), 1)
        self.assertEqual(self.agent.status, AgentStatus.IDLE)
    
    def test_agent_skill_management(self):
        """Test agent skill management."""
        # Test adding skill
        new_skill = Skill(name="planning", description="Task planning")
        self.agent.add_skill(new_skill)
        self.assertEqual(len(self.agent.skills), 2)
        self.assertTrue(self.agent.has_skill("planning"))
        
        # Test using skill
        self.assertTrue(self.agent.use_skill("reasoning"))
        self.assertFalse(self.agent.use_skill("nonexistent"))
        
        # Test removing skill
        self.agent.remove_skill("planning")
        self.assertEqual(len(self.agent.skills), 1)
        self.assertFalse(self.agent.has_skill("planning"))
    
    def test_agent_goal_management(self):
        """Test agent goal management."""
        # Test adding goal
        new_goal = Goal(id="goal2", name="New Goal", description="A new goal")
        self.agent.add_goal(new_goal)
        self.assertEqual(len(self.agent.goals), 2)
        
        # Test updating goal progress
        self.assertTrue(self.agent.update_goal_progress("goal1", 0.5))
        goal = self.agent.get_goal("goal1")
        self.assertEqual(goal.progress, 0.5)
        
        # Test removing goal
        self.agent.remove_goal("goal2")
        self.assertEqual(len(self.agent.goals), 1)
    
    def test_agent_task_management(self):
        """Test agent task management."""
        # Test adding task
        self.agent.add_task(self.task)
        self.assertEqual(len(self.agent.tasks), 1)
        
        # Test updating task status
        self.assertTrue(self.agent.update_task_status("task1", "running"))
        task = self.agent.get_task("task1")
        self.assertEqual(task.status, "running")
        
        # Test removing task
        self.agent.remove_task("task1")
        self.assertEqual(len(self.agent.tasks), 0)
    
    def test_agent_reasoning(self):
        """Test agent reasoning capabilities."""
        context = {"test": "data"}
        result = self.agent.think(context)
        
        self.assertIsInstance(result, dict)
        self.assertIn("goals_analyzed", result)
        self.assertIn("tasks_available", result)
        self.assertIn("recommended_actions", result)
    
    def test_agent_action_execution(self):
        """Test agent action execution."""
        # Test using skill action
        result = self.agent.act("use_skill", {"skill_name": "reasoning"})
        self.assertTrue(result["success"])
        
        # Test invalid action
        result = self.agent.act("invalid_action", {})
        self.assertFalse(result["success"])
        self.assertIn("error", result)
    
    def test_agent_serialization(self):
        """Test agent serialization and deserialization."""
        agent_dict = self.agent.to_dict()
        restored_agent = SimpleAgent.from_dict(agent_dict)
        
        self.assertEqual(restored_agent.name, self.agent.name)
        self.assertEqual(restored_agent.description, self.agent.description)
        self.assertEqual(len(restored_agent.skills), len(self.agent.skills))
        self.assertEqual(len(restored_agent.goals), len(self.agent.goals))


class TestAgentRegistry(unittest.TestCase):
    """Test cases for AgentRegistry functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.registry = AgentRegistry("TestRegistry")
        self.agent = SimpleAgent(name="TestAgent", description="A test agent")
    
    def test_registry_creation(self):
        """Test registry creation."""
        self.assertEqual(self.registry.name, "TestRegistry")
        self.assertEqual(self.registry.get_agent_count(), 0)
    
    def test_agent_registration(self):
        """Test agent registration."""
        # Test successful registration
        self.assertTrue(self.registry.register_agent(self.agent))
        self.assertEqual(self.registry.get_agent_count(), 1)
        
        # Test duplicate registration
        self.assertFalse(self.registry.register_agent(self.agent))
    
    def test_agent_unregistration(self):
        """Test agent unregistration."""
        self.registry.register_agent(self.agent)
        
        # Test successful unregistration
        self.assertTrue(self.registry.unregister_agent(self.agent.agent_id))
        self.assertEqual(self.registry.get_agent_count(), 0)
        
        # Test unregistering non-existent agent
        self.assertFalse(self.registry.unregister_agent("nonexistent"))
    
    def test_agent_discovery(self):
        """Test agent discovery functionality."""
        skill = Skill(name="reasoning", description="Logical reasoning")
        self.agent.add_skill(skill)
        self.registry.register_agent(self.agent)
        
        # Test finding agents by skill
        agents_with_skill = self.registry.find_agents_by_skill("reasoning")
        self.assertEqual(len(agents_with_skill), 1)
        self.assertEqual(agents_with_skill[0].agent_id, self.agent.agent_id)
    
    def test_registry_events(self):
        """Test registry event system."""
        events_received = []
        
        def event_handler(event_data):
            events_received.append(event_data)
        
        self.registry.add_event_listener(RegistryEvent.AGENT_REGISTERED, event_handler)
        self.registry.register_agent(self.agent)
        
        # Wait for event processing
        time.sleep(0.1)
        
        self.assertEqual(len(events_received), 1)
        self.assertEqual(events_received[0].event_type, RegistryEvent.AGENT_REGISTERED)
        self.assertEqual(events_received[0].agent_id, self.agent.agent_id)
    
    def test_registry_summary(self):
        """Test registry summary generation."""
        self.registry.register_agent(self.agent)
        summary = self.registry.get_registry_summary()
        
        self.assertEqual(summary["total_agents"], 1)
        self.assertIn("status_distribution", summary)
        self.assertIn("skill_distribution", summary)
        self.assertIn("goal_distribution", summary)


class TestAgentLifecycleManager(unittest.TestCase):
    """Test cases for AgentLifecycleManager functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.registry = AgentRegistry("TestRegistry")
        self.lifecycle_manager = AgentLifecycleManager(self.registry)
        self.agent = SimpleAgent(name="TestAgent", description="A test agent")
    
    def test_lifecycle_manager_creation(self):
        """Test lifecycle manager creation."""
        self.assertIsNotNone(self.lifecycle_manager)
        self.assertEqual(len(self.lifecycle_manager.agents), 0)
    
    def test_agent_lifecycle_registration(self):
        """Test agent lifecycle registration."""
        # Test successful registration
        self.assertTrue(self.lifecycle_manager.register_agent(self.agent, auto_start=False))
        self.assertEqual(len(self.lifecycle_manager.agents), 1)
        
        # Check initial phase
        phase = self.lifecycle_manager.get_agent_phase(self.agent.agent_id)
        self.assertEqual(phase, LifecyclePhase.CREATED)
    
    def test_agent_lifecycle_start_stop(self):
        """Test agent lifecycle start and stop."""
        self.lifecycle_manager.register_agent(self.agent)
        
        # Test starting agent
        self.assertTrue(self.lifecycle_manager.start_agent(self.agent.agent_id))
        phase = self.lifecycle_manager.get_agent_phase(self.agent.agent_id)
        self.assertEqual(phase, LifecyclePhase.RUNNING)
        
        # Test stopping agent
        self.assertTrue(self.lifecycle_manager.stop_agent(self.agent.agent_id))
        phase = self.lifecycle_manager.get_agent_phase(self.agent.agent_id)
        self.assertEqual(phase, LifecyclePhase.STOPPED)
    
    def test_agent_health_monitoring(self):
        """Test agent health monitoring."""
        self.lifecycle_manager.register_agent(self.agent)
        self.lifecycle_manager.start_agent(self.agent.agent_id)
        
        # Test health status
        health = self.lifecycle_manager.get_agent_health(self.agent.agent_id)
        self.assertIsNotNone(health)
        self.assertTrue(health.is_healthy)
    
    def test_lifecycle_events(self):
        """Test lifecycle event system."""
        events_received = []
        
        def event_handler(event_data):
            events_received.append(event_data)
        
        self.lifecycle_manager.add_lifecycle_listener(LifecycleEvent.AGENT_STARTED, event_handler)
        self.lifecycle_manager.register_agent(self.agent)
        self.lifecycle_manager.start_agent(self.agent.agent_id)
        
        # Wait for event processing
        time.sleep(0.1)
        
        self.assertEqual(len(events_received), 1)
        self.assertEqual(events_received[0].event_type, LifecycleEvent.AGENT_STARTED)
        self.assertEqual(events_received[0].agent_id, self.agent.agent_id)


class TestIntention(unittest.TestCase):
    """Test cases for Intention functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.intention = Intention(
            id="intention_001",
            goal_id="goal_001",
            agent_id="agent_001",
            priority=7,
            retry_strategy=RetryStrategy.EXPONENTIAL_BACKOFF
        )
    
    def test_intention_creation(self):
        """Test intention creation."""
        self.assertEqual(self.intention.id, "intention_001")
        self.assertEqual(self.intention.goal_id, "goal_001")
        self.assertEqual(self.intention.agent_id, "agent_001")
        self.assertEqual(self.intention.state, IntentionState.PENDING)
        self.assertEqual(self.intention.retry_count, 0)
    
    def test_intention_lifecycle(self):
        """Test intention lifecycle transitions."""
        # Test starting intention
        self.intention.start()
        self.assertEqual(self.intention.state, IntentionState.ACTIVE)
        self.assertIsNotNone(self.intention.started_at)
        
        # Test pausing intention
        self.intention.pause()
        self.assertEqual(self.intention.state, IntentionState.PAUSED)
        
        # Test resuming intention
        self.intention.resume()
        self.assertEqual(self.intention.state, IntentionState.ACTIVE)
        
        # Test completing intention
        self.intention.complete()
        self.assertEqual(self.intention.state, IntentionState.COMPLETED)
        self.assertIsNotNone(self.intention.completed_at)
    
    def test_intention_retry_logic(self):
        """Test intention retry logic."""
        self.intention.start()
        self.intention.fail()
        
        # Test retry capability
        self.assertTrue(self.intention.can_retry())
        self.assertTrue(self.intention.should_retry_now())
        
        # Test retry execution
        self.intention.retry()
        self.assertEqual(self.intention.state, IntentionState.ACTIVE)
        self.assertEqual(self.intention.retry_count, 1)
        self.assertEqual(self.intention.current_task_index, 0)
    
    def test_intention_progress(self):
        """Test intention progress tracking."""
        self.intention.plan = ["task1", "task2", "task3"]
        
        # Test initial progress
        self.assertEqual(self.intention.get_progress(), 0.0)
        
        # Test progress after advancing tasks
        self.intention.current_task_index = 1
        self.assertEqual(self.intention.get_progress(), 1/3)
        
        # Test completed progress
        self.intention.current_task_index = 3
        self.assertEqual(self.intention.get_progress(), 1.0)
    
    def test_intention_serialization(self):
        """Test intention serialization."""
        self.intention.start()
        intention_dict = self.intention.to_dict()
        restored_intention = Intention.from_dict(intention_dict)
        
        self.assertEqual(restored_intention.id, self.intention.id)
        self.assertEqual(restored_intention.state, self.intention.state)
        self.assertEqual(restored_intention.retry_count, self.intention.retry_count)


class TestIntentionManager(unittest.TestCase):
    """Test cases for IntentionManager functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.manager = IntentionManager()
    
    def test_intention_creation(self):
        """Test intention creation through manager."""
        intention = self.manager.create_intention(
            goal_id="goal_001",
            agent_id="agent_001",
            priority=8
        )
        
        self.assertIsNotNone(intention)
        self.assertEqual(intention.goal_id, "goal_001")
        self.assertEqual(intention.agent_id, "agent_001")
        self.assertEqual(intention.priority, 8)
    
    def test_intention_retrieval(self):
        """Test intention retrieval."""
        intention = self.manager.create_intention("goal_001", "agent_001")
        
        retrieved = self.manager.get_intention(intention.id)
        self.assertEqual(retrieved.id, intention.id)
        
        # Test non-existent intention
        self.assertIsNone(self.manager.get_intention("nonexistent"))
    
    def test_agent_intentions(self):
        """Test retrieving intentions by agent."""
        intention1 = self.manager.create_intention("goal_001", "agent_001")
        intention2 = self.manager.create_intention("goal_002", "agent_001")
        intention3 = self.manager.create_intention("goal_003", "agent_002")
        
        agent_intentions = self.manager.get_agent_intentions("agent_001")
        self.assertEqual(len(agent_intentions), 2)
        
        # Test with state filter
        intention1.start()
        active_intentions = self.manager.get_agent_intentions("agent_001", IntentionState.ACTIVE)
        self.assertEqual(len(active_intentions), 1)
    
    def test_intention_lifecycle_management(self):
        """Test intention lifecycle management."""
        intention = self.manager.create_intention("goal_001", "agent_001")
        
        # Test starting intention
        self.assertTrue(self.manager.start_intention(intention.id))
        self.assertEqual(intention.state, IntentionState.ACTIVE)
        
        # Test completing intention
        self.assertTrue(self.manager.complete_intention(intention.id))
        self.assertEqual(intention.state, IntentionState.COMPLETED)
    
    def test_retryable_intentions(self):
        """Test retryable intentions functionality."""
        intention = self.manager.create_intention("goal_001", "agent_001")
        intention.start()
        intention.fail()
        
        retryable = self.manager.get_retryable_intentions()
        self.assertEqual(len(retryable), 1)
        self.assertEqual(retryable[0].id, intention.id)


class TestRetrySystem(unittest.TestCase):
    """Test cases for retry system functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.retry_policy = RetryPolicy(max_retries=3)
        self.retry_manager = RetryManager(self.retry_policy)
        self.circuit_breaker = CircuitBreaker(failure_threshold=3)
        self.retry_executor = RetryExecutor(self.retry_policy, self.circuit_breaker)
    
    def test_retry_policy_analysis(self):
        """Test retry policy failure analysis."""
        error = Exception("Connection timeout")
        context = {"operation": "network_call"}
        
        failure_info = self.retry_policy.analyze_failure(error, context)
        
        self.assertEqual(failure_info.failure_type, FailureType.TIMEOUT)
        self.assertEqual(failure_info.recovery_action, RecoveryAction.RETRY)
        self.assertIn("operation", failure_info.context)
    
    def test_retry_delay_calculation(self):
        """Test retry delay calculation."""
        failure_info = FailureInfo(
            failure_type=FailureType.TIMEOUT,
            error_message="Timeout",
            timestamp=datetime.now(),
            retry_count=2
        )
        
        delay = self.retry_policy.get_retry_delay(failure_info)
        self.assertIsInstance(delay, timedelta)
        self.assertGreater(delay.total_seconds(), 0)
    
    def test_circuit_breaker(self):
        """Test circuit breaker functionality."""
        # Test successful calls
        def successful_operation():
            return "success"
        
        result = self.circuit_breaker.call(successful_operation)
        self.assertEqual(result, "success")
        self.assertEqual(self.circuit_breaker.get_state(), CircuitState.CLOSED)
        
        # Test failing calls
        def failing_operation():
            raise Exception("Test failure")
        
        # Should fail but not open circuit yet
        with self.assertRaises(Exception):
            self.circuit_breaker.call(failing_operation)
        
        # After multiple failures, circuit should open
        for _ in range(3):
            with self.assertRaises(Exception):
                self.circuit_breaker.call(failing_operation)
        
        self.assertEqual(self.circuit_breaker.get_state(), CircuitState.OPEN)
        
        # Should raise CircuitBreakerOpenError when open
        with self.assertRaises(CircuitBreakerOpenError):
            self.circuit_breaker.call(successful_operation)
    
    def test_retry_executor(self):
        """Test retry executor functionality."""
        call_count = 0
        
        def flaky_operation():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise Exception("Temporary failure")
            return "success"
        
        # Should succeed after retries
        result = self.retry_executor.execute_with_retry(flaky_operation)
        self.assertEqual(result, "success")
        self.assertEqual(call_count, 3)
    
    def test_retry_executor_permanent_failure(self):
        """Test retry executor with permanent failure."""
        def permanent_failure():
            raise ValueError("Invalid input")
        
        # Should fail immediately for permanent failures
        with self.assertRaises(ValueError):
            self.retry_executor.execute_with_retry(permanent_failure)


class TestIntentionPlanner(unittest.TestCase):
    """Test cases for IntentionPlanner functionality."""
    
    def setUp(self):
        self.planner = SimpleIntentionPlanner()
        self.agent = SimpleAgent(name="TestAgent")

        # Add skills to agent
        setup_skill = Skill(name="setup", description="Setup skills", level=SkillLevel.INTERMEDIATE)
        implement_skill = Skill(name="implement", description="Implementation skills", level=SkillLevel.EXPERT)
        test_skill = Skill(name="test", description="Testing skills", level=SkillLevel.INTERMEDIATE)

        self.agent.add_skill(setup_skill)
        self.agent.add_skill(implement_skill)
        self.agent.add_skill(test_skill)

        self.goal = Goal(id="goal1", name="Complete Project", description="Complete a project")

        # Create tasks with dependencies and required skills
        self.task1 = Task(id="task1", name="Setup", description="Setup project", priority=5, required_skills=["setup"])
        self.task2 = Task(id="task2", name="Implement", description="Implement features", priority=8, dependencies=["task1"], required_skills=["implement"])
        self.task3 = Task(id="task3", name="Test", description="Test implementation", priority=6, dependencies=["task2"], required_skills=["test"])
    
    def test_plan_generation(self):
        """Test plan generation."""
        available_tasks = [self.task1, self.task2, self.task3]
        plan = self.planner.plan_intention(self.goal, self.agent, available_tasks)
        self.assertIsInstance(plan, list)
        self.assertEqual(set(plan), {"task1", "task2", "task3"})
        # Check that dependencies are respected (task1 before task2, task2 before task3)
        task1_index = plan.index("task1")
        task2_index = plan.index("task2")
        task3_index = plan.index("task3")
        self.assertLess(task1_index, task2_index)
        self.assertLess(task2_index, task3_index)
    
    def test_plan_with_no_tasks(self):
        """Test plan generation with no available tasks."""
        plan = self.planner.plan_intention(self.goal, self.agent, [])
        
        self.assertEqual(plan, [])
    
    def test_plan_with_unrelated_tasks(self):
        """Test plan generation with tasks unrelated to goal."""
        unrelated_task = Task(id="unrelated", name="Unrelated", description="Unrelated task")
        
        plan = self.planner.plan_intention(self.goal, self.agent, [unrelated_task])
        
        # Should filter out unrelated tasks
        self.assertEqual(plan, [])


if __name__ == "__main__":
    # Configure logging for tests
    logging.basicConfig(level=logging.WARNING)
    
    # Run all tests
    unittest.main(verbosity=2) 