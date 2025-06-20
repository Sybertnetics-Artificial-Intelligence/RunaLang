#!/usr/bin/env python3
"""
Test script for Runa Training Data Generator

Demonstrates the training data generation framework functionality.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from runa.training_data_generator import RunaTrainingDataGenerator


def test_basic_examples():
    """Test basic example generation."""
    print("Testing basic example generation...")
    generator = RunaTrainingDataGenerator("test_training_data")
    
    # Generate a small set of basic examples
    examples = generator.generate_basic_examples(100)
    print(f"Generated {len(examples)} basic examples")
    
    # Show a few examples
    for i, example in enumerate(examples[:3]):
        print(f"\nExample {i + 1}:")
        print(f"  Natural Language: {example.natural_language}")
        print(f"  Runa Code: {example.runa_code}")
        print(f"  Complexity: {example.complexity.value}")
        print(f"  Domain: {example.domain.value}")
    
    return examples


def test_ai_specific_examples():
    """Test AI-specific example generation."""
    print("\nTesting AI-specific example generation...")
    generator = RunaTrainingDataGenerator("test_training_data")
    
    # Generate AI-specific examples
    examples = generator.generate_ai_specific_examples(50)
    print(f"Generated {len(examples)} AI-specific examples")
    
    # Show a few examples
    for i, example in enumerate(examples[:3]):
        print(f"\nAI Example {i + 1}:")
        print(f"  Natural Language: {example.natural_language}")
        print(f"  Runa Code: {example.runa_code}")
        print(f"  Tags: {example.tags}")
    
    return examples


def test_domain_specific_examples():
    """Test domain-specific example generation."""
    print("\nTesting domain-specific example generation...")
    generator = RunaTrainingDataGenerator("test_training_data")
    
    # Generate domain-specific examples
    examples = generator.generate_domain_specific_examples(100)
    print(f"Generated {len(examples)} domain-specific examples")
    
    # Count by domain
    domain_counts = {}
    for example in examples:
        domain = example.domain.value
        domain_counts[domain] = domain_counts.get(domain, 0) + 1
    
    print("Domain distribution:")
    for domain, count in domain_counts.items():
        print(f"  {domain}: {count} examples")
    
    return examples


def test_progressive_complexity():
    """Test progressive complexity sequence generation."""
    print("\nTesting progressive complexity sequences...")
    generator = RunaTrainingDataGenerator("test_training_data")
    
    # Generate progressive complexity sequences
    examples = generator.generate_progressive_complexity_sequences(20)
    print(f"Generated {len(examples)} progressive complexity examples")
    
    # Show complexity distribution
    complexity_counts = {}
    for example in examples:
        complexity = example.complexity.value
        complexity_counts[complexity] = complexity_counts.get(complexity, 0) + 1
    
    print("Complexity distribution:")
    for complexity, count in complexity_counts.items():
        print(f"  {complexity}: {count} examples")
    
    return examples


def test_quality_validation():
    """Test quality validation."""
    print("\nTesting quality validation...")
    generator = RunaTrainingDataGenerator("test_training_data")
    
    # Create some test examples
    from runa.training_data_generator import TrainingExample, ComplexityLevel, DomainType
    
    # Valid example
    valid_example = TrainingExample(
        id="test_valid",
        natural_language="Define a variable called counter containing 0",
        runa_code="Let counter be 0",
        complexity=ComplexityLevel.BEGINNER,
        domain=DomainType.GENERAL,
        tags=["variable", "declaration"],
        description="Test valid example"
    )
    
    # Invalid example (unbalanced parentheses)
    invalid_example = TrainingExample(
        id="test_invalid",
        natural_language="Create a function with parameters",
        runa_code="Process function taking (param1, param2",  # Missing closing parenthesis
        complexity=ComplexityLevel.BEGINNER,
        domain=DomainType.GENERAL,
        tags=["function", "parameters"],
        description="Test invalid example"
    )
    
    # Test validation
    valid_result = generator.validate_example_quality(valid_example)
    invalid_result = generator.validate_example_quality(invalid_example)
    
    print(f"Valid example validation: {valid_result}")
    print(f"Invalid example validation: {invalid_result}")
    
    return valid_result, invalid_result


def test_complete_dataset():
    """Test complete dataset generation (small scale)."""
    print("\nTesting complete dataset generation...")
    generator = RunaTrainingDataGenerator("test_training_data")
    
    # Generate a small complete dataset
    dataset = generator.generate_complete_dataset(1000)  # Small scale for testing
    print(f"Generated complete dataset with {dataset.total_examples} examples")
    
    # Show dataset statistics
    print(f"Dataset name: {dataset.name}")
    print(f"Dataset version: {dataset.version}")
    print(f"Complexity distribution: {dataset.complexity_distribution}")
    print(f"Domain distribution: {dataset.domain_distribution}")
    
    # Save dataset
    filepath = generator.save_dataset(dataset, "test_dataset.json")
    print(f"Dataset saved to: {filepath}")
    
    return dataset


def main():
    """Run all tests."""
    print("=== Runa Training Data Generator Test ===\n")
    
    try:
        # Test basic examples
        basic_examples = test_basic_examples()
        
        # Test AI-specific examples
        ai_examples = test_ai_specific_examples()
        
        # Test domain-specific examples
        domain_examples = test_domain_specific_examples()
        
        # Test progressive complexity
        progressive_examples = test_progressive_complexity()
        
        # Test quality validation
        valid_result, invalid_result = test_quality_validation()
        
        # Test complete dataset
        dataset = test_complete_dataset()
        
        print("\n=== Test Results Summary ===")
        print(f"✅ Basic examples: {len(basic_examples)} generated")
        print(f"✅ AI-specific examples: {len(ai_examples)} generated")
        print(f"✅ Domain-specific examples: {len(domain_examples)} generated")
        print(f"✅ Progressive complexity: {len(progressive_examples)} generated")
        print(f"✅ Quality validation: Valid={valid_result}, Invalid={invalid_result}")
        print(f"✅ Complete dataset: {dataset.total_examples} examples")
        
        print("\n🎉 All tests passed! Training data generator is working correctly.")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main()) 