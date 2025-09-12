//! Core annotation system for Runa's AI-to-AI communication
//! 
//! This module defines the canonical representation of Runa's annotation system,
//! enabling structured communication between AI systems (Brain-Hat) and providing
//! rich metadata for code documentation, reasoning, and translation guidance.

use std::collections::HashMap;
use serde::{Deserialize, Serialize};

/// Represents the type of annotation block
#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum AnnotationType {
    /// @Reasoning: Documents the logical reasoning process and decision rationale
    Reasoning,
    /// @Implementation: Provides detailed implementation notes and guidance
    Implementation,
    /// @Uncertainty: Represents multiple possible choices with confidence levels
    Uncertainty,
    /// @Request_Clarification: Enables Hat to request additional information from Brain
    RequestClarification,
    /// @KnowledgeReference: Links implementation to external knowledge sources
    KnowledgeReference,
    /// @TestCases: Defines testing criteria and validation requirements
    TestCases,
    /// @Resource_Constraints: Specifies computational and memory limitations
    ResourceConstraints,
    /// @Security_Scope: Defines security capabilities and restrictions
    SecurityScope,
    /// @Execution_Model: Specifies how code should be executed
    ExecutionModel,
    /// @Performance_Hints: Optimization guidance for implementation
    PerformanceHints,
    /// @Progress: Real-time progress reporting from Hat to Brain
    Progress,
    /// @Feedback: Hat's feedback to Brain about implementation challenges
    Feedback,
    /// @Translation_Note: Language-specific implementation guidance
    TranslationNote,
    /// @Error_Handling: Comprehensive error management strategy
    ErrorHandling,
    /// @Request: Enables Hat to request information from Brain
    Request,
    /// @Context: Provides situational context for implementation decisions
    Context,
    /// @Task: Formal task specification from Brain to Hat
    Task,
    /// @Requirements: Detailed functional and non-functional requirements
    Requirements,
    /// @Verify: Embedded verification conditions
    Verify,
    /// @Collaboration: Coordination between multiple Hat AIs
    Collaboration,
    /// @Iteration: Support for iterative development cycles
    Iteration,
    /// @Clarification: Brain's response to Hat's clarification requests
    Clarification,
}

/// Represents a single annotation block in Runa code
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct AnnotationBlock {
    /// The type of annotation
    pub annotation_type: AnnotationType,
    /// The raw content of the annotation (free-form text)
    pub content: String,
    /// Structured data extracted from the annotation
    pub structured_data: HashMap<String, serde_json::Value>,
    /// Source location information
    pub location: SourceLocation,
    /// Metadata about the annotation
    pub metadata: AnnotationMetadata,
}

/// Source location information for annotations
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct SourceLocation {
    /// Line number where annotation starts
    pub start_line: usize,
    /// Column number where annotation starts
    pub start_column: usize,
    /// Line number where annotation ends
    pub end_line: usize,
    /// Column number where annotation ends
    pub end_column: usize,
    /// File path (if available)
    pub file_path: Option<String>,
}

/// Metadata about an annotation
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct AnnotationMetadata {
    /// When the annotation was created
    pub created_at: Option<String>,
    /// Author of the annotation (AI system or human)
    pub author: Option<String>,
    /// Confidence level (0.0 to 1.0) for uncertainty annotations
    pub confidence: Option<f64>,
    /// Priority level for feedback annotations
    pub priority: Option<String>,
    /// Tags for categorization
    pub tags: Vec<String>,
    /// Version information
    pub version: Option<String>,
}

/// Represents uncertainty in decision-making
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct UncertaintyExpression {
    /// The uncertain value or choice
    pub value: String,
    /// Confidence level (0.0 to 1.0)
    pub confidence: f64,
    /// Alternative options if applicable
    pub alternatives: Vec<String>,
    /// Reasoning for the uncertainty
    pub reasoning: Option<String>,
}

/// Represents resource constraints
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct ResourceConstraints {
    /// Memory limit in bytes
    pub memory_limit: Option<u64>,
    /// CPU limit (number of cores)
    pub cpu_limit: Option<u32>,
    /// Execution timeout in seconds
    pub execution_timeout: Option<u64>,
    /// Disk space limit in bytes
    pub disk_space: Option<u64>,
    /// Network bandwidth limit in bytes per second
    pub network_bandwidth: Option<u64>,
    /// Optimization target
    pub optimize_for: Option<String>,
    /// Maximum iterations
    pub max_iterations: Option<u64>,
    /// Cache size in bytes
    pub cache_size: Option<u64>,
}

/// Represents security scope and capabilities
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct SecurityScope {
    /// Allowed capabilities
    pub capabilities: Vec<String>,
    /// Forbidden operations
    pub forbidden: Vec<String>,
    /// Sandbox level
    pub sandbox_level: Option<String>,
    /// Data access level
    pub data_access: Option<String>,
    /// Whether encryption is required
    pub encryption_required: Option<bool>,
    /// Audit logging level
    pub audit_logging: Option<String>,
    /// Privilege level
    pub privilege_level: Option<String>,
}

/// Represents execution model specifications
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct ExecutionModel {
    /// Execution mode
    pub mode: Option<String>,
    /// Concurrency model
    pub concurrency: Option<String>,
    /// Parallelism level
    pub parallelism_level: Option<u32>,
    /// Scheduling strategy
    pub scheduling: Option<String>,
    /// Priority level
    pub priority: Option<String>,
    /// Retry policy
    pub retry_policy: Option<String>,
    /// Error recovery strategy
    pub error_recovery: Option<String>,
    /// Monitoring level
    pub monitoring: Option<String>,
}

/// Represents performance hints and optimizations
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct PerformanceHints {
    /// Cache strategy
    pub cache_strategy: Option<String>,
    /// Whether vectorization is enabled
    pub vectorization: Option<bool>,
    /// Memory layout preference
    pub memory_layout: Option<String>,
    /// Parallel threshold
    pub parallel_threshold: Option<u64>,
    /// Batch size
    pub batch_size: Option<u32>,
    /// Whether prefetching is enabled
    pub prefetch_enabled: Option<bool>,
    /// Whether compression is enabled
    pub compression: Option<bool>,
    /// Hot path optimizations
    pub hot_path_optimization: Vec<String>,
}

/// Represents progress reporting
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct ProgressReport {
    /// Completion percentage (0-100)
    pub completion_percentage: f64,
    /// Current milestone
    pub current_milestone: String,
    /// Next milestone
    pub next_milestone: Option<String>,
    /// Estimated time remaining
    pub estimated_time_remaining: Option<String>,
    /// Current blockers
    pub blockers: Vec<String>,
    /// Intermediate results
    pub intermediate_results: HashMap<String, serde_json::Value>,
    /// Confidence level
    pub confidence_level: f64,
}

/// Represents feedback from Hat to Brain
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct FeedbackReport {
    /// Implementation status
    pub implementation_status: String,
    /// Challenges encountered
    pub challenges_encountered: Vec<String>,
    /// Suggested modifications
    pub suggested_modifications: Vec<String>,
    /// Alternative approaches
    pub alternative_approaches: Vec<String>,
    /// Confidence in current approach
    pub confidence_in_current_approach: f64,
}

/// Represents translation notes for different target languages
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct TranslationNote {
    /// Target languages
    pub target_languages: Vec<String>,
    /// Critical features
    pub critical_feature: Option<String>,
    /// Platform-specific considerations
    pub platform_specific: HashMap<String, String>,
    /// Performance considerations
    pub performance_considerations: HashMap<String, String>,
    /// Compatibility notes
    pub compatibility_notes: HashMap<String, String>,
}

/// Represents error handling strategy
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct ErrorHandling {
    /// Error handling strategy
    pub strategy: String,
    /// Expected errors
    pub expected_errors: Vec<ExpectedError>,
    /// Fallback behavior
    pub fallback_behavior: Option<String>,
    /// Error reporting level
    pub error_reporting: Option<String>,
}

/// Represents an expected error
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct ExpectedError {
    /// Error type
    pub error_type: String,
    /// Probability of occurrence
    pub probability: f64,
    /// Recovery strategy
    pub recovery: String,
    /// Maximum retries
    pub max_retries: Option<u32>,
    /// Fallback behavior
    pub fallback: Option<String>,
}

impl AnnotationBlock {
    /// Create a new annotation block
    pub fn new(
        annotation_type: AnnotationType,
        content: String,
        location: SourceLocation,
    ) -> Self {
        Self {
            annotation_type,
            content,
            structured_data: HashMap::new(),
            location,
            metadata: AnnotationMetadata {
                created_at: None,
                author: None,
                confidence: None,
                priority: None,
                tags: Vec::new(),
                version: None,
            },
        }
    }

    /// Add structured data to the annotation
    pub fn add_structured_data(&mut self, key: String, value: serde_json::Value) {
        self.structured_data.insert(key, value);
    }

    /// Set confidence level for uncertainty annotations
    pub fn set_confidence(&mut self, confidence: f64) {
        self.metadata.confidence = Some(confidence);
    }

    /// Add a tag to the annotation
    pub fn add_tag(&mut self, tag: String) {
        self.metadata.tags.push(tag);
    }
}

impl SourceLocation {
    /// Create a new source location
    pub fn new(start_line: usize, start_column: usize, end_line: usize, end_column: usize) -> Self {
        Self {
            start_line,
            start_column,
            end_line,
            end_column,
            file_path: None,
        }
    }

    /// Set the file path
    pub fn with_file_path(mut self, file_path: String) -> Self {
        self.file_path = Some(file_path);
        self
    }
} 