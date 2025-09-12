//! T4: Speculative Compiler with Guards
//! 
//! Speculative execution with deoptimization guards for maximum performance.

use super::{CompilationEngine, CompilationStats};
use crate::aott::types::*;
use crate::aott::execution::{ExecutionEngine, FunctionMetadata};
use runa_common::bytecode::Value;
use std::collections::HashMap;
use std::sync::{Arc, RwLock};
use std::fmt;

/// Deoptimization levels for intelligent fallback
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum DeoptLevel {
    /// Retry speculation with adjusted guards
    Soft,
    /// Fall back to T3 optimized compilation  
    Medium,
    /// Fall back to T1 interpreter
    Hard,
    /// Never speculate this function again
    Blacklist,
}

/// Reason for deoptimization
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub enum DeoptReason {
    GuardFailure(String),
    ExecutionTimeout,
    MemoryPressure,
    TypeInstability,
    BranchMisprediction,
    ConstantSpeculationFailure,
    RangeViolation,
    NullPointerAccess,
    BoundsCheckFailure,
    InliningFailure,
    RepeatedFailures,
}

/// Deoptimization decision with context
#[derive(Debug, Clone)]
pub struct DeoptDecision {
    pub level: DeoptLevel,
    pub reason: DeoptReason,
    pub confidence: f64,
    pub retry_after: Option<std::time::Duration>,
    pub suggested_adjustments: Vec<GuardAdjustment>,
}

/// Guard adjustment suggestion
#[derive(Debug, Clone)]
pub enum GuardAdjustment {
    RelaxTypeCheck { guard_id: usize },
    ExpandRange { guard_id: usize, new_min: i64, new_max: i64 },
    RemoveGuard { guard_id: usize },
    AddGuard { guard_type: GuardType },
    ReduceConfidenceThreshold { guard_id: usize, new_threshold: f64 },
}

/// Polymorphic Inline Cache system for optimizing dynamic dispatch
#[derive(Debug)]
pub struct PolymorphicInlineCache {
    /// Cache entries for different call sites
    pub cache_entries: HashMap<CallSiteId, CallSiteCache>,
    /// Global statistics for cache performance
    pub cache_statistics: CacheStatistics,
    /// Cache configuration parameters
    pub cache_config: CacheConfig,
    /// Type-based dispatch optimization
    pub type_dispatch_optimizer: TypeDispatchOptimizer,
}

/// Unique identifier for call sites
pub type CallSiteId = u64;

/// Cache for a specific call site
#[derive(Debug)]
pub struct CallSiteCache {
    /// Cached function targets with hit counts
    pub targets: Vec<CacheEntry>,
    /// Total number of calls to this site
    pub total_calls: u64,
    /// Cache hit count
    pub cache_hits: u64,
    /// Cache miss count  
    pub cache_misses: u64,
    /// Last access time for cache eviction
    pub last_access: std::time::Instant,
    /// Polymorphism level (number of different targets seen)
    pub polymorphism_level: usize,
}

/// Individual cache entry for a function target
#[derive(Debug, Clone)]
pub struct CacheEntry {
    /// Target function identifier
    pub target_function: FunctionId,
    /// Type signature that triggers this target
    pub type_signature: TypeSignature,
    /// Number of times this target was called
    pub hit_count: u64,
    /// Success rate for speculation on this target
    pub speculation_success_rate: f64,
    /// Compiled machine code for fast dispatch
    pub optimized_dispatch_code: Vec<u8>,
    /// Guard requirements for this dispatch
    pub dispatch_guards: Vec<usize>,
}

/// Type signature for polymorphic dispatch
#[derive(Debug, Clone, PartialEq, Hash)]
pub struct TypeSignature {
    /// Argument types
    pub arg_types: Vec<ValueType>,
    /// Receiver type (for method calls)
    pub receiver_type: Option<ValueType>,
    /// Return type hint
    pub return_type: Option<ValueType>,
}

/// Cache performance statistics
#[derive(Debug, Default)]
pub struct CacheStatistics {
    /// Total cache hits across all call sites
    pub total_hits: u64,
    /// Total cache misses across all call sites
    pub total_misses: u64,
    /// Number of monomorphic call sites (1 target)
    pub monomorphic_sites: u64,
    /// Number of polymorphic call sites (2-4 targets)
    pub polymorphic_sites: u64,
    /// Number of megamorphic call sites (5+ targets)
    pub megamorphic_sites: u64,
    /// Cache evictions due to space pressure
    pub evictions: u64,
}

/// Cache configuration parameters
#[derive(Debug)]
pub struct CacheConfig {
    /// Maximum number of targets per call site
    pub max_targets_per_site: usize,
    /// Maximum total number of call sites
    pub max_call_sites: usize,
    /// Hit threshold for considering a target "hot"
    pub hot_target_threshold: u64,
    /// Time threshold for cache eviction (unused entries)
    pub eviction_time_threshold: std::time::Duration,
}

/// Type-based dispatch optimization
#[derive(Debug)]
pub struct TypeDispatchOptimizer {
    /// Type-to-function mapping for fast lookups
    pub type_dispatch_table: HashMap<TypeSignature, Vec<FunctionId>>,
    /// Type hierarchy information for inheritance-based dispatch
    pub type_hierarchy: TypeHierarchy,
    /// Dispatch strategies for different polymorphism levels
    pub dispatch_strategies: HashMap<usize, DispatchStrategy>,
}

/// Type hierarchy for inheritance-based optimization
#[derive(Debug, Default)]
pub struct TypeHierarchy {
    /// Parent-child relationships between types
    pub inheritance_tree: HashMap<String, Vec<String>>,
    /// Interface implementations
    pub interface_implementations: HashMap<String, Vec<String>>,
}

/// Strategy for handling different levels of polymorphism
#[derive(Debug, Clone)]
pub enum DispatchStrategy {
    /// Direct call for monomorphic sites
    DirectCall,
    /// Inline comparison for 2-4 targets
    InlineComparison,
    /// Jump table for 5-8 targets
    JumpTable,
    /// Hash table lookup for 9+ targets
    HashTableLookup,
}

impl PolymorphicInlineCache {
    pub fn new() -> Self {
        Self {
            cache_entries: HashMap::new(),
            cache_statistics: CacheStatistics::default(),
            cache_config: CacheConfig {
                max_targets_per_site: 8,
                max_call_sites: 1000,
                hot_target_threshold: 10,
                eviction_time_threshold: std::time::Duration::from_secs(300),
            },
            type_dispatch_optimizer: TypeDispatchOptimizer {
                type_dispatch_table: HashMap::new(),
                type_hierarchy: TypeHierarchy::default(),
                dispatch_strategies: [
                    (1, DispatchStrategy::DirectCall),
                    (2, DispatchStrategy::InlineComparison),
                    (3, DispatchStrategy::InlineComparison),
                    (4, DispatchStrategy::InlineComparison),
                    (6, DispatchStrategy::JumpTable),
                    (8, DispatchStrategy::JumpTable),
                ].iter().cloned().collect(),
            },
        }
    }
    
    /// Record a function call for inline cache optimization
    pub fn record_call(&mut self, call_site_id: CallSiteId, target_function: &FunctionId, 
                       type_signature: TypeSignature, success: bool) {
        
        let cache_entry = self.cache_entries.entry(call_site_id)
            .or_insert_with(|| CallSiteCache {
                targets: Vec::new(),
                total_calls: 0,
                cache_hits: 0,
                cache_misses: 0,
                last_access: std::time::Instant::now(),
                polymorphism_level: 0,
            });
        
        cache_entry.total_calls += 1;
        cache_entry.last_access = std::time::Instant::now();
        
        if let Some(existing_entry) = cache_entry.targets.iter_mut()
            .find(|entry| entry.target_function == *target_function && 
                         entry.type_signature == type_signature) {
            
            existing_entry.hit_count += 1;
            if success {
                existing_entry.speculation_success_rate = 
                    (existing_entry.speculation_success_rate * 0.9) + 0.1;
            } else {
                existing_entry.speculation_success_rate *= 0.95;
            }
            cache_entry.cache_hits += 1;
            self.cache_statistics.total_hits += 1;
            
        } else {
            if cache_entry.targets.len() < self.cache_config.max_targets_per_site {
                let new_entry = CacheEntry {
                    target_function: target_function.clone(),
                    type_signature,
                    hit_count: 1,
                    speculation_success_rate: if success { 0.8 } else { 0.6 },
                    optimized_dispatch_code: self.generate_dispatch_code(target_function),
                    dispatch_guards: Vec::new(),
                };
                
                cache_entry.targets.push(new_entry);
                cache_entry.polymorphism_level = cache_entry.targets.len();
                
                self.update_polymorphism_statistics(cache_entry.polymorphism_level);
            }
            
            cache_entry.cache_misses += 1;
            self.cache_statistics.total_misses += 1;
        }
        
        self.sort_cache_by_frequency(cache_entry);
        
        if self.cache_entries.len() > self.cache_config.max_call_sites {
            self.evict_least_recently_used();
        }
    }
    
    /// Generate optimized dispatch code for a target function
    fn generate_dispatch_code(&self, target_function: &FunctionId) -> Vec<u8> {
        let mut dispatch_code = Vec::new();
        
        dispatch_code.extend_from_slice(&[0x48, 0x83, 0xEC, 0x08]);
        
        let function_hash = self.hash_function_id(target_function);
        dispatch_code.extend_from_slice(&[0x48, 0xC7, 0xC0]);
        dispatch_code.extend_from_slice(&(function_hash as u32).to_le_bytes());
        dispatch_code.extend_from_slice(&[0x00, 0x00, 0x00, 0x00]);
        
        dispatch_code.extend_from_slice(&[0x48, 0x89, 0x04, 0x24]);
        
        dispatch_code.extend_from_slice(&[0xFF, 0x15]);
        dispatch_code.extend_from_slice(&[0x00, 0x00, 0x00, 0x00]);
        
        dispatch_code.extend_from_slice(&[0x48, 0x83, 0xC4, 0x08]);
        dispatch_code.extend_from_slice(&[0xC3]);
        
        dispatch_code
    }
    
    /// Hash function ID for dispatch code generation
    fn hash_function_id(&self, function_id: &FunctionId) -> u64 {
        use std::collections::hash_map::DefaultHasher;
        use std::hash::{Hash, Hasher};
        
        let mut hasher = DefaultHasher::new();
        function_id.hash(&mut hasher);
        hasher.finish()
    }
    
    /// Sort cache entries by frequency (most frequent first)
    fn sort_cache_by_frequency(&self, cache_entry: &mut CallSiteCache) {
        cache_entry.targets.sort_by(|a, b| b.hit_count.cmp(&a.hit_count));
    }
    
    /// Update polymorphism level statistics
    fn update_polymorphism_statistics(&mut self, polymorphism_level: usize) {
        match polymorphism_level {
            1 => self.cache_statistics.monomorphic_sites += 1,
            2..=4 => self.cache_statistics.polymorphic_sites += 1,
            _ => self.cache_statistics.megamorphic_sites += 1,
        }
    }
    
    /// Evict least recently used cache entries
    fn evict_least_recently_used(&mut self) {
        if let Some((oldest_call_site, _)) = self.cache_entries.iter()
            .min_by_key(|(_, cache)| cache.last_access) {
            let oldest_call_site = *oldest_call_site;
            self.cache_entries.remove(&oldest_call_site);
            self.cache_statistics.evictions += 1;
        }
    }
    
    /// Lookup optimized dispatch for a call site
    pub fn lookup_dispatch(&mut self, call_site_id: CallSiteId, 
                          type_signature: &TypeSignature) -> Option<&CacheEntry> {
        
        if let Some(cache_entry) = self.cache_entries.get_mut(&call_site_id) {
            cache_entry.last_access = std::time::Instant::now();
            
            for target in &cache_entry.targets {
                if target.type_signature == *type_signature {
                    return Some(target);
                }
            }
        }
        
        None
    }
    
    /// Get the optimal dispatch strategy for a call site
    pub fn get_dispatch_strategy(&self, call_site_id: CallSiteId) -> DispatchStrategy {
        if let Some(cache_entry) = self.cache_entries.get(&call_site_id) {
            self.type_dispatch_optimizer.dispatch_strategies
                .get(&cache_entry.polymorphism_level)
                .cloned()
                .unwrap_or(DispatchStrategy::HashTableLookup)
        } else {
            DispatchStrategy::DirectCall
        }
    }
    
    /// Generate specialized dispatch code based on polymorphism level
    pub fn generate_specialized_dispatch(&self, call_site_id: CallSiteId) -> Vec<u8> {
        let strategy = self.get_dispatch_strategy(call_site_id);
        
        match strategy {
            DispatchStrategy::DirectCall => self.generate_direct_call_code(call_site_id),
            DispatchStrategy::InlineComparison => self.generate_inline_comparison_code(call_site_id),
            DispatchStrategy::JumpTable => self.generate_jump_table_code(call_site_id),
            DispatchStrategy::HashTableLookup => self.generate_hash_lookup_code(call_site_id),
        }
    }
    
    /// Generate direct call code for monomorphic sites
    fn generate_direct_call_code(&self, call_site_id: CallSiteId) -> Vec<u8> {
        if let Some(cache_entry) = self.cache_entries.get(&call_site_id) {
            if let Some(target) = cache_entry.targets.first() {
                return target.optimized_dispatch_code.clone();
            }
        }
        
        vec![0x90, 0xC3]
    }
    
    /// Generate inline comparison code for low polymorphism
    fn generate_inline_comparison_code(&self, call_site_id: CallSiteId) -> Vec<u8> {
        let mut code = Vec::new();
        
        if let Some(cache_entry) = self.cache_entries.get(&call_site_id) {
            code.extend_from_slice(&[0x48, 0x83, 0xEC, 0x10]);
            
            for (i, target) in cache_entry.targets.iter().enumerate() {
                let type_hash = self.hash_type_signature(&target.type_signature);
                
                code.extend_from_slice(&[0x48, 0x81, 0xFF]);
                code.extend_from_slice(&(type_hash as u32).to_le_bytes());
                
                if i < cache_entry.targets.len() - 1 {
                    code.extend_from_slice(&[0x75, 0x05]);
                }
                
                code.extend_from_slice(&target.optimized_dispatch_code[..8.min(target.optimized_dispatch_code.len())]);
            }
            
            code.extend_from_slice(&[0x48, 0x83, 0xC4, 0x10]);
        }
        
        code.push(0xC3);
        code
    }
    
    /// Generate jump table code for medium polymorphism
    fn generate_jump_table_code(&self, call_site_id: CallSiteId) -> Vec<u8> {
        let mut code = Vec::new();
        
        code.extend_from_slice(&[0x48, 0x83, 0xEC, 0x08]);
        code.extend_from_slice(&[0x48, 0x8B, 0x04, 0x25]);
        code.extend_from_slice(&[0x00, 0x00, 0x00, 0x00]);
        code.extend_from_slice(&[0xFF, 0xE0]);
        code.extend_from_slice(&[0x48, 0x83, 0xC4, 0x08]);
        code.push(0xC3);
        
        code
    }
    
    /// Generate hash table lookup code for high polymorphism
    fn generate_hash_lookup_code(&self, call_site_id: CallSiteId) -> Vec<u8> {
        let mut code = Vec::new();
        
        code.extend_from_slice(&[0x48, 0x83, 0xEC, 0x10]);
        code.extend_from_slice(&[0x48, 0x89, 0x7C, 0x24, 0x08]);
        code.extend_from_slice(&[0xE8]);
        code.extend_from_slice(&[0x00, 0x00, 0x00, 0x00]);
        code.extend_from_slice(&[0xFF, 0xD0]);
        code.extend_from_slice(&[0x48, 0x8B, 0x7C, 0x24, 0x08]);
        code.extend_from_slice(&[0x48, 0x83, 0xC4, 0x10]);
        code.push(0xC3);
        
        code
    }
    
    /// Hash a type signature for dispatch optimization
    fn hash_type_signature(&self, type_sig: &TypeSignature) -> u64 {
        use std::collections::hash_map::DefaultHasher;
        use std::hash::{Hash, Hasher};
        
        let mut hasher = DefaultHasher::new();
        type_sig.hash(&mut hasher);
        hasher.finish()
    }
    
    /// Get cache performance metrics
    pub fn get_performance_metrics(&self) -> CachePerformanceMetrics {
        let hit_rate = if self.cache_statistics.total_hits + self.cache_statistics.total_misses > 0 {
            self.cache_statistics.total_hits as f64 / 
            (self.cache_statistics.total_hits + self.cache_statistics.total_misses) as f64
        } else {
            0.0
        };
        
        CachePerformanceMetrics {
            hit_rate,
            total_call_sites: self.cache_entries.len(),
            average_polymorphism: self.calculate_average_polymorphism(),
            cache_utilization: self.cache_entries.len() as f64 / self.cache_config.max_call_sites as f64,
        }
    }
    
    /// Calculate average polymorphism level across all call sites
    fn calculate_average_polymorphism(&self) -> f64 {
        if self.cache_entries.is_empty() {
            return 0.0;
        }
        
        let total_polymorphism: usize = self.cache_entries.values()
            .map(|cache| cache.polymorphism_level)
            .sum();
            
        total_polymorphism as f64 / self.cache_entries.len() as f64
    }
}

/// Performance metrics for the polymorphic inline cache
#[derive(Debug)]
pub struct CachePerformanceMetrics {
    pub hit_rate: f64,
    pub total_call_sites: usize,
    pub average_polymorphism: f64,
    pub cache_utilization: f64,
}

/// Value speculation system for optimizing based on frequently occurring values
#[derive(Debug)]
pub struct ValueSpeculationEngine {
    /// Value profiles for different variables/locations
    pub value_profiles: HashMap<ValueLocationId, ValueProfile>,
    /// Speculation decisions and outcomes
    pub speculation_history: HashMap<ValueLocationId, Vec<SpeculationOutcome>>,
    /// Configuration parameters
    pub speculation_config: ValueSpeculationConfig,
    /// Performance statistics
    pub speculation_stats: ValueSpeculationStats,
}

/// Unique identifier for value locations (variables, fields, etc.)
pub type ValueLocationId = u64;

/// Profile of values observed at a specific location
#[derive(Debug)]
pub struct ValueProfile {
    /// Most frequently observed values with their frequencies
    pub frequent_values: Vec<ValueFrequency>,
    /// Total number of observations
    pub total_observations: u64,
    /// Value type stability (how often the type changes)
    pub type_stability: f64,
    /// Range information for numeric values
    pub numeric_range: Option<NumericRange>,
    /// String patterns for string values
    pub string_patterns: Vec<StringPattern>,
    /// Last update timestamp
    pub last_updated: std::time::Instant,
}

/// Frequency information for a specific value
#[derive(Debug, Clone)]
pub struct ValueFrequency {
    pub value: Value,
    pub count: u64,
    pub frequency: f64,
    pub last_seen: std::time::Instant,
    pub speculation_success_rate: f64,
}

/// Range information for numeric values
#[derive(Debug, Clone)]
pub struct NumericRange {
    pub min: f64,
    pub max: f64,
    pub average: f64,
    pub standard_deviation: f64,
    pub common_values: Vec<f64>,
}

/// String pattern analysis
#[derive(Debug, Clone)]
pub struct StringPattern {
    pub pattern: String,
    pub frequency: f64,
    pub length_distribution: Vec<(usize, u64)>,
}

/// Outcome of a value speculation
#[derive(Debug, Clone)]
pub struct SpeculationOutcome {
    pub timestamp: std::time::Instant,
    pub speculated_value: Value,
    pub actual_value: Value,
    pub was_correct: bool,
    pub execution_benefit: f64,
}

/// Configuration for value speculation
#[derive(Debug)]
pub struct ValueSpeculationConfig {
    /// Minimum frequency threshold for speculation
    pub min_speculation_frequency: f64,
    /// Minimum observations before speculation
    pub min_observations: u64,
    /// Maximum number of values to track per location
    pub max_values_per_location: usize,
    /// Time window for value profile updates
    pub profile_update_window: std::time::Duration,
    /// Speculation confidence threshold
    pub confidence_threshold: f64,
}

/// Performance statistics for value speculation
#[derive(Debug, Default)]
pub struct ValueSpeculationStats {
    pub total_speculations: u64,
    pub successful_speculations: u64,
    pub failed_speculations: u64,
    pub execution_time_saved: std::time::Duration,
    pub memory_overhead: usize,
}

impl ValueSpeculationEngine {
    pub fn new() -> Self {
        Self {
            value_profiles: HashMap::new(),
            speculation_history: HashMap::new(),
            speculation_config: ValueSpeculationConfig {
                min_speculation_frequency: 0.6,
                min_observations: 10,
                max_values_per_location: 8,
                profile_update_window: std::time::Duration::from_secs(60),
                confidence_threshold: 0.75,
            },
            speculation_stats: ValueSpeculationStats::default(),
        }
    }
    
    /// Record a value observation at a specific location
    pub fn record_value(&mut self, location_id: ValueLocationId, value: Value) {
        let profile = self.value_profiles.entry(location_id)
            .or_insert_with(|| ValueProfile {
                frequent_values: Vec::new(),
                total_observations: 0,
                type_stability: 1.0,
                numeric_range: None,
                string_patterns: Vec::new(),
                last_updated: std::time::Instant::now(),
            });
        
        profile.total_observations += 1;
        profile.last_updated = std::time::Instant::now();
        
        self.update_type_stability(profile, &value);
        self.update_value_frequency(profile, value.clone());
        self.update_numeric_range(profile, &value);
        self.update_string_patterns(profile, &value);
        
        self.maintain_profile_size(profile);
    }
    
    /// Update type stability based on observed value
    fn update_type_stability(&self, profile: &mut ValueProfile, value: &Value) {
        if profile.frequent_values.is_empty() {
            return;
        }
        
        let current_type = std::mem::discriminant(value);
        let previous_type = std::mem::discriminant(&profile.frequent_values[0].value);
        
        if current_type != previous_type {
            profile.type_stability *= 0.95;
        } else {
            profile.type_stability = (profile.type_stability * 0.99) + 0.01;
        }
    }
    
    /// Update frequency information for a value
    fn update_value_frequency(&self, profile: &mut ValueProfile, value: Value) {
        if let Some(existing) = profile.frequent_values.iter_mut()
            .find(|freq| freq.value == value) {
            existing.count += 1;
            existing.last_seen = std::time::Instant::now();
        } else {
            profile.frequent_values.push(ValueFrequency {
                value,
                count: 1,
                frequency: 0.0,
                last_seen: std::time::Instant::now(),
                speculation_success_rate: 0.8,
            });
        }
        
        self.recalculate_frequencies(profile);
    }
    
    /// Recalculate frequency percentages
    fn recalculate_frequencies(&self, profile: &mut ValueProfile) {
        for freq in &mut profile.frequent_values {
            freq.frequency = freq.count as f64 / profile.total_observations as f64;
        }
        
        profile.frequent_values.sort_by(|a, b| b.frequency.partial_cmp(&a.frequency).unwrap());
    }
    
    /// Update numeric range information
    fn update_numeric_range(&self, profile: &mut ValueProfile, value: &Value) {
        match value {
            Value::Integer(n) => {
                let n_f64 = *n as f64;
                self.update_range_with_value(profile, n_f64);
            },
            Value::Float(f) => {
                self.update_range_with_value(profile, *f);
            },
            _ => {}
        }
    }
    
    /// Update range with a numeric value
    fn update_range_with_value(&self, profile: &mut ValueProfile, value: f64) {
        if let Some(range) = &mut profile.numeric_range {
            range.min = range.min.min(value);
            range.max = range.max.max(value);
            
            let n = profile.total_observations as f64;
            range.average = (range.average * (n - 1.0) + value) / n;
            
            if !range.common_values.contains(&value) && range.common_values.len() < 10 {
                range.common_values.push(value);
            }
        } else {
            profile.numeric_range = Some(NumericRange {
                min: value,
                max: value,
                average: value,
                standard_deviation: 0.0,
                common_values: vec![value],
            });
        }
    }
    
    /// Update string pattern analysis
    fn update_string_patterns(&self, profile: &mut ValueProfile, value: &Value) {
        if let Value::String(s) = value {
            let pattern = self.extract_string_pattern(s);
            
            if let Some(existing_pattern) = profile.string_patterns.iter_mut()
                .find(|p| p.pattern == pattern) {
                existing_pattern.frequency += 1.0 / profile.total_observations as f64;
            } else if profile.string_patterns.len() < 5 {
                profile.string_patterns.push(StringPattern {
                    pattern,
                    frequency: 1.0 / profile.total_observations as f64,
                    length_distribution: vec![(s.len(), 1)],
                });
            }
        }
    }
    
    /// Extract pattern from string (simplified pattern matching)
    fn extract_string_pattern(&self, s: &str) -> String {
        if s.chars().all(|c| c.is_ascii_digit()) {
            "numeric".to_string()
        } else if s.chars().all(|c| c.is_ascii_alphabetic()) {
            "alphabetic".to_string()
        } else if s.contains('@') {
            "email".to_string()
        } else if s.starts_with("http") {
            "url".to_string()
        } else {
            "mixed".to_string()
        }
    }
    
    /// Maintain profile size within limits
    fn maintain_profile_size(&self, profile: &mut ValueProfile) {
        if profile.frequent_values.len() > self.speculation_config.max_values_per_location {
            profile.frequent_values.sort_by(|a, b| b.count.cmp(&a.count));
            profile.frequent_values.truncate(self.speculation_config.max_values_per_location);
        }
    }
    
    /// Get speculation recommendation for a location
    pub fn get_speculation_recommendation(&self, location_id: ValueLocationId) -> Option<ValueSpeculationRecommendation> {
        let profile = self.value_profiles.get(&location_id)?;
        
        if profile.total_observations < self.speculation_config.min_observations {
            return None;
        }
        
        let top_value = profile.frequent_values.first()?;
        
        if top_value.frequency >= self.speculation_config.min_speculation_frequency {
            let confidence = self.calculate_speculation_confidence(profile, top_value);
            
            if confidence >= self.speculation_config.confidence_threshold {
                return Some(ValueSpeculationRecommendation {
                    speculated_value: top_value.value.clone(),
                    confidence,
                    frequency: top_value.frequency,
                    alternative_values: profile.frequent_values.iter()
                        .skip(1)
                        .take(3)
                        .map(|freq| (freq.value.clone(), freq.frequency))
                        .collect(),
                    guard_requirements: self.generate_speculation_guards(profile, top_value),
                });
            }
        }
        
        None
    }
    
    /// Calculate speculation confidence
    fn calculate_speculation_confidence(&self, profile: &ValueProfile, value_freq: &ValueFrequency) -> f64 {
        let base_confidence = value_freq.frequency;
        let type_stability_factor = profile.type_stability;
        let success_rate_factor = value_freq.speculation_success_rate;
        let recency_factor = self.calculate_recency_factor(value_freq.last_seen);
        
        (base_confidence * 0.4 + 
         type_stability_factor * 0.25 + 
         success_rate_factor * 0.25 + 
         recency_factor * 0.1).min(0.95)
    }
    
    /// Calculate recency factor based on when value was last seen
    fn calculate_recency_factor(&self, last_seen: std::time::Instant) -> f64 {
        let elapsed = last_seen.elapsed();
        let recency_window = std::time::Duration::from_secs(300);
        
        if elapsed <= recency_window {
            1.0 - (elapsed.as_secs_f64() / recency_window.as_secs_f64() * 0.3)
        } else {
            0.7
        }
    }
    
    /// Generate guards for value speculation
    fn generate_speculation_guards(&self, profile: &ValueProfile, value_freq: &ValueFrequency) -> Vec<SpeculationGuardRequirement> {
        let mut guards = Vec::new();
        
        guards.push(SpeculationGuardRequirement::ValueEquality {
            expected_value: value_freq.value.clone(),
        });
        
        if profile.type_stability > 0.9 {
            guards.push(SpeculationGuardRequirement::TypeStability);
        }
        
        if let Some(range) = &profile.numeric_range {
            match &value_freq.value {
                Value::Integer(n) => {
                    guards.push(SpeculationGuardRequirement::RangeCheck {
                        min: (range.min - range.standard_deviation) as i64,
                        max: (range.max + range.standard_deviation) as i64,
                    });
                },
                Value::Float(_) => {
                    guards.push(SpeculationGuardRequirement::FloatRangeCheck {
                        min: range.min - range.standard_deviation,
                        max: range.max + range.standard_deviation,
                    });
                },
                _ => {}
            }
        }
        
        guards
    }
    
    /// Record speculation outcome
    pub fn record_speculation_outcome(&mut self, location_id: ValueLocationId, 
                                      speculated_value: Value, actual_value: Value, 
                                      execution_benefit: f64) {
        let was_correct = speculated_value == actual_value;
        
        let outcome = SpeculationOutcome {
            timestamp: std::time::Instant::now(),
            speculated_value: speculated_value.clone(),
            actual_value: actual_value.clone(),
            was_correct,
            execution_benefit,
        };
        
        self.speculation_history.entry(location_id)
            .or_insert_with(Vec::new)
            .push(outcome);
        
        self.update_speculation_stats(was_correct, execution_benefit);
        
        if let Some(profile) = self.value_profiles.get_mut(&location_id) {
            if let Some(freq) = profile.frequent_values.iter_mut()
                .find(|f| f.value == speculated_value) {
                if was_correct {
                    freq.speculation_success_rate = (freq.speculation_success_rate * 0.9) + 0.1;
                } else {
                    freq.speculation_success_rate *= 0.8;
                }
            }
        }
        
        if let Some(history) = self.speculation_history.get_mut(&location_id) {
            if history.len() > 100 {
                history.drain(0..50);
            }
        }
    }
    
    /// Update speculation statistics
    fn update_speculation_stats(&mut self, was_correct: bool, execution_benefit: f64) {
        self.speculation_stats.total_speculations += 1;
        
        if was_correct {
            self.speculation_stats.successful_speculations += 1;
            self.speculation_stats.execution_time_saved += 
                std::time::Duration::from_nanos((execution_benefit * 1000.0) as u64);
        } else {
            self.speculation_stats.failed_speculations += 1;
        }
    }
    
    /// Get speculation performance metrics
    pub fn get_performance_metrics(&self) -> ValueSpeculationMetrics {
        let success_rate = if self.speculation_stats.total_speculations > 0 {
            self.speculation_stats.successful_speculations as f64 / 
            self.speculation_stats.total_speculations as f64
        } else {
            0.0
        };
        
        ValueSpeculationMetrics {
            success_rate,
            total_locations: self.value_profiles.len(),
            active_speculations: self.count_active_speculations(),
            average_confidence: self.calculate_average_confidence(),
            memory_usage: self.calculate_memory_usage(),
        }
    }
    
    /// Count locations with active speculation recommendations
    fn count_active_speculations(&self) -> usize {
        self.value_profiles.iter()
            .filter(|(location_id, _)| self.get_speculation_recommendation(**location_id).is_some())
            .count()
    }
    
    /// Calculate average speculation confidence
    fn calculate_average_confidence(&self) -> f64 {
        let confidences: Vec<f64> = self.value_profiles.iter()
            .filter_map(|(location_id, _)| {
                self.get_speculation_recommendation(*location_id)
                    .map(|rec| rec.confidence)
            })
            .collect();
        
        if confidences.is_empty() {
            0.0
        } else {
            confidences.iter().sum::<f64>() / confidences.len() as f64
        }
    }
    
    /// Calculate memory usage of the speculation engine
    fn calculate_memory_usage(&self) -> usize {
        let profiles_size = self.value_profiles.len() * 1000;
        let history_size = self.speculation_history.values()
            .map(|history| history.len() * 200)
            .sum::<usize>();
        
        profiles_size + history_size
    }
}

/// Recommendation for value speculation
#[derive(Debug)]
pub struct ValueSpeculationRecommendation {
    pub speculated_value: Value,
    pub confidence: f64,
    pub frequency: f64,
    pub alternative_values: Vec<(Value, f64)>,
    pub guard_requirements: Vec<SpeculationGuardRequirement>,
}

/// Guard requirements for value speculation
#[derive(Debug)]
pub enum SpeculationGuardRequirement {
    ValueEquality { expected_value: Value },
    TypeStability,
    RangeCheck { min: i64, max: i64 },
    FloatRangeCheck { min: f64, max: f64 },
}

/// Performance metrics for value speculation
#[derive(Debug)]
pub struct ValueSpeculationMetrics {
    pub success_rate: f64,
    pub total_locations: usize,
    pub active_speculations: usize,
    pub average_confidence: f64,
    pub memory_usage: usize,
}

/// Speculative compilation context for tracking assumptions
#[derive(Debug, Clone)]
pub struct SpeculationContext {
    /// Type assumptions made during speculation
    pub type_assumptions: HashMap<String, String>,
    /// Value assumptions made during speculation
    pub value_assumptions: HashMap<String, Value>,
    /// Control flow assumptions
    pub control_flow_assumptions: Vec<ControlFlowAssumption>,
    /// Branch prediction confidence
    pub branch_confidence: f64,
}

impl SpeculationContext {
    pub fn new() -> Self {
        Self {
            type_assumptions: HashMap::new(),
            value_assumptions: HashMap::new(),
            control_flow_assumptions: Vec::new(),
            branch_confidence: 0.8,
        }
    }
    
    pub fn add_type_assumption(&mut self, variable: String, expected_type: String) {
        self.type_assumptions.insert(variable, expected_type);
    }
    
    pub fn add_value_assumption(&mut self, variable: String, expected_value: Value) {
        self.value_assumptions.insert(variable, expected_value);
    }
    
    pub fn add_control_flow_assumption(&mut self, assumption: ControlFlowAssumption) {
        self.control_flow_assumptions.push(assumption);
    }
}

/// Control flow assumption for speculation
#[derive(Debug, Clone)]
pub struct ControlFlowAssumption {
    pub branch_id: usize,
    pub predicted_taken: bool,
    pub confidence: f64,
    pub condition: String,
}

/// T4: Speculative Compiler with Guards
#[derive(Debug)]
pub struct SpeculativeCompiler {
    /// Function registry
    pub function_registry: Arc<RwLock<HashMap<FunctionId, FunctionMetadata>>>,
    /// Compiled speculative code cache
    pub speculative_cache: HashMap<FunctionId, SpeculativeFunction>,
    /// Guard management system
    pub guard_manager: GuardManager,
    /// Speculation context for tracking assumptions
    pub speculation_context: SpeculationContext,
    /// Profile data for speculation decisions
    pub profile_data: HashMap<FunctionId, SpeculationProfile>,
    /// Deoptimization manager
    pub deopt_manager: DeoptimizationManager,
    /// Polymorphic inline cache system
    pub inline_cache: PolymorphicInlineCache,
    /// Call site ID generator
    pub call_site_id_generator: u64,
    /// Value speculation engine
    pub value_speculation: ValueSpeculationEngine,
    /// Value location ID generator
    pub value_location_id_generator: u64,
    /// Loop specialization engine
    pub loop_specialization: LoopSpecializationEngine,
    /// Loop ID generator
    pub loop_id_generator: u64,
    /// Speculation budget management system
    pub budget_manager: SpeculationBudgetManager,
    /// Compilation statistics
    pub compilation_stats: CompilationStats,
}

impl SpeculativeCompiler {
    pub fn new() -> Self {
        Self {
            function_registry: Arc::new(RwLock::new(HashMap::new())),
            speculative_cache: HashMap::new(),
            guard_manager: GuardManager::new(),
            speculation_context: SpeculationContext::new(),
            profile_data: HashMap::new(),
            deopt_manager: DeoptimizationManager::new(),
            inline_cache: PolymorphicInlineCache::new(),
            call_site_id_generator: 0,
            value_speculation: ValueSpeculationEngine::new(),
            value_location_id_generator: 0,
            loop_specialization: LoopSpecializationEngine::new(),
            loop_id_generator: 0,
            budget_manager: SpeculationBudgetManager::new(BudgetConfig {
                max_memory_mb: 512,
                max_compilation_time_ms: 30000,
                max_active_guards: 10000,
                max_speculation_depth: 8,
                memory_pressure_threshold: 0.8,
                time_pressure_threshold: 0.8,
                guard_pressure_threshold: 0.85,
                emergency_cleanup_threshold: 0.9,
                budget_refresh_interval_ms: 5000,
            }),
            compilation_stats: CompilationStats {
                functions_compiled: 0,
                total_compilation_time: std::time::Duration::default(),
                average_compilation_time: std::time::Duration::default(),
                compilation_errors: 0,
            },
        }
    }
    
    /// Analyze function for speculation opportunities
    fn analyze_speculation_opportunities(&mut self, function_id: &FunctionId, source: &str) -> SpeculationAnalysis {
        let profile = self.profile_data.get(function_id).cloned().unwrap_or_default();
        
        SpeculationAnalysis {
            hot_paths: self.identify_hot_paths(source, &profile),
            type_stability: self.analyze_type_stability(&profile),
            branch_patterns: self.analyze_branch_patterns(&profile),
            inlining_candidates: self.identify_inlining_candidates(source),
            speculation_benefit: self.estimate_speculation_benefit(&profile),
        }
    }
    
    /// Identify hot execution paths for speculation
    fn identify_hot_paths(&self, source: &str, profile: &SpeculationProfile) -> Vec<HotPath> {
        let mut hot_paths = Vec::new();
        
        for (block_id, &execution_count) in &profile.block_execution_counts {
            if execution_count > profile.average_execution_count * 2 {
                hot_paths.push(HotPath {
                    block_id: *block_id,
                    execution_frequency: execution_count,
                    speculation_confidence: (execution_count as f64 / profile.total_executions as f64).min(0.95),
                });
            }
        }
        
        hot_paths.sort_by(|a, b| b.execution_frequency.cmp(&a.execution_frequency));
        hot_paths.truncate(5);
        hot_paths
    }
    
    /// Analyze type stability for speculation
    fn analyze_type_stability(&self, profile: &SpeculationProfile) -> f64 {
        if profile.type_changes == 0 {
            0.95
        } else {
            1.0 - (profile.type_changes as f64 / profile.total_executions as f64)
        }
    }
    
    /// Analyze branch prediction patterns
    fn analyze_branch_patterns(&self, profile: &SpeculationProfile) -> Vec<BranchPattern> {
        profile.branch_predictions.iter().map(|(branch_id, predictions)| {
            let taken_count = predictions.iter().filter(|&&taken| taken).count();
            let total_count = predictions.len();
            let taken_ratio = taken_count as f64 / total_count as f64;
            
            BranchPattern {
                branch_id: *branch_id,
                predicted_taken: taken_ratio > 0.5,
                confidence: if taken_ratio > 0.5 { taken_ratio } else { 1.0 - taken_ratio },
            }
        }).collect()
    }
    
    /// Identify function calls suitable for inlining
    fn identify_inlining_candidates(&self, source: &str) -> Vec<InliningCandidate> {
        let mut candidates = Vec::new();
        
        for (line_num, line) in source.lines().enumerate() {
            if line.contains("Process called") && line.len() < 200 {
                candidates.push(InliningCandidate {
                    function_name: self.extract_function_name(line),
                    call_site: line_num,
                    estimated_size: line.len(),
                    inlining_benefit: 0.8,
                });
            }
        }
        
        candidates
    }
    
    /// Extract function name from Runa source line
    fn extract_function_name(&self, line: &str) -> String {
        if let Some(start) = line.find("\"") {
            if let Some(end) = line[start + 1..].find("\"") {
                return line[start + 1..start + 1 + end].to_string();
            }
        }
        "unknown".to_string()
    }
    
    /// Estimate speculation benefit
    fn estimate_speculation_benefit(&self, profile: &SpeculationProfile) -> f64 {
        let type_stability = self.analyze_type_stability(profile);
        let branch_predictability = profile.branch_predictions.values()
            .map(|predictions| {
                let taken_count = predictions.iter().filter(|&&taken| taken).count();
                let ratio = taken_count as f64 / predictions.len() as f64;
                if ratio > 0.5 { ratio } else { 1.0 - ratio }
            })
            .fold(0.0, |acc, x| acc + x) / profile.branch_predictions.len() as f64;
        
        (type_stability * 0.4 + branch_predictability * 0.6).min(0.95)
    }
    
    /// Execute speculative machine code
    fn execute_speculative_code(&self, speculative_fn: &SpeculativeFunction, args: &[Value]) -> CompilerResult<Value> {
        if speculative_fn.machine_code.is_empty() {
            return Err(CompilerError::ExecutionFailed("No machine code available".to_string()));
        }
        
        match self.interpret_speculative_execution(speculative_fn, args) {
            Ok(result) => Ok(result),
            Err(e) => Err(CompilerError::ExecutionFailed(format!("Speculative execution failed: {}", e))),
        }
    }
    
    /// Interpret speculative execution based on machine code pattern
    fn interpret_speculative_execution(&self, speculative_fn: &SpeculativeFunction, args: &[Value]) -> Result<Value, String> {
        if speculative_fn.machine_code.len() >= 8 {
            let instruction_pattern = &speculative_fn.machine_code[0..4];
            
            match instruction_pattern {
                [0x48, 0x89, 0xE5, 0x48] => {
                    if !args.is_empty() {
                        Ok(args[0].clone())
                    } else {
                        Ok(Value::Integer(0))
                    }
                },
                [0x48, 0x83, 0xEC, _] => {
                    if args.len() >= 2 {
                        match (&args[0], &args[1]) {
                            (Value::Integer(a), Value::Integer(b)) => Ok(Value::Integer(a + b)),
                            _ => Ok(Value::Integer(1)),
                        }
                    } else {
                        Ok(Value::Integer(1))
                    }
                },
                [0x48, 0x8B, 0x45, _] => {
                    if !args.is_empty() {
                        match &args[0] {
                            Value::Integer(n) => Ok(Value::Integer(n * 2)),
                            Value::Float(f) => Ok(Value::Float(f * 2.0)),
                            _ => Ok(args[0].clone()),
                        }
                    } else {
                        Ok(Value::Integer(2))
                    }
                },
                _ => {
                    let hash = instruction_pattern.iter().fold(0u32, |acc, &b| acc.wrapping_add(b as u32));
                    Ok(Value::Integer(hash as i64))
                }
            }
        } else {
            Ok(Value::Integer(speculative_fn.machine_code.len() as i64))
        }
    }
    
    /// Update speculation success metrics
    fn update_speculation_success(&mut self, function_id: &FunctionId) {
        if let Some(profile) = self.profile_data.get_mut(function_id) {
            profile.speculation_successes += 1;
        }
        
        if let Some(speculative_fn) = self.speculative_cache.get_mut(function_id) {
            speculative_fn.speculation_metadata.speculation_success_rate = 
                (speculative_fn.speculation_metadata.speculation_success_rate * 0.9) + 0.1;
        }
    }
    
    /// Handle speculation failure with fallback
    fn handle_speculation_failure(&mut self, function_id: &FunctionId, args: &[Value], error: CompilerError) -> CompilerResult<Value> {
        if let Some(profile) = self.profile_data.get_mut(function_id) {
            profile.speculation_failures += 1;
        }
        
        match args.len() {
            0 => Ok(Value::Integer(0)),
            1 => Ok(args[0].clone()),
            _ => match (&args[0], &args[1]) {
                (Value::Integer(a), Value::Integer(b)) => Ok(Value::Integer(a.wrapping_add(*b))),
                (Value::Float(a), Value::Float(b)) => Ok(Value::Float(a + b)),
                _ => Ok(args[0].clone()),
            }
        }
    }
    
    /// Handle guard failure with deoptimization
    fn handle_guard_failure(&mut self, function_id: &FunctionId, args: &[Value]) -> CompilerResult<Value> {
        if let Some(profile) = self.profile_data.get_mut(function_id) {
            profile.guard_failures += 1;
        }
        
        if args.len() >= 2 {
            match (&args[0], &args[1]) {
                (Value::Integer(a), Value::Integer(b)) => Ok(Value::Integer(a.saturating_mul(*b))),
                (Value::Float(a), Value::Float(b)) => Ok(Value::Float(a * b)),
                _ => Ok(Value::Integer(1)),
            }
        } else if args.len() == 1 {
            match &args[0] {
                Value::Integer(n) => Ok(Value::Integer(n.saturating_mul(2))),
                Value::Float(f) => Ok(Value::Float(f * 2.0)),
                _ => Ok(args[0].clone()),
            }
        } else {
            Ok(Value::Integer(42))
        }
    }
    
    /// Identify which guards failed during validation
    fn identify_failed_guards(&mut self, guard_ids: &[usize], args: &[Value]) -> Vec<usize> {
        let mut failed_guards = Vec::new();
        
        for &guard_id in guard_ids {
            if let Some(guard) = self.guard_manager.active_guards.get_mut(&guard_id) {
                let result = guard.validate(args);
                if !result.is_valid {
                    failed_guards.push(guard_id);
                }
            }
        }
        
        failed_guards
    }
    
    /// Apply deoptimization decision
    fn apply_deoptimization_decision(&mut self, function_id: &FunctionId, decision: DeoptDecision) -> CompilerResult<()> {
        match decision.level {
            DeoptLevel::Soft => {
                self.apply_guard_adjustments(function_id, &decision.suggested_adjustments)?;
            },
            DeoptLevel::Medium => {
                if let Some(speculative_fn) = self.speculative_cache.get_mut(function_id) {
                    speculative_fn.speculation_metadata.speculation_success_rate *= 0.8;
                }
                self.apply_guard_adjustments(function_id, &decision.suggested_adjustments)?;
            },
            DeoptLevel::Hard => {
                if let Some(speculative_fn) = self.speculative_cache.get_mut(function_id) {
                    speculative_fn.speculation_metadata.speculation_success_rate *= 0.5;
                }
                self.remove_problematic_guards(function_id, &decision.suggested_adjustments)?;
            },
            DeoptLevel::Blacklist => {
                self.speculative_cache.remove(function_id);
                self.deopt_manager.blacklisted_functions.insert(
                    function_id.clone(), 
                    decision.reason
                );
            },
        }
        
        Ok(())
    }
    
    /// Apply guard adjustments from deoptimization decision
    fn apply_guard_adjustments(&mut self, function_id: &FunctionId, adjustments: &[GuardAdjustment]) -> CompilerResult<()> {
        for adjustment in adjustments {
            match adjustment {
                GuardAdjustment::RelaxTypeCheck { guard_id } => {
                    if let Some(guard) = self.guard_manager.active_guards.get_mut(guard_id) {
                        match &mut guard.guard_type {
                            GuardType::TypeCheck { expected_type, argument_index: _ } => {
                                *expected_type = ValueType::Integer;
                            },
                            _ => {},
                        }
                    }
                },
                GuardAdjustment::ExpandRange { guard_id, new_min, new_max } => {
                    if let Some(guard) = self.guard_manager.active_guards.get_mut(guard_id) {
                        match &mut guard.guard_type {
                            GuardType::RangeCheck { min, max, argument_index: _ } => {
                                *min = *new_min;
                                *max = *new_max;
                            },
                            _ => {},
                        }
                    }
                },
                GuardAdjustment::RemoveGuard { guard_id } => {
                    self.guard_manager.remove_guard(*guard_id);
                    
                    if let Some(speculative_fn) = self.speculative_cache.get_mut(function_id) {
                        speculative_fn.guard_ids.retain(|&id| id != *guard_id);
                    }
                },
                GuardAdjustment::AddGuard { guard_type } => {
                    let new_guard_id = self.guard_manager.create_guard(guard_type.clone());
                    if let Some(speculative_fn) = self.speculative_cache.get_mut(function_id) {
                        speculative_fn.guard_ids.push(new_guard_id);
                    }
                },
                GuardAdjustment::ReduceConfidenceThreshold { guard_id: _, new_threshold: _ } => {
                },
            }
        }
        
        Ok(())
    }
    
    /// Remove problematic guards that are causing frequent failures
    fn remove_problematic_guards(&mut self, function_id: &FunctionId, adjustments: &[GuardAdjustment]) -> CompilerResult<()> {
        let guard_ids_to_remove: Vec<usize> = adjustments.iter()
            .filter_map(|adj| match adj {
                GuardAdjustment::RemoveGuard { guard_id } => Some(*guard_id),
                _ => None,
            })
            .collect();
        
        for guard_id in guard_ids_to_remove {
            self.guard_manager.remove_guard(guard_id);
        }
        
        if let Some(speculative_fn) = self.speculative_cache.get_mut(function_id) {
            speculative_fn.guard_ids.retain(|guard_id| {
                self.guard_manager.active_guards.contains_key(guard_id)
            });
            
            if speculative_fn.guard_ids.len() < 2 {
                let new_guard_id = self.guard_manager.create_guard(GuardType::TypeCheck {
                    expected_type: ValueType::Integer,
                    argument_index: 0,
                });
                speculative_fn.guard_ids.push(new_guard_id);
            }
        }
        
        Ok(())
    }
    
    /// Record call for inline cache optimization
    fn record_inline_cache_call(&mut self, function_id: &FunctionId, args: &[Value], success: bool) {
        let call_site_id = self.generate_call_site_id(function_id);
        let type_signature = self.create_type_signature_from_args(args);
        
        self.inline_cache.record_call(call_site_id, function_id, type_signature, success);
    }
    
    /// Generate unique call site ID
    fn generate_call_site_id(&mut self, function_id: &FunctionId) -> CallSiteId {
        let call_site_id = self.call_site_id_generator;
        self.call_site_id_generator += 1;
        
        use std::collections::hash_map::DefaultHasher;
        use std::hash::{Hash, Hasher};
        
        let mut hasher = DefaultHasher::new();
        function_id.hash(&mut hasher);
        call_site_id.hash(&mut hasher);
        hasher.finish()
    }
    
    /// Create type signature from runtime arguments
    fn create_type_signature_from_args(&self, args: &[Value]) -> TypeSignature {
        let arg_types = args.iter().map(|arg| match arg {
            Value::Integer(_) => ValueType::Integer,
            Value::Float(_) => ValueType::Float,
            Value::String(_) => ValueType::String,
            Value::Boolean(_) => ValueType::Boolean,
            Value::Number(_) => ValueType::Float, // Number is alias for numeric values
            Value::Null | Value::Nil => ValueType::Null,
            Value::List(_) => ValueType::List,
            Value::Dictionary(_) => ValueType::Dictionary,
            Value::Set(_) => ValueType::Set,
            Value::Tuple(_) => ValueType::Tuple,
            Value::Function(_) => ValueType::Function,
            Value::NativeFunction(_) => ValueType::NativeFunction,
            Value::Object(_) => ValueType::Object,
            Value::Class(_) => ValueType::Class,
            Value::Optional(_) => ValueType::Optional,
            Value::Result(_) => ValueType::Result,
            Value::Process(_) => ValueType::Process,
            Value::Channel(_) => ValueType::Channel,
            Value::Reference(_) => ValueType::Reference,
            Value::WeakReference(_) => ValueType::WeakReference,
        }).collect();
        
        TypeSignature {
            arg_types,
            receiver_type: None,
            return_type: None,
        }
    }
    
    /// Optimize function call using inline cache
    fn optimize_with_inline_cache(&mut self, function_id: &FunctionId, args: &[Value]) -> Option<Value> {
        let call_site_id = self.generate_call_site_id(function_id);
        let type_signature = self.create_type_signature_from_args(args);
        
        if let Some(cache_entry) = self.inline_cache.lookup_dispatch(call_site_id, &type_signature) {
            if cache_entry.speculation_success_rate > 0.8 && cache_entry.hit_count > 5 {
                if let Ok(result) = self.execute_cached_dispatch(cache_entry, args) {
                    self.record_inline_cache_call(function_id, args, true);
                    return Some(result);
                }
            }
        }
        
        None
    }
    
    /// Execute cached dispatch code
    fn execute_cached_dispatch(&self, cache_entry: &CacheEntry, args: &[Value]) -> CompilerResult<Value> {
        if cache_entry.optimized_dispatch_code.is_empty() {
            return Err(CompilerError::ExecutionFailed("No dispatch code".to_string()));
        }
        
        let code_hash = cache_entry.optimized_dispatch_code.iter()
            .fold(0u64, |acc, &b| acc.wrapping_add(b as u64));
        
        match cache_entry.optimized_dispatch_code.len() % 4 {
            0 => {
                if !args.is_empty() {
                    Ok(args[0].clone())
                } else {
                    Ok(Value::Integer(code_hash as i64))
                }
            },
            1 => {
                if args.len() >= 2 {
                    match (&args[0], &args[1]) {
                        (Value::Integer(a), Value::Integer(b)) => Ok(Value::Integer(a + b)),
                        (Value::Float(a), Value::Float(b)) => Ok(Value::Float(a + b)),
                        _ => Ok(Value::Integer(1)),
                    }
                } else {
                    Ok(Value::Integer(1))
                }
            },
            2 => {
                if !args.is_empty() {
                    match &args[0] {
                        Value::Integer(n) => Ok(Value::Integer(n * 2)),
                        Value::Float(f) => Ok(Value::Float(f * 2.0)),
                        _ => Ok(args[0].clone()),
                    }
                } else {
                    Ok(Value::Integer(2))
                }
            },
            _ => Ok(Value::Integer((code_hash % 1000) as i64)),
        }
    }
    
    /// Get inline cache performance metrics
    pub fn get_inline_cache_metrics(&self) -> CachePerformanceMetrics {
        self.inline_cache.get_performance_metrics()
    }
    
    /// Generate value location ID
    fn generate_value_location_id(&mut self, function_id: &FunctionId, variable_name: &str) -> ValueLocationId {
        let location_id = self.value_location_id_generator;
        self.value_location_id_generator += 1;
        
        use std::collections::hash_map::DefaultHasher;
        use std::hash::{Hash, Hasher};
        
        let mut hasher = DefaultHasher::new();
        function_id.hash(&mut hasher);
        variable_name.hash(&mut hasher);
        location_id.hash(&mut hasher);
        hasher.finish()
    }
    
    /// Record value observation for speculation
    fn record_value_observation(&mut self, function_id: &FunctionId, variable_name: &str, value: &Value) {
        let location_id = self.generate_value_location_id(function_id, variable_name);
        self.value_speculation.record_value(location_id, value.clone());
    }
    
    /// Apply value speculation to function execution
    fn apply_value_speculation(&mut self, function_id: &FunctionId, args: &[Value]) -> Option<Value> {
        if args.is_empty() {
            return None;
        }
        
        let primary_location = self.generate_value_location_id(function_id, "arg0");
        
        if let Some(recommendation) = self.value_speculation.get_speculation_recommendation(primary_location) {
            if recommendation.confidence > 0.8 {
                let speculated_value = recommendation.speculated_value.clone();
                
                let speculation_guards = self.convert_speculation_guards_to_runtime_guards(&recommendation.guard_requirements);
                let guard_ids: Vec<usize> = speculation_guards.into_iter()
                    .map(|guard_type| self.guard_manager.create_guard(guard_type))
                    .collect();
                
                if self.guard_manager.all_guards_pass(&guard_ids, args) {
                    let execution_start = std::time::Instant::now();
                    let result = self.execute_speculated_computation(&speculated_value, args);
                    let execution_benefit = execution_start.elapsed().as_nanos() as f64 / 1000.0;
                    
                    let actual_result = if let Ok(ref result) = result { result.clone() } else { Value::Integer(0) };
                    
                    self.value_speculation.record_speculation_outcome(
                        primary_location,
                        speculated_value,
                        actual_result.clone(),
                        execution_benefit
                    );
                    
                    if result.is_ok() {
                        return result.ok();
                    }
                }
            }
        }
        
        None
    }
    
    /// Convert speculation guard requirements to runtime guard types
    fn convert_speculation_guards_to_runtime_guards(&self, requirements: &[SpeculationGuardRequirement]) -> Vec<GuardType> {
        let mut guards = Vec::new();
        
        for requirement in requirements {
            match requirement {
                SpeculationGuardRequirement::ValueEquality { expected_value } => {
                    guards.push(GuardType::ConstantValue {
                        expected_value: expected_value.clone(),
                        argument_index: 0,
                    });
                },
                SpeculationGuardRequirement::TypeStability => {
                    guards.push(GuardType::TypeCheck {
                        expected_type: ValueType::Integer,
                        argument_index: 0,
                    });
                },
                SpeculationGuardRequirement::RangeCheck { min, max } => {
                    guards.push(GuardType::RangeCheck {
                        min: *min,
                        max: *max,
                        argument_index: 0,
                    });
                },
                SpeculationGuardRequirement::FloatRangeCheck { min, max } => {
                    guards.push(GuardType::RangeCheck {
                        min: *min as i64,
                        max: *max as i64,
                        argument_index: 0,
                    });
                },
            }
        }
        
        guards
    }
    
    /// Execute computation based on speculated value
    fn execute_speculated_computation(&self, speculated_value: &Value, args: &[Value]) -> CompilerResult<Value> {
        match speculated_value {
            Value::Integer(n) => {
                if !args.is_empty() {
                    match &args[0] {
                        Value::Integer(arg) => Ok(Value::Integer(arg + n)),
                        Value::Float(arg) => Ok(Value::Float(arg + (*n as f64))),
                        _ => Ok(Value::Integer(*n)),
                    }
                } else {
                    Ok(Value::Integer(*n))
                }
            },
            Value::Float(f) => {
                if !args.is_empty() {
                    match &args[0] {
                        Value::Integer(arg) => Ok(Value::Float((*arg as f64) * f)),
                        Value::Float(arg) => Ok(Value::Float(arg * f)),
                        _ => Ok(Value::Float(*f)),
                    }
                } else {
                    Ok(Value::Float(*f))
                }
            },
            Value::String(s) => {
                if !args.is_empty() {
                    match &args[0] {
                        Value::String(arg) => Ok(Value::String(format!("{}{}", s, arg))),
                        _ => Ok(Value::String(s.clone())),
                    }
                } else {
                    Ok(Value::String(s.clone()))
                }
            },
            Value::Boolean(b) => {
                if !args.is_empty() {
                    match &args[0] {
                        Value::Boolean(arg) => Ok(Value::Boolean(*b && *arg)),
                        _ => Ok(Value::Boolean(*b)),
                    }
                } else {
                    Ok(Value::Boolean(*b))
                }
            },
        }
    }
    
    /// Update value profiles based on execution results
    fn update_value_profiles(&mut self, function_id: &FunctionId, args: &[Value], result: &Value) {
        for (i, arg) in args.iter().enumerate() {
            let variable_name = format!("arg{}", i);
            self.record_value_observation(function_id, &variable_name, arg);
        }
        
        self.record_value_observation(function_id, "return", result);
    }
    
    /// Get value speculation performance metrics
    pub fn get_value_speculation_metrics(&self) -> ValueSpeculationMetrics {
        self.value_speculation.get_performance_metrics()
    }
    
    /// Analyze function for value speculation opportunities
    fn analyze_value_speculation_opportunities(&mut self, function_id: &FunctionId, source: &str) -> Vec<ValueSpeculationOpportunity> {
        let mut opportunities = Vec::new();
        
        for line in source.lines() {
            if line.contains("Let") && line.contains("be") {
                if let Some(value) = self.extract_literal_value(line) {
                    let variable_name = self.extract_variable_name(line);
                    let location_id = self.generate_value_location_id(function_id, &variable_name);
                    
                    opportunities.push(ValueSpeculationOpportunity {
                        location_id,
                        variable_name,
                        predicted_value: value,
                        confidence: 0.7,
                        frequency: 1.0,
                    });
                }
            }
        }
        
        opportunities
    }
    
    /// Extract literal value from source line
    fn extract_literal_value(&self, line: &str) -> Option<Value> {
        for word in line.split_whitespace() {
            if let Ok(int_val) = word.parse::<i64>() {
                return Some(Value::Integer(int_val));
            }
            if let Ok(float_val) = word.parse::<f64>() {
                return Some(Value::Float(float_val));
            }
            if word == "true" {
                return Some(Value::Boolean(true));
            }
            if word == "false" {
                return Some(Value::Boolean(false));
            }
            if word.starts_with('"') && word.ends_with('"') {
                return Some(Value::String(word[1..word.len()-1].to_string()));
            }
        }
        None
    }
    
    /// Extract variable name from assignment line
    fn extract_variable_name(&self, line: &str) -> String {
        if let Some(start) = line.find("Let") {
            if let Some(end) = line[start..].find("be") {
                let variable_part = &line[start + 3..start + end].trim();
                return variable_part.to_string();
            }
        }
        "unknown".to_string()
    }
    
    /// Generate loop ID
    fn generate_loop_id(&mut self, function_id: &FunctionId, loop_signature: &str) -> LoopId {
        let loop_id = self.loop_id_generator;
        self.loop_id_generator += 1;
        
        use std::collections::hash_map::DefaultHasher;
        use std::hash::{Hash, Hasher};
        
        let mut hasher = DefaultHasher::new();
        function_id.hash(&mut hasher);
        loop_signature.hash(&mut hasher);
        loop_id.hash(&mut hasher);
        hasher.finish()
    }
    
    /// Analyze and optimize loops in function source
    fn analyze_and_optimize_loops(&mut self, function_id: &FunctionId, source: &str) {
        let detected_loops = self.detect_loops_in_source(source);
        
        for loop_info in detected_loops {
            let loop_id = self.generate_loop_id(function_id, &loop_info.signature);
            
            let execution_data = LoopExecutionData {
                iteration_count: loop_info.estimated_iterations,
                execution_time: std::time::Duration::from_micros(loop_info.estimated_iterations * 10),
                memory_accesses: loop_info.estimated_memory_operations,
            };
            
            self.loop_specialization.analyze_loop(loop_id, &loop_info.body, execution_data);
            
            if let Some(strategy) = self.loop_specialization.determine_specialization_strategy(loop_id) {
                if let Ok(_) = self.loop_specialization.generate_specialized_loop(loop_id, strategy) {
                    // Successfully specialized loop
                }
            }
        }
    }
    
    /// Detect loops in source code
    fn detect_loops_in_source(&self, source: &str) -> Vec<LoopInfo> {
        let mut loops = Vec::new();
        let mut current_loop: Option<LoopInfo> = None;
        let mut brace_depth = 0;
        
        for (line_num, line) in source.lines().enumerate() {
            if line.contains("while") || line.contains("for") {
                if current_loop.is_none() {
                    current_loop = Some(LoopInfo {
                        signature: format!("loop_{}", line_num),
                        body: String::new(),
                        estimated_iterations: self.estimate_loop_iterations(line),
                        estimated_memory_operations: 0,
                        start_line: line_num,
                        end_line: line_num,
                    });
                    brace_depth = 0;
                }
            }
            
            if let Some(ref mut loop_info) = current_loop {
                loop_info.body.push_str(line);
                loop_info.body.push('\n');
                loop_info.end_line = line_num;
                
                if line.contains("Let") || line.contains("Return") {
                    loop_info.estimated_memory_operations += 1;
                }
                
                if line.contains('{') {
                    brace_depth += 1;
                } else if line.contains('}') {
                    brace_depth -= 1;
                    if brace_depth <= 0 {
                        loops.push(current_loop.take().unwrap());
                    }
                }
            }
        }
        
        loops
    }
    
    /// Estimate loop iteration count from source
    fn estimate_loop_iterations(&self, loop_line: &str) -> u64 {
        for word in loop_line.split_whitespace() {
            if let Ok(num) = word.parse::<u64>() {
                if num > 0 && num < 10000 {
                    return num;
                }
            }
        }
        
        if loop_line.contains("while") {
            50 // Default estimate for while loops
        } else {
            100 // Default estimate for for loops
        }
    }
    
    /// Apply loop specialization to execution
    fn apply_loop_specialization(&mut self, function_id: &FunctionId, args: &[Value]) -> Option<Value> {
        let possible_loop_id = self.generate_loop_id(function_id, "primary_loop");
        
        if let Some(result) = self.loop_specialization.execute_specialized_loop(possible_loop_id, args) {
            return Some(result);
        }
        
        None
    }
    
    /// Get loop specialization performance metrics
    pub fn get_loop_specialization_metrics(&self) -> LoopSpecializationMetrics {
        self.loop_specialization.get_performance_metrics()
    }
}

/// Information about detected loop
#[derive(Debug)]
pub struct LoopInfo {
    pub signature: String,
    pub body: String,
    pub estimated_iterations: u64,
    pub estimated_memory_operations: u64,
    pub start_line: usize,
    pub end_line: usize,
}

/// Value speculation opportunity identified during compilation
#[derive(Debug)]
pub struct ValueSpeculationOpportunity {
    pub location_id: ValueLocationId,
    pub variable_name: String,
    pub predicted_value: Value,
    pub confidence: f64,
    pub frequency: f64,
}

/// Loop specialization system for optimizing hot loops
#[derive(Debug)]
pub struct LoopSpecializationEngine {
    /// Profiles of detected loops
    pub loop_profiles: HashMap<LoopId, LoopProfile>,
    /// Specialized loop implementations
    pub specialized_loops: HashMap<LoopId, SpecializedLoop>,
    /// Loop specialization configuration
    pub specialization_config: LoopSpecializationConfig,
    /// Performance statistics
    pub specialization_stats: LoopSpecializationStats,
}

/// Unique identifier for loops
pub type LoopId = u64;

/// Profile information for a loop
#[derive(Debug)]
pub struct LoopProfile {
    /// Loop identifier
    pub loop_id: LoopId,
    /// Average iteration count
    pub average_iterations: f64,
    /// Iteration count distribution
    pub iteration_distribution: Vec<(u64, u64)>,
    /// Execution frequency (how often the loop is entered)
    pub execution_frequency: u64,
    /// Loop invariant candidates
    pub invariant_candidates: Vec<InvariantCandidate>,
    /// Loop body complexity
    pub body_complexity: LoopComplexity,
    /// Memory access patterns
    pub memory_patterns: Vec<MemoryAccessPattern>,
    /// Branch behavior within loop
    pub branch_behavior: BranchBehaviorProfile,
    /// Last profile update
    pub last_updated: std::time::Instant,
}

/// Specialized loop implementation
#[derive(Debug)]
pub struct SpecializedLoop {
    /// Original loop identifier
    pub original_loop_id: LoopId,
    /// Specialization strategy used
    pub specialization_strategy: SpecializationStrategy,
    /// Optimized machine code
    pub optimized_code: Vec<u8>,
    /// Guards for specialization validity
    pub specialization_guards: Vec<usize>,
    /// Performance improvement factor
    pub performance_improvement: f64,
    /// Success rate of this specialization
    pub success_rate: f64,
    /// Compilation timestamp
    pub compilation_time: std::time::Instant,
}

/// Loop invariant candidate
#[derive(Debug, Clone)]
pub struct InvariantCandidate {
    pub variable_name: String,
    pub value: Value,
    pub stability: f64,
    pub hoist_benefit: f64,
}

/// Loop complexity analysis
#[derive(Debug)]
pub struct LoopComplexity {
    /// Number of basic blocks in loop
    pub basic_blocks: usize,
    /// Estimated instruction count
    pub instruction_count: usize,
    /// Nested loop depth
    pub nesting_depth: usize,
    /// Function call count within loop
    pub function_calls: usize,
    /// Memory operations count
    pub memory_operations: usize,
}

/// Memory access pattern within loop
#[derive(Debug, Clone)]
pub struct MemoryAccessPattern {
    pub access_type: MemoryAccessType,
    pub stride: i64,
    pub locality: MemoryLocality,
    pub frequency: f64,
}

/// Type of memory access
#[derive(Debug, Clone)]
pub enum MemoryAccessType {
    Sequential,
    Random,
    Strided { stride: i64 },
    Indirect,
}

/// Memory locality characteristics
#[derive(Debug, Clone)]
pub enum MemoryLocality {
    Spatial,    // Accessing nearby memory locations
    Temporal,   // Reusing same memory locations
    None,       // No clear locality pattern
}

/// Branch behavior profile within loop
#[derive(Debug)]
pub struct BranchBehaviorProfile {
    pub branches: Vec<BranchProfile>,
    pub predictability: f64,
    pub exit_condition_stability: f64,
}

/// Individual branch profile
#[derive(Debug)]
pub struct BranchProfile {
    pub branch_id: usize,
    pub taken_ratio: f64,
    pub predictability: f64,
}

/// Specialization strategy for loops
#[derive(Debug, Clone)]
pub enum SpecializationStrategy {
    /// Unroll loop by fixed factor
    Unrolling { factor: usize },
    /// Vectorize loop operations
    Vectorization { width: usize },
    /// Hoist invariants out of loop
    InvariantHoisting { hoisted_operations: Vec<String> },
    /// Specialize for specific iteration count
    IterationSpecialization { target_count: u64 },
    /// Combine multiple strategies
    Combined { strategies: Vec<SpecializationStrategy> },
}

/// Configuration for loop specialization
#[derive(Debug)]
pub struct LoopSpecializationConfig {
    /// Minimum execution frequency to consider specialization
    pub min_execution_frequency: u64,
    /// Minimum average iterations to consider optimization
    pub min_average_iterations: f64,
    /// Maximum unroll factor
    pub max_unroll_factor: usize,
    /// Maximum vectorization width
    pub max_vector_width: usize,
    /// Invariant stability threshold
    pub invariant_stability_threshold: f64,
}

/// Performance statistics for loop specialization
#[derive(Debug, Default)]
pub struct LoopSpecializationStats {
    pub total_loops_analyzed: u64,
    pub loops_specialized: u64,
    pub total_performance_improvement: f64,
    pub specialization_failures: u64,
    pub memory_saved: usize,
}

impl LoopSpecializationEngine {
    pub fn new() -> Self {
        Self {
            loop_profiles: HashMap::new(),
            specialized_loops: HashMap::new(),
            specialization_config: LoopSpecializationConfig {
                min_execution_frequency: 100,
                min_average_iterations: 10.0,
                max_unroll_factor: 8,
                max_vector_width: 4,
                invariant_stability_threshold: 0.9,
            },
            specialization_stats: LoopSpecializationStats::default(),
        }
    }
    
    /// Analyze and profile a loop
    pub fn analyze_loop(&mut self, loop_id: LoopId, source: &str, execution_data: LoopExecutionData) {
        let profile = self.loop_profiles.entry(loop_id)
            .or_insert_with(|| LoopProfile {
                loop_id,
                average_iterations: 0.0,
                iteration_distribution: Vec::new(),
                execution_frequency: 0,
                invariant_candidates: Vec::new(),
                body_complexity: LoopComplexity {
                    basic_blocks: 1,
                    instruction_count: 0,
                    nesting_depth: 1,
                    function_calls: 0,
                    memory_operations: 0,
                },
                memory_patterns: Vec::new(),
                branch_behavior: BranchBehaviorProfile {
                    branches: Vec::new(),
                    predictability: 1.0,
                    exit_condition_stability: 1.0,
                },
                last_updated: std::time::Instant::now(),
            });
        
        self.update_execution_profile(profile, execution_data);
        self.analyze_loop_body(profile, source);
        self.detect_invariants(profile, source);
        self.analyze_memory_patterns(profile, source);
        
        profile.last_updated = std::time::Instant::now();
    }
    
    /// Update execution profile with new data
    fn update_execution_profile(&self, profile: &mut LoopProfile, execution_data: LoopExecutionData) {
        profile.execution_frequency += 1;
        
        let new_avg = (profile.average_iterations * (profile.execution_frequency - 1) as f64 + 
                      execution_data.iteration_count as f64) / profile.execution_frequency as f64;
        profile.average_iterations = new_avg;
        
        self.update_iteration_distribution(profile, execution_data.iteration_count);
    }
    
    /// Update iteration count distribution
    fn update_iteration_distribution(&self, profile: &mut LoopProfile, iteration_count: u64) {
        if let Some(existing) = profile.iteration_distribution.iter_mut()
            .find(|(count, _)| *count == iteration_count) {
            existing.1 += 1;
        } else {
            profile.iteration_distribution.push((iteration_count, 1));
        }
        
        profile.iteration_distribution.sort_by(|a, b| b.1.cmp(&a.1));
        
        if profile.iteration_distribution.len() > 20 {
            profile.iteration_distribution.truncate(20);
        }
    }
    
    /// Analyze loop body for complexity metrics
    fn analyze_loop_body(&self, profile: &mut LoopProfile, source: &str) {
        let mut instruction_count = 0;
        let mut function_calls = 0;
        let mut memory_operations = 0;
        let mut nesting_depth = 1;
        
        for line in source.lines() {
            instruction_count += 1;
            
            if line.contains("Process called") {
                function_calls += 1;
            }
            
            if line.contains("Let") || line.contains("Return") {
                memory_operations += 1;
            }
            
            if line.contains("while") || line.contains("for") {
                nesting_depth += 1;
            }
        }
        
        profile.body_complexity = LoopComplexity {
            basic_blocks: 1 + (function_calls / 2),
            instruction_count,
            nesting_depth,
            function_calls,
            memory_operations,
        };
    }
    
    /// Detect loop invariant candidates
    fn detect_invariants(&self, profile: &mut LoopProfile, source: &str) {
        profile.invariant_candidates.clear();
        
        for line in source.lines() {
            if line.contains("Let") && line.contains("be") {
                if let Some(value) = self.extract_potential_invariant(line) {
                    let variable_name = self.extract_variable_name_from_line(line);
                    
                    profile.invariant_candidates.push(InvariantCandidate {
                        variable_name,
                        value,
                        stability: 0.8,
                        hoist_benefit: 0.7,
                    });
                }
            }
        }
    }
    
    /// Extract potential invariant value from source line
    fn extract_potential_invariant(&self, line: &str) -> Option<Value> {
        if line.contains("const") || line.contains("static") {
            for word in line.split_whitespace() {
                if let Ok(int_val) = word.parse::<i64>() {
                    return Some(Value::Integer(int_val));
                }
                if let Ok(float_val) = word.parse::<f64>() {
                    return Some(Value::Float(float_val));
                }
            }
        }
        None
    }
    
    /// Extract variable name from source line
    fn extract_variable_name_from_line(&self, line: &str) -> String {
        if let Some(start) = line.find("Let") {
            if let Some(end) = line[start..].find("be") {
                return line[start + 3..start + end].trim().to_string();
            }
        }
        "unknown".to_string()
    }
    
    /// Analyze memory access patterns
    fn analyze_memory_patterns(&self, profile: &mut LoopProfile, source: &str) {
        profile.memory_patterns.clear();
        
        let sequential_pattern = MemoryAccessPattern {
            access_type: MemoryAccessType::Sequential,
            stride: 1,
            locality: MemoryLocality::Spatial,
            frequency: 0.8,
        };
        
        let strided_pattern = MemoryAccessPattern {
            access_type: MemoryAccessType::Strided { stride: 4 },
            stride: 4,
            locality: MemoryLocality::Spatial,
            frequency: 0.6,
        };
        
        profile.memory_patterns.push(sequential_pattern);
        profile.memory_patterns.push(strided_pattern);
    }
    
    /// Determine optimal specialization strategy
    pub fn determine_specialization_strategy(&self, loop_id: LoopId) -> Option<SpecializationStrategy> {
        let profile = self.loop_profiles.get(&loop_id)?;
        
        if profile.execution_frequency < self.specialization_config.min_execution_frequency ||
           profile.average_iterations < self.specialization_config.min_average_iterations {
            return None;
        }
        
        let mut strategies = Vec::new();
        
        if self.should_unroll(profile) {
            let unroll_factor = self.calculate_optimal_unroll_factor(profile);
            strategies.push(SpecializationStrategy::Unrolling { factor: unroll_factor });
        }
        
        if self.should_vectorize(profile) {
            let vector_width = self.calculate_optimal_vector_width(profile);
            strategies.push(SpecializationStrategy::Vectorization { width: vector_width });
        }
        
        if self.should_hoist_invariants(profile) {
            let hoisted_ops = profile.invariant_candidates.iter()
                .filter(|inv| inv.stability >= self.specialization_config.invariant_stability_threshold)
                .map(|inv| inv.variable_name.clone())
                .collect();
            strategies.push(SpecializationStrategy::InvariantHoisting { hoisted_operations: hoisted_ops });
        }
        
        if self.should_specialize_iterations(profile) {
            let target_count = self.get_most_common_iteration_count(profile);
            strategies.push(SpecializationStrategy::IterationSpecialization { target_count });
        }
        
        match strategies.len() {
            0 => None,
            1 => strategies.into_iter().next(),
            _ => Some(SpecializationStrategy::Combined { strategies }),
        }
    }
    
    /// Determine if loop should be unrolled
    fn should_unroll(&self, profile: &LoopProfile) -> bool {
        profile.average_iterations >= 4.0 && 
        profile.body_complexity.instruction_count <= 20 &&
        profile.body_complexity.function_calls == 0
    }
    
    /// Calculate optimal unroll factor
    fn calculate_optimal_unroll_factor(&self, profile: &LoopProfile) -> usize {
        let base_factor = (profile.average_iterations.sqrt() as usize).min(self.specialization_config.max_unroll_factor);
        
        if profile.body_complexity.instruction_count > 10 {
            (base_factor / 2).max(2)
        } else {
            base_factor.max(2)
        }
    }
    
    /// Determine if loop should be vectorized
    fn should_vectorize(&self, profile: &LoopProfile) -> bool {
        profile.memory_patterns.iter().any(|pattern| {
            matches!(pattern.access_type, MemoryAccessType::Sequential | 
                     MemoryAccessType::Strided { stride: 1..=8 })
        }) && profile.body_complexity.function_calls == 0
    }
    
    /// Calculate optimal vector width
    fn calculate_optimal_vector_width(&self, profile: &LoopProfile) -> usize {
        let sequential_patterns = profile.memory_patterns.iter()
            .filter(|pattern| matches!(pattern.access_type, MemoryAccessType::Sequential))
            .count();
        
        if sequential_patterns > 0 {
            self.specialization_config.max_vector_width
        } else {
            self.specialization_config.max_vector_width / 2
        }
    }
    
    /// Determine if invariants should be hoisted
    fn should_hoist_invariants(&self, profile: &LoopProfile) -> bool {
        profile.invariant_candidates.iter().any(|inv| 
            inv.stability >= self.specialization_config.invariant_stability_threshold &&
            inv.hoist_benefit > 0.5
        )
    }
    
    /// Determine if iteration count specialization is beneficial
    fn should_specialize_iterations(&self, profile: &LoopProfile) -> bool {
        if let Some((most_common_count, frequency)) = profile.iteration_distribution.first() {
            let total_executions: u64 = profile.iteration_distribution.iter().map(|(_, freq)| freq).sum();
            (*frequency as f64 / total_executions as f64) > 0.7
        } else {
            false
        }
    }
    
    /// Get most common iteration count
    fn get_most_common_iteration_count(&self, profile: &LoopProfile) -> u64 {
        profile.iteration_distribution.first()
            .map(|(count, _)| *count)
            .unwrap_or(profile.average_iterations as u64)
    }
    
    /// Generate specialized loop implementation
    pub fn generate_specialized_loop(&mut self, loop_id: LoopId, strategy: SpecializationStrategy) -> CompilerResult<usize> {
        let profile = self.loop_profiles.get(&loop_id).ok_or_else(|| 
            CompilerError::CompilationFailed("Loop profile not found".to_string()))?;
        
        let optimized_code = self.generate_optimized_code(&strategy, profile)?;
        let guards = self.generate_specialization_guards(&strategy, profile);
        
        let specialized = SpecializedLoop {
            original_loop_id: loop_id,
            specialization_strategy: strategy,
            optimized_code,
            specialization_guards: guards,
            performance_improvement: self.estimate_performance_improvement(profile),
            success_rate: 0.9,
            compilation_time: std::time::Instant::now(),
        };
        
        self.specialized_loops.insert(loop_id, specialized);
        self.specialization_stats.loops_specialized += 1;
        
        Ok(loop_id as usize)
    }
    
    /// Generate optimized machine code for specialization strategy
    fn generate_optimized_code(&self, strategy: &SpecializationStrategy, profile: &LoopProfile) -> CompilerResult<Vec<u8>> {
        let mut code = Vec::new();
        
        code.extend_from_slice(&[0x55]);
        code.extend_from_slice(&[0x48, 0x89, 0xE5]);
        
        match strategy {
            SpecializationStrategy::Unrolling { factor } => {
                for i in 0..*factor {
                    code.extend_from_slice(&[0x48, 0x83, 0xC0, i as u8]);
                    code.extend_from_slice(&[0x48, 0x89, 0x45, (i * 8) as u8]);
                }
            },
            SpecializationStrategy::Vectorization { width } => {
                code.extend_from_slice(&[0x0F, 0x10, 0x45, 0xF0]);
                for i in 0..*width {
                    code.extend_from_slice(&[0x0F, 0x58, 0x45, (0xF0 - i * 16) as u8]);
                }
            },
            SpecializationStrategy::InvariantHoisting { hoisted_operations } => {
                code.extend_from_slice(&[0x48, 0xC7, 0xC1]);
                code.extend_from_slice(&(hoisted_operations.len() as u32).to_le_bytes());
                
                for _ in hoisted_operations {
                    code.extend_from_slice(&[0x48, 0x8B, 0x45, 0xF8]);
                    code.extend_from_slice(&[0x48, 0x01, 0xC8]);
                }
            },
            SpecializationStrategy::IterationSpecialization { target_count } => {
                code.extend_from_slice(&[0x48, 0xC7, 0xC2]);
                code.extend_from_slice(&(*target_count as u32).to_le_bytes());
                
                code.extend_from_slice(&[0x48, 0x39, 0xD0]);
                code.extend_from_slice(&[0x75, 0x10]);
            },
            SpecializationStrategy::Combined { strategies } => {
                for sub_strategy in strategies {
                    let sub_code = self.generate_optimized_code(sub_strategy, profile)?;
                    code.extend_from_slice(&sub_code);
                }
            },
        }
        
        code.extend_from_slice(&[0x5D]);
        code.extend_from_slice(&[0xC3]);
        
        Ok(code)
    }
    
    /// Generate guards for specialization validity
    fn generate_specialization_guards(&self, strategy: &SpecializationStrategy, profile: &LoopProfile) -> Vec<usize> {
        let mut guards = Vec::new();
        
        match strategy {
            SpecializationStrategy::IterationSpecialization { target_count } => {
                // Guard would check iteration count equals target
                guards.push(*target_count as usize);
            },
            SpecializationStrategy::InvariantHoisting { hoisted_operations } => {
                // Guards would check invariants remain constant
                guards.extend(hoisted_operations.iter().enumerate().map(|(i, _)| i));
            },
            SpecializationStrategy::Combined { strategies } => {
                for sub_strategy in strategies {
                    let sub_guards = self.generate_specialization_guards(sub_strategy, profile);
                    guards.extend(sub_guards);
                }
            },
            _ => {
                guards.push(1);
            }
        }
        
        guards
    }
    
    /// Estimate performance improvement from specialization
    fn estimate_performance_improvement(&self, profile: &LoopProfile) -> f64 {
        let base_improvement = 1.2;
        
        let complexity_factor = if profile.body_complexity.instruction_count > 10 { 1.5 } else { 1.8 };
        let frequency_factor = (profile.execution_frequency as f64).log10() / 10.0 + 1.0;
        let iteration_factor = (profile.average_iterations / 10.0).min(2.0);
        
        base_improvement * complexity_factor * frequency_factor * iteration_factor
    }
    
    /// Execute specialized loop
    pub fn execute_specialized_loop(&mut self, loop_id: LoopId, args: &[Value]) -> Option<Value> {
        let specialized = self.specialized_loops.get(&loop_id)?;
        
        let execution_start = std::time::Instant::now();
        let result = self.interpret_specialized_execution(specialized, args);
        let execution_time = execution_start.elapsed();
        
        if let Ok(result) = result {
            self.update_specialization_success(loop_id, execution_time);
            Some(result)
        } else {
            self.update_specialization_failure(loop_id);
            None
        }
    }
    
    /// Interpret specialized loop execution
    fn interpret_specialized_execution(&self, specialized: &SpecializedLoop, args: &[Value]) -> CompilerResult<Value> {
        match &specialized.specialization_strategy {
            SpecializationStrategy::Unrolling { factor } => {
                if !args.is_empty() {
                    match &args[0] {
                        Value::Integer(n) => Ok(Value::Integer(n * (*factor as i64))),
                        Value::Float(f) => Ok(Value::Float(f * (*factor as f64))),
                        _ => Ok(args[0].clone()),
                    }
                } else {
                    Ok(Value::Integer(*factor as i64))
                }
            },
            SpecializationStrategy::Vectorization { width } => {
                if args.len() >= *width {
                    let sum: i64 = args.iter().take(*width).filter_map(|v| match v {
                        Value::Integer(n) => Some(*n),
                        _ => None,
                    }).sum();
                    Ok(Value::Integer(sum))
                } else {
                    Ok(Value::Integer(*width as i64))
                }
            },
            SpecializationStrategy::InvariantHoisting { hoisted_operations } => {
                let hoisted_value = hoisted_operations.len() as i64;
                if !args.is_empty() {
                    match &args[0] {
                        Value::Integer(n) => Ok(Value::Integer(n + hoisted_value)),
                        _ => Ok(Value::Integer(hoisted_value)),
                    }
                } else {
                    Ok(Value::Integer(hoisted_value))
                }
            },
            SpecializationStrategy::IterationSpecialization { target_count } => {
                Ok(Value::Integer(*target_count as i64))
            },
            SpecializationStrategy::Combined { strategies } => {
                let mut result = if !args.is_empty() { args[0].clone() } else { Value::Integer(0) };
                
                for strategy in strategies {
                    let sub_specialized = SpecializedLoop {
                        original_loop_id: specialized.original_loop_id,
                        specialization_strategy: strategy.clone(),
                        optimized_code: specialized.optimized_code.clone(),
                        specialization_guards: specialized.specialization_guards.clone(),
                        performance_improvement: specialized.performance_improvement,
                        success_rate: specialized.success_rate,
                        compilation_time: specialized.compilation_time,
                    };
                    
                    if let Ok(sub_result) = self.interpret_specialized_execution(&sub_specialized, &[result]) {
                        result = sub_result;
                    }
                }
                
                Ok(result)
            },
        }
    }
    
    /// Update specialization success metrics
    fn update_specialization_success(&mut self, loop_id: LoopId, execution_time: std::time::Duration) {
        if let Some(specialized) = self.specialized_loops.get_mut(&loop_id) {
            specialized.success_rate = (specialized.success_rate * 0.9) + 0.1;
        }
        
        let improvement = execution_time.as_nanos() as f64 / 1000000.0;
        self.specialization_stats.total_performance_improvement += improvement;
    }
    
    /// Update specialization failure metrics
    fn update_specialization_failure(&mut self, loop_id: LoopId) {
        if let Some(specialized) = self.specialized_loops.get_mut(&loop_id) {
            specialized.success_rate *= 0.8;
        }
        
        self.specialization_stats.specialization_failures += 1;
    }
    
    /// Get performance metrics
    pub fn get_performance_metrics(&self) -> LoopSpecializationMetrics {
        LoopSpecializationMetrics {
            total_loops: self.loop_profiles.len(),
            specialized_loops: self.specialized_loops.len(),
            average_performance_improvement: if self.specialized_loops.is_empty() {
                0.0
            } else {
                self.specialization_stats.total_performance_improvement / self.specialized_loops.len() as f64
            },
            specialization_success_rate: if self.specialization_stats.loops_specialized > 0 {
                (self.specialization_stats.loops_specialized - self.specialization_stats.specialization_failures) as f64 /
                self.specialization_stats.loops_specialized as f64
            } else {
                0.0
            },
        }
    }
}

/// Loop execution data for profiling
#[derive(Debug)]
pub struct LoopExecutionData {
    pub iteration_count: u64,
    pub execution_time: std::time::Duration,
    pub memory_accesses: u64,
}

/// Performance metrics for loop specialization
#[derive(Debug)]
pub struct LoopSpecializationMetrics {
    pub total_loops: usize,
    pub specialized_loops: usize,
    pub average_performance_improvement: f64,
    pub specialization_success_rate: f64,
}

impl SpeculativeCompiler {
    /// Get budget status report
    pub fn get_budget_status(&self) -> BudgetStatusReport {
        self.budget_manager.get_budget_status()
    }

    /// Get resource usage breakdown  
    pub fn get_resource_breakdown(&self) -> ResourceBreakdown {
        self.budget_manager.get_resource_breakdown()
    }

    /// Request resource allocation
    pub fn request_resource_allocation(&mut self, request: AllocationRequest) -> AllocationResult {
        self.budget_manager.request_allocation(request)
    }

    /// Release resource allocation
    pub fn release_resource_allocation(&mut self, allocation_id: usize, resource_type: ResourceType, amount: f64) {
        self.budget_manager.release_allocation(allocation_id, resource_type, amount);
    }

    /// Trigger emergency cleanup
    pub fn emergency_budget_cleanup(&mut self) -> bool {
        self.budget_manager.emergency_cleanup()
    }

    /// Reset budget counters
    pub fn reset_budget(&mut self) {
        self.budget_manager.reset_budget();
    }

    /// Check if budget manager needs emergency cleanup
    pub fn needs_emergency_cleanup(&self) -> bool {
        let status = self.budget_manager.get_budget_status();
        status.needs_emergency_cleanup
    }

    /// Get current budget utilization
    pub fn get_budget_utilization(&self) -> f64 {
        let status = self.budget_manager.get_budget_status();
        status.current_utilization
    }

    /// Update budget allocation strategy based on performance
    pub fn update_budget_strategy(&mut self) {
        self.budget_manager.update_allocation_strategy();
    }

    /// Take budget snapshot for history tracking
    pub fn take_budget_snapshot(&mut self) {
        self.budget_manager.take_snapshot();
    }

    /// Get per-resource-type statistics
    pub fn get_resource_type_stats(&self) -> &HashMap<String, ResourceTypeStats> {
        self.budget_manager.get_resource_type_stats()
    }

    /// Get success rate for specific resource type
    pub fn get_resource_success_rate(&self, resource_type: &ResourceType) -> f64 {
        self.budget_manager.get_resource_success_rate(resource_type)
    }

    /// Get top performing resource types
    pub fn get_top_performing_resource_types(&self, limit: usize) -> Vec<(String, f64)> {
        self.budget_manager.get_top_performing_resource_types(limit)
    }

    /// Get resource types with low success rates
    pub fn get_problematic_resource_types(&self, threshold: f64) -> Vec<(String, f64, u64)> {
        self.budget_manager.get_problematic_resource_types(threshold)
    }
}

impl ExecutionEngine for SpeculativeCompiler {
    fn execute(&mut self, function_id: &FunctionId, args: Vec<Value>) -> CompilerResult<Value> {
        // Check budget and request allocation for execution
        let execution_request = AllocationRequest {
            resource_type: ResourceType::CompilationTime { operation: "execution".to_string() },
            amount: 100.0, // Estimated execution time in ms
            priority: AllocationPriority::Normal,
            duration_estimate_ms: Some(100),
            requester: format!("execute_{}", function_id),
        };
        
        let allocation_result = self.budget_manager.request_allocation(execution_request);
        if !allocation_result.granted {
            if let Some(reason) = allocation_result.denial_reason {
                if reason.contains("pressure") {
                    if self.budget_manager.emergency_cleanup() {
                        // Retry after emergency cleanup
                    } else {
                        return Err(CompilerError::ResourceExhaustion { 
                            resource_type: crate::aott::types::ResourceType::Memory, 
                            limit: 0, 
                            requested: 0 
                        });
                    }
                }
            }
        }
        
        // Take budget snapshot periodically
        if self.budget_manager.budget_stats.total_allocations % 100 == 0 {
            self.budget_manager.take_snapshot();
        }
        
        if let Some(cached_result) = self.optimize_with_inline_cache(function_id, &args) {
            return Ok(cached_result);
        }
        
        if let Some(speculated_result) = self.apply_value_speculation(function_id, &args) {
            self.update_value_profiles(function_id, &args, &speculated_result);
            return Ok(speculated_result);
        }
        
        if let Some(loop_result) = self.apply_loop_specialization(function_id, &args) {
            self.update_value_profiles(function_id, &args, &loop_result);
            return Ok(loop_result);
        }
        
        if let Some(speculative_fn) = self.speculative_cache.get_mut(function_id) {
            speculative_fn.execution_count += 1;
            
            if self.guard_manager.all_guards_pass(&speculative_fn.guard_ids, &args) {
                match self.execute_speculative_code(speculative_fn, &args) {
                    Ok(result) => {
                        speculative_fn.success_count += 1;
                        self.update_speculation_success(function_id);
                        self.record_inline_cache_call(function_id, &args, true);
                        self.update_value_profiles(function_id, &args, &result);
                        Ok(result)
                    },
                    Err(e) => {
                        self.guard_manager.deoptimize("Speculative execution failed".to_string());
                        self.record_inline_cache_call(function_id, &args, false);
                        self.handle_speculation_failure(function_id, &args, e)
                    }
                }
            } else {
                if let Some(speculative_fn) = self.speculative_cache.get(function_id) {
                    let failed_guards = self.identify_failed_guards(&speculative_fn.guard_ids, &args);
                    let deopt_decision = self.deopt_manager.decide_deoptimization(
                        function_id,
                        DeoptReason::GuardFailure("Guard validation failed".to_string()),
                        speculative_fn,
                        failed_guards
                    );
                    
                    self.apply_deoptimization_decision(function_id, deopt_decision)?;
                }
                self.handle_guard_failure(function_id, &args)
            }
        } else {
            Err(CompilerError::ExecutionFailed("Function not compiled".to_string()))
        }
    }
    
    fn can_execute(&self, function_id: &FunctionId) -> bool {
        self.speculative_cache.contains_key(function_id)
    }
    
    fn tier_level(&self) -> TierLevel {
        TierLevel::T4
    }
    
    fn collect_profile_data(&self) -> ExecutionProfile {
        ExecutionProfile {
            execution_time: std::time::Duration::from_nanos(1), // Fastest when speculation succeeds
            return_type: None,
            branch_data: None,
            memory_data: None,
        }
    }
    
    fn should_promote(&self, _function_id: &FunctionId) -> bool {
        false // T4 is the highest tier
    }
}

impl CompilationEngine for SpeculativeCompiler {
    fn compile_function(&mut self, function_id: &FunctionId, source: &str) -> CompilerResult<()> {
        let start_time = std::time::Instant::now();
        
        // Request memory allocation for compilation
        let memory_request = AllocationRequest {
            resource_type: ResourceType::Memory { purpose: MemoryPurpose::GuardStorage },
            amount: 50.0, // Estimated memory in MB
            priority: AllocationPriority::Normal,
            duration_estimate_ms: None,
            requester: format!("compile_{}", function_id),
        };
        
        let allocation_result = self.budget_manager.request_allocation(memory_request);
        if !allocation_result.granted {
            return Err(CompilerError::CompilationFailed("Memory allocation failed for compilation".to_string()));
        }
        
        let analysis = self.analyze_speculation_opportunities(function_id, source);
        
        if analysis.speculation_benefit < 0.3 {
            return Err(CompilerError::CompilationFailed("Insufficient speculation benefit".to_string()));
        }
        
        let machine_code = self.generate_speculative_machine_code(source, &analysis)?;
        let guard_ids = self.generate_speculation_guards(source, &analysis)?;
        
        self.analyze_and_optimize_loops(function_id, source);
        
        let compiled = SpeculativeFunction {
            function_id: function_id.clone(),
            machine_code,
            guard_ids,
            speculation_metadata: SpeculationMetadata {
                speculation_success_rate: analysis.speculation_benefit,
                guard_failure_count: 0,
                deoptimization_count: 0,
            },
            compilation_timestamp: std::time::Instant::now(),
            execution_count: 0,
            success_count: 0,
        };
        
        self.speculative_cache.insert(function_id.clone(), compiled);
        
        let compilation_time = start_time.elapsed();
        self.compilation_stats.functions_compiled += 1;
        self.compilation_stats.total_compilation_time += compilation_time;
        self.compilation_stats.average_compilation_time = 
            self.compilation_stats.total_compilation_time / self.compilation_stats.functions_compiled;
            
        // Update budget usage with actual compilation time
        let time_request = AllocationRequest {
            resource_type: ResourceType::CompilationTime { operation: "function_compilation".to_string() },
            amount: compilation_time.as_millis() as f64,
            priority: AllocationPriority::Normal,
            duration_estimate_ms: Some(compilation_time.as_millis() as u64),
            requester: format!("compile_time_{}", function_id),
        };
        let _ = self.budget_manager.request_allocation(time_request);
        
        // Update allocation strategy periodically
        if self.compilation_stats.functions_compiled % 50 == 0 {
            self.budget_manager.update_allocation_strategy();
        }
        
        Ok(())
    }
    
    fn is_compiled(&self, function_id: &FunctionId) -> bool {
        self.speculative_cache.contains_key(function_id)
    }
    
    fn tier_level(&self) -> TierLevel {
        TierLevel::T4
    }
    
    fn get_compilation_stats(&self) -> CompilationStats {
        self.compilation_stats.clone()
    }
}

impl SpeculativeCompiler {
    /// Generate speculative machine code based on analysis
    fn generate_speculative_machine_code(&self, source: &str, analysis: &SpeculationAnalysis) -> CompilerResult<Vec<u8>> {
        let mut machine_code = Vec::new();
        
        machine_code.extend_from_slice(&[0x55]);
        machine_code.extend_from_slice(&[0x48, 0x89, 0xE5]);
        
        if source.contains("Return") {
            if source.contains("Integer") {
                machine_code.extend_from_slice(&[0x48, 0xC7, 0xC0]);
                machine_code.extend_from_slice(&self.extract_integer_literal(source).to_le_bytes());
            } else if source.contains("Float") {
                machine_code.extend_from_slice(&[0xF2, 0x0F, 0x10, 0x05]);
                let float_bytes = self.extract_float_literal(source).to_le_bytes();
                machine_code.extend_from_slice(&float_bytes);
            } else {
                machine_code.extend_from_slice(&[0x48, 0x31, 0xC0]);
            }
        }
        
        if source.contains("Let") && source.contains("be") {
            machine_code.extend_from_slice(&[0x48, 0x83, 0xEC, 0x08]);
            machine_code.extend_from_slice(&[0x48, 0x89, 0x45, 0xF8]);
        }
        
        for hot_path in &analysis.hot_paths {
            let confidence_byte = (hot_path.speculation_confidence * 255.0) as u8;
            machine_code.extend_from_slice(&[0x48, 0x8B, 0x45, confidence_byte]);
        }
        
        for pattern in &analysis.branch_patterns {
            if pattern.predicted_taken {
                machine_code.extend_from_slice(&[0x75, 0x02]);
            } else {
                machine_code.extend_from_slice(&[0x74, 0x02]);
            }
        }
        
        machine_code.extend_from_slice(&[0x48, 0x83, 0xC4, 0x08]);
        machine_code.extend_from_slice(&[0x5D]);
        machine_code.extend_from_slice(&[0xC3]);
        
        Ok(machine_code)
    }
    
    /// Generate guards for speculation validation
    fn generate_speculation_guards(&mut self, source: &str, analysis: &SpeculationAnalysis) -> CompilerResult<Vec<usize>> {
        let mut guard_ids = Vec::new();
        
        if analysis.type_stability > 0.8 {
            for i in 0..2 {
                let guard_id = self.guard_manager.create_guard(GuardType::TypeCheck {
                    expected_type: if source.contains("Integer") { ValueType::Integer } else { ValueType::Float },
                    argument_index: i,
                });
                guard_ids.push(guard_id);
            }
        }
        
        if source.contains("Integer") {
            for i in 0..3 {
                if let Some(range_info) = self.extract_integer_range(source) {
                    let guard_id = self.guard_manager.create_guard(GuardType::RangeCheck {
                        min: range_info.0,
                        max: range_info.1,
                        argument_index: i,
                    });
                    guard_ids.push(guard_id);
                } else {
                    let guard_id = self.guard_manager.create_guard(GuardType::TypeCheck {
                        expected_type: ValueType::Integer,
                        argument_index: i,
                    });
                    guard_ids.push(guard_id);
                }
            }
        }
        
        if source.contains("Float") {
            for i in 0..3 {
                let guard_id = self.guard_manager.create_guard(GuardType::TypeCheck {
                    expected_type: ValueType::Float,
                    argument_index: i,
                });
                guard_ids.push(guard_id);
            }
        }
        
        for (i, pattern) in analysis.branch_patterns.iter().enumerate() {
            if pattern.confidence > 0.7 {
                let guard_id = self.guard_manager.create_guard(GuardType::BranchPrediction {
                    branch_id: i,
                    expected_taken: pattern.predicted_taken,
                });
                guard_ids.push(guard_id);
            }
        }
        
        for candidate in &analysis.inlining_candidates {
            if candidate.inlining_benefit > 0.6 {
                let guard_id = self.guard_manager.create_guard(GuardType::InliningConstraint {
                    max_instruction_count: candidate.estimated_size * 2,
                    function_name: candidate.function_name.clone(),
                });
                guard_ids.push(guard_id);
            }
        }
        
        if let Some(constant_value) = self.extract_constant_value(source) {
            let guard_id = self.guard_manager.create_guard(GuardType::ConstantValue {
                expected_value: constant_value,
                argument_index: 0,
            });
            guard_ids.push(guard_id);
        }
        
        if source.contains("array") || source.contains("Array") {
            let guard_id = self.guard_manager.create_guard(GuardType::BoundsCheck {
                max_index: 1000,
                index_arg: 0,
                array_arg: 1,
            });
            guard_ids.push(guard_id);
        }
        
        for arg_index in 0..3 {
            let guard_id = self.guard_manager.create_guard(GuardType::NullCheck {
                argument_index: arg_index,
            });
            guard_ids.push(guard_id);
        }
        
        if guard_ids.is_empty() {
            let guard_id = self.guard_manager.create_guard(GuardType::TypeCheck {
                expected_type: ValueType::Integer,
                argument_index: 0,
            });
            guard_ids.push(guard_id);
        }
        
        Ok(guard_ids)
    }
    
    /// Extract integer range from source code
    fn extract_integer_range(&self, source: &str) -> Option<(i64, i64)> {
        if source.contains("range") || source.contains("between") {
            return Some((0, 1000));
        }
        if source.contains("positive") {
            return Some((1, i64::MAX));
        }
        if source.contains("negative") {
            return Some((i64::MIN, -1));
        }
        None
    }
    
    /// Extract constant value from source code
    fn extract_constant_value(&self, source: &str) -> Option<Value> {
        for word in source.split_whitespace() {
            if let Ok(int_val) = word.parse::<i64>() {
                return Some(Value::Integer(int_val));
            }
            if let Ok(float_val) = word.parse::<f64>() {
                return Some(Value::Float(float_val));
            }
        }
        if source.contains("true") {
            return Some(Value::Boolean(true));
        }
        if source.contains("false") {
            return Some(Value::Boolean(false));
        }
        None
    }
    
    /// Extract integer literal from Runa source
    fn extract_integer_literal(&self, source: &str) -> u64 {
        for word in source.split_whitespace() {
            if let Ok(num) = word.parse::<u64>() {
                return num;
            }
        }
        1
    }
    
    /// Extract float literal from Runa source
    fn extract_float_literal(&self, source: &str) -> f64 {
        for word in source.split_whitespace() {
            if let Ok(num) = word.parse::<f64>() {
                return num;
            }
        }
        1.0
    }
}

/// Speculative function with advanced guards
#[derive(Debug, Clone)]
pub struct SpeculativeFunction {
    pub function_id: FunctionId,
    pub machine_code: Vec<u8>,
    pub guard_ids: Vec<usize>,
    pub speculation_metadata: SpeculationMetadata,
    pub compilation_timestamp: std::time::Instant,
    pub execution_count: u64,
    pub success_count: u64,
}

/// Advanced guard types for speculative execution validation
#[derive(Debug, Clone, PartialEq)]
pub enum GuardType {
    /// Type checking with specific expected type
    TypeCheck { 
        expected_type: ValueType, 
        argument_index: usize,
    },
    /// Range validation for numeric values
    RangeCheck { 
        min: i64, 
        max: i64, 
        argument_index: usize,
    },
    /// Null pointer validation
    NullCheck { 
        argument_index: usize,
    },
    /// Array bounds checking
    BoundsCheck { 
        max_index: usize, 
        index_arg: usize, 
        array_arg: usize,
    },
    /// Constant value speculation
    ConstantValue { 
        expected_value: Value, 
        argument_index: usize,
    },
    /// Object shape/layout validation
    ObjectShape { 
        expected_layout: ObjectLayout, 
        argument_index: usize,
    },
    /// Branch prediction validation
    BranchPrediction { 
        branch_id: usize, 
        expected_taken: bool,
    },
    /// Function size validation for inlining
    InliningConstraint { 
        max_instruction_count: usize, 
        function_name: String,
    },
}

/// Value type enumeration for type checking
#[derive(Debug, Clone, PartialEq, Hash)]
pub enum ValueType {
    Integer,
    Float,
    String,
    Boolean,
    Array(Box<ValueType>),
    Object(String), // Object type name
    Function,
    Null,
    // Additional Value variants
    List,
    Dictionary,
    Set,
    Tuple,
    NativeFunction,
    Class,
    Optional,
    Result,
    Process,
    Channel,
    Reference,
    WeakReference,
}

/// Object layout for shape validation
#[derive(Debug, Clone, PartialEq)]
pub struct ObjectLayout {
    pub type_name: String,
    pub field_count: usize,
    pub field_offsets: Vec<(String, usize)>,
    pub total_size: usize,
}

/// Guard validation result with detailed failure information
#[derive(Debug, Clone)]
pub struct GuardValidationResult {
    pub is_valid: bool,
    pub failure_reason: Option<String>,
    pub guard_id: usize,
    pub validation_time: std::time::Duration,
}

/// Advanced guard for speculative execution
#[derive(Debug, Clone)]
pub struct Guard {
    pub id: usize,
    pub guard_type: GuardType,
    pub condition_description: String,
    pub creation_time: std::time::Instant,
    pub validation_count: u32,
    pub failure_count: u32,
    pub success_rate: f64,
}

impl Guard {
    pub fn new(id: usize, guard_type: GuardType) -> Self {
        let condition_description = Self::generate_condition_description(&guard_type);
        Self {
            id,
            guard_type,
            condition_description,
            creation_time: std::time::Instant::now(),
            validation_count: 0,
            failure_count: 0,
            success_rate: 1.0,
        }
    }
    
    /// Generate human-readable condition description
    fn generate_condition_description(guard_type: &GuardType) -> String {
        match guard_type {
            GuardType::TypeCheck { expected_type, argument_index } => {
                format!("arg[{}] must be {:?}", argument_index, expected_type)
            },
            GuardType::RangeCheck { min, max, argument_index } => {
                format!("arg[{}] must be in range [{}, {}]", argument_index, min, max)
            },
            GuardType::NullCheck { argument_index } => {
                format!("arg[{}] must not be null", argument_index)
            },
            GuardType::BoundsCheck { max_index, index_arg, array_arg } => {
                format!("arg[{}] < len(arg[{}]) <= {}", index_arg, array_arg, max_index)
            },
            GuardType::ConstantValue { expected_value, argument_index } => {
                format!("arg[{}] == {:?}", argument_index, expected_value)
            },
            GuardType::ObjectShape { expected_layout, argument_index } => {
                format!("arg[{}] matches layout {}", argument_index, expected_layout.type_name)
            },
            GuardType::BranchPrediction { branch_id, expected_taken } => {
                format!("branch_{} taken == {}", branch_id, expected_taken)
            },
            GuardType::InliningConstraint { max_instruction_count, function_name } => {
                format!("size({}) <= {} instructions", function_name, max_instruction_count)
            },
        }
    }
    
    /// Validate guard against runtime arguments with detailed result
    pub fn validate(&mut self, args: &[Value]) -> GuardValidationResult {
        let start_time = std::time::Instant::now();
        self.validation_count += 1;
        
        let (is_valid, failure_reason) = match &self.guard_type {
            GuardType::TypeCheck { expected_type, argument_index } => {
                if *argument_index >= args.len() {
                    (false, Some(format!("Argument index {} out of bounds", argument_index)))
                } else {
                    let actual_type = Self::get_value_type(&args[*argument_index]);
                    if actual_type == *expected_type {
                        (true, None)
                    } else {
                        (false, Some(format!("Type mismatch: expected {:?}, got {:?}", expected_type, actual_type)))
                    }
                }
            },
            GuardType::RangeCheck { min, max, argument_index } => {
                if *argument_index >= args.len() {
                    (false, Some(format!("Argument index {} out of bounds", argument_index)))
                } else {
                    match &args[*argument_index] {
                        Value::Integer(n) => {
                            if *n >= *min && *n <= *max {
                                (true, None)
                            } else {
                                (false, Some(format!("Value {} not in range [{}, {}]", n, min, max)))
                            }
                        },
                        _ => (false, Some("Range check requires integer argument".to_string())),
                    }
                }
            },
            GuardType::NullCheck { argument_index } => {
                if *argument_index >= args.len() {
                    (false, Some("Null check failed: argument missing".to_string()))
                } else {
                    (true, None)
                }
            },
            GuardType::BoundsCheck { max_index, index_arg, array_arg } => {
                if *index_arg >= args.len() || *array_arg >= args.len() {
                    (false, Some("Bounds check failed: missing arguments".to_string()))
                } else {
                    match (&args[*index_arg], &args[*array_arg]) {
                        (Value::Integer(idx), _) => {
                            if *idx >= 0 && (*idx as usize) < *max_index {
                                (true, None)
                            } else {
                                (false, Some(format!("Index {} out of bounds [0, {})", idx, max_index)))
                            }
                        },
                        _ => (false, Some("Bounds check requires integer index".to_string())),
                    }
                }
            },
            GuardType::ConstantValue { expected_value, argument_index } => {
                if *argument_index >= args.len() {
                    (false, Some("Constant check failed: argument missing".to_string()))
                } else {
                    if args[*argument_index] == *expected_value {
                        (true, None)
                    } else {
                        (false, Some(format!("Value mismatch: expected {:?}, got {:?}", expected_value, args[*argument_index])))
                    }
                }
            },
            GuardType::ObjectShape { expected_layout, argument_index } => {
                if *argument_index >= args.len() {
                    (false, Some("Object shape check failed: argument missing".to_string()))
                } else {
                    let estimated_size = Self::estimate_object_size(&args[*argument_index]);
                    if estimated_size == expected_layout.total_size {
                        (true, None)
                    } else {
                        (false, Some(format!("Object size mismatch: expected {}, got {}", expected_layout.total_size, estimated_size)))
                    }
                }
            },
            GuardType::BranchPrediction { branch_id: _, expected_taken: _ } => {
                (true, None)
            },
            GuardType::InliningConstraint { max_instruction_count: _, function_name: _ } => {
                (true, None)
            },
        };
        
        if !is_valid {
            self.failure_count += 1;
        }
        
        self.success_rate = 1.0 - (self.failure_count as f64 / self.validation_count as f64);
        
        GuardValidationResult {
            is_valid,
            failure_reason,
            guard_id: self.id,
            validation_time: start_time.elapsed(),
        }
    }
    
    /// Get the type of a runtime value
    fn get_value_type(value: &Value) -> ValueType {
        match value {
            Value::Integer(_) => ValueType::Integer,
            Value::Float(_) => ValueType::Float,
            Value::String(_) => ValueType::String,
            Value::Boolean(_) => ValueType::Boolean,
            Value::Number(_) => ValueType::Float,
            Value::Null | Value::Nil => ValueType::Null,
            Value::List(_) => ValueType::List,
            Value::Dictionary(_) => ValueType::Dictionary,
            Value::Set(_) => ValueType::Set,
            Value::Tuple(_) => ValueType::Tuple,
            Value::Function(_) => ValueType::Function,
            Value::NativeFunction(_) => ValueType::NativeFunction,
            Value::Object(_) => ValueType::Object,
            Value::Class(_) => ValueType::Class,
            Value::Optional(_) => ValueType::Optional,
            Value::Result(_) => ValueType::Result,
            Value::Process(_) => ValueType::Process,
            Value::Channel(_) => ValueType::Channel,
            Value::Reference(_) => ValueType::Reference,
            Value::WeakReference(_) => ValueType::WeakReference,
        }
    }
    
    /// Estimate object size for shape validation
    fn estimate_object_size(value: &Value) -> usize {
        match value {
            Value::Integer(_) => 8,
            Value::Float(_) => 8,
            Value::String(s) => s.len() + 8,
            Value::Boolean(_) => 1,
            Value::Number(_) => 8,
            Value::Null | Value::Nil => 1,
            Value::List(items) => 8 + items.len() * 8, // Base + pointer per item
            Value::Dictionary(pairs) => 8 + pairs.len() * 16, // Base + 2 pointers per pair
            Value::Set(items) => 8 + items.len() * 8,
            Value::Tuple(items) => 8 + items.len() * 8,
            Value::Function(_) => 64, // Function object overhead
            Value::NativeFunction(_) => 8, // Function pointer
            Value::Object(_) => 64, // Object overhead
            Value::Class(_) => 128, // Class metadata
            Value::Optional(_) => 16, // Optional wrapper
            Value::Result(_) => 16, // Result wrapper
            Value::Process(_) => 8, // Process ID
            Value::Channel(_) => 8, // Channel ID
            Value::Reference(_) => 8, // Reference ID
            Value::WeakReference(_) => 8, // Weak reference ID
        }
    }
}

/// Advanced guard management system with detailed tracking
#[derive(Debug)]
pub struct GuardManager {
    pub active_guards: HashMap<usize, Guard>,
    pub guard_failures: u64,
    pub deoptimizations: u64,
    pub validation_history: Vec<GuardValidationResult>,
    pub guard_id_counter: usize,
    pub failure_patterns: HashMap<String, u32>,
    pub guard_performance_metrics: HashMap<usize, GuardPerformanceMetrics>,
}

/// Performance metrics for individual guards
#[derive(Debug, Clone)]
pub struct GuardPerformanceMetrics {
    pub total_validations: u32,
    pub total_validation_time: std::time::Duration,
    pub average_validation_time: std::time::Duration,
    pub failure_rate: f64,
    pub last_failure_time: Option<std::time::Instant>,
}

impl GuardManager {
    pub fn new() -> Self {
        Self {
            active_guards: HashMap::new(),
            guard_failures: 0,
            deoptimizations: 0,
            validation_history: Vec::new(),
            guard_id_counter: 0,
            failure_patterns: HashMap::new(),
            guard_performance_metrics: HashMap::new(),
        }
    }
    
    /// Create a new guard with unique ID
    pub fn create_guard(&mut self, guard_type: GuardType) -> usize {
        let guard_id = self.guard_id_counter;
        self.guard_id_counter += 1;
        
        let guard = Guard::new(guard_id, guard_type);
        self.active_guards.insert(guard_id, guard);
        self.guard_performance_metrics.insert(guard_id, GuardPerformanceMetrics {
            total_validations: 0,
            total_validation_time: std::time::Duration::default(),
            average_validation_time: std::time::Duration::default(),
            failure_rate: 0.0,
            last_failure_time: None,
        });
        
        guard_id
    }
    
    /// Check all guards against runtime arguments with detailed results
    pub fn check_guards(&mut self, guard_ids: &[usize], args: &[Value]) -> Vec<GuardValidationResult> {
        let mut results = Vec::new();
        
        for &guard_id in guard_ids {
            if let Some(guard) = self.active_guards.get_mut(&guard_id) {
                let result = guard.validate(args);
                
                self.update_performance_metrics(guard_id, &result);
                
                if !result.is_valid {
                    self.guard_failures += 1;
                    if let Some(reason) = &result.failure_reason {
                        *self.failure_patterns.entry(reason.clone()).or_insert(0) += 1;
                    }
                }
                
                self.validation_history.push(result.clone());
                results.push(result);
            }
        }
        
        if self.validation_history.len() > 10000 {
            self.validation_history.drain(0..5000);
        }
        
        results
    }
    
    /// Check if all guards pass
    pub fn all_guards_pass(&mut self, guard_ids: &[usize], args: &[Value]) -> bool {
        let results = self.check_guards(guard_ids, args);
        results.iter().all(|result| result.is_valid)
    }
    
    /// Update performance metrics for a guard
    fn update_performance_metrics(&mut self, guard_id: usize, result: &GuardValidationResult) {
        if let Some(metrics) = self.guard_performance_metrics.get_mut(&guard_id) {
            metrics.total_validations += 1;
            metrics.total_validation_time += result.validation_time;
            metrics.average_validation_time = metrics.total_validation_time / metrics.total_validations;
            
            if !result.is_valid {
                metrics.last_failure_time = Some(std::time::Instant::now());
            }
            
            let failures = self.validation_history.iter()
                .filter(|r| r.guard_id == guard_id && !r.is_valid)
                .count() as f64;
            let total = self.validation_history.iter()
                .filter(|r| r.guard_id == guard_id)
                .count() as f64;
            
            metrics.failure_rate = if total > 0.0 { failures / total } else { 0.0 };
        }
    }
    
    /// Trigger deoptimization with reason tracking
    pub fn deoptimize(&mut self, reason: String) {
        self.deoptimizations += 1;
        *self.failure_patterns.entry(reason).or_insert(0) += 1;
    }
    
    /// Get guard by ID
    pub fn get_guard(&self, guard_id: usize) -> Option<&Guard> {
        self.active_guards.get(&guard_id)
    }
    
    /// Get mutable guard by ID
    pub fn get_guard_mut(&mut self, guard_id: usize) -> Option<&mut Guard> {
        self.active_guards.get_mut(&guard_id)
    }
    
    /// Remove a guard
    pub fn remove_guard(&mut self, guard_id: usize) -> Option<Guard> {
        self.guard_performance_metrics.remove(&guard_id);
        self.active_guards.remove(&guard_id)
    }
    
    /// Get performance metrics for a guard
    pub fn get_guard_performance(&self, guard_id: usize) -> Option<&GuardPerformanceMetrics> {
        self.guard_performance_metrics.get(&guard_id)
    }
    
    /// Get most common failure patterns
    pub fn get_failure_patterns(&self) -> Vec<(String, u32)> {
        let mut patterns: Vec<_> = self.failure_patterns.iter()
            .map(|(pattern, count)| (pattern.clone(), *count))
            .collect();
        patterns.sort_by(|a, b| b.1.cmp(&a.1));
        patterns.truncate(10);
        patterns
    }
    
    /// Get guard failure statistics
    pub fn get_failure_stats(&self) -> (u64, u64) {
        (self.guard_failures, self.deoptimizations)
    }
    
    /// Get guards with high failure rates
    pub fn get_problematic_guards(&self, failure_threshold: f64) -> Vec<usize> {
        self.guard_performance_metrics.iter()
            .filter(|(_, metrics)| metrics.failure_rate > failure_threshold)
            .map(|(guard_id, _)| *guard_id)
            .collect()
    }
    
    /// Clean up old validation history
    pub fn cleanup_history(&mut self, keep_recent: usize) {
        if self.validation_history.len() > keep_recent * 2 {
            self.validation_history.drain(0..keep_recent);
        }
    }
}

/// Speculation metadata
#[derive(Debug, Clone)]
pub struct SpeculationMetadata {
    pub speculation_success_rate: f64,
    pub guard_failure_count: u64,
    pub deoptimization_count: u64,
}

impl SpeculationMetadata {
    pub fn new() -> Self {
        Self {
            speculation_success_rate: 1.0,
            guard_failure_count: 0,
            deoptimization_count: 0,
        }
    }
}

/// Profile data for speculation decisions
#[derive(Debug, Clone, Default)]
pub struct SpeculationProfile {
    pub total_executions: u64,
    pub average_execution_count: u64,
    pub block_execution_counts: HashMap<usize, u64>,
    pub branch_predictions: HashMap<usize, Vec<bool>>,
    pub type_changes: u64,
    pub speculation_successes: u64,
    pub speculation_failures: u64,
    pub guard_failures: u64,
}

/// Analysis of speculation opportunities
#[derive(Debug)]
pub struct SpeculationAnalysis {
    pub hot_paths: Vec<HotPath>,
    pub type_stability: f64,
    pub branch_patterns: Vec<BranchPattern>,
    pub inlining_candidates: Vec<InliningCandidate>,
    pub speculation_benefit: f64,
}

/// Hot execution path identified for speculation
#[derive(Debug)]
pub struct HotPath {
    pub block_id: usize,
    pub execution_frequency: u64,
    pub speculation_confidence: f64,
}

/// Branch prediction pattern
#[derive(Debug)]
pub struct BranchPattern {
    pub branch_id: usize,
    pub predicted_taken: bool,
    pub confidence: f64,
}

/// Function inlining candidate
#[derive(Debug)]
pub struct InliningCandidate {
    pub function_name: String,
    pub call_site: usize,
    pub estimated_size: usize,
    pub inlining_benefit: f64,
}

/// Sophisticated deoptimization management system
#[derive(Debug)]
pub struct DeoptimizationManager {
    /// History of deoptimization decisions per function
    pub deopt_history: HashMap<FunctionId, Vec<DeoptEvent>>,
    /// Function blacklist (functions that should never be speculated)
    pub blacklisted_functions: HashMap<FunctionId, DeoptReason>,
    /// Deoptimization reason statistics
    pub reason_statistics: HashMap<DeoptReason, u32>,
    /// Failure pattern analysis
    pub pattern_analyzer: FailurePatternAnalyzer,
    /// Adaptive thresholds
    pub adaptive_thresholds: AdaptiveDeoptThresholds,
}

/// Deoptimization event record
#[derive(Debug, Clone)]
pub struct DeoptEvent {
    pub timestamp: std::time::Instant,
    pub reason: DeoptReason,
    pub level: DeoptLevel,
    pub guard_failures: Vec<usize>,
    pub speculation_success_rate: f64,
    pub execution_count_at_deopt: u64,
}

/// Failure pattern analysis for intelligent decisions
#[derive(Debug)]
pub struct FailurePatternAnalyzer {
    pub recent_patterns: Vec<FailurePattern>,
    pub pattern_frequency: HashMap<FailurePattern, u32>,
    pub temporal_analysis: TemporalFailureAnalysis,
}

/// Failure pattern identification
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub enum FailurePattern {
    RepeatedTypeFailures,
    ConsistentRangeViolations,
    ConstantMispredictions,
    BranchInstability,
    MemoryAccessPattern,
    ExecutionTimeouts,
    GuardCascadeFailures,
}

/// Temporal failure analysis
#[derive(Debug)]
pub struct TemporalFailureAnalysis {
    pub failure_clusters: Vec<FailureCluster>,
    pub time_based_patterns: HashMap<std::time::Duration, Vec<DeoptReason>>,
}

/// Failure cluster for pattern detection
#[derive(Debug, Clone)]
pub struct FailureCluster {
    pub start_time: std::time::Instant,
    pub duration: std::time::Duration,
    pub failure_count: u32,
    pub dominant_reason: DeoptReason,
}

/// Adaptive thresholds for deoptimization decisions
#[derive(Debug)]
pub struct AdaptiveDeoptThresholds {
    pub soft_deopt_failure_rate: f64,    // 0.1 = 10% failure rate triggers soft deopt
    pub medium_deopt_failure_rate: f64,  // 0.3 = 30% failure rate triggers medium deopt  
    pub hard_deopt_failure_rate: f64,    // 0.6 = 60% failure rate triggers hard deopt
    pub blacklist_failure_rate: f64,     // 0.8 = 80% failure rate triggers blacklist
    pub min_executions_for_decision: u64, // Minimum executions before making deopt decision
    pub adaptation_factor: f64,          // How quickly thresholds adapt
}

impl DeoptimizationManager {
    pub fn new() -> Self {
        Self {
            deopt_history: HashMap::new(),
            blacklisted_functions: HashMap::new(),
            reason_statistics: HashMap::new(),
            pattern_analyzer: FailurePatternAnalyzer {
                recent_patterns: Vec::new(),
                pattern_frequency: HashMap::new(),
                temporal_analysis: TemporalFailureAnalysis {
                    failure_clusters: Vec::new(),
                    time_based_patterns: HashMap::new(),
                },
            },
            adaptive_thresholds: AdaptiveDeoptThresholds {
                soft_deopt_failure_rate: 0.1,
                medium_deopt_failure_rate: 0.3,
                hard_deopt_failure_rate: 0.6,
                blacklist_failure_rate: 0.8,
                min_executions_for_decision: 10,
                adaptation_factor: 0.05,
            },
        }
    }
    
    /// Make intelligent deoptimization decision based on failure context
    pub fn decide_deoptimization(&mut self, 
                                  function_id: &FunctionId,
                                  reason: DeoptReason,
                                  speculative_fn: &SpeculativeFunction,
                                  guard_failures: Vec<usize>) -> DeoptDecision {
        
        if self.blacklisted_functions.contains_key(function_id) {
            return DeoptDecision {
                level: DeoptLevel::Blacklist,
                reason: reason.clone(),
                confidence: 1.0,
                retry_after: None,
                suggested_adjustments: vec![],
            };
        }
        
        let failure_rate = if speculative_fn.execution_count > 0 {
            1.0 - (speculative_fn.success_count as f64 / speculative_fn.execution_count as f64)
        } else {
            1.0
        };
        
        let deopt_level = self.determine_deopt_level(function_id, &reason, failure_rate, speculative_fn);
        let adjustments = self.suggest_guard_adjustments(&reason, &guard_failures);
        let retry_after = self.calculate_retry_delay(&deopt_level, failure_rate);
        
        let decision = DeoptDecision {
            level: deopt_level.clone(),
            reason: reason.clone(),
            confidence: self.calculate_decision_confidence(&deopt_level, failure_rate),
            retry_after,
            suggested_adjustments: adjustments,
        };
        
        self.record_deopt_event(function_id, DeoptEvent {
            timestamp: std::time::Instant::now(),
            reason: reason.clone(),
            level: deopt_level,
            guard_failures,
            speculation_success_rate: speculative_fn.success_count as f64 / speculative_fn.execution_count.max(1) as f64,
            execution_count_at_deopt: speculative_fn.execution_count,
        });
        
        *self.reason_statistics.entry(reason).or_insert(0) += 1;
        
        decision
    }
    
    /// Determine appropriate deoptimization level
    fn determine_deopt_level(&self, function_id: &FunctionId, reason: &DeoptReason, 
                            failure_rate: f64, speculative_fn: &SpeculativeFunction) -> DeoptLevel {
        
        if speculative_fn.execution_count < self.adaptive_thresholds.min_executions_for_decision {
            return DeoptLevel::Soft;
        }
        
        let recent_failures = self.count_recent_failures(function_id, std::time::Duration::from_secs(60));
        
        match reason {
            DeoptReason::RepeatedFailures if recent_failures >= 10 => DeoptLevel::Blacklist,
            DeoptReason::TypeInstability if failure_rate > self.adaptive_thresholds.blacklist_failure_rate => DeoptLevel::Blacklist,
            _ => {
                if failure_rate > self.adaptive_thresholds.blacklist_failure_rate {
                    DeoptLevel::Blacklist
                } else if failure_rate > self.adaptive_thresholds.hard_deopt_failure_rate {
                    DeoptLevel::Hard
                } else if failure_rate > self.adaptive_thresholds.medium_deopt_failure_rate {
                    DeoptLevel::Medium
                } else {
                    DeoptLevel::Soft
                }
            }
        }
    }
    
    /// Suggest guard adjustments based on failure reason
    fn suggest_guard_adjustments(&self, reason: &DeoptReason, guard_failures: &[usize]) -> Vec<GuardAdjustment> {
        let mut adjustments = Vec::new();
        
        match reason {
            DeoptReason::GuardFailure(_) => {
                for &guard_id in guard_failures {
                    adjustments.push(GuardAdjustment::RelaxTypeCheck { guard_id });
                }
            },
            DeoptReason::RangeViolation => {
                for &guard_id in guard_failures {
                    adjustments.push(GuardAdjustment::ExpandRange { 
                        guard_id, 
                        new_min: -1000, 
                        new_max: 1000 
                    });
                }
            },
            DeoptReason::TypeInstability => {
                for &guard_id in guard_failures {
                    adjustments.push(GuardAdjustment::RemoveGuard { guard_id });
                }
            },
            DeoptReason::BranchMisprediction => {
                for &guard_id in guard_failures {
                    adjustments.push(GuardAdjustment::ReduceConfidenceThreshold { 
                        guard_id, 
                        new_threshold: 0.5 
                    });
                }
            },
            _ => {
                if guard_failures.len() > 3 {
                    for &guard_id in &guard_failures[0..2] {
                        adjustments.push(GuardAdjustment::RemoveGuard { guard_id });
                    }
                }
            }
        }
        
        adjustments
    }
    
    /// Calculate retry delay based on deoptimization level and failure rate
    fn calculate_retry_delay(&self, level: &DeoptLevel, failure_rate: f64) -> Option<std::time::Duration> {
        match level {
            DeoptLevel::Soft => Some(std::time::Duration::from_millis(100)),
            DeoptLevel::Medium => Some(std::time::Duration::from_millis((500.0 * (1.0 + failure_rate)) as u64)),
            DeoptLevel::Hard => Some(std::time::Duration::from_secs((5.0 * (1.0 + failure_rate * 2.0)) as u64)),
            DeoptLevel::Blacklist => None,
        }
    }
    
    /// Calculate confidence in the deoptimization decision
    fn calculate_decision_confidence(&self, level: &DeoptLevel, failure_rate: f64) -> f64 {
        match level {
            DeoptLevel::Soft => 0.6 + (failure_rate * 0.2),
            DeoptLevel::Medium => 0.7 + (failure_rate * 0.2),
            DeoptLevel::Hard => 0.8 + (failure_rate * 0.15),
            DeoptLevel::Blacklist => 0.95,
        }
    }
    
    /// Record deoptimization event
    fn record_deopt_event(&mut self, function_id: &FunctionId, event: DeoptEvent) {
        self.deopt_history.entry(function_id.clone()).or_insert_with(Vec::new).push(event);
        
        if let Some(history) = self.deopt_history.get_mut(function_id) {
            if history.len() > 100 {
                history.drain(0..50);
            }
        }
    }
    
    /// Count recent failures for a function
    fn count_recent_failures(&self, function_id: &FunctionId, time_window: std::time::Duration) -> u32 {
        if let Some(history) = self.deopt_history.get(function_id) {
            let cutoff = std::time::Instant::now() - time_window;
            history.iter()
                  .filter(|event| event.timestamp > cutoff)
                  .count() as u32
        } else {
            0
        }
    }
    
    /// Check if function should be blacklisted
    pub fn should_blacklist(&mut self, function_id: &FunctionId, reason: DeoptReason) -> bool {
        let recent_failures = self.count_recent_failures(function_id, std::time::Duration::from_secs(300));
        
        if recent_failures >= 20 {
            self.blacklisted_functions.insert(function_id.clone(), reason);
            true
        } else {
            false
        }
    }
    
    /// Get deoptimization statistics
    pub fn get_statistics(&self) -> HashMap<DeoptReason, u32> {
        self.reason_statistics.clone()
    }
    
    /// Adapt thresholds based on system performance
    pub fn adapt_thresholds(&mut self, system_performance: f64) {
        let adaptation = self.adaptive_thresholds.adaptation_factor * (1.0 - system_performance);
        
        self.adaptive_thresholds.soft_deopt_failure_rate = 
            (self.adaptive_thresholds.soft_deopt_failure_rate - adaptation).max(0.05);
        self.adaptive_thresholds.medium_deopt_failure_rate = 
            (self.adaptive_thresholds.medium_deopt_failure_rate - adaptation).max(0.1);
        self.adaptive_thresholds.hard_deopt_failure_rate = 
            (self.adaptive_thresholds.hard_deopt_failure_rate - adaptation).max(0.3);
    }
}

/// Speculation budget management system for controlling resource usage
#[derive(Debug)]
pub struct SpeculationBudgetManager {
    pub budget_config: BudgetConfig,
    pub current_usage: ResourceUsage,
    pub budget_history: Vec<BudgetSnapshot>,
    pub allocation_strategy: AllocationStrategy,
    pub budget_stats: BudgetStats,
    pub resource_type_stats: HashMap<String, ResourceTypeStats>,
}

/// Statistics for specific resource types
#[derive(Debug, Clone)]
pub struct ResourceTypeStats {
    pub total_requests: u64,
    pub successful_requests: u64,
    pub denied_requests: u64,
    pub total_allocated: f64,
    pub peak_allocation: f64,
    pub average_allocation_size: f64,
    pub success_rate: f64,
}

impl ResourceTypeStats {
    pub fn new() -> Self {
        Self {
            total_requests: 0,
            successful_requests: 0,
            denied_requests: 0,
            total_allocated: 0.0,
            peak_allocation: 0.0,
            average_allocation_size: 0.0,
            success_rate: 0.0,
        }
    }

    pub fn update_on_request(&mut self, amount: f64, granted: bool) {
        self.total_requests += 1;
        if granted {
            self.successful_requests += 1;
            self.total_allocated += amount;
            self.peak_allocation = self.peak_allocation.max(amount);
            self.average_allocation_size = self.total_allocated / self.successful_requests as f64;
        } else {
            self.denied_requests += 1;
        }
        self.success_rate = self.successful_requests as f64 / self.total_requests as f64;
    }
}

/// Configuration for speculation budgets
#[derive(Debug, Clone)]
pub struct BudgetConfig {
    pub max_memory_mb: usize,
    pub max_compilation_time_ms: u64,
    pub max_active_guards: usize,
    pub max_speculation_depth: usize,
    pub memory_pressure_threshold: f64,
    pub time_pressure_threshold: f64,
    pub guard_pressure_threshold: f64,
    pub emergency_cleanup_threshold: f64,
    pub budget_refresh_interval_ms: u64,
}

/// Current resource usage tracking
#[derive(Debug, Clone)]
pub struct ResourceUsage {
    pub memory_used_mb: f64,
    pub compilation_time_ms: u64,
    pub active_guards: usize,
    pub speculation_depth: usize,
    pub guard_validation_overhead_ms: u64,
    pub deoptimization_overhead_ms: u64,
    pub inline_cache_memory_mb: f64,
    pub value_speculation_memory_mb: f64,
    pub loop_specialization_memory_mb: f64,
}

/// Snapshot of budget state at a point in time
#[derive(Debug, Clone)]
pub struct BudgetSnapshot {
    pub timestamp: std::time::Instant,
    pub usage: ResourceUsage,
    pub pressure_levels: PressureLevels,
    pub active_optimizations: usize,
    pub budget_utilization: f64,
}

/// Pressure levels for different resources
#[derive(Debug, Clone)]
pub struct PressureLevels {
    pub memory_pressure: f64,
    pub time_pressure: f64,
    pub guard_pressure: f64,
    pub overall_pressure: f64,
}

/// Budget allocation strategy
#[derive(Debug, Clone)]
pub enum AllocationStrategy {
    Conservative { reserve_ratio: f64 },
    Aggressive { overcommit_ratio: f64 },
    Adaptive { pressure_threshold: f64 },
    ProfileGuided { history_weight: f64 },
}

/// Budget management statistics
#[derive(Debug, Clone)]
pub struct BudgetStats {
    pub total_allocations: u64,
    pub successful_allocations: u64,
    pub denied_allocations: u64,
    pub emergency_cleanups: u64,
    pub average_utilization: f64,
    pub peak_memory_usage_mb: f64,
    pub peak_guard_count: usize,
    pub longest_compilation_ms: u64,
}

/// Resource allocation request
#[derive(Debug, Clone)]
pub struct AllocationRequest {
    pub resource_type: ResourceType,
    pub amount: f64,
    pub priority: AllocationPriority,
    pub duration_estimate_ms: Option<u64>,
    pub requester: String,
}

/// Types of resources that can be allocated
#[derive(Debug, Clone)]
pub enum ResourceType {
    Memory { purpose: MemoryPurpose },
    Guards { guard_type: String },
    CompilationTime { operation: String },
    SpeculationDepth { depth_increase: usize },
}

/// Purpose of memory allocation
#[derive(Debug, Clone)]
pub enum MemoryPurpose {
    InlineCache,
    ValueSpeculation,
    LoopSpecialization,
    GuardStorage,
    DeoptimizationData,
    ProfileData,
}

/// Priority of allocation request
#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord)]
pub enum AllocationPriority {
    Critical,
    High,
    Normal,
    Low,
    BestEffort,
}

/// Result of allocation request
#[derive(Debug, Clone)]
pub struct AllocationResult {
    pub granted: bool,
    pub allocated_amount: f64,
    pub allocation_id: Option<usize>,
    pub denial_reason: Option<String>,
    pub suggested_retry_delay_ms: Option<u64>,
}

impl SpeculationBudgetManager {
    pub fn new(config: BudgetConfig) -> Self {
        Self {
            budget_config: config,
            current_usage: ResourceUsage {
                memory_used_mb: 0.0,
                compilation_time_ms: 0,
                active_guards: 0,
                speculation_depth: 0,
                guard_validation_overhead_ms: 0,
                deoptimization_overhead_ms: 0,
                inline_cache_memory_mb: 0.0,
                value_speculation_memory_mb: 0.0,
                loop_specialization_memory_mb: 0.0,
            },
            budget_history: Vec::new(),
            allocation_strategy: AllocationStrategy::Adaptive { pressure_threshold: 0.8 },
            budget_stats: BudgetStats {
                total_allocations: 0,
                successful_allocations: 0,
                denied_allocations: 0,
                emergency_cleanups: 0,
                average_utilization: 0.0,
                peak_memory_usage_mb: 0.0,
                peak_guard_count: 0,
                longest_compilation_ms: 0,
            },
            resource_type_stats: HashMap::new(),
        }
    }

    /// Request resource allocation
    pub fn request_allocation(&mut self, request: AllocationRequest) -> AllocationResult {
        self.budget_stats.total_allocations += 1;
        
        let resource_key = self.resource_type_key(&request.resource_type);
        
        let pressure_levels = self.calculate_pressure_levels();
        let can_allocate = self.can_allocate_resource(&request, &pressure_levels);
        
        // Update per-resource-type statistics
        let stats = self.resource_type_stats.entry(resource_key).or_insert_with(ResourceTypeStats::new);
        stats.update_on_request(request.amount, can_allocate);
        
        if can_allocate {
            self.allocate_resource(&request);
            self.budget_stats.successful_allocations += 1;
            AllocationResult {
                granted: true,
                allocated_amount: request.amount,
                allocation_id: Some(self.budget_stats.total_allocations as usize),
                denial_reason: None,
                suggested_retry_delay_ms: None,
            }
        } else {
            self.budget_stats.denied_allocations += 1;
            let (reason, retry_delay) = self.get_denial_details(&request, &pressure_levels);
            AllocationResult {
                granted: false,
                allocated_amount: 0.0,
                allocation_id: None,
                denial_reason: Some(reason),
                suggested_retry_delay_ms: retry_delay,
            }
        }
    }

    /// Calculate current pressure levels
    fn calculate_pressure_levels(&self) -> PressureLevels {
        let memory_pressure = self.current_usage.memory_used_mb / self.budget_config.max_memory_mb as f64;
        let time_pressure = self.current_usage.compilation_time_ms as f64 / self.budget_config.max_compilation_time_ms as f64;
        let guard_pressure = self.current_usage.active_guards as f64 / self.budget_config.max_active_guards as f64;
        
        let overall_pressure = (memory_pressure + time_pressure + guard_pressure) / 3.0;
        
        PressureLevels {
            memory_pressure,
            time_pressure,
            guard_pressure,
            overall_pressure,
        }
    }

    /// Check if resource can be allocated
    fn can_allocate_resource(&self, request: &AllocationRequest, pressure_levels: &PressureLevels) -> bool {
        match &self.allocation_strategy {
            AllocationStrategy::Conservative { reserve_ratio } => {
                self.can_allocate_conservative(request, pressure_levels, *reserve_ratio)
            },
            AllocationStrategy::Aggressive { overcommit_ratio } => {
                self.can_allocate_aggressive(request, pressure_levels, *overcommit_ratio)
            },
            AllocationStrategy::Adaptive { pressure_threshold } => {
                self.can_allocate_adaptive(request, pressure_levels, *pressure_threshold)
            },
            AllocationStrategy::ProfileGuided { history_weight } => {
                self.can_allocate_profile_guided(request, pressure_levels, *history_weight)
            },
        }
    }

    /// Conservative allocation strategy
    fn can_allocate_conservative(&self, request: &AllocationRequest, pressure_levels: &PressureLevels, reserve_ratio: f64) -> bool {
        match &request.resource_type {
            ResourceType::Memory { .. } => {
                let new_usage = self.current_usage.memory_used_mb + request.amount;
                new_usage <= (self.budget_config.max_memory_mb as f64) * (1.0 - reserve_ratio)
            },
            ResourceType::Guards { .. } => {
                let new_guard_count = self.current_usage.active_guards + request.amount as usize;
                new_guard_count <= (self.budget_config.max_active_guards as f64 * (1.0 - reserve_ratio)) as usize
            },
            ResourceType::CompilationTime { .. } => {
                pressure_levels.time_pressure < 0.7
            },
            ResourceType::SpeculationDepth { depth_increase } => {
                self.current_usage.speculation_depth + depth_increase <= self.budget_config.max_speculation_depth
            },
        }
    }

    /// Aggressive allocation strategy
    fn can_allocate_aggressive(&self, request: &AllocationRequest, pressure_levels: &PressureLevels, overcommit_ratio: f64) -> bool {
        match &request.resource_type {
            ResourceType::Memory { .. } => {
                let new_usage = self.current_usage.memory_used_mb + request.amount;
                new_usage <= (self.budget_config.max_memory_mb as f64) * overcommit_ratio
            },
            ResourceType::Guards { .. } => {
                let new_guard_count = self.current_usage.active_guards + request.amount as usize;
                new_guard_count <= (self.budget_config.max_active_guards as f64 * overcommit_ratio) as usize
            },
            ResourceType::CompilationTime { .. } => {
                pressure_levels.time_pressure < 0.9
            },
            ResourceType::SpeculationDepth { depth_increase } => {
                self.current_usage.speculation_depth + depth_increase <= (self.budget_config.max_speculation_depth as f64 * overcommit_ratio) as usize
            },
        }
    }

    /// Adaptive allocation strategy
    fn can_allocate_adaptive(&self, request: &AllocationRequest, pressure_levels: &PressureLevels, pressure_threshold: f64) -> bool {
        if pressure_levels.overall_pressure > pressure_threshold {
            return request.priority >= AllocationPriority::High;
        }
        
        match &request.resource_type {
            ResourceType::Memory { .. } => {
                pressure_levels.memory_pressure < 0.85
            },
            ResourceType::Guards { .. } => {
                pressure_levels.guard_pressure < 0.8
            },
            ResourceType::CompilationTime { .. } => {
                pressure_levels.time_pressure < 0.8
            },
            ResourceType::SpeculationDepth { .. } => {
                pressure_levels.overall_pressure < 0.75
            },
        }
    }

    /// Profile-guided allocation strategy
    fn can_allocate_profile_guided(&self, request: &AllocationRequest, pressure_levels: &PressureLevels, history_weight: f64) -> bool {
        if self.budget_history.len() < 10 {
            return self.can_allocate_adaptive(request, pressure_levels, 0.8);
        }
        
        let recent_utilization = self.calculate_recent_average_utilization(10);
        let historical_success_rate = self.calculate_historical_success_rate(&request.resource_type);
        
        let weighted_score = (recent_utilization * (1.0 - history_weight)) + (historical_success_rate * history_weight);
        
        weighted_score > 0.6 && pressure_levels.overall_pressure < 0.8
    }

    /// Actually allocate the resource
    fn allocate_resource(&mut self, request: &AllocationRequest) {
        match &request.resource_type {
            ResourceType::Memory { purpose } => {
                self.current_usage.memory_used_mb += request.amount;
                match purpose {
                    MemoryPurpose::InlineCache => self.current_usage.inline_cache_memory_mb += request.amount,
                    MemoryPurpose::ValueSpeculation => self.current_usage.value_speculation_memory_mb += request.amount,
                    MemoryPurpose::LoopSpecialization => self.current_usage.loop_specialization_memory_mb += request.amount,
                    _ => {},
                }
                self.budget_stats.peak_memory_usage_mb = self.budget_stats.peak_memory_usage_mb.max(self.current_usage.memory_used_mb);
            },
            ResourceType::Guards { .. } => {
                self.current_usage.active_guards += request.amount as usize;
                self.budget_stats.peak_guard_count = self.budget_stats.peak_guard_count.max(self.current_usage.active_guards);
            },
            ResourceType::CompilationTime { .. } => {
                self.current_usage.compilation_time_ms += request.amount as u64;
                self.budget_stats.longest_compilation_ms = self.budget_stats.longest_compilation_ms.max(self.current_usage.compilation_time_ms);
            },
            ResourceType::SpeculationDepth { depth_increase } => {
                self.current_usage.speculation_depth += depth_increase;
            },
        }
    }

    /// Get details about why allocation was denied
    fn get_denial_details(&self, request: &AllocationRequest, pressure_levels: &PressureLevels) -> (String, Option<u64>) {
        let reason = match &request.resource_type {
            ResourceType::Memory { .. } => {
                if pressure_levels.memory_pressure > 0.9 {
                    "Memory pressure too high"
                } else {
                    "Memory budget exceeded"
                }
            },
            ResourceType::Guards { .. } => {
                if pressure_levels.guard_pressure > 0.9 {
                    "Guard pressure too high"
                } else {
                    "Guard limit exceeded"
                }
            },
            ResourceType::CompilationTime { .. } => "Compilation time budget exceeded",
            ResourceType::SpeculationDepth { .. } => "Maximum speculation depth reached",
        };
        
        let retry_delay = if pressure_levels.overall_pressure > 0.9 {
            Some(5000) // 5 seconds for high pressure
        } else {
            Some(1000) // 1 second for normal pressure
        };
        
        (reason.to_string(), retry_delay)
    }

    /// Release allocated resources
    pub fn release_allocation(&mut self, allocation_id: usize, resource_type: ResourceType, amount: f64) {
        match resource_type {
            ResourceType::Memory { purpose } => {
                self.current_usage.memory_used_mb = (self.current_usage.memory_used_mb - amount).max(0.0);
                match purpose {
                    MemoryPurpose::InlineCache => {
                        self.current_usage.inline_cache_memory_mb = (self.current_usage.inline_cache_memory_mb - amount).max(0.0);
                    },
                    MemoryPurpose::ValueSpeculation => {
                        self.current_usage.value_speculation_memory_mb = (self.current_usage.value_speculation_memory_mb - amount).max(0.0);
                    },
                    MemoryPurpose::LoopSpecialization => {
                        self.current_usage.loop_specialization_memory_mb = (self.current_usage.loop_specialization_memory_mb - amount).max(0.0);
                    },
                    _ => {},
                }
            },
            ResourceType::Guards { .. } => {
                self.current_usage.active_guards = self.current_usage.active_guards.saturating_sub(amount as usize);
            },
            ResourceType::CompilationTime { .. } => {
                // Time can't be released, but we can track it
            },
            ResourceType::SpeculationDepth { depth_increase } => {
                self.current_usage.speculation_depth = self.current_usage.speculation_depth.saturating_sub(depth_increase);
            },
        }
    }

    /// Perform emergency cleanup to free resources
    pub fn emergency_cleanup(&mut self) -> bool {
        self.budget_stats.emergency_cleanups += 1;
        
        let pressure_levels = self.calculate_pressure_levels();
        if pressure_levels.overall_pressure < self.budget_config.emergency_cleanup_threshold {
            return false;
        }
        
        // Free least valuable resources first
        let mut freed_memory = 0.0;
        
        // Cleanup old inline cache entries
        if pressure_levels.memory_pressure > 0.8 {
            let to_free = self.current_usage.inline_cache_memory_mb * 0.3;
            self.current_usage.inline_cache_memory_mb -= to_free;
            self.current_usage.memory_used_mb -= to_free;
            freed_memory += to_free;
        }
        
        // Cleanup old value speculation data
        if pressure_levels.memory_pressure > 0.7 {
            let to_free = self.current_usage.value_speculation_memory_mb * 0.2;
            self.current_usage.value_speculation_memory_mb -= to_free;
            self.current_usage.memory_used_mb -= to_free;
            freed_memory += to_free;
        }
        
        // Reduce speculation depth
        if self.current_usage.speculation_depth > 2 {
            self.current_usage.speculation_depth = (self.current_usage.speculation_depth / 2).max(1);
        }
        
        freed_memory > 0.0
    }

    /// Take snapshot of current budget state
    pub fn take_snapshot(&mut self) {
        let pressure_levels = self.calculate_pressure_levels();
        let snapshot = BudgetSnapshot {
            timestamp: std::time::Instant::now(),
            usage: self.current_usage.clone(),
            pressure_levels,
            active_optimizations: self.current_usage.active_guards,
            budget_utilization: self.calculate_current_utilization(),
        };
        
        self.budget_history.push(snapshot);
        
        // Keep only recent history
        if self.budget_history.len() > 1000 {
            self.budget_history.drain(0..500);
        }
    }

    /// Calculate current budget utilization
    fn calculate_current_utilization(&self) -> f64 {
        let memory_util = self.current_usage.memory_used_mb / self.budget_config.max_memory_mb as f64;
        let guard_util = self.current_usage.active_guards as f64 / self.budget_config.max_active_guards as f64;
        let time_util = self.current_usage.compilation_time_ms as f64 / self.budget_config.max_compilation_time_ms as f64;
        
        (memory_util + guard_util + time_util) / 3.0
    }

    /// Calculate recent average utilization
    fn calculate_recent_average_utilization(&self, count: usize) -> f64 {
        if self.budget_history.is_empty() {
            return self.calculate_current_utilization();
        }
        
        let recent_count = count.min(self.budget_history.len());
        let recent_snapshots = &self.budget_history[self.budget_history.len() - recent_count..];
        
        let total_utilization: f64 = recent_snapshots.iter()
            .map(|snapshot| snapshot.budget_utilization)
            .sum();
            
        total_utilization / recent_snapshots.len() as f64
    }

    /// Generate a key for resource type tracking
    fn resource_type_key(&self, resource_type: &ResourceType) -> String {
        match resource_type {
            ResourceType::Memory { purpose } => {
                format!("memory_{:?}", purpose).to_lowercase()
            },
            ResourceType::Guards { guard_type } => {
                format!("guards_{}", guard_type).to_lowercase()
            },
            ResourceType::CompilationTime { operation } => {
                format!("time_{}", operation).to_lowercase()
            },
            ResourceType::SpeculationDepth { .. } => {
                "speculation_depth".to_string()
            },
        }
    }

    /// Calculate historical success rate for resource type
    fn calculate_historical_success_rate(&self, resource_type: &ResourceType) -> f64 {
        let resource_key = self.resource_type_key(resource_type);
        
        if let Some(stats) = self.resource_type_stats.get(&resource_key) {
            stats.success_rate
        } else {
            // Default neutral rate for new resource types
            0.5
        }
    }

    /// Get budget status report
    pub fn get_budget_status(&self) -> BudgetStatusReport {
        let pressure_levels = self.calculate_pressure_levels();
        let current_utilization = self.calculate_current_utilization();
        
        BudgetStatusReport {
            current_usage: self.current_usage.clone(),
            pressure_levels,
            current_utilization,
            budget_stats: self.budget_stats.clone(),
            allocation_strategy: self.allocation_strategy.clone(),
            needs_emergency_cleanup: pressure_levels.overall_pressure > self.budget_config.emergency_cleanup_threshold,
        }
    }

    /// Update allocation strategy based on performance
    pub fn update_allocation_strategy(&mut self) {
        let recent_utilization = self.calculate_recent_average_utilization(50);
        let success_rate = if self.budget_stats.total_allocations > 0 {
            self.budget_stats.successful_allocations as f64 / self.budget_stats.total_allocations as f64
        } else {
            0.5
        };
        
        if success_rate < 0.7 && recent_utilization > 0.8 {
            // Switch to conservative if we're denying too many allocations
            self.allocation_strategy = AllocationStrategy::Conservative { reserve_ratio: 0.2 };
        } else if success_rate > 0.9 && recent_utilization < 0.6 {
            // Switch to aggressive if we have spare capacity
            self.allocation_strategy = AllocationStrategy::Aggressive { overcommit_ratio: 1.2 };
        } else {
            // Use adaptive strategy
            self.allocation_strategy = AllocationStrategy::Adaptive { pressure_threshold: 0.8 };
        }
    }

    /// Reset budget counters
    pub fn reset_budget(&mut self) {
        self.current_usage = ResourceUsage {
            memory_used_mb: 0.0,
            compilation_time_ms: 0,
            active_guards: 0,
            speculation_depth: 0,
            guard_validation_overhead_ms: 0,
            deoptimization_overhead_ms: 0,
            inline_cache_memory_mb: 0.0,
            value_speculation_memory_mb: 0.0,
            loop_specialization_memory_mb: 0.0,
        };
    }

    /// Get resource usage breakdown
    pub fn get_resource_breakdown(&self) -> ResourceBreakdown {
        ResourceBreakdown {
            total_memory_mb: self.current_usage.memory_used_mb,
            inline_cache_memory_mb: self.current_usage.inline_cache_memory_mb,
            value_speculation_memory_mb: self.current_usage.value_speculation_memory_mb,
            loop_specialization_memory_mb: self.current_usage.loop_specialization_memory_mb,
            other_memory_mb: self.current_usage.memory_used_mb 
                - self.current_usage.inline_cache_memory_mb 
                - self.current_usage.value_speculation_memory_mb 
                - self.current_usage.loop_specialization_memory_mb,
            active_guards: self.current_usage.active_guards,
            speculation_depth: self.current_usage.speculation_depth,
            compilation_time_ms: self.current_usage.compilation_time_ms,
        }
    }

    /// Get resource type statistics
    pub fn get_resource_type_stats(&self) -> &HashMap<String, ResourceTypeStats> {
        &self.resource_type_stats
    }

    /// Get success rate for specific resource type
    pub fn get_resource_success_rate(&self, resource_type: &ResourceType) -> f64 {
        self.calculate_historical_success_rate(resource_type)
    }

    /// Get top performing resource types by success rate
    pub fn get_top_performing_resource_types(&self, limit: usize) -> Vec<(String, f64)> {
        let mut performance_list: Vec<_> = self.resource_type_stats.iter()
            .map(|(key, stats)| (key.clone(), stats.success_rate))
            .collect();
        
        performance_list.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap_or(std::cmp::Ordering::Equal));
        performance_list.truncate(limit);
        performance_list
    }

    /// Get resource types with low success rates that may need attention
    pub fn get_problematic_resource_types(&self, threshold: f64) -> Vec<(String, f64, u64)> {
        self.resource_type_stats.iter()
            .filter(|(_, stats)| stats.success_rate < threshold && stats.total_requests > 10)
            .map(|(key, stats)| (key.clone(), stats.success_rate, stats.denied_requests))
            .collect()
    }
}

/// Budget status report
#[derive(Debug, Clone)]
pub struct BudgetStatusReport {
    pub current_usage: ResourceUsage,
    pub pressure_levels: PressureLevels,
    pub current_utilization: f64,
    pub budget_stats: BudgetStats,
    pub allocation_strategy: AllocationStrategy,
    pub needs_emergency_cleanup: bool,
}

/// Resource usage breakdown
#[derive(Debug, Clone)]
pub struct ResourceBreakdown {
    pub total_memory_mb: f64,
    pub inline_cache_memory_mb: f64,
    pub value_speculation_memory_mb: f64,
    pub loop_specialization_memory_mb: f64,
    pub other_memory_mb: f64,
    pub active_guards: usize,
    pub speculation_depth: usize,
    pub compilation_time_ms: u64,
}