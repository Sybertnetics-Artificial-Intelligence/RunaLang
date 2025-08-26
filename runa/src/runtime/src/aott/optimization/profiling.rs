//! Adaptive Profile Optimizer
//! 
//! Performs profile-guided optimization across all AOTT tiers.

use crate::aott::types::*;
use std::collections::HashMap;
use std::time::Duration;

/// Adaptive profile optimizer
#[derive(Debug)]
pub struct AdaptiveProfileOptimizer {
    pub profiles: HashMap<FunctionId, FunctionProfile>,
    pub optimization_decisions: HashMap<FunctionId, Vec<OptimizationDecision>>,
    pub tier_promotion_candidates: Vec<TierPromotionCandidate>,
}

impl AdaptiveProfileOptimizer {
    pub fn new() -> Self {
        Self {
            profiles: HashMap::new(),
            optimization_decisions: HashMap::new(),
            tier_promotion_candidates: Vec::new(),
        }
    }
    
    pub fn record_execution(&mut self, function_id: FunctionId, execution_data: ExecutionData) {
        let profile = self.profiles.entry(function_id).or_insert_with(FunctionProfile::new);
        profile.update_with_execution(execution_data);
    }
    
    pub fn analyze_optimization_opportunities(&mut self, function_id: &FunctionId) -> CompilerResult<Vec<OptimizationDecision>> {
        if let Some(profile) = self.profiles.get(function_id) {
            let mut decisions = Vec::new();
            
            // Analyze call frequency for inlining
            if profile.call_frequency > 100.0 {
                decisions.push(OptimizationDecision::AggressiveInlining);
            }
            
            // Analyze type stability for specialization
            if profile.type_stability > 0.9 {
                decisions.push(OptimizationDecision::SpecializeForType("String".to_string()));
            }
            
            // Analyze loop patterns for vectorization
            if profile.has_vectorizable_loops {
                decisions.push(OptimizationDecision::Vectorization);
            }
            
            self.optimization_decisions.insert(function_id.clone(), decisions.clone());
            Ok(decisions)
        } else {
            Ok(vec![OptimizationDecision::Conservative])
        }
    }
    
    pub fn identify_tier_promotion_candidates(&mut self) -> Vec<TierPromotionCandidate> {
        let mut candidates = Vec::new();
        
        for (function_id, profile) in &self.profiles {
            if profile.should_promote() {
                candidates.push(TierPromotionCandidate {
                    function_id: function_id.clone(),
                    current_tier: profile.current_tier,
                    target_tier: profile.current_tier.next_tier().unwrap_or(profile.current_tier),
                    promotion_score: profile.calculate_promotion_score(),
                });
            }
        }
        
        candidates.sort_by(|a, b| b.promotion_score.partial_cmp(&a.promotion_score).unwrap());
        self.tier_promotion_candidates = candidates.clone();
        candidates
    }
}

/// Function execution profile
#[derive(Debug, Clone)]
pub struct FunctionProfile {
    pub call_count: u64,
    pub call_frequency: f64,
    pub average_execution_time: Duration,
    pub total_execution_time: Duration,
    pub type_stability: f64,
    pub branch_predictability: f64,
    pub memory_locality: f64,
    pub has_vectorizable_loops: bool,
    pub current_tier: TierLevel,
    pub last_updated: std::time::Instant,
}

impl FunctionProfile {
    pub fn new() -> Self {
        Self {
            call_count: 0,
            call_frequency: 0.0,
            average_execution_time: Duration::default(),
            total_execution_time: Duration::default(),
            type_stability: 0.0,
            branch_predictability: 0.0,
            memory_locality: 0.0,
            has_vectorizable_loops: false,
            current_tier: TierLevel::T0,
            last_updated: std::time::Instant::now(),
        }
    }
    
    pub fn update_with_execution(&mut self, data: ExecutionData) {
        self.call_count += 1;
        self.total_execution_time += data.execution_time;
        self.average_execution_time = self.total_execution_time / self.call_count as u32;
        
        // Update frequency (calls per second)
        let time_since_last = self.last_updated.elapsed();
        if time_since_last > Duration::from_secs(1) {
            self.call_frequency = self.call_count as f64 / time_since_last.as_secs_f64();
        }
        
        // Update type stability
        self.type_stability = data.type_consistency;
        
        // Update branch predictability
        self.branch_predictability = data.branch_prediction_accuracy;
        
        // Update memory locality
        self.memory_locality = data.cache_hit_ratio;
        
        // Check for vectorizable loops
        self.has_vectorizable_loops = data.loop_analysis.has_vectorizable_loops;
        
        self.last_updated = std::time::Instant::now();
    }
    
    pub fn should_promote(&self) -> bool {
        match self.current_tier {
            TierLevel::T0 => self.call_count > 10,
            TierLevel::T1 => self.call_count > 100,
            TierLevel::T2 => self.call_count > 1000,
            TierLevel::T3 => self.call_count > 10000,
            TierLevel::T4 => false,
        }
    }
    
    pub fn calculate_promotion_score(&self) -> f64 {
        let frequency_score = (self.call_frequency / 1000.0).min(1.0);
        let stability_score = (self.type_stability + self.branch_predictability) / 2.0;
        let performance_score = if self.average_execution_time > Duration::from_millis(1) { 1.0 } else { 0.5 };
        
        (frequency_score * 0.4 + stability_score * 0.4 + performance_score * 0.2) * 100.0
    }
}

/// Execution data for profiling
#[derive(Debug, Clone)]
pub struct ExecutionData {
    pub execution_time: Duration,
    pub type_consistency: f64,
    pub branch_prediction_accuracy: f64,
    pub cache_hit_ratio: f64,
    pub loop_analysis: LoopAnalysisData,
    pub memory_usage: MemoryUsageData,
}

/// Loop analysis data
#[derive(Debug, Clone)]
pub struct LoopAnalysisData {
    pub loop_count: usize,
    pub has_vectorizable_loops: bool,
    pub average_trip_count: f64,
    pub nested_depth: usize,
}

/// Memory usage data
#[derive(Debug, Clone)]
pub struct MemoryUsageData {
    pub allocations: u64,
    pub peak_usage: usize,
    pub locality_score: f64,
}

/// Tier promotion candidate
#[derive(Debug, Clone)]
pub struct TierPromotionCandidate {
    pub function_id: FunctionId,
    pub current_tier: TierLevel,
    pub target_tier: TierLevel,
    pub promotion_score: f64,
}

/// Optimization decisions from profiling
#[derive(Debug, Clone)]
pub enum OptimizationDecision {
    Conservative,
    AggressiveInlining,
    BranchPredictionOptimization,
    Vectorization,
    SpecializeForType(String),
    LoopUnrolling(usize),
    FunctionSpecialization,
}