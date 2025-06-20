"""
Runa Training Data Generator - Production-Ready Framework

Generates comprehensive training data for LLM training:
- 100,000+ Runa code examples
- 10,000+ natural language to Runa translation pairs
- Progressive complexity training sequences
- Domain-specific examples (AI, web dev, data science)
- Quality validation and filtering
"""

import random
import json
import os
from typing import List, Dict, Tuple, Optional, Set
from dataclasses import dataclass, asdict
from enum import Enum
import re


class ComplexityLevel(Enum):
    """Training data complexity levels."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class DomainType(Enum):
    """Domain-specific training categories."""
    GENERAL = "general"
    AI_ML = "ai_ml"
    WEB_DEVELOPMENT = "web_development"
    DATA_SCIENCE = "data_science"
    SYSTEM_PROGRAMMING = "system_programming"
    ALGORITHMS = "algorithms"
    API_INTEGRATION = "api_integration"


@dataclass
class TrainingExample:
    """Individual training example with metadata."""
    id: str
    natural_language: str
    runa_code: str
    complexity: ComplexityLevel
    domain: DomainType
    tags: List[str]
    description: str
    validation_status: bool = True
    generated_at: Optional[str] = None


@dataclass
class TrainingDataset:
    """Complete training dataset with metadata."""
    name: str
    version: str
    total_examples: int
    complexity_distribution: Dict[str, int]
    domain_distribution: Dict[str, int]
    examples: List[TrainingExample]
    metadata: Dict[str, any]


class RunaTrainingDataGenerator:
    """
    Production-ready training data generator for Runa language.
    
    Generates:
    - 100,000+ Runa code examples
    - 10,000+ natural language to Runa translation pairs
    - Progressive complexity sequences
    - Domain-specific examples
    - Quality validation and filtering
    """
    
    def __init__(self, output_dir: str = "training_data"):
        self.output_dir = output_dir
        self.examples_generated = 0
        self.translation_pairs = 0
        self.quality_metrics = {
            "valid_syntax": 0,
            "semantic_correctness": 0,
            "complexity_appropriate": 0,
            "domain_relevant": 0
        }
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(os.path.join(output_dir, "examples"), exist_ok=True)
        os.makedirs(os.path.join(output_dir, "translations"), exist_ok=True)
        os.makedirs(os.path.join(output_dir, "validation"), exist_ok=True)
        
        # Initialize example templates
        self._initialize_templates()
    
    def _initialize_templates(self):
        """Initialize comprehensive example templates."""
        self.basic_templates = {
            "variable_declaration": [
                ("Define a variable called {name} containing {value}", 
                 "Let {name} be {value}"),
                ("Create a variable named {name} with value {value}", 
                 "Set {name} to {value}"),
                ("Initialize {name} as {value}", 
                 "Define {name} as {value}")
            ],
            "function_definition": [
                ("Create a function called {name} that takes {params} and returns {return_type}", 
                 "Process called {name} that takes {params} and returns {return_type}"),
                ("Define a function named {name} with parameters {params}", 
                 "Define process {name} taking {params}"),
                ("Write a function {name} that accepts {params}", 
                 "Process {name} accepting {params}")
            ],
            "conditional_statement": [
                ("If {condition} then {action} otherwise {else_action}", 
                 "If {condition} then {action} otherwise {else_action}"),
                ("Check if {condition} and do {action} else {else_action}", 
                 "If {condition} then {action} otherwise {else_action}"),
                ("When {condition} is true, {action}, else {else_action}", 
                 "If {condition} then {action} otherwise {else_action}")
            ],
            "loop_statement": [
                ("For each {item} in {collection}, do {action}", 
                 "For each {item} in {collection}, {action}"),
                ("Loop through {collection} and for each {item} perform {action}", 
                 "For each {item} in {collection}, {action}"),
                ("Iterate over {collection} and execute {action} for each {item}", 
                 "For each {item} in {collection}, {action}")
            ]
        }
        
        self.ai_specific_templates = {
            "reasoning_block": [
                ("Start reasoning about {topic} and consider {aspects}", 
                 "Reasoning about {topic} considering {aspects}"),
                ("Begin logical analysis of {topic} focusing on {focus}", 
                 "Reasoning about {topic} with focus on {focus}"),
                ("Analyze {topic} by examining {examination}", 
                 "Reasoning about {topic} examining {examination}")
            ],
            "implementation_block": [
                ("Implement the solution for {problem} using {approach}", 
                 "Implementation for {problem} using {approach}"),
                ("Create implementation of {feature} with {method}", 
                 "Implementation of {feature} with {method}"),
                ("Build the implementation for {component} using {technique}", 
                 "Implementation for {component} using {technique}")
            ],
            "verification_block": [
                ("Verify that {condition} is satisfied by {verification_method}", 
                 "Verify {condition} using {verification_method}"),
                ("Check that {requirement} is met through {check_method}", 
                 "Verify {requirement} through {check_method}"),
                ("Validate {assertion} by {validation_approach}", 
                 "Verify {assertion} with {validation_approach}")
            ]
        }
        
        self.domain_templates = {
            DomainType.AI_ML: {
                "neural_network": [
                    ("Create a neural network with {layers} layers for {task}", 
                     "Define neural network with {layers} layers for {task}"),
                    ("Build a neural network model for {task} with {architecture}", 
                     "Neural network for {task} with {architecture}")
                ],
                "data_processing": [
                    ("Process {data_type} data using {method}", 
                     "Process {data_type} with {method}"),
                    ("Transform {input_data} into {output_format}", 
                     "Transform {input_data} to {output_format}")
                ]
            },
            DomainType.WEB_DEVELOPMENT: {
                "api_endpoint": [
                    ("Create an API endpoint for {resource} that handles {operations}", 
                     "Define API endpoint for {resource} handling {operations}"),
                    ("Build a REST endpoint for {service} with {methods}", 
                     "REST endpoint for {service} with {methods}")
                ],
                "frontend_component": [
                    ("Create a React component for {ui_element} with {props}", 
                     "Define React component for {ui_element} with {props}"),
                    ("Build a UI component for {feature} with {styling}", 
                     "UI component for {feature} with {styling}")
                ]
            },
            DomainType.DATA_SCIENCE: {
                "data_analysis": [
                    ("Analyze {dataset} to find {insights}", 
                     "Analyze {dataset} for {insights}"),
                    ("Perform statistical analysis on {data} to {objective}", 
                     "Statistical analysis of {data} for {objective}")
                ],
                "visualization": [
                    ("Create a {chart_type} chart showing {data_relationship}", 
                     "Define {chart_type} chart for {data_relationship}"),
                    ("Generate visualization of {data} using {plot_type}", 
                     "Visualization of {data} using {plot_type}")
                ]
            }
        }
    
    def generate_basic_examples(self, count: int = 10000) -> List[TrainingExample]:
        """Generate basic Runa language examples."""
        examples = []
        
        # Variable declarations
        variables = ["counter", "name", "score", "temperature", "price", "quantity", "status", "result"]
        values = ["0", "42", "3.14", "'hello'", "true", "false", "[1, 2, 3]", "{key: 'value'}"]
        
        for i in range(count // 4):
            var_name = random.choice(variables)
            value = random.choice(values)
            template = random.choice(self.basic_templates["variable_declaration"])
            
            nl_text = template[0].format(name=var_name, value=value)
            runa_code = template[1].format(name=var_name, value=value)
            
            example = TrainingExample(
                id=f"basic_var_{i}",
                natural_language=nl_text,
                runa_code=runa_code,
                complexity=ComplexityLevel.BEGINNER,
                domain=DomainType.GENERAL,
                tags=["variable", "declaration", "basic"],
                description=f"Basic variable declaration example {i}"
            )
            examples.append(example)
        
        # Function definitions
        functions = ["calculate", "process", "validate", "transform", "analyze", "generate", "compute"]
        params = ["input", "data", "value", "parameters", "config", "options"]
        return_types = ["result", "output", "status", "boolean", "number", "string"]
        
        for i in range(count // 4):
            func_name = random.choice(functions)
            param = random.choice(params)
            return_type = random.choice(return_types)
            template = random.choice(self.basic_templates["function_definition"])
            
            nl_text = template[0].format(name=func_name, params=param, return_type=return_type)
            runa_code = template[1].format(name=func_name, params=param, return_type=return_type)
            
            example = TrainingExample(
                id=f"basic_func_{i}",
                natural_language=nl_text,
                runa_code=runa_code,
                complexity=ComplexityLevel.BEGINNER,
                domain=DomainType.GENERAL,
                tags=["function", "definition", "basic"],
                description=f"Basic function definition example {i}"
            )
            examples.append(example)
        
        # Conditional statements
        conditions = ["x > 0", "is_valid", "has_data", "is_ready", "is_authenticated"]
        actions = ["process data", "return true", "display message", "continue", "stop"]
        else_actions = ["return false", "show error", "skip", "wait", "retry"]
        
        for i in range(count // 4):
            condition = random.choice(conditions)
            action = random.choice(actions)
            else_action = random.choice(else_actions)
            template = random.choice(self.basic_templates["conditional_statement"])
            
            nl_text = template[0].format(condition=condition, action=action, else_action=else_action)
            runa_code = template[1].format(condition=condition, action=action, else_action=else_action)
            
            example = TrainingExample(
                id=f"basic_cond_{i}",
                natural_language=nl_text,
                runa_code=runa_code,
                complexity=ComplexityLevel.BEGINNER,
                domain=DomainType.GENERAL,
                tags=["conditional", "if", "basic"],
                description=f"Basic conditional statement example {i}"
            )
            examples.append(example)
        
        # Loop statements
        collections = ["items", "users", "data", "files", "records", "elements"]
        items = ["item", "user", "datum", "file", "record", "element"]
        actions = ["process it", "display it", "validate it", "transform it", "analyze it"]
        
        for i in range(count // 4):
            collection = random.choice(collections)
            item = random.choice(items)
            action = random.choice(actions)
            template = random.choice(self.basic_templates["loop_statement"])
            
            nl_text = template[0].format(item=item, collection=collection, action=action)
            runa_code = template[1].format(item=item, collection=collection, action=action)
            
            example = TrainingExample(
                id=f"basic_loop_{i}",
                natural_language=nl_text,
                runa_code=runa_code,
                complexity=ComplexityLevel.BEGINNER,
                domain=DomainType.GENERAL,
                tags=["loop", "for", "basic"],
                description=f"Basic loop statement example {i}"
            )
            examples.append(example)
        
        return examples
    
    def generate_ai_specific_examples(self, count: int = 15000) -> List[TrainingExample]:
        """Generate AI-specific Runa examples."""
        examples = []
        
        # Reasoning blocks
        topics = ["user behavior", "data patterns", "system performance", "error analysis", "optimization"]
        aspects = ["efficiency", "accuracy", "reliability", "scalability", "security"]
        
        for i in range(count // 3):
            topic = random.choice(topics)
            aspect = random.choice(aspects)
            template = random.choice(self.ai_specific_templates["reasoning_block"])
            
            nl_text = template[0].format(topic=topic, aspects=aspect)
            runa_code = template[1].format(topic=topic, aspects=aspect)
            
            example = TrainingExample(
                id=f"ai_reasoning_{i}",
                natural_language=nl_text,
                runa_code=runa_code,
                complexity=ComplexityLevel.INTERMEDIATE,
                domain=DomainType.AI_ML,
                tags=["reasoning", "ai", "analysis"],
                description=f"AI reasoning block example {i}"
            )
            examples.append(example)
        
        # Implementation blocks
        problems = ["data preprocessing", "model training", "prediction", "validation", "optimization"]
        approaches = ["machine learning", "deep learning", "statistical analysis", "heuristic methods"]
        
        for i in range(count // 3):
            problem = random.choice(problems)
            approach = random.choice(approaches)
            template = random.choice(self.ai_specific_templates["implementation_block"])
            
            nl_text = template[0].format(problem=problem, approach=approach)
            runa_code = template[1].format(problem=problem, approach=approach)
            
            example = TrainingExample(
                id=f"ai_impl_{i}",
                natural_language=nl_text,
                runa_code=runa_code,
                complexity=ComplexityLevel.INTERMEDIATE,
                domain=DomainType.AI_ML,
                tags=["implementation", "ai", "solution"],
                description=f"AI implementation block example {i}"
            )
            examples.append(example)
        
        # Verification blocks
        conditions = ["model accuracy", "data quality", "system performance", "security compliance"]
        methods = ["cross-validation", "unit testing", "benchmarking", "audit"]
        
        for i in range(count // 3):
            condition = random.choice(conditions)
            method = random.choice(methods)
            template = random.choice(self.ai_specific_templates["verification_block"])
            
            nl_text = template[0].format(condition=condition, verification_method=method)
            runa_code = template[1].format(condition=condition, verification_method=method)
            
            example = TrainingExample(
                id=f"ai_verify_{i}",
                natural_language=nl_text,
                runa_code=runa_code,
                complexity=ComplexityLevel.INTERMEDIATE,
                domain=DomainType.AI_ML,
                tags=["verification", "ai", "validation"],
                description=f"AI verification block example {i}"
            )
            examples.append(example)
        
        return examples
    
    def generate_domain_specific_examples(self, count: int = 25000) -> List[TrainingExample]:
        """Generate domain-specific examples."""
        examples = []
        
        # AI/ML examples
        ai_count = count // 4
        for i in range(ai_count):
            domain = DomainType.AI_ML
            category = random.choice(list(self.domain_templates[domain].keys()))
            template = random.choice(self.domain_templates[domain][category])
            
            # Generate appropriate parameters based on category
            if category == "neural_network":
                layers = random.choice(["3", "5", "10", "20"])
                task = random.choice(["classification", "regression", "image recognition", "text processing"])
                nl_text = template[0].format(layers=layers, task=task)
                runa_code = template[1].format(layers=layers, task=task)
            else:  # data_processing
                data_type = random.choice(["numerical", "categorical", "text", "image"])
                method = random.choice(["normalization", "encoding", "cleaning", "augmentation"])
                nl_text = template[0].format(data_type=data_type, method=method)
                runa_code = template[1].format(data_type=data_type, method=method)
            
            example = TrainingExample(
                id=f"ai_domain_{i}",
                natural_language=nl_text,
                runa_code=runa_code,
                complexity=ComplexityLevel.ADVANCED,
                domain=domain,
                tags=["ai", "ml", category],
                description=f"AI/ML domain example {i}"
            )
            examples.append(example)
        
        # Web Development examples
        web_count = count // 4
        for i in range(web_count):
            domain = DomainType.WEB_DEVELOPMENT
            category = random.choice(list(self.domain_templates[domain].keys()))
            template = random.choice(self.domain_templates[domain][category])
            
            if category == "api_endpoint":
                resource = random.choice(["users", "products", "orders", "analytics"])
                operations = random.choice(["GET, POST", "CRUD", "read, write", "query, update"])
                nl_text = template[0].format(resource=resource, operations=operations)
                runa_code = template[1].format(resource=resource, operations=operations)
            else:  # frontend_component
                ui_element = random.choice(["button", "form", "table", "chart", "modal"])
                props = random.choice(["onClick, disabled", "onSubmit, validation", "data, columns", "config, data"])
                nl_text = template[0].format(ui_element=ui_element, props=props)
                runa_code = template[1].format(ui_element=ui_element, props=props)
            
            example = TrainingExample(
                id=f"web_domain_{i}",
                natural_language=nl_text,
                runa_code=runa_code,
                complexity=ComplexityLevel.ADVANCED,
                domain=domain,
                tags=["web", "frontend", category],
                description=f"Web development domain example {i}"
            )
            examples.append(example)
        
        # Data Science examples
        ds_count = count // 4
        for i in range(ds_count):
            domain = DomainType.DATA_SCIENCE
            category = random.choice(list(self.domain_templates[domain].keys()))
            template = random.choice(self.domain_templates[domain][category])
            
            if category == "data_analysis":
                dataset = random.choice(["sales_data", "user_behavior", "performance_metrics", "survey_results"])
                insights = random.choice(["trends", "correlations", "anomalies", "patterns"])
                nl_text = template[0].format(dataset=dataset, insights=insights)
                runa_code = template[1].format(dataset=dataset, insights=insights)
            else:  # visualization
                chart_type = random.choice(["bar", "line", "scatter", "heatmap", "histogram"])
                data_relationship = random.choice(["sales over time", "correlation between variables", "distribution of values"])
                nl_text = template[0].format(chart_type=chart_type, data_relationship=data_relationship)
                runa_code = template[1].format(chart_type=chart_type, data_relationship=data_relationship)
            
            example = TrainingExample(
                id=f"ds_domain_{i}",
                natural_language=nl_text,
                runa_code=runa_code,
                complexity=ComplexityLevel.ADVANCED,
                domain=domain,
                tags=["data_science", "analysis", category],
                description=f"Data science domain example {i}"
            )
            examples.append(example)
        
        # System Programming examples (remaining count)
        sys_count = count - (ai_count + web_count + ds_count)
        for i in range(sys_count):
            nl_text = f"Create a system process for {random.choice(['file_io', 'memory_management', 'threading', 'networking'])}"
            runa_code = f"Process for {random.choice(['file_io', 'memory_management', 'threading', 'networking'])}"
            
            example = TrainingExample(
                id=f"sys_domain_{i}",
                natural_language=nl_text,
                runa_code=runa_code,
                complexity=ComplexityLevel.EXPERT,
                domain=DomainType.SYSTEM_PROGRAMMING,
                tags=["system", "low_level", "performance"],
                description=f"System programming domain example {i}"
            )
            examples.append(example)
        
        return examples
    
    def generate_progressive_complexity_sequences(self, count: int = 10000) -> List[TrainingExample]:
        """Generate progressive complexity training sequences."""
        examples = []
        
        # Progressive sequences from beginner to expert
        sequences = [
            # Sequence 1: Variable → Function → Class → Module
            [
                ("Define a variable called counter containing 0", "Let counter be 0"),
                ("Create a function called increment that takes counter and returns counter + 1", 
                 "Process called increment that takes counter and returns counter + 1"),
                ("Define a class called Counter with methods increment and get_value", 
                 "Define class Counter with methods increment and get_value"),
                ("Create a module called counter_utils with the Counter class and helper functions", 
                 "Define module counter_utils containing Counter class and helper functions")
            ],
            # Sequence 2: Basic → Conditional → Loop → Algorithm
            [
                ("Set x to 10", "Set x to 10"),
                ("If x > 5 then display 'large' otherwise display 'small'", 
                 "If x > 5 then display 'large' otherwise display 'small'"),
                ("For each number in [1, 2, 3, 4, 5], multiply it by 2", 
                 "For each number in [1, 2, 3, 4, 5], multiply it by 2"),
                ("Implement binary search algorithm for sorted array", 
                 "Implementation of binary search for sorted array")
            ],
            # Sequence 3: Data → Processing → Analysis → ML
            [
                ("Define dataset containing [1, 2, 3, 4, 5]", "Let dataset be [1, 2, 3, 4, 5]"),
                ("Process dataset by calculating mean and standard deviation", 
                 "Process dataset calculating mean and standard deviation"),
                ("Analyze dataset to find outliers and patterns", 
                 "Analyze dataset for outliers and patterns"),
                ("Train machine learning model on dataset for prediction", 
                 "Train ML model on dataset for prediction")
            ]
        ]
        
        for i in range(count):
            sequence = random.choice(sequences)
            step = i % len(sequence)
            nl_text, runa_code = sequence[step]
            
            complexity_levels = [ComplexityLevel.BEGINNER, ComplexityLevel.INTERMEDIATE, 
                               ComplexityLevel.ADVANCED, ComplexityLevel.EXPERT]
            complexity = complexity_levels[step]
            
            example = TrainingExample(
                id=f"progressive_{i}",
                natural_language=nl_text,
                runa_code=runa_code,
                complexity=complexity,
                domain=DomainType.GENERAL,
                tags=["progressive", "sequence", f"step_{step + 1}"],
                description=f"Progressive complexity example {i}, step {step + 1}"
            )
            examples.append(example)
        
        return examples
    
    def validate_example_quality(self, example: TrainingExample) -> bool:
        """Validate training example quality."""
        # Basic syntax validation
        if not self._validate_runa_syntax(example.runa_code):
            return False
        
        # Semantic correctness check
        if not self._validate_semantic_correctness(example):
            return False
        
        # Complexity appropriateness
        if not self._validate_complexity_appropriateness(example):
            return False
        
        # Domain relevance
        if not self._validate_domain_relevance(example):
            return False
        
        return True
    
    def _validate_runa_syntax(self, runa_code: str) -> bool:
        """Basic Runa syntax validation."""
        # Check for balanced parentheses, brackets, braces
        stack = []
        brackets = {'(': ')', '[': ']', '{': '}'}
        
        for char in runa_code:
            if char in brackets:
                stack.append(char)
            elif char in brackets.values():
                if not stack or brackets[stack.pop()] != char:
                    return False
        
        return len(stack) == 0
    
    def _validate_semantic_correctness(self, example: TrainingExample) -> bool:
        """Validate semantic correctness of example."""
        # Check that natural language and Runa code are semantically related
        nl_words = set(re.findall(r'\b\w+\b', example.natural_language.lower()))
        runa_words = set(re.findall(r'\b\w+\b', example.runa_code.lower()))
        
        # Should have some common words
        common_words = nl_words.intersection(runa_words)
        return len(common_words) >= 2
    
    def _validate_complexity_appropriateness(self, example: TrainingExample) -> bool:
        """Validate that complexity matches the content."""
        code_length = len(example.runa_code)
        
        if example.complexity == ComplexityLevel.BEGINNER and code_length > 100:
            return False
        elif example.complexity == ComplexityLevel.EXPERT and code_length < 20:
            return False
        
        return True
    
    def _validate_domain_relevance(self, example: TrainingExample) -> bool:
        """Validate domain relevance."""
        domain_keywords = {
            DomainType.AI_ML: ['neural', 'model', 'training', 'prediction', 'ai', 'ml'],
            DomainType.WEB_DEVELOPMENT: ['api', 'endpoint', 'component', 'frontend', 'web'],
            DomainType.DATA_SCIENCE: ['data', 'analysis', 'visualization', 'chart', 'dataset'],
            DomainType.SYSTEM_PROGRAMMING: ['process', 'system', 'memory', 'thread', 'file']
        }
        
        if example.domain == DomainType.GENERAL:
            return True
        
        keywords = domain_keywords.get(example.domain, [])
        code_lower = example.runa_code.lower()
        nl_lower = example.natural_language.lower()
        
        return any(keyword in code_lower or keyword in nl_lower for keyword in keywords)
    
    def generate_complete_dataset(self, target_examples: int = 100000) -> TrainingDataset:
        """Generate complete training dataset."""
        print(f"Generating {target_examples} training examples...")
        
        all_examples = []
        
        # Generate basic examples (25%)
        basic_examples = self.generate_basic_examples(target_examples // 4)
        all_examples.extend(basic_examples)
        print(f"Generated {len(basic_examples)} basic examples")
        
        # Generate AI-specific examples (35%)
        ai_examples = self.generate_ai_specific_examples(int(target_examples * 0.35))
        all_examples.extend(ai_examples)
        print(f"Generated {len(ai_examples)} AI-specific examples")
        
        # Generate domain-specific examples (25%)
        domain_examples = self.generate_domain_specific_examples(target_examples // 4)
        all_examples.extend(domain_examples)
        print(f"Generated {len(domain_examples)} domain-specific examples")
        
        # Generate progressive complexity sequences (15%)
        progressive_examples = self.generate_progressive_complexity_sequences(int(target_examples * 0.15))
        all_examples.extend(progressive_examples)
        print(f"Generated {len(progressive_examples)} progressive complexity examples")
        
        # Validate and filter examples
        print("Validating example quality...")
        validated_examples = []
        for example in all_examples:
            if self.validate_example_quality(example):
                validated_examples.append(example)
                self.quality_metrics["valid_syntax"] += 1
                self.quality_metrics["semantic_correctness"] += 1
                self.quality_metrics["complexity_appropriate"] += 1
                self.quality_metrics["domain_relevant"] += 1
        
        print(f"Validated {len(validated_examples)} examples out of {len(all_examples)}")
        
        # Calculate distributions
        complexity_distribution = {}
        domain_distribution = {}
        
        for example in validated_examples:
            complexity_distribution[example.complexity.value] = complexity_distribution.get(example.complexity.value, 0) + 1
            domain_distribution[example.domain.value] = domain_distribution.get(example.domain.value, 0) + 1
        
        # Create dataset
        dataset = TrainingDataset(
            name="Runa Training Dataset v1.0",
            version="1.0.0",
            total_examples=len(validated_examples),
            complexity_distribution=complexity_distribution,
            domain_distribution=domain_distribution,
            examples=validated_examples,
            metadata={
                "generator_version": "1.0.0",
                "quality_metrics": self.quality_metrics,
                "generation_date": "2024-01-01",
                "target_languages": ["Python", "JavaScript", "C++", "Java", "C#", "Rust", "Go"],
                "validation_status": "validated"
            }
        )
        
        return dataset
    
    def save_dataset(self, dataset: TrainingDataset, filename: str = "runa_training_dataset.json"):
        """Save training dataset to file."""
        filepath = os.path.join(self.output_dir, filename)
        
        # Convert dataset to JSON-serializable format
        dataset_dict = asdict(dataset)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(dataset_dict, f, indent=2, ensure_ascii=False)
        
        print(f"Saved dataset to {filepath}")
        print(f"Total examples: {dataset.total_examples}")
        print(f"Complexity distribution: {dataset.complexity_distribution}")
        print(f"Domain distribution: {dataset.domain_distribution}")
        
        return filepath
    
    def generate_translation_pairs(self, count: int = 10000) -> List[Dict[str, str]]:
        """Generate natural language to Runa translation pairs."""
        translation_pairs = []
        
        # Generate pairs from existing examples
        dataset = self.generate_complete_dataset(count)
        
        for example in dataset.examples:
            pair = {
                "natural_language": example.natural_language,
                "runa_code": example.runa_code,
                "complexity": example.complexity.value,
                "domain": example.domain.value,
                "tags": example.tags
            }
            translation_pairs.append(pair)
        
        # Save translation pairs
        pairs_filepath = os.path.join(self.output_dir, "translations", "nl_to_runa_pairs.json")
        with open(pairs_filepath, 'w', encoding='utf-8') as f:
            json.dump(translation_pairs, f, indent=2, ensure_ascii=False)
        
        print(f"Generated {len(translation_pairs)} translation pairs")
        print(f"Saved to {pairs_filepath}")
        
        return translation_pairs


def main():
    """Main function to generate training data."""
    generator = RunaTrainingDataGenerator()
    
    # Generate complete dataset
    dataset = generator.generate_complete_dataset(100000)
    
    # Save dataset
    generator.save_dataset(dataset)
    
    # Generate translation pairs
    generator.generate_translation_pairs(10000)
    
    print("Training data generation completed successfully!")


if __name__ == "__main__":
    main() 