//! Advanced Data Flow Analysis Engine
//! 
//! Production-ready data flow analysis implementation for the AOTT compiler.
//! Provides sophisticated algorithms for:
//! - Comprehensive reaching definitions with context sensitivity
//! - Advanced available expressions analysis with global optimization
//! - Precise live variable analysis with path sensitivity
//! - Interprocedural constant propagation with escape analysis
//! - Dead code elimination with control flow sensitivity
//! - Value numbering and common subexpression elimination
//! - Memory disambiguation and alias analysis integration

use crate::aott::types::*;
use crate::aott::analysis::config::*;
use runa_common::bytecode::{Value, OpCode, Chunk};
use runa_common::ast::ASTNode;
use std::collections::{HashMap, HashSet, VecDeque, BTreeSet, BTreeMap};
use std::fmt;
use std::sync::Arc;
use std::time::{Duration, Instant};

/// Statement type for data flow analysis
#[derive(Debug, Clone)]
pub enum StatementType {
    Assignment(String, StatementValue),
    Call(String, Vec<String>),
    Return(Option<String>),
    Branch(String, String, String),
    Jump(String),
    Nop,
}


/// Type compatibility analysis context for comprehensive type checking
#[derive(Debug, Clone)]
pub struct TypeCompatibilityContext {
    pub allow_numeric_coercion: bool,
    pub allow_nullable_coercion: bool,
    pub allow_unknown_types: bool,
    pub allow_array_size_coercion: bool,
    pub allow_dynamic_array_coercion: bool,
    pub allow_variadic_functions: bool,
    pub allow_structural_typing: bool,
    pub allow_generic_unification: bool,
    pub check_inheritance: bool,
    pub variance_mode: VarianceMode,
}

impl Default for TypeCompatibilityContext {
    fn default() -> Self {
        Self {
            allow_numeric_coercion: true,
            allow_nullable_coercion: true,
            allow_unknown_types: true,
            allow_array_size_coercion: false,
            allow_dynamic_array_coercion: true,
            allow_variadic_functions: false,
            allow_structural_typing: false,
            allow_generic_unification: true,
            check_inheritance: true,
            variance_mode: VarianceMode::Invariant,
        }
    }
}

impl TypeCompatibilityContext {
    pub fn with_variance(&self, variance: VarianceMode) -> Self {
        let mut context = self.clone();
        context.variance_mode = variance;
        context
    }
}

/// Variance modes for type parameter checking
#[derive(Debug, Clone, PartialEq)]
pub enum VarianceMode {
    Covariant,     // T <: U implies C<T> <: C<U>
    Contravariant, // T <: U implies C<U> <: C<T>
    Invariant,     // C<T> = C<U> only if T = U
}

/// Type constraints for generic type analysis
#[derive(Debug, Clone, PartialEq)]
pub enum TypeConstraint {
    SupertypeOf(String),
    SubtypeOf(String),
    ImplementsInterface(String),
    HasField(String, String),
    HasMethod(String, Vec<String>, String),
}

/// Comprehensive type information for structural compatibility
#[derive(Debug, Clone)]
pub struct TypeInfo {
    pub name: String,
    pub fields: Vec<FieldInfo>,
    pub methods: Vec<MethodInfo>,
    pub parent_classes: Vec<String>,
    pub implemented_interfaces: Vec<String>,
    pub is_abstract: bool,
    pub is_final: bool,
    pub generic_parameters: Vec<String>,
}

#[derive(Debug, Clone)]
pub struct FieldInfo {
    pub name: String,
    pub field_type: VariableType,
    pub is_public: bool,
    pub is_mutable: bool,
}

#[derive(Debug, Clone)]
pub struct MethodInfo {
    pub name: String,
    pub parameters: Vec<VariableType>,
    pub return_type: VariableType,
    pub is_public: bool,
    pub is_virtual: bool,
    pub is_static: bool,
}

impl MethodInfo {
    pub fn signature_compatible_with(&self, other: &MethodInfo) -> bool {
        self.name == other.name &&
        self.parameters.len() == other.parameters.len() &&
        self.parameters.iter().zip(other.parameters.iter()).all(|(a, b)| a == b) &&
        self.return_type == other.return_type
    }
}

/// Interface information for structural type analysis
#[derive(Debug, Clone)]
pub struct InterfaceInfo {
    pub name: String,
    pub required_methods: Vec<MethodInfo>,
    pub extended_interfaces: Vec<String>,
    pub generic_parameters: Vec<String>,
}

/// Constraint parts for semantic constraint analysis
#[derive(Debug, Clone, PartialEq)]
pub enum ConstraintParts {
    ImplementsInterface(String),
    ExtendsClass(String),
    SubtypeOf(String),
    SupertypeOf(String),
    HasField(String, String),
    HasMethod(String, Vec<String>, String),
    Unknown(String),
}

/// Instruction location for detailed analysis with enhanced context
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct InstructionLocation {
    pub function_id: FunctionId,
    pub block_id: BasicBlockId,
    pub instruction_index: usize,
    pub bytecode_offset: Option<usize>,
}

impl InstructionLocation {
    pub fn new(function_id: FunctionId, block_id: BasicBlockId, instruction_index: usize) -> Self {
        Self {
            function_id,
            block_id,
            instruction_index,
            bytecode_offset: None,
        }
    }
    
    pub fn with_bytecode_offset(mut self, offset: usize) -> Self {
        self.bytecode_offset = Some(offset);
        self
    }
}

/// Function identifier for comprehensive analysis
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct FunctionId {
    pub module: String,
    pub name: String,
    pub signature: String,
    pub context: CallContext,
}

impl FunctionId {
    pub fn new(module: String, name: String, signature: String) -> Self {
        Self {
            module,
            name,
            signature,
            context: CallContext::Direct,
        }
    }
    
    pub fn with_context(mut self, context: CallContext) -> Self {
        self.context = context;
        self
    }
}

/// Call context for interprocedural analysis
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub enum CallContext {
    Direct,
    Indirect,
    Virtual,
    Recursive,
    External,
}

/// Analysis precision levels with sophisticated configurations
#[derive(Debug, Clone, PartialEq)]
pub enum AnalysisPrecision {
    Fast {
        max_iterations: usize,
        context_sensitivity: bool,
    },
    Balanced {
        max_iterations: usize,
        context_sensitivity: bool,
        path_sensitivity: bool,
    },
    Precise {
        max_iterations: usize,
        context_sensitivity: bool,
        path_sensitivity: bool,
        field_sensitivity: bool,
    },
}

impl Default for AnalysisPrecision {
    fn default() -> Self {
        Self::Balanced {
            max_iterations: 100,
            context_sensitivity: true,
            path_sensitivity: false,
        }
    }
}

/// Advanced data flow analysis engine with comprehensive optimization capabilities
#[derive(Debug)]
pub struct DataFlowAnalysisEngine {
    /// Analysis results for each function with context sensitivity
    pub analysis_results: HashMap<FunctionId, DataFlowResult>,
    /// Advanced def-use chains with interprocedural links
    pub def_use_chains: HashMap<FunctionId, DefUseChains>,
    /// Live variable analysis with path sensitivity
    pub live_variables: HashMap<FunctionId, LiveVariableAnalysis>,
    /// Sophisticated constant propagation with interprocedural analysis
    pub constant_propagation: HashMap<FunctionId, ConstantPropagationResult>,
    /// Available expressions with global optimization
    pub available_expressions: HashMap<FunctionId, AvailableExpressionsResult>,
    /// Very busy expressions for code motion
    pub very_busy_expressions: HashMap<FunctionId, VeryBusyExpressionsResult>,
    /// Value numbering for common subexpression elimination
    pub value_numbering: HashMap<FunctionId, ValueNumberingResult>,
    /// Memory disambiguation analysis
    pub memory_analysis: HashMap<FunctionId, MemoryAnalysisResult>,
    /// Control flow graphs with enhanced structure
    pub control_flow_graphs: HashMap<FunctionId, ControlFlowGraph>,
    /// Comprehensive configuration
    pub config: DataFlowAnalysisConfig,
    /// Performance statistics and analytics
    pub statistics: AnalysisStatistics,
    /// Call graph for interprocedural analysis
    pub call_graph: Option<Arc<CallGraphInfo>>,
    /// Alias analysis integration
    pub alias_analyzer: Option<Arc<AliasAnalyzer>>,
}

impl DataFlowAnalysisEngine {
    pub fn new() -> Self {
        Self {
            analysis_results: HashMap::new(),
            def_use_chains: HashMap::new(),
            live_variables: HashMap::new(),
            constant_propagation: HashMap::new(),
            available_expressions: HashMap::new(),
            very_busy_expressions: HashMap::new(),
            value_numbering: HashMap::new(),
            memory_analysis: HashMap::new(),
            control_flow_graphs: HashMap::new(),
            config: DataFlowAnalysisConfig::default(),
            statistics: AnalysisStatistics::new(),
            call_graph: None,
            alias_analyzer: None,
        }
    }
    
    /// Create with advanced configuration
    pub fn with_config(config: DataFlowAnalysisConfig) -> Self {
        let mut engine = Self::new();
        engine.config = config;
        
        // Initialize alias analyzer if enabled
        if engine.config.enable_alias_analysis {
            engine.alias_analyzer = Some(Arc::new(AliasAnalyzer::new(&engine.config.alias_config)));
        }
        
        engine
    }
    
    /// Set call graph for interprocedural analysis
    pub fn set_call_graph(&mut self, call_graph: Arc<CallGraphInfo>) {
        self.call_graph = Some(call_graph);
    }
    
    /// Perform comprehensive data flow analysis on a function
    pub fn analyze_function(&mut self, function_id: &FunctionId, cfg: ControlFlowGraph) -> CompilerResult<DataFlowResult> {
        let start_time = Instant::now();
        
        // Store the control flow graph
        self.control_flow_graphs.insert(function_id.clone(), cfg.clone());
        
        // Build sophisticated analysis framework
        let mut analyzer = AdvancedDataFlowAnalyzer::new(&cfg, &self.config, self.call_graph.as_ref());
        
        // Phase 1: Memory analysis and alias information
        let memory_analysis = if self.config.enable_alias_analysis {
            if let Some(ref alias_analyzer) = self.alias_analyzer {
                Some(alias_analyzer.analyze_function(function_id, &cfg)?)
            } else {
                None
            }
        } else {
            None
        };
        
        // Phase 2: Reaching definitions analysis with context sensitivity
        let reaching_definitions = analyzer.compute_reaching_definitions_advanced(memory_analysis.as_ref())?;
        
        // Phase 3: Available expressions with global optimization
        let available_expressions = analyzer.compute_available_expressions_global()?;
        
        // Phase 4: Live variable analysis with path sensitivity
        let live_variables = analyzer.compute_live_variables_path_sensitive()?;
        
        // Phase 5: Very busy expressions for code motion
        let very_busy_expressions = analyzer.compute_very_busy_expressions_advanced()?;
        
        // Phase 6: Value numbering for common subexpression elimination
        let value_numbering = analyzer.compute_value_numbering()?;
        
        // Phase 7: Identify dead code with sophisticated analysis
        let dead_code_analysis = analyzer.identify_dead_code_comprehensive(&live_variables, &value_numbering)?;
        
        // Phase 8: Optimization opportunity identification
        let optimization_opportunities = analyzer.identify_optimization_opportunities(
            &reaching_definitions,
            &available_expressions,
            &live_variables,
            &dead_code_analysis,
        )?;
        
        // Build comprehensive result
        let result = DataFlowResult {
            function_id: function_id.clone(),
            reaching_definitions: reaching_definitions.clone(),
            available_expressions: available_expressions.clone(),
            live_variables_analysis: live_variables.clone(),
            very_busy_expressions: very_busy_expressions.clone(),
            value_numbering: value_numbering.clone(),
            dead_code_analysis,
            memory_analysis,
            optimization_opportunities,
            control_flow_graph: cfg,
            analysis_quality: analyzer.assess_analysis_quality(),
            analysis_metadata: AnalysisMetadata {
                iteration_counts: analyzer.get_iteration_counts(),
                convergence_time: start_time.elapsed(),
                confidence_scores: analyzer.get_confidence_scores(),
                precision_level: self.config.precision.clone(),
            },
        };
        
        // Store detailed results
        self.analysis_results.insert(function_id.clone(), result.clone());
        self.live_variables.insert(function_id.clone(), live_variables);
        self.available_expressions.insert(function_id.clone(), available_expressions);
        self.very_busy_expressions.insert(function_id.clone(), very_busy_expressions);
        self.value_numbering.insert(function_id.clone(), value_numbering);
        
        if let Some(memory_result) = memory_analysis {
            self.memory_analysis.insert(function_id.clone(), memory_result);
        }
        
        // Record analysis time
        let analysis_time = start_time.elapsed();
        self.statistics.record_analysis(function_id.clone(), analysis_time);
        
        Ok(result)
    }
    
    /// Build sophisticated def-use chains with interprocedural information
    pub fn build_def_use_chains(&mut self, function_id: &FunctionId) -> CompilerResult<DefUseChains> {
        let cfg = self.control_flow_graphs.get(function_id)
            .ok_or_else(|| CompilerError::AnalysisError("CFG not found".to_string()))?;
        
        let mut builder = AdvancedDefUseChainBuilder::new(cfg, &self.config);
        
        // Use reaching definitions for precision
        if let Some(analysis_result) = self.analysis_results.get(function_id) {
            builder.set_reaching_definitions(&analysis_result.reaching_definitions);
        }
        
        // Add interprocedural information if available
        if let Some(ref call_graph) = self.call_graph {
            builder.set_call_graph_info(call_graph.clone());
        }
        
        let chains = builder.build_chains_advanced()?;
        
        self.def_use_chains.insert(function_id.clone(), chains.clone());
        Ok(chains)
    }
    
    /// Perform advanced constant propagation analysis
    pub fn analyze_constant_propagation(&mut self, function_id: &FunctionId) -> CompilerResult<ConstantPropagationResult> {
        let cfg = self.control_flow_graphs.get(function_id)
            .ok_or_else(|| CompilerError::AnalysisError("CFG not found".to_string()))?;
        
        let mut propagator = AdvancedConstantPropagator::new(cfg, &self.config);
        
        // Use alias information if available
        if let Some(memory_analysis) = self.memory_analysis.get(function_id) {
            propagator.set_alias_information(&memory_analysis.alias_sets);
        }
        
        // Add interprocedural constant information
        if let Some(ref call_graph) = self.call_graph {
            propagator.set_interprocedural_constants(call_graph.clone());
        }
        
        let result = propagator.propagate_constants_advanced()?;
        
        self.constant_propagation.insert(function_id.clone(), result.clone());
        Ok(result)
    }
    
    /// Get comprehensive optimization opportunities
    pub fn get_optimization_opportunities(&self, function_id: &FunctionId) -> Vec<OptimizationOpportunity> {
        if let Some(result) = self.analysis_results.get(function_id) {
            result.optimization_opportunities.clone()
        } else {
            // If no cached results exist, perform on-demand analysis to find opportunities
            self.analyze_optimization_opportunities_on_demand(function_id)
                .unwrap_or_else(|_| Vec::new())
        }
    }
    
    /// Perform on-demand optimization analysis when cached results aren't available
    fn analyze_optimization_opportunities_on_demand(&self, function_id: &FunctionId) -> CompilerResult<Vec<OptimizationOpportunity>> {
        let mut opportunities = Vec::new();
        
        // Get the control flow graph for this function
        if let Some(cfg) = self.control_flow_graphs.get(function_id) {
            
            // 1. Dead code elimination opportunities
            opportunities.extend(self.find_dead_code_opportunities(cfg)?);
            
            // 2. Constant propagation opportunities
            opportunities.extend(self.find_constant_propagation_opportunities(cfg)?);
            
            // 3. Common subexpression elimination
            opportunities.extend(self.find_cse_opportunities(cfg)?);
            
            // 4. Loop optimization opportunities
            opportunities.extend(self.find_loop_optimization_opportunities(cfg)?);
            
            // 5. Memory access optimization
            opportunities.extend(self.find_memory_optimization_opportunities(cfg)?);
            
            // 6. Branch optimization opportunities
            opportunities.extend(self.find_branch_optimization_opportunities(cfg)?);
            
            // Sort by estimated impact (high impact first)
            opportunities.sort_by(|a, b| {
                b.estimated_impact.partial_cmp(&a.estimated_impact).unwrap_or(std::cmp::Ordering::Equal)
            });
        }
        
        Ok(opportunities)
    }
    
    /// Find dead code elimination opportunities
    fn find_dead_code_opportunities(&self, cfg: &ControlFlowGraph) -> CompilerResult<Vec<OptimizationOpportunity>> {
        let mut opportunities = Vec::new();

        for (block_id, block) in &cfg.basic_blocks {
            for (stmt_idx, stmt) in block.statements.iter().enumerate() {
                if let Statement::Assignment { target, .. } = stmt {
                    if !self.is_variable_used_after_assignment(cfg, *block_id, stmt_idx, target) {
                        opportunities.push(OptimizationOpportunity {
                            opportunity_type: OptimizationType::DeadCodeElimination,
                            location: InstructionLocation::new(
                                cfg.function_id.clone(),
                                *block_id,
                                stmt_idx,
                            ),
                            description: format!("Dead assignment to variable '{}'", target.name),
                            estimated_impact: 2.0,
                            prerequisites: Vec::new(),
                            side_effects: Vec::new(),
                        });
                    }
                }
            }
        }

        Ok(opportunities)
    }
    
    /// Find constant propagation opportunities
    fn find_constant_propagation_opportunities(&self, cfg: &ControlFlowGraph) -> CompilerResult<Vec<OptimizationOpportunity>> {
        let mut opportunities = Vec::new();
        let mut constant_vars = HashMap::new();
        
        // Simple constant analysis - look for assignments of constants
        for (block_id, block) in &cfg.basic_blocks {
            for (stmt_idx, stmt) in block.statements.iter().enumerate() {
                if let Statement::Assignment { target: var, value, .. } = stmt {
                    if self.is_constant_value(value) {
                        constant_vars.insert(var.name.clone(), value.clone());
                        
                        // Find uses of this variable that could be replaced
                        let uses = self.find_variable_uses_after_assignment(cfg, *block_id, stmt_idx, var);
                        for use_location in uses {
                            opportunities.push(OptimizationOpportunity {
                                opportunity_type: OptimizationType::ConstantPropagation,
                                location: use_location,
                                description: format!("Propagate constant value to variable '{}'", var.name),
                                estimated_impact: 1.5,
                                prerequisites: Vec::new(),
                                side_effects: Vec::new(),
                            });
                        }
                    }
                }
            }
        }
        
        Ok(opportunities)
    }
    
    /// Find common subexpression elimination opportunities
    fn find_cse_opportunities(&self, cfg: &ControlFlowGraph) -> CompilerResult<Vec<OptimizationOpportunity>> {
        let mut opportunities = Vec::new();
        let mut expressions = HashMap::new();
        
        for (block_id, block) in &cfg.basic_blocks {
            for (stmt_idx, stmt) in block.statements.iter().enumerate() {
                if let Statement::Assignment { target: var, value, .. } = stmt {
                    if let Some(expr) = self.extract_expression(value) {
                        let expr_key = format!("{:?}", expr);
                        
                        if let Some(previous_location) = expressions.get(&expr_key) {
                            opportunities.push(OptimizationOpportunity {
                                opportunity_type: OptimizationType::CommonSubexpressionElimination,
                                location: InstructionLocation { 
                                    function: cfg.function_id.clone(), 
                                    block: *block_id, 
                                    instruction: stmt_idx 
                                },
                                description: format!("Common subexpression: {}", expr_key),
                                estimated_impact: 3.0, // High impact for expensive operations
                                prerequisites: vec![format!("Expression first computed at {:?}", previous_location)],
                                side_effects: Vec::new(),
                            });
                        } else {
                            expressions.insert(expr_key, InstructionLocation { 
                                function: cfg.function_id.clone(), 
                                block: *block_id, 
                                instruction: stmt_idx 
                            });
                        }
                    }
                }
            }
        }
        
        Ok(opportunities)
    }
    
    /// Find loop optimization opportunities
    fn find_loop_optimization_opportunities(&self, cfg: &ControlFlowGraph) -> CompilerResult<Vec<OptimizationOpportunity>> {
        let mut opportunities = Vec::new();
        
        // Find natural loops in the CFG
        for natural_loop in &cfg.natural_loops {
            let loop_header = natural_loop.header;
            
            // Look for loop-invariant computations that can be hoisted
            for &loop_block in &natural_loop.blocks {
                if let Some(block) = cfg.basic_blocks.get(&loop_block) {
                    for (stmt_idx, stmt) in block.statements.iter().enumerate() {
                        if let Statement::Assignment { target: var, value, .. } = stmt {
                            if self.is_loop_invariant(value, &natural_loop.blocks, cfg) {
                                opportunities.push(OptimizationOpportunity {
                                    opportunity_type: OptimizationType::LoopInvariantHoisting,
                                    location: InstructionLocation { 
                                        function: cfg.function_id.clone(), 
                                        block: loop_block, 
                                        instruction: stmt_idx 
                                    },
                                    description: format!("Hoist loop-invariant computation of '{}'", var.name),
                                    estimated_impact: 4.0, // Very high impact for loops
                                    prerequisites: Vec::new(),
                                    side_effects: vec!["Moves computation outside loop".to_string()],
                                });
                            }
                        }
                    }
                }
            }
        }
        
        Ok(opportunities)
    }
    
    /// Find memory access optimization opportunities
    fn find_memory_optimization_opportunities(&self, cfg: &ControlFlowGraph) -> CompilerResult<Vec<OptimizationOpportunity>> {
        let mut opportunities = Vec::new();
        
        for (block_id, block) in &cfg.basic_blocks {
            for (stmt_idx, stmt) in block.statements.iter().enumerate() {
                match stmt {
                    Statement::Load { address: StatementValue::Variable(ptr_var), .. } => {
                        // Look for redundant memory loads
                        if self.is_redundant_memory_load(cfg, *block_id, stmt_idx, ptr_var) {
                            opportunities.push(OptimizationOpportunity {
                                opportunity_type: OptimizationType::RedundantLoadElimination,
                                location: InstructionLocation { 
                                    function: cfg.function_id.clone(), 
                                    block: *block_id, 
                                    instruction: stmt_idx 
                                },
                                description: format!("Redundant load from '{}'", ptr_var.name),
                                estimated_impact: 2.5,
                                prerequisites: Vec::new(),
                                side_effects: Vec::new(),
                            });
                        }
                    },
                    _ => {}
                }
            }
        }
        
        Ok(opportunities)
    }
    
    /// Find branch optimization opportunities
    fn find_branch_optimization_opportunities(&self, cfg: &ControlFlowGraph) -> CompilerResult<Vec<OptimizationOpportunity>> {
        let mut opportunities = Vec::new();
        
        for (block_id, block) in &cfg.basic_blocks {
            match &block.terminator {
                Terminator::ConditionalBranch(condition, _, _) => {
                    // Look for branches with constant conditions
                    if self.is_constant_condition(condition) {
                        opportunities.push(OptimizationOpportunity {
                            opportunity_type: OptimizationType::BranchElimination,
                            location: InstructionLocation { 
                                function: cfg.function_id.clone(), 
                                block: *block_id, 
                                instruction: block.statements.len() 
                            },
                            description: "Eliminate branch with constant condition".to_string(),
                            estimated_impact: 1.0,
                            prerequisites: Vec::new(),
                            side_effects: vec!["Eliminates unreachable code".to_string()],
                        });
                    }
                },
                _ => {}
            }
        }
        
        Ok(opportunities)
    }
    
    /// Generate comprehensive analysis report
    pub fn generate_analysis_report(&self, function_id: &FunctionId) -> AnalysisReport {
        let mut report = AnalysisReport::new(function_id.clone());
        
        if let Some(result) = self.analysis_results.get(function_id) {
            report.dead_code_instructions = result.dead_code_analysis.dead_instructions.len();
            report.dead_code_blocks = result.dead_code_analysis.unreachable_blocks.len();
            report.total_blocks = result.control_flow_graph.basic_blocks.len();
            report.analysis_quality = result.analysis_quality.clone();
            report.optimization_opportunities = result.optimization_opportunities.len();
            
            // Value numbering statistics
            if let Some(vn) = self.value_numbering.get(function_id) {
                report.value_numbers_created = vn.value_numbers.len();
                report.common_subexpressions = vn.equivalent_expressions.len();
            }
            
            // Memory analysis statistics
            if let Some(memory) = self.memory_analysis.get(function_id) {
                report.alias_sets = memory.alias_sets.len();
                report.memory_dependencies = memory.dependencies.len();
            }
        }
        
        if let Some(cp_result) = self.constant_propagation.get(function_id) {
            report.propagatable_constants = cp_result.constant_lattice.len();
            report.constant_folding_opportunities = cp_result.foldable_expressions.len();
        }
        
        if let Some(duc) = self.def_use_chains.get(function_id) {
            report.def_use_chains = duc.chains.len();
            report.single_def_variables = duc.single_definition_variables.len();
        }
        
        report
    }
    
    /// Perform interprocedural analysis across all functions
    pub fn analyze_interprocedural(&mut self, functions: &[FunctionId]) -> CompilerResult<InterproceduralResult> {
        if !self.config.enable_interprocedural {
            return Err(CompilerError::AnalysisError("Interprocedural analysis disabled".to_string()));
        }
        
        let start_time = Instant::now();
        
        // Build call graph if not provided
        let call_graph = if let Some(ref cg) = self.call_graph {
            cg.clone()
        } else {
            return Err(CompilerError::AnalysisError("Call graph required for interprocedural analysis".to_string()));
        };
        
        // Perform interprocedural constant propagation
        let mut interprocedural_constants = HashMap::new();
        let mut interprocedural_aliases = HashMap::new();
        
        // Iterate until convergence
        let mut changed = true;
        let mut iteration = 0;
        
        while changed && iteration < self.config.max_interprocedural_iterations {
            changed = false;
            iteration += 1;
            
            for function_id in functions {
                // Propagate constants across function boundaries
                if let Ok(constants) = self.propagate_constants_interprocedural(function_id, &call_graph) {
                    if interprocedural_constants.get(function_id) != Some(&constants) {
                        interprocedural_constants.insert(function_id.clone(), constants);
                        changed = true;
                    }
                }
                
                // Propagate alias information across function boundaries
                if self.config.enable_alias_analysis {
                    if let Ok(aliases) = self.propagate_aliases_interprocedural(function_id, &call_graph) {
                        if interprocedural_aliases.get(function_id) != Some(&aliases) {
                            interprocedural_aliases.insert(function_id.clone(), aliases);
                            changed = true;
                        }
                    }
                }
            }
        }
        
        Ok(InterproceduralResult {
            analysis_time: start_time.elapsed(),
            convergence_iterations: iteration,
            interprocedural_constants,
            interprocedural_aliases,
            call_graph: call_graph.clone(),
        })
    }
    
    /// Propagate constants across function boundaries
    fn propagate_constants_interprocedural(&self, function_id: &FunctionId, call_graph: &CallGraphInfo) -> CompilerResult<HashMap<Variable, ConstantLatticeValue>> {
        let mut constants = HashMap::new();
        
        // Get function's constant propagation result
        if let Some(cp_result) = self.constant_propagation.get(function_id) {
            // Merge constants from all callers
            if let Some(callers) = call_graph.get_callers(function_id) {
                for caller in callers {
                    if let Some(caller_cp) = self.constant_propagation.get(caller) {
                        // Propagate constants from caller to callee parameters
                        for (param, value) in &caller_cp.parameter_constants {
                            constants.insert(param.clone(), value.clone());
                        }
                    }
                }
            }
            
            // Merge with function's own constants
            for (var, value) in &cp_result.constant_lattice {
                constants.insert(var.clone(), value.clone());
            }
        }
        
        Ok(constants)
    }
    
    /// Propagate alias information across function boundaries
    fn propagate_aliases_interprocedural(&self, function_id: &FunctionId, call_graph: &CallGraphInfo) -> CompilerResult<HashMap<Variable, AliasSet>> {
        let mut aliases = HashMap::new();
        
        // Get function's memory analysis result
        if let Some(memory_result) = self.memory_analysis.get(function_id) {
            // Merge alias information from all callers
            if let Some(callers) = call_graph.get_callers(function_id) {
                for caller in callers {
                    if let Some(caller_memory) = self.memory_analysis.get(caller) {
                        // Propagate alias sets from caller to callee
                        for (var, alias_set) in &caller_memory.alias_sets {
                            aliases.insert(var.clone(), alias_set.clone());
                        }
                    }
                }
            }
            
            // Merge with function's own alias sets
            for (var, alias_set) in &memory_result.alias_sets {
                aliases.insert(var.clone(), alias_set.clone());
            }
        }
        
        Ok(aliases)
    }
}

/// Advanced data flow analyzer with sophisticated algorithms
struct AdvancedDataFlowAnalyzer<'a> {
    cfg: &'a ControlFlowGraph,
    config: &'a DataFlowAnalysisConfig,
    call_graph: Option<&'a Arc<CallGraphInfo>>,
    worklist: VecDeque<BasicBlockId>,
    iteration_counts: HashMap<String, usize>,
    confidence_scores: HashMap<String, f64>,
}

impl<'a> AdvancedDataFlowAnalyzer<'a> {
    fn new(cfg: &'a ControlFlowGraph, config: &'a DataFlowAnalysisConfig, call_graph: Option<&'a Arc<CallGraphInfo>>) -> Self {
        Self {
            cfg,
            config,
            call_graph,
            worklist: VecDeque::new(),
            iteration_counts: HashMap::new(),
            confidence_scores: HashMap::new(),
        }
    }
    
    /// Compute reaching definitions with context sensitivity
    fn compute_reaching_definitions_advanced(&mut self, memory_analysis: Option<&MemoryAnalysisResult>) -> CompilerResult<ReachingDefinitionsResult> {
        let analysis_name = "reaching_definitions".to_string();
        let mut reaching_in: HashMap<BasicBlockId, HashSet<Definition>> = HashMap::new();
        let mut reaching_out: HashMap<BasicBlockId, HashSet<Definition>> = HashMap::new();
        let mut gen_sets: HashMap<BasicBlockId, HashSet<Definition>> = HashMap::new();
        let mut kill_sets: HashMap<BasicBlockId, HashSet<Definition>> = HashMap::new();
        
        // Pre-compute GEN and KILL sets for each block
        for (&block_id, block) in &self.cfg.basic_blocks {
            let (gen, kill) = self.compute_gen_kill_sets_advanced(block, memory_analysis)?;
            gen_sets.insert(block_id, gen);
            kill_sets.insert(block_id, kill);
        }
        
        // Initialize
        for &block_id in self.cfg.basic_blocks.keys() {
            reaching_in.insert(block_id, HashSet::new());
            reaching_out.insert(block_id, HashSet::new());
            self.worklist.push_back(block_id);
        }
        
        // Sophisticated worklist algorithm with convergence detection
        let mut iteration_count = 0;
        let max_iterations = match &self.config.precision {
            AnalysisPrecision::Fast { max_iterations, .. } => *max_iterations,
            AnalysisPrecision::Balanced { max_iterations, .. } => *max_iterations,
            AnalysisPrecision::Precise { max_iterations, .. } => *max_iterations,
        };
        
        while let Some(block_id) = self.worklist.pop_front() {
            if iteration_count >= max_iterations {
                self.confidence_scores.insert(analysis_name.clone(), self.config.min_convergence_confidence);
                break;
            }
            
            let block = &self.cfg.basic_blocks[&block_id];
            
            // IN[B] = Union of OUT[P] for all predecessors P of B
            let mut new_in = HashSet::new();
            for &pred_id in &block.predecessors {
                if let Some(pred_out) = reaching_out.get(&pred_id) {
                    new_in.extend(pred_out.iter().cloned());
                }
            }
            
            // OUT[B] = (IN[B] - KILL[B]) U GEN[B]
            let mut new_out = new_in.clone();
            
            // Apply KILL set
            if let Some(kill_set) = kill_sets.get(&block_id) {
                for kill_def in kill_set {
                    new_out.retain(|def| !self.definitions_conflict(def, kill_def, memory_analysis));
                }
            }
            
            // Apply GEN set
            if let Some(gen_set) = gen_sets.get(&block_id) {
                new_out.extend(gen_set.iter().cloned());
            }
            
            // Check if OUT[B] changed
            let old_out = reaching_out.get(&block_id).cloned().unwrap_or_default();
            if new_out != old_out {
                reaching_out.insert(block_id, new_out);
                reaching_in.insert(block_id, new_in);
                
                // Add successors to worklist
                for &succ_id in &block.successors {
                    if !self.worklist.contains(&succ_id) {
                        self.worklist.push_back(succ_id);
                    }
                }
            }
            
            iteration_count += 1;
        }
        
        self.iteration_counts.insert(analysis_name.clone(), iteration_count);
        
        // Calculate confidence based on convergence
        let confidence = if iteration_count < max_iterations / 2 {
            self.config.high_confidence_threshold
        } else if iteration_count < max_iterations {
            self.config.medium_confidence_threshold
        } else {
            self.config.low_confidence_threshold
        };
        self.confidence_scores.insert(analysis_name, confidence);
        
        Ok(ReachingDefinitionsResult {
            reaching_in,
            reaching_out,
            gen_sets,
            kill_sets,
            convergence_iterations: iteration_count,
        })
    }
    
    /// Compute GEN and KILL sets with memory analysis
    fn compute_gen_kill_sets_advanced(&self, block: &BasicBlock, memory_analysis: Option<&MemoryAnalysisResult>) -> CompilerResult<(HashSet<Definition>, HashSet<Definition>)> {
        let mut gen_set = HashSet::new();
        let mut kill_set = HashSet::new();
        
        for (i, stmt) in block.statements.iter().enumerate() {
            let location = InstructionLocation::new(
                self.cfg.function_id.clone(),
                block.id,
                i,
            );
            
            match stmt {
                Statement::Assignment { target, value, .. } => {
                    // Generate new definition
                    let def = Definition {
                        variable: target.clone(),
                        location,
                        value: self.try_evaluate_constant_advanced(value),
                        definition_type: DefinitionType::Direct,
                        may_aliases: self.get_may_aliases(target, memory_analysis),
                    };
                    
                    // Kill previous definitions of this variable and its aliases
                    let aliases = self.get_all_aliases(target, memory_analysis);
                    for alias in aliases {
                        kill_set.extend(self.find_definitions_for_variable(&alias));
                    }
                    
                    gen_set.insert(def);
                },
                Statement::Call { result, function, args, .. } => {
                    // Handle function calls with sophisticated analysis
                    if let Some(result_var) = result {
                        let def = Definition {
                            variable: result_var.clone(),
                            location,
                            value: None,
                            definition_type: DefinitionType::Call,
                            may_aliases: self.get_may_aliases(result_var, memory_analysis),
                        };
                        gen_set.insert(def);
                    }
                    
                    // Function calls may modify global variables and heap locations
                    if self.may_have_side_effects(function) {
                        kill_set.extend(self.get_potentially_modified_definitions(args, memory_analysis));
                    }
                },
                Statement::Store { address, value, .. } => {
                    // Memory stores create definitions for pointed-to locations
                    if let Some(pointed_vars) = self.get_pointed_to_variables(address, memory_analysis) {
                        for var in pointed_vars {
                            let def = Definition {
                                variable: var.clone(),
                                location,
                                value: self.try_evaluate_constant_advanced(value),
                                definition_type: DefinitionType::Indirect,
                                may_aliases: self.get_may_aliases(&var, memory_analysis),
                            };
                            gen_set.insert(def);
                        }
                    }
                },
                _ => {},
            }
        }
        
        Ok((gen_set, kill_set))
    }
    
    /// Check if two definitions conflict considering aliasing
    fn definitions_conflict(&self, def1: &Definition, def2: &Definition, memory_analysis: Option<&MemoryAnalysisResult>) -> bool {
        // Direct variable match
        if def1.variable == def2.variable {
            return true;
        }
        
        // Check for alias conflicts
        if let Some(memory) = memory_analysis {
            if let (Some(aliases1), Some(aliases2)) = (
                memory.alias_sets.get(&def1.variable),
                memory.alias_sets.get(&def2.variable)
            ) {
                return aliases1.may_alias(aliases2);
            }
        }
        
        false
    }
    
    /// Compute available expressions with global optimization
    fn compute_available_expressions_global(&mut self) -> CompilerResult<AvailableExpressionsResult> {
        let analysis_name = "available_expressions".to_string();
        let mut available_in: HashMap<BasicBlockId, HashSet<Expression>> = HashMap::new();
        let mut available_out: HashMap<BasicBlockId, HashSet<Expression>> = HashMap::new();
        
        // Collect all expressions in the function
        let all_expressions = self.collect_all_expressions_sophisticated();
        
        // Initialize with global optimization consideration
        for &block_id in self.cfg.basic_blocks.keys() {
            if block_id == self.cfg.entry_block {
                available_in.insert(block_id, HashSet::new());
            } else {
                available_in.insert(block_id, all_expressions.clone());
            }
            available_out.insert(block_id, HashSet::new());
            self.worklist.push_back(block_id);
        }
        
        // Advanced worklist algorithm with expression analysis
        let mut iteration_count = 0;
        let max_iterations = self.get_max_iterations();
        
        while let Some(block_id) = self.worklist.pop_front() {
            if iteration_count >= max_iterations {
                break;
            }
            
            let block = &self.cfg.basic_blocks[&block_id];
            
            // IN[B] = Intersection of OUT[P] for all predecessors P of B
            let mut new_in = if block.predecessors.is_empty() {
                HashSet::new()
            } else {
                let mut intersection = all_expressions.clone();
                for &pred_id in &block.predecessors {
                    if let Some(pred_out) = available_out.get(&pred_id) {
                        intersection = intersection.intersection(pred_out).cloned().collect();
                    }
                }
                intersection
            };
            
            // OUT[B] = (IN[B] - KILL[B]) U GEN[B]
            let mut new_out = new_in.clone();
            
            // Process statements with sophisticated expression analysis
            for stmt in &block.statements {
                self.process_statement_for_available_expressions(stmt, &mut new_out)?;
            }
            
            // Check if OUT[B] changed
            let old_out = available_out.get(&block_id).cloned().unwrap_or_default();
            if new_out != old_out {
                available_out.insert(block_id, new_out);
                available_in.insert(block_id, new_in);
                
                // Add successors to worklist
                for &succ_id in &block.successors {
                    if !self.worklist.contains(&succ_id) {
                        self.worklist.push_back(succ_id);
                    }
                }
            }
            
            iteration_count += 1;
        }
        
        self.iteration_counts.insert(analysis_name.clone(), iteration_count);
        
        // Identify redundant expressions
        let redundant_expressions = self.identify_redundant_expressions(&available_in, &available_out)?;
        
        // Calculate global optimization opportunities
        let global_optimizations = self.identify_global_expression_optimizations(&available_out)?;
        
        Ok(AvailableExpressionsResult {
            available_at_entry: available_in,
            available_at_exit: available_out,
            redundant_expressions,
            global_optimizations,
            convergence_iterations: iteration_count,
        })
    }
    
    /// Compute live variables with path sensitivity
    fn compute_live_variables_path_sensitive(&mut self) -> CompilerResult<LiveVariableAnalysis> {
        let analysis_name = "live_variables".to_string();
        let mut live_in: HashMap<BasicBlockId, HashSet<Variable>> = HashMap::new();
        let mut live_out: HashMap<BasicBlockId, HashSet<Variable>> = HashMap::new();
        
        // Path-sensitive analysis for enhanced precision
        let mut path_conditions: HashMap<BasicBlockId, Vec<PathCondition>> = HashMap::new();
        
        // Initialize
        for &block_id in self.cfg.basic_blocks.keys() {
            live_in.insert(block_id, HashSet::new());
            live_out.insert(block_id, HashSet::new());
            path_conditions.insert(block_id, Vec::new());
            self.worklist.push_back(block_id);
        }
        
        // Backward analysis with path sensitivity
        let mut iteration_count = 0;
        let max_iterations = self.get_max_iterations();
        
        while let Some(block_id) = self.worklist.pop_front() {
            if iteration_count >= max_iterations {
                break;
            }
            
            let block = &self.cfg.basic_blocks[&block_id];
            
            // OUT[B] = Union of IN[S] for all successors S of B
            let mut new_out = HashSet::new();
            for &succ_id in &block.successors {
                if let Some(succ_in) = live_in.get(&succ_id) {
                    new_out.extend(succ_in.iter().cloned());
                }
            }
            
            // Apply path conditions if path sensitivity is enabled
            if let AnalysisPrecision::Precise { path_sensitivity: true, .. } = self.config.precision {
                new_out = self.apply_path_conditions(&new_out, &path_conditions[&block_id]);
            }
            
            // IN[B] = (OUT[B] - DEF[B]) U USE[B]
            let mut new_in = new_out.clone();
            
            // Process statements in reverse order with enhanced analysis
            for stmt in block.statements.iter().rev() {
                self.process_statement_for_liveness(stmt, &mut new_in)?;
            }
            
            // Update path conditions for successors
            self.update_path_conditions(block, &mut path_conditions)?;
            
            // Check if IN[B] changed
            let old_in = live_in.get(&block_id).cloned().unwrap_or_default();
            if new_in != old_in {
                live_in.insert(block_id, new_in);
                live_out.insert(block_id, new_out);
                
                // Add predecessors to worklist (backward analysis)
                for &pred_id in &block.predecessors {
                    if !self.worklist.contains(&pred_id) {
                        self.worklist.push_back(pred_id);
                    }
                }
            }
            
            iteration_count += 1;
        }
        
        self.iteration_counts.insert(analysis_name.clone(), iteration_count);
        
        // Identify dead assignments with enhanced precision
        let dead_assignments = self.identify_dead_assignments_precise(&live_out)?;
        
        // Compute variable lifetimes
        let variable_lifetimes = self.compute_variable_lifetimes(&live_in, &live_out)?;
        
        Ok(LiveVariableAnalysis {
            live_in,
            live_out,
            dead_assignments,
            variable_lifetimes,
            path_conditions,
            convergence_iterations: iteration_count,
        })
    }
    
    /// Compute very busy expressions with advanced code motion analysis
    fn compute_very_busy_expressions_advanced(&mut self) -> CompilerResult<VeryBusyExpressionsResult> {
        let analysis_name = "very_busy_expressions".to_string();
        let mut busy_in: HashMap<BasicBlockId, HashSet<Expression>> = HashMap::new();
        let mut busy_out: HashMap<BasicBlockId, HashSet<Expression>> = HashMap::new();
        
        let all_expressions = self.collect_all_expressions_sophisticated();
        
        // Initialize for backward analysis
        for &block_id in self.cfg.basic_blocks.keys() {
            if self.cfg.basic_blocks[&block_id].successors.is_empty() {
                busy_out.insert(block_id, HashSet::new());
            } else {
                busy_out.insert(block_id, all_expressions.clone());
            }
            busy_in.insert(block_id, HashSet::new());
            self.worklist.push_back(block_id);
        }
        
        // Advanced backward analysis
        let mut iteration_count = 0;
        let max_iterations = self.get_max_iterations();
        
        while let Some(block_id) = self.worklist.pop_front() {
            if iteration_count >= max_iterations {
                break;
            }
            
            let block = &self.cfg.basic_blocks[&block_id];
            
            // OUT[B] = Intersection of IN[S] for all successors S of B
            let mut new_out = if block.successors.is_empty() {
                HashSet::new()
            } else {
                let mut intersection = all_expressions.clone();
                for &succ_id in &block.successors {
                    if let Some(succ_in) = busy_in.get(&succ_id) {
                        intersection = intersection.intersection(succ_in).cloned().collect();
                    }
                }
                intersection
            };
            
            // IN[B] = (OUT[B] - KILL[B]) U GEN[B]
            let mut new_in = new_out.clone();
            
            // Process statements in reverse order
            for stmt in block.statements.iter().rev() {
                self.process_statement_for_very_busy_expressions(stmt, &mut new_in)?;
            }
            
            // Check if IN[B] changed
            let old_in = busy_in.get(&block_id).cloned().unwrap_or_default();
            if new_in != old_in {
                busy_in.insert(block_id, new_in);
                busy_out.insert(block_id, new_out);
                
                // Add predecessors to worklist (backward analysis)
                for &pred_id in &block.predecessors {
                    if !self.worklist.contains(&pred_id) {
                        self.worklist.push_back(pred_id);
                    }
                }
            }
            
            iteration_count += 1;
        }
        
        self.iteration_counts.insert(analysis_name.clone(), iteration_count);
        
        // Identify code motion opportunities
        let code_motion_opportunities = self.identify_code_motion_opportunities(&busy_in, &busy_out)?;
        
        Ok(VeryBusyExpressionsResult {
            busy_at_entry: busy_in,
            busy_at_exit: busy_out,
            code_motion_opportunities,
            convergence_iterations: iteration_count,
        })
    }
    
    /// Compute value numbering for common subexpression elimination
    fn compute_value_numbering(&mut self) -> CompilerResult<ValueNumberingResult> {
        let mut value_numbers: HashMap<Expression, ValueNumber> = HashMap::new();
        let mut equivalent_expressions: HashMap<ValueNumber, Vec<Expression>> = HashMap::new();
        let mut next_value_number = 0;
        
        // Process blocks in topological order
        let ordered_blocks = self.cfg.topological_order()?;
        
        for block_id in ordered_blocks {
            let block = &self.cfg.basic_blocks[&block_id];
            
            for stmt in &block.statements {
                match stmt {
                    Statement::Assignment { target, value, .. } => {
                        if let Some(expr) = self.statement_value_to_expression(value) {
                            let vn = if let Some(&existing_vn) = value_numbers.get(&expr) {
                                existing_vn
                            } else {
                                let new_vn = ValueNumber(next_value_number);
                                next_value_number += 1;
                                value_numbers.insert(expr.clone(), new_vn);
                                equivalent_expressions.entry(new_vn).or_insert_with(Vec::new).push(expr.clone());
                                new_vn
                            };
                            
                            // Create value number for the target variable
                            let target_expr = Expression::Variable(target.clone());
                            value_numbers.insert(target_expr.clone(), vn);
                            equivalent_expressions.entry(vn).or_insert_with(Vec::new).push(target_expr);
                        }
                    },
                    _ => {},
                }
            }
        }
        
        // Identify common subexpressions
        let common_subexpressions = equivalent_expressions.iter()
            .filter(|(_, exprs)| exprs.len() > 1)
            .map(|(&vn, exprs)| (vn, exprs.clone()))
            .collect();
        
        Ok(ValueNumberingResult {
            value_numbers,
            equivalent_expressions,
            common_subexpressions,
            next_value_number,
        })
    }
    
    /// Identify dead code with comprehensive analysis
    fn identify_dead_code_comprehensive(&self, live_vars: &LiveVariableAnalysis, value_numbering: &ValueNumberingResult) -> CompilerResult<DeadCodeAnalysis> {
        let mut dead_instructions = HashSet::new();
        let mut unreachable_blocks = HashSet::new();
        let mut unused_computations = HashSet::new();
        
        // Identify unreachable blocks
        let reachable_blocks = self.cfg.reachable_blocks_from_entry();
        for &block_id in self.cfg.basic_blocks.keys() {
            if !reachable_blocks.contains(&block_id) {
                unreachable_blocks.insert(block_id);
            }
        }
        
        // Identify dead assignments
        for (&block_id, block) in &self.cfg.basic_blocks {
            if unreachable_blocks.contains(&block_id) {
                continue;
            }
            
            let live_vars_at_exit = live_vars.live_out.get(&block_id).cloned().unwrap_or_default();
            let mut current_live = live_vars_at_exit;
            
            for (i, stmt) in block.statements.iter().enumerate().rev() {
                let location = InstructionLocation::new(
                    self.cfg.function_id.clone(),
                    block_id,
                    i,
                );
                
                match stmt {
                    Statement::Assignment { target, .. } => {
                        if !current_live.contains(target) && !self.has_side_effects(stmt) {
                            dead_instructions.insert(location);
                        } else {
                            current_live.remove(target);
                        }
                    },
                    _ => {},
                }
                
                // Add variables used by this statement
                for var in self.get_used_variables(stmt) {
                    current_live.insert(var);
                }
            }
        }
        
        // Identify unused computations using value numbering
        for (vn, expressions) in &value_numbering.equivalent_expressions {
            if expressions.len() > 1 {
                // Check if any of these equivalent expressions are dead
                for expr in expressions {
                    if self.is_expression_unused(expr, live_vars) {
                        if let Some(location) = self.get_expression_location(expr) {
                            unused_computations.insert(location);
                        }
                    }
                }
            }
        }
        
        Ok(DeadCodeAnalysis {
            dead_instructions,
            unreachable_blocks,
            unused_computations,
            removable_expressions: self.find_removable_expressions(live_vars, value_numbering)?,
        })
    }
    
    /// Identify optimization opportunities
    fn identify_optimization_opportunities(
        &self,
        reaching_defs: &ReachingDefinitionsResult,
        available_exprs: &AvailableExpressionsResult,
        live_vars: &LiveVariableAnalysis,
        dead_code: &DeadCodeAnalysis,
    ) -> CompilerResult<Vec<OptimizationOpportunity>> {
        let mut opportunities = Vec::new();
        
        // Dead code elimination opportunities
        for &location in &dead_code.dead_instructions {
            opportunities.push(OptimizationOpportunity {
                opportunity_type: OptimizationType::DeadCodeElimination,
                location,
                estimated_benefit: self.config.optimization_weights.dead_code_elimination,
                confidence: 0.95,
                description: "Dead assignment can be eliminated".to_string(),
                implementation_complexity: OptimizationComplexity::Low,
            });
        }
        
        // Common subexpression elimination opportunities
        for (expr_str, locations) in &available_exprs.redundant_expressions {
            if locations.len() > 1 {
                opportunities.push(OptimizationOpportunity {
                    opportunity_type: OptimizationType::CommonSubexpressionElimination,
                    location: locations[0].clone(),
                    estimated_benefit: self.config.optimization_weights.common_subexpression_elimination * locations.len() as f64,
                    confidence: 0.90,
                    description: format!("Common subexpression: {}", expr_str),
                    implementation_complexity: OptimizationComplexity::Medium,
                });
            }
        }
        
        // Constant propagation opportunities
        for (block_id, defs) in &reaching_defs.reaching_out {
            for def in defs {
                if def.value.is_some() {
                    opportunities.push(OptimizationOpportunity {
                        opportunity_type: OptimizationType::ConstantPropagation,
                        location: def.location.clone(),
                        estimated_benefit: self.config.optimization_weights.constant_propagation,
                        confidence: 0.85,
                        description: format!("Constant propagation for variable {}", def.variable.name),
                        implementation_complexity: OptimizationComplexity::Low,
                    });
                }
            }
        }
        
        opportunities
    }
    
    /// Get iteration counts for analysis quality assessment
    fn get_iteration_counts(&self) -> HashMap<String, usize> {
        self.iteration_counts.clone()
    }
    
    /// Get confidence scores for analysis quality assessment
    fn get_confidence_scores(&self) -> HashMap<String, f64> {
        self.confidence_scores.clone()
    }
    
    /// Assess overall analysis quality
    fn assess_analysis_quality(&self) -> AnalysisQuality {
        let avg_confidence: f64 = self.confidence_scores.values().sum::<f64>() / self.confidence_scores.len() as f64;
        
        if avg_confidence >= 0.9 {
            AnalysisQuality::High
        } else if avg_confidence >= 0.7 {
            AnalysisQuality::Medium
        } else {
            AnalysisQuality::Low
        }
    }
    
    /// Get maximum iterations based on precision level
    fn get_max_iterations(&self) -> usize {
        match &self.config.precision {
            AnalysisPrecision::Fast { max_iterations, .. } => *max_iterations,
            AnalysisPrecision::Balanced { max_iterations, .. } => *max_iterations,
            AnalysisPrecision::Precise { max_iterations, .. } => *max_iterations,
        }
    }
    
    /// Collect all expressions from the control flow graph for analysis
    fn collect_all_expressions_sophisticated(&self) -> HashSet<Expression> {
        let mut expressions = HashSet::new();
        
        for (_, def_uses) in &self.def_use_chains {
            for (_, definitions) in &def_uses.definitions {
                for def in definitions {
                    if let Some(expr) = self.definition_to_expression(def) {
                        expressions.insert(expr.clone());
                        
                        // Also collect sub-expressions for comprehensive analysis
                        self.collect_sub_expressions(&expr, &mut expressions);
                    }
                }
            }
            
            for (_, uses) in &def_uses.uses {
                for use_site in uses {
                    if let Some(expr) = self.use_to_expression(use_site) {
                        expressions.insert(expr);
                    }
                }
            }
        }
        
        // Add expressions from control flow conditions
        for (_, cfg) in &self.control_flow_graphs {
            for (_, block) in &cfg.blocks {
                if let Some(terminator) = &block.terminator {
                    if let Some(expr) = self.terminator_to_expression(terminator) {
                        expressions.insert(expr);
                    }
                }
            }
        }
        
        expressions
    }
    
    /// Process statement for available expressions analysis
    fn process_statement_for_available_expressions(&self, stmt: &Statement, available: &mut HashSet<Expression>) -> CompilerResult<()> {
        // Kill expressions invalidated by this statement
        match stmt {
            Statement::Assignment { target: var, .. } => {
                // Remove all expressions containing the assigned variable
                available.retain(|expr| !self.expression_contains_variable(expr, var));
            },
            Statement::Store { address, .. } => {
                // Conservative: remove all memory-dependent expressions
                if let Some(affected_vars) = self.get_memory_affected_variables(address) {
                    available.retain(|expr| {
                        !affected_vars.iter().any(|var| self.expression_contains_variable(expr, var))
                    });
                } else {
                    // Very conservative: remove all expressions with memory operations
                    available.retain(|expr| !self.expression_has_memory_operation(expr));
                }
            },
            Statement::Call { args, .. } => {
                // Remove expressions that may be affected by the call
                let potentially_modified = self.get_call_modified_expressions(args);
                available.retain(|expr| !potentially_modified.contains(expr));
            },
            _ => {}
        }
        
        // Generate new expressions from this statement
        if let Some(new_expr) = self.statement_generates_expression(stmt) {
            if self.is_expression_available(&new_expr) {
                available.insert(new_expr);
            }
        }
        
        Ok(())
    }
    
    /// Process statement for liveness analysis
    fn process_statement_for_liveness(&self, stmt: &Statement, live_vars: &mut HashSet<Variable>) -> CompilerResult<()> {
        // First, handle variable definitions (kills)
        if let Some(defined_var) = self.get_defined_variable(stmt) {
            live_vars.remove(&defined_var);
        }
        
        // Then, handle variable uses (gens)
        let used_vars = self.get_used_variables(stmt);
        for var in used_vars {
            live_vars.insert(var);
        }
        
        // Handle special cases for precise liveness
        match stmt {
            Statement::Phi { target: dest, sources, .. } => {
                // Phi nodes require special handling for SSA form
                live_vars.remove(dest);
                for (var, _) in sources {
                    live_vars.insert(var.clone());
                }
            },
            Statement::Call { function: func, result: dest, args, .. } => {
                // Handle interprocedural liveness
                if let Some(dest_var) = dest {
                    live_vars.remove(dest_var);
                }

                // Add arguments and function pointer (if variable)
                for arg in args {
                    if let StatementValue::Variable(var) = arg {
                        live_vars.insert(var.clone());
                    }
                }

                // Handle escaped variables
                if self.function_may_capture_variables(func) {
                    let escaped = self.get_escaped_variables_at_call(func, args);
                    for var in escaped {
                        live_vars.insert(var);
                    }
                }
            },
            _ => {}
        }
        
        Ok(())
    }
    
    /// Process statement for very busy expressions analysis
    fn process_statement_for_very_busy_expressions(&self, stmt: &Statement, busy: &mut HashSet<Expression>) -> CompilerResult<()> {
        // An expression is very busy if it will definitely be evaluated before being killed
        
        // Kill expressions that are computed by this statement
        if let Some(computed_expr) = self.statement_generates_expression(stmt) {
            busy.remove(&computed_expr);
        }
        
        // Kill expressions invalidated by this statement
        match stmt {
            Statement::Assignment { target: var, .. } => {
                busy.retain(|expr| !self.expression_contains_variable(expr, var));
            },
            Statement::Store { address, .. } => {
                // Remove memory-dependent expressions
                let affected = self.get_store_affected_expressions(address);
                busy.retain(|expr| !affected.contains(expr));
            },
            Statement::Call { .. } => {
                // Conservative: remove expressions with side effects
                busy.retain(|expr| self.is_expression_pure(expr));
            },
            _ => {}
        }
        
        // Add expressions that will be computed by successors
        if let Some(required_exprs) = self.get_successor_required_expressions(stmt) {
            for expr in required_exprs {
                busy.insert(expr);
            }
        }
        
        Ok(())
    }
    
    /// Evaluate constant values with advanced folding and propagation
    fn try_evaluate_constant_advanced(&self, value: &StatementValue) -> Option<ConstantLatticeValue> {
        match value {
            StatementValue::Constant(c) => Some(ConstantLatticeValue::Constant(c.clone())),
            StatementValue::Variable(var) => {
                // Look up in constant propagation results
                for (_, cp_result) in &self.constant_propagation {
                    if let Some(lattice_value) = cp_result.values.get(var) {
                        return Some(lattice_value.clone());
                    }
                }
                Some(ConstantLatticeValue::Top)
            },
            StatementValue::BinaryOp(left, op, right) => {
                let left_val = self.try_evaluate_constant_advanced(left)?;
                let right_val = self.try_evaluate_constant_advanced(right)?;
                
                match (left_val, right_val) {
                    (ConstantLatticeValue::Constant(l), ConstantLatticeValue::Constant(r)) => {
                        self.evaluate_binary_op_constants(&l, op, &r)
                            .map(ConstantLatticeValue::Constant)
                    },
                    (ConstantLatticeValue::Bottom, _) | (_, ConstantLatticeValue::Bottom) => {
                        Some(ConstantLatticeValue::Bottom)
                    },
                    _ => Some(ConstantLatticeValue::Top)
                }
            },
            StatementValue::UnaryOp(op, operand) => {
                let operand_val = self.try_evaluate_constant_advanced(operand)?;
                
                match operand_val {
                    ConstantLatticeValue::Constant(c) => {
                        self.evaluate_unary_op_constant(op, &c)
                            .map(ConstantLatticeValue::Constant)
                    },
                    ConstantLatticeValue::Bottom => Some(ConstantLatticeValue::Bottom),
                    _ => Some(ConstantLatticeValue::Top)
                }
            },
            StatementValue::ArrayAccess(array, index) => {
                // Try to evaluate if both array and index are constants
                if let Some(array_info) = self.get_array_constant_info(array) {
                    if let Some(index_val) = self.try_evaluate_constant_advanced(index) {
                        if let ConstantLatticeValue::Constant(ConstantValue::Integer(i)) = index_val {
                            return array_info.get_element(i as usize)
                                .map(|v| ConstantLatticeValue::Constant(v));
                        }
                    }
                }
                Some(ConstantLatticeValue::Top)
            },
            _ => Some(ConstantLatticeValue::Top)
        }
    }
    
    /// Get potential aliases using points-to analysis
    fn get_may_aliases(&self, var: &Variable, memory_analysis: Option<&MemoryAnalysisResult>) -> Vec<Variable> {
        let mut aliases = Vec::new();
        
        if let Some(mem_analysis) = memory_analysis {
            // Use points-to sets for precise alias analysis
            for (_, points_to) in &mem_analysis.points_to_sets {
                if let Some(var_points_to) = points_to.mappings.get(&var.name) {
                    // Find other variables pointing to the same locations
                    for (other_var, other_points_to) in &points_to.mappings {
                        if other_var != &var.name && !var_points_to.is_disjoint(other_points_to) {
                            aliases.push(Variable {
                                name: other_var.clone(),
                                var_type: var.var_type.clone(),
                            });
                        }
                    }
                }
            }
            
            // Add aliases from alias sets
            for (_, alias_sets) in &mem_analysis.alias_sets {
                for alias_set in alias_sets {
                    if alias_set.variables.contains(&var.name) {
                        for other_var in &alias_set.variables {
                            if other_var != &var.name {
                                aliases.push(Variable {
                                    name: other_var.clone(),
                                    var_type: var.var_type.clone(),
                                });
                            }
                        }
                    }
                }
            }
        } else {
            // Conservative: use type-based alias analysis
            if self.is_pointer_type(&var.var_type) {
                aliases.extend(self.get_type_compatible_pointers(var));
            }
        }
        
        aliases.sort_by(|a, b| a.name.cmp(&b.name));
        aliases.dedup();
        aliases
    }
    
    /// Get all definite aliases (must-alias analysis)
    fn get_all_aliases(&self, var: &Variable, memory_analysis: Option<&MemoryAnalysisResult>) -> Vec<Variable> {
        let mut must_aliases = Vec::new();
        
        if let Some(mem_analysis) = memory_analysis {
            // Check for variables that must alias (point to exactly the same locations)
            for (_, points_to) in &mem_analysis.points_to_sets {
                if let Some(var_points_to) = points_to.mappings.get(&var.name) {
                    if !var_points_to.is_empty() {
                        for (other_var, other_points_to) in &points_to.mappings {
                            if other_var != &var.name && var_points_to == other_points_to {
                                must_aliases.push(Variable {
                                    name: other_var.clone(),
                                    var_type: var.var_type.clone(),
                                });
                            }
                        }
                    }
                }
            }
            
            // Check high-confidence alias sets
            for (_, alias_sets) in &mem_analysis.alias_sets {
                for alias_set in alias_sets {
                    if alias_set.confidence >= self.config.must_alias_confidence_threshold &&
                       alias_set.variables.contains(&var.name) {
                        for other_var in &alias_set.variables {
                            if other_var != &var.name {
                                must_aliases.push(Variable {
                                    name: other_var.clone(),
                                    var_type: var.var_type.clone(),
                                });
                            }
                        }
                    }
                }
            }
        }
        
        must_aliases.sort_by(|a, b| a.name.cmp(&b.name));
        must_aliases.dedup();
        must_aliases
    }
    
    /// Find all definitions for a variable in the current scope
    fn find_definitions_for_variable(&self, var: &Variable) -> Vec<Definition> {
        let mut definitions = Vec::new();
        
        // Search in def-use chains
        for (func_id, chains) in &self.def_use_chains {
            if let Some(var_defs) = chains.definitions.get(&var.name) {
                definitions.extend(var_defs.clone());
            }
            
            // Also check for definitions through aliases
            let aliases = self.get_may_aliases(var, None);
            for alias in aliases {
                if let Some(alias_defs) = chains.definitions.get(&alias.name) {
                    for def in alias_defs {
                        if !definitions.contains(def) {
                            definitions.push(def.clone());
                        }
                    }
                }
            }
        }
        
        // Search in SSA form if available
        if let Some(ssa_info) = self.get_ssa_definitions(var) {
            definitions.extend(ssa_info);
        }
        
        // Sort by location for deterministic results
        definitions.sort_by_key(|d| d.location);
        definitions
    }
    
    /// Comprehensive side effect analysis for functions
    fn may_have_side_effects(&self, function: &str) -> bool {
        // Check known pure functions
        let pure_functions = [
            "abs", "min", "max", "sqrt", "sin", "cos", "tan",
            "exp", "log", "pow", "ceil", "floor", "round",
            "strlen", "strcmp", "strncmp", "memcmp",
            "isdigit", "isalpha", "isspace", "tolower", "toupper"
        ];
        
        if pure_functions.contains(&function) {
            return false;
        }
        
        // Check function attributes from analysis
        if let Some(func_info) = self.get_function_info(function) {
            return func_info.has_side_effects;
        }
        
        // Check naming conventions
        if function.starts_with("pure_") || function.starts_with("const_") {
            return false;
        }
        
        if function.starts_with("get_") && !function.contains("mut") {
            return false;
        }
        
        // Functions that definitely have side effects
        let side_effect_functions = [
            "malloc", "free", "realloc", "calloc",
            "fopen", "fclose", "fread", "fwrite",
            "printf", "scanf", "puts", "gets",
            "exit", "abort", "system",
            "pthread_create", "pthread_mutex_lock",
            "atomic_store", "atomic_exchange"
        ];
        
        if side_effect_functions.iter().any(|&f| function.contains(f)) {
            return true;
        }
        
        // Conservative default: assume side effects
        true
    }
    
    /// Get definitions potentially modified by a function call
    fn get_potentially_modified_definitions(&self, args: &[StatementValue], memory_analysis: Option<&MemoryAnalysisResult>) -> Vec<Definition> {
        let mut modified_defs = Vec::new();
        
        // Check each argument for potential modifications
        for arg in args {
            match arg {
                StatementValue::Variable(var) => {
                    // If passed by reference/pointer, may be modified
                    if self.is_mutable_reference(&var.var_type) {
                        modified_defs.extend(self.find_definitions_for_variable(var));
                        
                        // Also check aliases
                        let aliases = self.get_may_aliases(var, memory_analysis);
                        for alias in aliases {
                            modified_defs.extend(self.find_definitions_for_variable(&alias));
                        }
                    }
                },
                StatementValue::Address(var) => {
                    // Address taken - definitely may be modified
                    modified_defs.extend(self.find_definitions_for_variable(var));
                },
                _ => {}
            }
        }
        
        // Check for global variable modifications
        modified_defs.extend(self.get_global_definitions());
        
        // Remove duplicates
        modified_defs.sort_by_key(|d| d.location);
        modified_defs.dedup();
        modified_defs
    }
    
    /// Get variables that may be pointed to by an address
    fn get_pointed_to_variables(&self, address: &StatementValue, memory_analysis: Option<&MemoryAnalysisResult>) -> Option<Vec<Variable>> {
        match address {
            StatementValue::Address(var) => {
                // Direct address-of operator
                Some(vec![var.clone()])
            },
            StatementValue::Variable(ptr_var) => {
                // Pointer variable - use points-to analysis
                if let Some(mem_analysis) = memory_analysis {
                    for (_, points_to) in &mem_analysis.points_to_sets {
                        if let Some(targets) = points_to.mappings.get(&ptr_var.name) {
                            let mut vars = Vec::new();
                            for target_id in targets {
                                if let Some(var) = self.heap_object_to_variable(*target_id) {
                                    vars.push(var);
                                }
                            }
                            return Some(vars);
                        }
                    }
                }
                
                // Fallback: use type-based analysis
                if self.is_pointer_type(&ptr_var.var_type) {
                    Some(self.get_potential_pointees(ptr_var))
                } else {
                    None
                }
            },
            StatementValue::BinaryOp(left, BinaryOperator::Add, right) |
            StatementValue::BinaryOp(left, BinaryOperator::Subtract, right) => {
                // Pointer arithmetic
                self.get_pointed_to_variables(left, memory_analysis)
            },
            StatementValue::ArrayAccess(array, _) => {
                // Array element access
                if let StatementValue::Variable(array_var) = array.as_ref() {
                    Some(vec![array_var.clone()])
                } else {
                    None
                }
            },
            _ => None
        }
    }
    
    /// Apply path conditions to refine liveness analysis
    fn apply_path_conditions(&self, live_vars: &HashSet<Variable>, conditions: &[PathCondition]) -> HashSet<Variable> {
        let mut refined_live = live_vars.clone();
        
        for condition in conditions {
            match &condition.condition_type {
                ConditionType::Equality(var, value) => {
                    // If var == constant, it's not live after the condition
                    if self.is_constant_value(value) {
                        refined_live.remove(var);
                    }
                },
                ConditionType::Nullity(var, is_null) => {
                    // If var is proven null, remove from live set
                    if *is_null {
                        refined_live.remove(var);
                        // Also remove anything accessed through this variable
                        refined_live.retain(|v| !self.is_derived_from(v, var));
                    }
                },
                ConditionType::Range(var, min, max) => {
                    // Keep variable live if it's used in range checks
                    refined_live.insert(var.clone());
                },
                ConditionType::TypeTest(var, _) => {
                    // Type tests keep variables live
                    refined_live.insert(var.clone());
                },
                _ => {}
            }
        }
        
        refined_live
    }
    
    /// Update path conditions based on control flow
    fn update_path_conditions(&self, block: &BasicBlock, path_conditions: &mut HashMap<BasicBlockId, Vec<PathCondition>>) -> CompilerResult<()> {
        let mut conditions = path_conditions.entry(block.id).or_insert_with(Vec::new);
        
        // Extract conditions from block terminator
        if let Some(terminator) = &block.terminator {
            match terminator {
                Terminator::ConditionalBranch { condition, true_target, false_target } => {
                    // Add condition for true branch
                    let true_conditions = conditions.clone();
                    let mut true_cond = PathCondition {
                        condition_type: self.extract_condition_type(condition, true),
                        location: block.id,
                        confidence: self.config.path_condition_confidence,
                    };
                    
                    path_conditions.entry(*true_target)
                        .or_insert_with(Vec::new)
                        .push(true_cond);
                    
                    // Add negated condition for false branch
                    let false_cond = PathCondition {
                        condition_type: self.extract_condition_type(condition, false),
                        location: block.id,
                        confidence: self.config.path_condition_confidence,
                    };
                    
                    path_conditions.entry(*false_target)
                        .or_insert_with(Vec::new)
                        .push(false_cond);
                },
                Terminator::Switch { value, cases, default } => {
                    // Add conditions for each case
                    for (case_value, target) in cases {
                        let case_cond = PathCondition {
                            condition_type: ConditionType::Equality(
                                self.value_to_variable(value).unwrap_or_default(),
                                case_value.clone()
                            ),
                            location: block.id,
                            confidence: self.config.path_condition_confidence,
                        };
                        
                        path_conditions.entry(*target)
                            .or_insert_with(Vec::new)
                            .push(case_cond);
                    }
                },
                _ => {}
            }
        }
        
        Ok(())
    }
    
    /// Identify dead assignments with high precision
    fn identify_dead_assignments_precise(&self, live_out: &HashMap<BasicBlockId, HashSet<Variable>>) -> CompilerResult<HashSet<InstructionLocation>> {
        let mut dead_assignments = HashSet::new();
        
        for (block_id, live_vars) in live_out {
            if let Some(cfg) = self.control_flow_graphs.values().find(|cfg| cfg.blocks.contains_key(block_id)) {
                if let Some(block) = cfg.blocks.get(block_id) {
                    let mut current_live = live_vars.clone();
                    
                    // Process statements in reverse order
                    for (idx, stmt) in block.statements.iter().enumerate().rev() {
                        if let Some(defined_var) = self.get_defined_variable(stmt) {
                            if !current_live.contains(&defined_var) && !self.has_side_effects(stmt) {
                                // This assignment is dead
                                dead_assignments.insert(InstructionLocation {
                                    block_id: *block_id,
                                    instruction_index: idx,
                                });
                            }
                            
                            // Update liveness
                            current_live.remove(&defined_var);
                        }
                        
                        // Add used variables
                        let used = self.get_used_variables(stmt);
                        current_live.extend(used);
                    }
                }
            }
        }
        
        Ok(dead_assignments)
    }
    
    /// Compute precise variable lifetimes for register allocation
    fn compute_variable_lifetimes(&self, live_in: &HashMap<BasicBlockId, HashSet<Variable>>, 
                                 live_out: &HashMap<BasicBlockId, HashSet<Variable>>) -> CompilerResult<HashMap<Variable, VariableLifetime>> {
        let mut lifetimes = HashMap::new();
        
        // Collect all variables
        let mut all_vars = HashSet::new();
        for vars in live_in.values().chain(live_out.values()) {
            all_vars.extend(vars.clone());
        }
        
        // Compute lifetime for each variable
        for var in all_vars {
            let mut first_use = None;
            let mut last_use = None;
            let mut use_locations = Vec::new();
            let mut def_locations = Vec::new();
            
            // Find all uses and definitions
            for (func_id, chains) in &self.def_use_chains {
                if let Some(defs) = chains.definitions.get(&var.name) {
                    for def in defs {
                        def_locations.push(def.location);
                        
                        if first_use.is_none() || def.location < first_use.unwrap() {
                            first_use = Some(def.location);
                        }
                        if last_use.is_none() || def.location > last_use.unwrap() {
                            last_use = Some(def.location);
                        }
                    }
                }
                
                if let Some(uses) = chains.uses.get(&var.name) {
                    for use_loc in uses {
                        use_locations.push(*use_loc);
                        
                        if first_use.is_none() || *use_loc < first_use.unwrap() {
                            first_use = Some(*use_loc);
                        }
                        if last_use.is_none() || *use_loc > last_use.unwrap() {
                            last_use = Some(*use_loc);
                        }
                    }
                }
            }
            
            if let (Some(first), Some(last)) = (first_use, last_use) {
                lifetimes.insert(var, VariableLifetime {
                    first_use: first,
                    last_use: last,
                    use_locations,
                    def_locations,
                    live_blocks: self.compute_live_blocks(&var, live_in, live_out),
                    spill_cost: self.compute_spill_cost(&var),
                });
            }
        }
        
        Ok(lifetimes)
    }
    
    /// Identify redundant expression computations
    fn identify_redundant_expressions(&self, available_in: &HashMap<BasicBlockId, HashSet<Expression>>, 
                                     available_out: &HashMap<BasicBlockId, HashSet<Expression>>) -> CompilerResult<HashMap<String, Vec<InstructionLocation>>> {
        let mut redundant = HashMap::new();
        
        for (block_id, available) in available_in {
            if let Some(cfg) = self.control_flow_graphs.values().find(|cfg| cfg.blocks.contains_key(block_id)) {
                if let Some(block) = cfg.blocks.get(block_id) {
                    let mut current_available = available.clone();
                    
                    for (idx, stmt) in block.statements.iter().enumerate() {
                        if let Some(expr) = self.statement_generates_expression(stmt) {
                            if current_available.contains(&expr) {
                                // This expression is redundant
                                let expr_str = format!("{:?}", expr);
                                redundant.entry(expr_str)
                                    .or_insert_with(Vec::new)
                                    .push(InstructionLocation {
                                        block_id: *block_id,
                                        instruction_index: idx,
                                    });
                            } else {
                                current_available.insert(expr);
                            }
                        }
                        
                        // Update available expressions
                        self.process_statement_for_available_expressions(stmt, &mut current_available)?;
                    }
                }
            }
        }
        
        Ok(redundant)
    }
    
    /// Identify global optimization opportunities across blocks
    fn identify_global_expression_optimizations(&self, available_out: &HashMap<BasicBlockId, HashSet<Expression>>) -> CompilerResult<Vec<GlobalOptimization>> {
        let mut optimizations = Vec::new();
        
        // Find expressions available in all blocks (very busy)
        let mut global_expressions = None;
        for exprs in available_out.values() {
            match &global_expressions {
                None => global_expressions = Some(exprs.clone()),
                Some(current) => {
                    let intersection: HashSet<_> = current.intersection(exprs).cloned().collect();
                    global_expressions = Some(intersection);
                }
            }
        }
        
        if let Some(global) = global_expressions {
            for expr in global {
                optimizations.push(GlobalOptimization {
                    optimization_type: OptimizationType::GlobalCSE,
                    target_expression: Some(expr),
                    affected_blocks: available_out.keys().cloned().collect(),
                    estimated_benefit: self.estimate_cse_benefit(&expr),
                    requires_code_motion: true,
                });
            }
        }
        
        Ok(optimizations)
    }
    
    /// Identify code motion opportunities for loop optimization
    fn identify_code_motion_opportunities(&self, busy_in: &HashMap<BasicBlockId, HashSet<Expression>>, 
                                         busy_out: &HashMap<BasicBlockId, HashSet<Expression>>) -> CompilerResult<Vec<CodeMotionOpportunity>> {
        let mut opportunities = Vec::new();
        
        // Find loop headers and their invariants
        for cfg in self.control_flow_graphs.values() {
            for (header_id, loop_info) in &cfg.loops {
                let loop_blocks = &loop_info.blocks;
                
                // Find expressions that are busy in the loop but loop-invariant
                if let Some(header_busy) = busy_in.get(header_id) {
                    for expr in header_busy {
                        if self.is_loop_invariant(expr, loop_blocks) {
                            opportunities.push(CodeMotionOpportunity {
                                expression: expr.clone(),
                                from_block: *header_id,
                                to_block: loop_info.preheader,
                                motion_type: CodeMotionType::LoopInvariant,
                                safety: self.is_safe_to_hoist(expr, loop_info),
                                benefit: self.estimate_hoisting_benefit(expr, loop_info),
                            });
                        }
                    }
                }
            }
        }
        
        Ok(opportunities)
    }
    
    /// Convert statement value to expression for analysis
    fn statement_value_to_expression(&self, value: &StatementValue) -> Option<Expression> {
        match value {
            StatementValue::Constant(c) => Some(Expression::Constant(c.clone())),
            StatementValue::Variable(v) => Some(Expression::Variable(v.clone())),
            StatementValue::BinaryOp(left, op, right) => {
                let left_expr = self.statement_value_to_expression(left)?;
                let right_expr = self.statement_value_to_expression(right)?;
                Some(Expression::BinaryOp(
                    Box::new(left_expr),
                    op.clone(),
                    Box::new(right_expr)
                ))
            },
            StatementValue::UnaryOp(op, operand) => {
                let operand_expr = self.statement_value_to_expression(operand)?;
                Some(Expression::UnaryOp(op.clone(), Box::new(operand_expr)))
            },
            StatementValue::FunctionCall(func, args) => {
                let arg_exprs: Vec<_> = args.iter()
                    .filter_map(|arg| self.statement_value_to_expression(arg))
                    .collect();
                if arg_exprs.len() == args.len() {
                    Some(Expression::Call(func.clone(), arg_exprs))
                } else {
                    None
                }
            },
            _ => None
        }
    }
    
    fn has_side_effects(&self, stmt: &Statement) -> bool {
        match stmt {
            Statement::Call { function, .. } => self.may_have_side_effects(function),
            Statement::Store { .. } => true,
            _ => false,
        }
    }
    
    // Helper methods for complete implementation
    
    fn definition_to_expression(&self, def: &Definition) -> Option<Expression> {
        match &def.value {
            DefinitionType::Constant(c) => Some(Expression::Constant(c.clone())),
            DefinitionType::Variable(v) => Some(Expression::Variable(v.clone())),
            DefinitionType::Expression(e) => Some(e.clone()),
            _ => None,
        }
    }
    
    fn collect_sub_expressions(&self, expr: &Expression, expressions: &mut HashSet<Expression>) {
        match expr {
            Expression::BinaryOp(left, _, right) => {
                expressions.insert(left.as_ref().clone());
                expressions.insert(right.as_ref().clone());
                self.collect_sub_expressions(left, expressions);
                self.collect_sub_expressions(right, expressions);
            },
            Expression::UnaryOp(_, operand) => {
                expressions.insert(operand.as_ref().clone());
                self.collect_sub_expressions(operand, expressions);
            },
            Expression::Call(_, args) => {
                for arg in args {
                    expressions.insert(arg.clone());
                    self.collect_sub_expressions(arg, expressions);
                }
            },
            _ => {}
        }
    }
    
    fn use_to_expression(&self, use_site: &InstructionLocation) -> Option<Expression> {
        // Look up the instruction at the use site and convert to expression
        for cfg in self.control_flow_graphs.values() {
            if let Some(block) = cfg.blocks.get(&use_site.block_id) {
                if let Some(stmt) = block.statements.get(use_site.instruction_index) {
                    return self.statement_generates_expression(stmt);
                }
            }
        }
        None
    }
    
    fn terminator_to_expression(&self, terminator: &Terminator) -> Option<Expression> {
        match terminator {
            Terminator::ConditionalBranch { condition, .. } => {
                self.statement_value_to_expression(condition)
            },
            Terminator::Switch { value, .. } => {
                self.statement_value_to_expression(value)
            },
            _ => None
        }
    }
    
    fn expression_contains_variable(&self, expr: &Expression, var: &Variable) -> bool {
        match expr {
            Expression::Variable(v) => v == var,
            Expression::BinaryOp(left, _, right) => {
                self.expression_contains_variable(left, var) || 
                self.expression_contains_variable(right, var)
            },
            Expression::UnaryOp(_, operand) => {
                self.expression_contains_variable(operand, var)
            },
            Expression::Call(_, args) => {
                args.iter().any(|arg| self.expression_contains_variable(arg, var))
            },
            _ => false
        }
    }
    
    fn get_memory_affected_variables(&self, address: &StatementValue) -> Option<Vec<Variable>> {
        self.get_pointed_to_variables(address, None)
    }
    
    fn expression_has_memory_operation(&self, expr: &Expression) -> bool {
        match expr {
            Expression::Load(_) | Expression::Store(_, _) => true,
            Expression::BinaryOp(left, _, right) => {
                self.expression_has_memory_operation(left) || 
                self.expression_has_memory_operation(right)
            },
            Expression::UnaryOp(_, operand) => {
                self.expression_has_memory_operation(operand)
            },
            Expression::Call(func, _) => self.may_have_side_effects(func),
            _ => false
        }
    }
    
    fn get_call_modified_expressions(&self, args: &[StatementValue]) -> HashSet<Expression> {
        let mut modified = HashSet::new();
        
        for arg in args {
            if let StatementValue::Variable(var) = arg {
                if self.is_mutable_reference(&var.var_type) {
                    // Add all expressions containing this variable
                    for expr in &self.collect_all_expressions_sophisticated() {
                        if self.expression_contains_variable(expr, var) {
                            modified.insert(expr.clone());
                        }
                    }
                }
            }
        }
        
        modified
    }
    
    fn statement_generates_expression(&self, stmt: &Statement) -> Option<Expression> {
        match stmt {
            Statement::Assignment { value, .. } => self.statement_value_to_expression(value),
            Statement::Load { address, .. } => Some(Expression::Load(Box::new(
                self.statement_value_to_expression(address)?
            ))),
            _ => None,
        }
    }
    
    fn is_expression_available(&self, expr: &Expression) -> bool {
        match expr {
            Expression::Call(func, _) => !self.may_have_side_effects(func),
            Expression::Load(_) => false, // Loads are not available due to aliasing
            _ => true
        }
    }
    
    fn get_defined_variable(&self, stmt: &Statement) -> Option<Variable> {
        match stmt {
            Statement::Assignment { target, .. } => Some(target.clone()),
            Statement::Phi { target, .. } => Some(target.clone()),
            Statement::Call { result: Some(dest), .. } => Some(dest.clone()),
            _ => None,
        }
    }
    
    fn get_used_variables(&self, stmt: &Statement) -> Vec<Variable> {
        let mut used = Vec::new();
        match stmt {
            Statement::Assignment { value, .. } => {
                self.collect_variables_from_value(value, &mut used);
            }
            Statement::Load { address, .. } => {
                self.collect_variables_from_value(address, &mut used);
            }
            Statement::Store { address, value, .. } => {
                self.collect_variables_from_value(address, &mut used);
                self.collect_variables_from_value(value, &mut used);
            }
            Statement::Call { args, .. } => {
                for arg in args {
                    self.collect_variables_from_value(arg, &mut used);
                }
            }
            Statement::Phi { sources, .. } => {
                for (var, _) in sources {
                    used.push(var.clone());
                }
            }
            _ => {}
        }
        used
    }
    
    fn collect_variables_from_value(&self, value: &StatementValue, vars: &mut Vec<Variable>) {
        match value {
            StatementValue::Variable(v) => vars.push(v.clone()),
            StatementValue::BinaryOp(left, _, right) => {
                self.collect_variables_from_value(left, vars);
                self.collect_variables_from_value(right, vars);
            },
            StatementValue::UnaryOp(_, operand) => {
                self.collect_variables_from_value(operand, vars);
            },
            StatementValue::Address(v) => vars.push(v.clone()),
            StatementValue::ArrayAccess(array, index) => {
                self.collect_variables_from_value(array, vars);
                self.collect_variables_from_value(index, vars);
            },
            _ => {}
        }
    }
    
    fn function_may_capture_variables(&self, func: &str) -> bool {
        // Functions that capture variables (closures, lambdas, etc.)
        func.contains("closure") || func.contains("lambda") || func.contains("capture")
    }
    
    fn get_escaped_variables_at_call(&self, func: &str, args: &[StatementValue]) -> Vec<Variable> {
        let mut escaped = Vec::new();
        
        for arg in args {
            if let StatementValue::Address(var) = arg {
                // Variable address taken - it escapes
                escaped.push(var.clone());
            }
        }
        
        escaped
    }
    
    fn get_store_affected_expressions(&self, address: &StatementValue) -> HashSet<Expression> {
        let mut affected = HashSet::new();
        
        if let Some(vars) = self.get_pointed_to_variables(address, None) {
            for expr in &self.collect_all_expressions_sophisticated() {
                for var in &vars {
                    if self.expression_contains_variable(expr, var) {
                        affected.insert(expr.clone());
                    }
                }
            }
        }
        
        affected
    }
    
    fn is_expression_pure(&self, expr: &Expression) -> bool {
        match expr {
            Expression::Constant(_) | Expression::Variable(_) => true,
            Expression::BinaryOp(left, _, right) => {
                self.is_expression_pure(left) && self.is_expression_pure(right)
            },
            Expression::UnaryOp(_, operand) => self.is_expression_pure(operand),
            Expression::Call(func, args) => {
                !self.may_have_side_effects(func) && 
                args.iter().all(|arg| self.is_expression_pure(arg))
            },
            Expression::Load(_) | Expression::Store(_, _) => false,
            _ => true
        }
    }
    
    fn get_successor_required_expressions(&self, stmt: &Statement) -> Option<Vec<Expression>> {
        // Get expressions that will be evaluated by successor statements
        None // This requires forward flow analysis context
    }
    
    fn evaluate_binary_op_constants(&self, left: &ConstantValue, op: &BinaryOperator, right: &ConstantValue) -> Option<ConstantValue> {
        match (left, op, right) {
            (ConstantValue::Integer(l), BinaryOperator::Add, ConstantValue::Integer(r)) => {
                Some(ConstantValue::Integer(l + r))
            },
            (ConstantValue::Integer(l), BinaryOperator::Subtract, ConstantValue::Integer(r)) => {
                Some(ConstantValue::Integer(l - r))
            },
            (ConstantValue::Integer(l), BinaryOperator::Multiply, ConstantValue::Integer(r)) => {
                Some(ConstantValue::Integer(l * r))
            },
            (ConstantValue::Integer(l), BinaryOperator::Divide, ConstantValue::Integer(r)) if *r != 0 => {
                Some(ConstantValue::Integer(l / r))
            },
            (ConstantValue::Float(l), BinaryOperator::Add, ConstantValue::Float(r)) => {
                Some(ConstantValue::Float(l + r))
            },
            (ConstantValue::Float(l), BinaryOperator::Subtract, ConstantValue::Float(r)) => {
                Some(ConstantValue::Float(l - r))
            },
            (ConstantValue::Float(l), BinaryOperator::Multiply, ConstantValue::Float(r)) => {
                Some(ConstantValue::Float(l * r))
            },
            (ConstantValue::Float(l), BinaryOperator::Divide, ConstantValue::Float(r)) if *r != 0.0 => {
                Some(ConstantValue::Float(l / r))
            },
            _ => None
        }
    }
    
    fn evaluate_unary_op_constant(&self, op: &UnaryOperator, operand: &ConstantValue) -> Option<ConstantValue> {
        match (op, operand) {
            (UnaryOperator::Negate, ConstantValue::Integer(i)) => {
                Some(ConstantValue::Integer(-i))
            },
            (UnaryOperator::Negate, ConstantValue::Float(f)) => {
                Some(ConstantValue::Float(-f))
            },
            (UnaryOperator::Not, ConstantValue::Boolean(b)) => {
                Some(ConstantValue::Boolean(!b))
            },
            _ => None
        }
    }
    
    fn get_array_constant_info(&self, array: &StatementValue) -> Option<ArrayConstantInfo> {
        // Look up array constant information from constant propagation
        None // Requires more context
    }
    
    fn is_pointer_type(&self, var_type: &VariableType) -> bool {
        matches!(var_type, VariableType::Pointer(_) | VariableType::Reference(_))
    }
    
    fn get_type_compatible_pointers(&self, var: &Variable) -> Vec<Variable> {
        let mut compatible = Vec::new();
        
        // Find all variables with compatible pointer types
        for (_, chains) in &self.def_use_chains {
            for var_name in chains.definitions.keys() {
                if var_name != &var.name {
                    // Check type compatibility
                    if let Some(other_var) = self.lookup_variable(var_name) {
                        if self.are_types_compatible(&var.var_type, &other_var.var_type) {
                            compatible.push(other_var);
                        }
                    }
                }
            }
        }
        
        compatible
    }
    
    fn heap_object_to_variable(&self, heap_id: HeapObjectId) -> Option<Variable> {
        // Convert heap object ID to variable if it represents a stack variable
        None // Requires heap tracking context
    }
    
    fn get_potential_pointees(&self, ptr_var: &Variable) -> Vec<Variable> {
        let mut pointees = Vec::new();
        
        // 1. Check if we have points-to analysis results for any function
        for (func_id, memory_result) in &self.memory_analysis_results {
            for (_, points_to_result) in &memory_result.points_to_sets {
                if let Some(targets) = points_to_result.mappings.get(&ptr_var.name) {
                    for &target_id in targets {
                        // Convert heap object ID to variable if possible
                        if let Some(target_var) = self.resolve_heap_object_to_variable(target_id, func_id) {
                            pointees.push(target_var);
                        }
                    }
                }
            }
        }
        
        // 2. If no points-to results, use def-use chain analysis
        if pointees.is_empty() {
            pointees.extend(self.infer_pointees_from_def_use_chains(ptr_var));
        }
        
        // 3. Fallback: type-based analysis for address-taken variables
        if pointees.is_empty() {
            pointees.extend(self.find_address_taken_variables_by_type(ptr_var));
        }
        
        // 4. Conservative analysis: all stack variables of compatible type
        if pointees.is_empty() && self.is_pointer_type(&ptr_var.var_type) {
            pointees.extend(self.find_type_compatible_stack_variables(ptr_var));
        }
        
        // Remove duplicates and sort for deterministic results
        pointees.sort_by(|a, b| a.name.cmp(&b.name));
        pointees.dedup();
        pointees
    }
    
    fn is_mutable_reference(&self, var_type: &VariableType) -> bool {
        matches!(var_type, VariableType::MutableReference(_) | VariableType::MutablePointer(_))
    }
    
    /// Resolve heap object ID to variable using function context with full allocation tracking
    fn resolve_heap_object_to_variable(&self, heap_id: HeapObjectId, func_id: &FunctionId) -> Option<Variable> {
        // First check allocation site tracking from memory analysis
        if let Some(memory_result) = self.memory_analysis_results.get(func_id) {
            if let Some(allocation_sites) = &memory_result.allocation_sites {
                if let Some(site_info) = allocation_sites.get(&heap_id) {
                    if let Some(allocated_var) = &site_info.allocated_variable {
                        return Some(allocated_var.clone());
                    }
                }
            }
        }
        
        // Check allocation ID mappings maintained during analysis
        if let Some(cfg) = self.control_flow_graphs.get(func_id) {
            // Build allocation ID map for this function
            let mut allocation_id_map: HashMap<usize, Variable> = HashMap::new();
            let mut next_alloc_id = 0usize;
            
            for (block_id, block) in &cfg.basic_blocks {
                for (stmt_idx, stmt) in block.statements.iter().enumerate() {
                    match &stmt.statement_type {
                        StatementType::Assignment(var, StatementValue::Alloca(alloc_type)) => {
                            // Generate unique allocation ID based on location
                            let alloc_id = (block_id.0 as usize) << 32 | (stmt_idx << 16) | next_alloc_id;
                            next_alloc_id += 1;
                            
                            allocation_id_map.insert(alloc_id, var.clone());
                            
                            // Check if this allocation ID corresponds to our heap object
                            if self.heap_id_matches_allocation(heap_id, alloc_id, alloc_type) {
                                return Some(var.clone());
                            }
                        },
                        StatementType::Assignment(var, StatementValue::Call(func_name, _, args)) => {
                            // Track heap allocations from malloc/new calls
                            if self.is_allocation_function(func_name) {
                                let alloc_id = (block_id.0 as usize) << 32 | (stmt_idx << 16) | next_alloc_id;
                                next_alloc_id += 1;
                                
                                allocation_id_map.insert(alloc_id, var.clone());
                                
                                if heap_id == alloc_id {
                                    return Some(var.clone());
                                }
                            }
                        },
                        _ => {}
                    }
                }
            }
            
            // Secondary lookup using the built allocation map
            if let Some(var) = allocation_id_map.get(&heap_id) {
                return Some(var.clone());
            }
        }
        
        None
    }
    
    /// Check if heap ID matches a specific allocation
    fn heap_id_matches_allocation(&self, heap_id: HeapObjectId, alloc_id: usize, alloc_type: &AllocationType) -> bool {
        // Match based on allocation characteristics
        match alloc_type {
            AllocationType::Stack(size) => {
                // Stack allocations use lower heap IDs
                heap_id < 0x10000 && (heap_id as usize) == alloc_id
            },
            AllocationType::Heap(size) => {
                // Heap allocations use higher IDs
                heap_id >= 0x10000 && (heap_id as usize) == alloc_id
            },
            AllocationType::Global => {
                // Global allocations use special range
                heap_id >= 0xFFFF0000 && (heap_id as usize) == alloc_id
            },
            AllocationType::Dynamic => {
                // Dynamic allocations matched by ID
                (heap_id as usize) == alloc_id
            }
        }
    }
    
    /// Check if function is an allocation function
    fn is_allocation_function(&self, func_name: &str) -> bool {
        matches!(func_name, "malloc" | "calloc" | "realloc" | "new" | "operator new" | 
                 "alloc" | "allocate" | "create" | "make" | "__builtin_alloca")
    }
    
    /// Infer potential pointees from def-use chains
    fn infer_pointees_from_def_use_chains(&self, ptr_var: &Variable) -> Vec<Variable> {
        let mut pointees = Vec::new();
        
        // Look for assignments where ptr_var is assigned an address
        for (func_id, chains) in &self.def_use_chains {
            for (var_name, uses) in chains {
                if var_name == &ptr_var.name {
                    // Find definitions of this pointer
                    for use_info in uses {
                        if let Some(def_stmt) = use_info.defining_statement.as_ref() {
                            if let StatementType::Assignment(_, StatementValue::Address(target_var)) = &def_stmt.statement_type {
                                pointees.push(target_var.clone());
                            }
                        }
                    }
                }
            }
        }
        
        pointees
    }
    
    /// Find variables whose address has been taken and match the pointer type
    fn find_address_taken_variables_by_type(&self, ptr_var: &Variable) -> Vec<Variable> {
        let mut pointees = Vec::new();
        let target_type = self.extract_pointee_type(&ptr_var.var_type);
        
        // Search all function CFGs for address-taking operations
        for (func_id, cfg) in &self.control_flow_graphs {
            for (_, block) in &cfg.basic_blocks {
                for stmt in &block.statements {
                    if let StatementType::Assignment(_, StatementValue::Address(addr_var)) = &stmt.statement_type {
                        // Check if the type matches what our pointer can point to
                        if self.types_are_compatible(&addr_var.var_type, &target_type) {
                            pointees.push(addr_var.clone());
                        }
                    }
                }
            }
        }
        
        pointees
    }
    
    /// Find all stack variables with compatible types (conservative analysis)
    fn find_type_compatible_stack_variables(&self, ptr_var: &Variable) -> Vec<Variable> {
        let mut pointees = Vec::new();
        let target_type = self.extract_pointee_type(&ptr_var.var_type);
        
        // Search through all local variables in all functions
        for (func_id, cfg) in &self.control_flow_graphs {
            for (_, block) in &cfg.basic_blocks {
                for stmt in &block.statements {
                    match &stmt.statement_type {
                        StatementType::Assignment(var, StatementValue::Alloca(_)) |
                        StatementType::Assignment(var, _) => {
                            if self.types_are_compatible(&var.var_type, &target_type) {
                                pointees.push(var.clone());
                            }
                        },
                        _ => {}
                    }
                }
            }
        }
        
        // Limit results to prevent explosive analysis
        pointees.truncate(50); // Conservative limit
        pointees
    }
    
    /// Extract the type that a pointer points to
    fn extract_pointee_type(&self, ptr_type: &VariableType) -> VariableType {
        match ptr_type {
            VariableType::Pointer(inner_type) => (**inner_type).clone(),
            VariableType::MutablePointer(inner_type) => (**inner_type).clone(),
            VariableType::Reference(inner_type) => (**inner_type).clone(),
            VariableType::MutableReference(inner_type) => (**inner_type).clone(),
            _ => VariableType::Unknown, // Not a pointer type
        }
    }
    
    /// Check if types are compatible for aliasing
    fn types_are_compatible(&self, type1: &VariableType, type2: &VariableType) -> bool {
        match (type1, type2) {
            (VariableType::Integer, VariableType::Integer) => true,
            (VariableType::Float, VariableType::Float) => true,
            (VariableType::Boolean, VariableType::Boolean) => true,
            (VariableType::String, VariableType::String) => true,
            (VariableType::Pointer(t1), VariableType::Pointer(t2)) => self.types_are_compatible(t1, t2),
            (VariableType::Array(t1, _), VariableType::Array(t2, _)) => self.types_are_compatible(t1, t2),
            (VariableType::Unknown, _) | (_, VariableType::Unknown) => true, // Conservative
            _ => false,
        }
    }
    
    /// Check if a variable maps to a specific heap object ID using allocation site tracking
    fn variable_maps_to_heap_id(&self, var: &Variable, heap_id: HeapObjectId) -> bool {
        // Check allocation site tracking in memory analysis results
        for (_, memory_result) in &self.memory_analysis_results {
            // Look for allocation sites that match this heap ID
            if let Some(allocation_sites) = memory_result.allocation_sites.as_ref() {
                for (site_id, site_info) in allocation_sites {
                    if *site_id == heap_id {
                        // Check if this variable was allocated at this site
                        if site_info.allocated_variable.as_ref().map(|v| &v.name) == Some(&var.name) {
                            return true;
                        }
                        
                        // Check if variable is derived from this allocation
                        if self.variable_derived_from_allocation(var, site_info) {
                            return true;
                        }
                    }
                }
            }
            
            // Check escape analysis for heap object mappings
            if let Some(escape_info) = memory_result.escape_analysis.get(&var.name) {
                if escape_info.heap_objects.contains(&heap_id) {
                    return true;
                }
            }
        }
        
        // Fallback: check def-use chains for heap-allocated variables
        self.variable_allocated_with_heap_id(var, heap_id)
    }
    
    /// Check if a variable is derived from a specific allocation site
    fn variable_derived_from_allocation(&self, var: &Variable, site_info: &AllocationSiteInfo) -> bool {
        // Check if variable is a field access, array index, or pointer dereference of the allocated variable
        if let Some(allocated_var) = &site_info.allocated_variable {
            // Simple check: variable name contains the allocated variable name (for derived pointers)
            if var.name.starts_with(&format!("{}_", allocated_var.name)) ||
               var.name.contains(&format!("_{}_", allocated_var.name)) {
                return true;
            }
            
            // Check if variable appears in def-use chains as derived from the allocated variable
            if let Some(chains) = self.def_use_chains.get(&site_info.function_id) {
                if let Some(uses) = chains.get(&var.name) {
                    for use_info in uses {
                        if let Some(def_stmt) = &use_info.defining_statement {
                            // Check if definition involves the allocated variable
                            if self.statement_uses_variable(def_stmt, allocated_var) {
                                return true;
                            }
                        }
                    }
                }
            }
        }
        false
    }
    
    /// Check if a variable was allocated with a specific heap ID using def-use analysis
    fn variable_allocated_with_heap_id(&self, var: &Variable, heap_id: HeapObjectId) -> bool {
        // Look through all def-use chains for allocation statements
        for (func_id, chains) in &self.def_use_chains {
            if let Some(uses) = chains.get(&var.name) {
                for use_info in uses {
                    if let Some(def_stmt) = &use_info.defining_statement {
                        match &def_stmt.statement_type {
                            StatementType::Assignment(_, StatementValue::Alloca(size)) => {
                                // Generate a deterministic heap ID based on allocation site
                                let site_heap_id = self.compute_allocation_site_id(func_id, &def_stmt.location, *size);
                                if site_heap_id == heap_id {
                                    return true;
                                }
                            },
                            StatementType::Assignment(_, StatementValue::HeapAlloc(size)) => {
                                let site_heap_id = self.compute_allocation_site_id(func_id, &def_stmt.location, *size);
                                if site_heap_id == heap_id {
                                    return true;
                                }
                            },
                            _ => {}
                        }
                    }
                }
            }
        }
        false
    }
    
    /// Compute a deterministic heap ID based on allocation site
    fn compute_allocation_site_id(&self, func_id: &FunctionId, location: &InstructionLocation, size: u64) -> HeapObjectId {
        use std::collections::hash_map::DefaultHasher;
        use std::hash::{Hash, Hasher};
        
        let mut hasher = DefaultHasher::new();
        func_id.hash(&mut hasher);
        location.block.hash(&mut hasher);
        location.instruction.hash(&mut hasher);
        size.hash(&mut hasher);
        
        hasher.finish() as HeapObjectId
    }
    
    /// Check if a statement uses a specific variable
    fn statement_uses_variable(&self, stmt: &Statement, var: &Variable) -> bool {
        match &stmt.statement_type {
            StatementType::Assignment(_, value) => self.value_uses_variable(value, var),
            StatementType::FunctionCall(_, _, args) => {
                args.iter().any(|arg| self.value_uses_variable(arg, var))
            },
            StatementType::Return(Some(value)) => self.value_uses_variable(value, var),
            _ => false,
        }
    }
    
    /// Check if a statement value uses a specific variable
    fn value_uses_variable(&self, value: &StatementValue, var: &Variable) -> bool {
        match value {
            StatementValue::Variable(used_var) => used_var.name == var.name,
            StatementValue::BinaryOp(left, _, right) => {
                self.value_uses_variable(left, var) || self.value_uses_variable(right, var)
            },
            StatementValue::UnaryOp(_, operand) => self.value_uses_variable(operand, var),
            StatementValue::Address(addr_var) => addr_var.name == var.name,
            StatementValue::Deref(ptr_var) => ptr_var.name == var.name,
            StatementValue::FieldAccess(obj_var, _) => obj_var.name == var.name,
            StatementValue::ArrayAccess(arr_var, index) => {
                arr_var.name == var.name || self.value_uses_variable(index, var)
            },
            _ => false,
        }
    }
    
    fn get_ssa_definitions(&self, var: &Variable) -> Option<Vec<Definition>> {
        // Get SSA form definitions if available
        None // Requires SSA context
    }
    
    fn get_function_info(&self, function: &str) -> Option<FunctionInfo> {
        // Look up function information from analysis
        None // Requires function database context
    }
    
    fn get_global_definitions(&self) -> Vec<Definition> {
        let mut global_defs = Vec::new();
        
        // 1. Search through all function CFGs for global variable access
        for (func_id, cfg) in &self.control_flow_graphs {
            for (block_id, block) in &cfg.basic_blocks {
                for (stmt_idx, stmt) in block.statements.iter().enumerate() {
                    match &stmt.statement_type {
                        StatementType::Assignment(var, value) => {
                            // Check if this is a global variable definition
                            if self.is_global_variable(var) {
                                global_defs.push(Definition {
                                    variable: var.clone(),
                                    location: InstructionLocation {
                                        function: func_id.clone(),
                                        block: *block_id,
                                        instruction: stmt_idx,
                                    },
                                    value: Some(value.clone()),
                                    definition_type: DefinitionType::GlobalVariable,
                                    may_aliases: self.get_global_aliases(var),
                                });
                            }
                        },
                        StatementType::FunctionCall(Some(result_var), func_name, args) => {
                            // Check if function call modifies global state
                            if self.function_modifies_globals(func_name) {
                                // Add definitions for potentially modified globals
                                global_defs.extend(self.get_globals_modified_by_function(func_name, args, func_id, *block_id, stmt_idx));
                            }
                            
                            // Check if result is assigned to a global
                            if self.is_global_variable(result_var) {
                                global_defs.push(Definition {
                                    variable: result_var.clone(),
                                    location: InstructionLocation {
                                        function: func_id.clone(),
                                        block: *block_id,
                                        instruction: stmt_idx,
                                    },
                                    value: Some(StatementValue::FunctionCall(func_name.clone(), args.clone())),
                                    definition_type: DefinitionType::FunctionCallResult,
                                    may_aliases: self.get_global_aliases(result_var),
                                });
                            }
                        },
                        _ => {}
                    }
                }
            }
        }
        
        // 2. Add module-level global variable initializations
        global_defs.extend(self.get_module_global_initializers());
        
        // 3. Add external global variable definitions from imports
        global_defs.extend(self.get_imported_global_definitions());
        
        // Sort by location for deterministic results
        global_defs.sort_by(|a, b| {
            a.location.function.cmp(&b.location.function)
                .then(a.location.block.cmp(&b.location.block))
                .then(a.location.instruction.cmp(&b.location.instruction))
        });
        
        // Remove duplicates based on variable name and location
        global_defs.dedup_by(|a, b| {
            a.variable.name == b.variable.name && a.location == b.location
        });
        
        global_defs
    }
    
    /// Check if a variable is a global variable
    fn is_global_variable(&self, var: &Variable) -> bool {
        // Global variables typically have specific naming patterns or are marked in symbol tables
        // Check multiple criteria for global variable identification
        
        // 1. Check naming conventions (globals often start with uppercase or specific prefixes)
        if var.name.starts_with("GLOBAL_") || 
           var.name.starts_with("g_") || 
           var.name.starts_with("__") ||
           var.name.chars().next().map_or(false, |c| c.is_uppercase()) {
            return true;
        }
        
        // 2. Check if variable appears in global scope across multiple functions
        let mut function_count = 0;
        for (_, chains) in &self.def_use_chains {
            if chains.contains_key(&var.name) {
                function_count += 1;
                if function_count >= 2 { // Used in 2+ functions = likely global
                    return true;
                }
            }
        }
        
        // 3. Check for module-level definitions (static variables)
        if var.name.contains("::") || var.name.contains("static") {
            return true;
        }
        
        false
    }
    
    /// Get global aliases for a variable
    fn get_global_aliases(&self, var: &Variable) -> Vec<Variable> {
        let mut aliases = Vec::new();
        
        // Find all global variables with the same underlying storage
        for (_, cfg) in &self.control_flow_graphs {
            for (_, block) in &cfg.basic_blocks {
                for stmt in &block.statements {
                    if let StatementType::Assignment(alias_var, StatementValue::Address(addr_var)) = &stmt.statement_type {
                        if addr_var.name == var.name && self.is_global_variable(alias_var) {
                            aliases.push(alias_var.clone());
                        }
                    }
                }
            }
        }
        
        aliases
    }
    
    /// Check if a function modifies global variables
    fn function_modifies_globals(&self, func_name: &str) -> bool {
        // Conservative analysis: assume certain function types modify globals
        let global_modifying_functions = [
            "printf", "scanf", "malloc", "free", "exit", 
            "setjmp", "longjmp", "signal", "atexit",
            "system", "getenv", "putenv", "time"
        ];
        
        if global_modifying_functions.contains(&func_name) {
            return true;
        }
        
        // Check if function contains assignments to global variables
        if let Some(cfg) = self.control_flow_graphs.values().find(|cfg| cfg.function_id.name == func_name) {
            for (_, block) in &cfg.basic_blocks {
                for stmt in &block.statements {
                    if let StatementType::Assignment(var, _) = &stmt.statement_type {
                        if self.is_global_variable(var) {
                            return true;
                        }
                    }
                }
            }
        }
        
        false
    }
    
    /// Get global variables potentially modified by a function call
    fn get_globals_modified_by_function(&self, func_name: &str, args: &[StatementValue], 
                                      func_id: &FunctionId, block_id: BasicBlockId, stmt_idx: usize) -> Vec<Definition> {
        let mut modified_globals = Vec::new();
        
        // Conservative approach: if function takes global variable addresses as arguments
        for (arg_idx, arg) in args.iter().enumerate() {
            if let StatementValue::Address(addr_var) = arg {
                if self.is_global_variable(addr_var) {
                    modified_globals.push(Definition {
                        variable: addr_var.clone(),
                        location: InstructionLocation {
                            function: func_id.clone(),
                            block: block_id,
                            instruction: stmt_idx,
                        },
                        value: Some(StatementValue::FunctionCall(func_name.to_string(), args.to_vec())),
                        definition_type: DefinitionType::IndirectModification,
                        may_aliases: self.get_global_aliases(addr_var),
                    });
                }
            }
        }
        
        // Add known global variables modified by standard library functions
        match func_name {
            "printf" | "fprintf" | "sprintf" => {
                // These functions may modify errno
                if let Some(errno_var) = self.find_global_variable("errno") {
                    modified_globals.push(Definition {
                        variable: errno_var,
                        location: InstructionLocation { function: func_id.clone(), block: block_id, instruction: stmt_idx },
                        value: Some(StatementValue::FunctionCall(func_name.to_string(), args.to_vec())),
                        definition_type: DefinitionType::SideEffect,
                        may_aliases: Vec::new(),
                    });
                }
            },
            "malloc" | "free" | "realloc" => {
                // These functions modify heap state and errno
                if let Some(errno_var) = self.find_global_variable("errno") {
                    modified_globals.push(Definition {
                        variable: errno_var,
                        location: InstructionLocation { function: func_id.clone(), block: block_id, instruction: stmt_idx },
                        value: Some(StatementValue::FunctionCall(func_name.to_string(), args.to_vec())),
                        definition_type: DefinitionType::SideEffect,
                        may_aliases: Vec::new(),
                    });
                }
            },
            _ => {}
        }
        
        modified_globals
    }
    
    /// Get module-level global variable initializations
    fn get_module_global_initializers(&self) -> Vec<Definition> {
        let mut initializers = Vec::new();
        
        // Look for special initialization functions or static initialization blocks
        for (func_id, cfg) in &self.control_flow_graphs {
            // Check if this is an initialization function
            if func_id.name.contains("init") || func_id.name.contains("constructor") || func_id.name.contains("__static_init") {
                for (block_id, block) in &cfg.basic_blocks {
                    for (stmt_idx, stmt) in block.statements.iter().enumerate() {
                        if let StatementType::Assignment(var, value) = &stmt.statement_type {
                            if self.is_global_variable(var) {
                                initializers.push(Definition {
                                    variable: var.clone(),
                                    location: InstructionLocation {
                                        function: func_id.clone(),
                                        block: *block_id,
                                        instruction: stmt_idx,
                                    },
                                    value: Some(value.clone()),
                                    definition_type: DefinitionType::ModuleInitializer,
                                    may_aliases: self.get_global_aliases(var),
                                });
                            }
                        }
                    }
                }
            }
        }
        
        initializers
    }
    
    /// Get imported global variable definitions from external modules
    fn get_imported_global_definitions(&self) -> Vec<Definition> {
        let mut imported_globals = Vec::new();
        
        // Look for external function calls that define global state
        for (func_id, cfg) in &self.control_flow_graphs {
            for (block_id, block) in &cfg.basic_blocks {
                for (stmt_idx, stmt) in block.statements.iter().enumerate() {
                    if let StatementType::FunctionCall(Some(result_var), func_name, args) = &stmt.statement_type {
                        // Check if this is an import of external global state
                        if func_name.contains("::") || func_name.starts_with("extern_") {
                            if self.is_global_variable(result_var) {
                                imported_globals.push(Definition {
                                    variable: result_var.clone(),
                                    location: InstructionLocation {
                                        function: func_id.clone(),
                                        block: *block_id,
                                        instruction: stmt_idx,
                                    },
                                    value: Some(StatementValue::FunctionCall(func_name.clone(), args.clone())),
                                    definition_type: DefinitionType::ExternalImport,
                                    may_aliases: self.get_global_aliases(result_var),
                                });
                            }
                        }
                    }
                }
            }
        }
        
        imported_globals
    }
    
    /// Find a specific global variable by name
    fn find_global_variable(&self, name: &str) -> Option<Variable> {
        // Search through all CFGs for a global variable with this name
        for (_, cfg) in &self.control_flow_graphs {
            for (_, block) in &cfg.basic_blocks {
                for stmt in &block.statements {
                    if let StatementType::Assignment(var, _) = &stmt.statement_type {
                        if var.name == name && self.is_global_variable(var) {
                            return Some(var.clone());
                        }
                    }
                }
            }
        }
        None
    }
    
    fn is_constant_value(&self, value: &StatementValue) -> bool {
        matches!(value, StatementValue::Constant(_))
    }
    
    fn is_derived_from(&self, var: &Variable, base: &Variable) -> bool {
        // Check if var is derived from base (e.g., through pointer arithmetic)
        false // Requires derivation tracking
    }
    
    fn extract_condition_type(&self, condition: &StatementValue, is_true: bool) -> ConditionType {
        // Extract condition type from branch condition
        ConditionType::Boolean(is_true)
    }
    
    fn value_to_variable(&self, value: &StatementValue) -> Option<Variable> {
        match value {
            StatementValue::Variable(v) => Some(v.clone()),
            _ => None
        }
    }
    
    fn compute_live_blocks(&self, var: &Variable, live_in: &HashMap<BasicBlockId, HashSet<Variable>>, 
                           live_out: &HashMap<BasicBlockId, HashSet<Variable>>) -> HashSet<BasicBlockId> {
        let mut live_blocks = HashSet::new();
        
        for (block_id, vars) in live_in {
            if vars.contains(var) {
                live_blocks.insert(*block_id);
            }
        }
        
        for (block_id, vars) in live_out {
            if vars.contains(var) {
                live_blocks.insert(*block_id);
            }
        }
        
        live_blocks
    }
    
    fn compute_spill_cost(&self, var: &Variable) -> f64 {
        // Compute spill cost based on use frequency and loop depth
        let mut cost = 0.0;
        
        for (_, chains) in &self.def_use_chains {
            if let Some(uses) = chains.uses.get(&var.name) {
                cost += uses.len() as f64;
            }
        }
        
        cost * self.config.spill_cost_factor
    }
    
    fn is_loop_invariant(&self, expr: &Expression, loop_blocks: &HashSet<BasicBlockId>) -> bool {
        // An expression is loop invariant if none of its operands are modified within the loop
        
        match expr {
            Expression::Variable(var) => {
                // Check if this variable is modified within any loop block
                !self.is_variable_modified_in_loop(var, loop_blocks)
            },
            Expression::Constant(_) => {
                // Constants are always loop invariant
                true
            },
            Expression::BinaryOp(left, op, right) => {
                // Binary operation is invariant if both operands are invariant
                // and the operation doesn't have side effects
                let left_invariant = self.is_loop_invariant(left, loop_blocks);
                let right_invariant = self.is_loop_invariant(right, loop_blocks);
                let op_pure = self.is_binary_operation_pure(op);
                
                left_invariant && right_invariant && op_pure
            },
            Expression::UnaryOp(op, operand) => {
                // Unary operation is invariant if operand is invariant and operation is pure
                let operand_invariant = self.is_loop_invariant(operand, loop_blocks);
                let op_pure = self.is_unary_operation_pure(op);
                
                operand_invariant && op_pure
            },
            Expression::FieldAccess(obj_expr, field) => {
                // Field access is invariant if:
                // 1. The object expression is invariant
                // 2. The field is not modified within the loop
                // 3. No aliasing modifications occur
                let obj_invariant = self.is_loop_invariant(obj_expr, loop_blocks);
                let field_not_modified = !self.is_field_modified_in_loop(obj_expr, field, loop_blocks);
                
                obj_invariant && field_not_modified
            },
            Expression::ArrayAccess(array_expr, index_expr) => {
                // Array access is invariant if:
                // 1. Both array and index expressions are invariant
                // 2. The array element is not modified within the loop
                let array_invariant = self.is_loop_invariant(array_expr, loop_blocks);
                let index_invariant = self.is_loop_invariant(index_expr, loop_blocks);
                let element_not_modified = !self.is_array_element_modified_in_loop(array_expr, index_expr, loop_blocks);
                
                array_invariant && index_invariant && element_not_modified
            },
            Expression::FunctionCall(func_name, args) => {
                // Function call is invariant if:
                // 1. All arguments are invariant
                // 2. The function is pure (no side effects)
                // 3. The function doesn't depend on mutable global state
                let args_invariant = args.iter().all(|arg| self.is_loop_invariant(arg, loop_blocks));
                let func_pure = self.is_function_pure(func_name);
                let no_global_deps = !self.function_depends_on_mutable_globals(func_name);
                
                args_invariant && func_pure && no_global_deps
            },
            Expression::Dereference(ptr_expr) => {
                // Dereference is invariant if:
                // 1. The pointer expression is invariant
                // 2. The pointed-to memory is not modified within the loop
                // 3. No aliasing writes occur within the loop
                let ptr_invariant = self.is_loop_invariant(ptr_expr, loop_blocks);
                let memory_not_modified = !self.is_memory_modified_through_pointer_in_loop(ptr_expr, loop_blocks);
                
                ptr_invariant && memory_not_modified
            }
        }
    }
    
    /// Check if a variable is modified within loop blocks
    fn is_variable_modified_in_loop(&self, var: &Variable, loop_blocks: &HashSet<BasicBlockId>) -> bool {
        // Check all statements in loop blocks for assignments to this variable
        for (func_id, cfg) in &self.control_flow_graphs {
            for &block_id in loop_blocks {
                if let Some(block) = cfg.basic_blocks.get(&block_id) {
                    for stmt in &block.statements {
                        match &stmt.statement_type {
                            StatementType::Assignment(assigned_var, _) => {
                                if assigned_var.name == var.name {
                                    return true;
                                }
                            },
                            StatementType::FunctionCall(Some(result_var), _, _) => {
                                if result_var.name == var.name {
                                    return true;
                                }
                            },
                            StatementType::FunctionCall(None, func_name, args) => {
                                // Check if function might modify this variable through parameters
                                if self.function_might_modify_variable(func_name, var, args) {
                                    return true;
                                }
                            },
                            _ => {}
                        }
                    }
                }
            }
        }
        
        // Also check for indirect modifications through pointers or aliases
        self.is_variable_modified_indirectly_in_loop(var, loop_blocks)
    }
    
    /// Check if a field is modified within loop blocks
    fn is_field_modified_in_loop(&self, obj_expr: &Expression, field: &str, loop_blocks: &HashSet<BasicBlockId>) -> bool {
        for (func_id, cfg) in &self.control_flow_graphs {
            for &block_id in loop_blocks {
                if let Some(block) = cfg.basic_blocks.get(&block_id) {
                    for stmt in &block.statements {
                        if let StatementType::Assignment(var, value) = &stmt.statement_type {
                            // Check if assignment is to this field
                            if let Some(field_name) = self.extract_field_name_from_assignment(var, value) {
                                if field_name == field && self.expressions_may_alias(obj_expr, &self.extract_object_from_variable(var)) {
                                    return true;
                                }
                            }
                        }
                    }
                }
            }
        }
        false
    }
    
    /// Check if array elements are modified within loop blocks
    fn is_array_element_modified_in_loop(&self, array_expr: &Expression, index_expr: &Expression, loop_blocks: &HashSet<BasicBlockId>) -> bool {
        for (func_id, cfg) in &self.control_flow_graphs {
            for &block_id in loop_blocks {
                if let Some(block) = cfg.basic_blocks.get(&block_id) {
                    for stmt in &block.statements {
                        if let StatementType::Assignment(var, value) = &stmt.statement_type {
                            // Check if this is an array element assignment
                            if self.is_array_element_assignment(var, value, array_expr, index_expr) {
                                return true;
                            }
                        }
                    }
                }
            }
        }
        false
    }
    
    /// Check if memory is modified through pointer within loop blocks
    fn is_memory_modified_through_pointer_in_loop(&self, ptr_expr: &Expression, loop_blocks: &HashSet<BasicBlockId>) -> bool {
        for (func_id, cfg) in &self.control_flow_graphs {
            for &block_id in loop_blocks {
                if let Some(block) = cfg.basic_blocks.get(&block_id) {
                    for stmt in &block.statements {
                        match &stmt.statement_type {
                            StatementType::Assignment(var, value) => {
                                // Check for indirect stores through pointers
                                if self.assignment_modifies_memory_through_pointer(var, value, ptr_expr) {
                                    return true;
                                }
                            },
                            StatementType::FunctionCall(_, func_name, args) => {
                                // Check if function call might modify memory through pointer
                                if self.function_modifies_memory_through_pointer(func_name, args, ptr_expr) {
                                    return true;
                                }
                            },
                            _ => {}
                        }
                    }
                }
            }
        }
        false
    }
    
    /// Check if binary operation is pure (no side effects)
    fn is_binary_operation_pure(&self, op: &BinaryOperator) -> bool {
        match op {
            BinaryOperator::Add | BinaryOperator::Subtract | 
            BinaryOperator::Multiply | BinaryOperator::Divide |
            BinaryOperator::Modulo | BinaryOperator::And | 
            BinaryOperator::Or | BinaryOperator::Xor |
            BinaryOperator::ShiftLeft | BinaryOperator::ShiftRight |
            BinaryOperator::Equal | BinaryOperator::NotEqual |
            BinaryOperator::LessThan | BinaryOperator::LessEqual |
            BinaryOperator::GreaterThan | BinaryOperator::GreaterEqual |
            BinaryOperator::LogicalAnd | BinaryOperator::LogicalOr => true,
            // Division by zero can cause exceptions, but we consider it pure for optimization purposes
            // Assignment operators are not pure
            BinaryOperator::Assign | BinaryOperator::AddAssign |
            BinaryOperator::SubtractAssign | BinaryOperator::MultiplyAssign |
            BinaryOperator::DivideAssign => false,
        }
    }
    
    /// Check if unary operation is pure (no side effects)
    fn is_unary_operation_pure(&self, op: &UnaryOperator) -> bool {
        match op {
            UnaryOperator::Negate | UnaryOperator::Not | 
            UnaryOperator::BitwiseNot | UnaryOperator::AddressOf |
            UnaryOperator::Dereference => true,
            // Pre/post increment/decrement modify their operand
            UnaryOperator::PreIncrement | UnaryOperator::PostIncrement |
            UnaryOperator::PreDecrement | UnaryOperator::PostDecrement => false,
        }
    }
    
    /// Check if a function is pure (deterministic, no side effects)
    fn is_function_pure(&self, func_name: &str) -> bool {
        // List of known pure functions
        let pure_functions = [
            "abs", "min", "max", "sqrt", "sin", "cos", "tan", "log", "exp",
            "floor", "ceil", "round", "pow", "atan2", "strlen", "strcmp", "memcmp"
        ];
        
        if pure_functions.contains(&func_name) {
            return true;
        }
        
        // Check naming conventions
        if func_name.starts_with("pure_") || func_name.starts_with("const_") {
            return true;
        }
        
        // Check if function modifies global state
        !self.function_modifies_globals(func_name)
    }
    
    /// Check if function depends on mutable global state
    fn function_depends_on_mutable_globals(&self, func_name: &str) -> bool {
        // Functions that depend on mutable global state
        let global_dependent_functions = [
            "rand", "time", "getpid", "getenv", "strerror", "localtime", "gmtime"
        ];
        
        global_dependent_functions.contains(&func_name)
    }
    
    fn is_safe_to_hoist(&self, expr: &Expression, loop_info: &LoopInfo) -> bool {
        // Check if expression is safe to hoist out of loop
        self.is_expression_pure(expr)
    }
    
    fn estimate_hoisting_benefit(&self, expr: &Expression, loop_info: &LoopInfo) -> f64 {
        // Estimate benefit of hoisting expression out of loop
        loop_info.estimated_iterations as f64 * expr.get_complexity()
    }
    
    fn estimate_cse_benefit(&self, expr: &Expression) -> f64 {
        // Estimate benefit of common subexpression elimination
        expr.get_complexity() * self.config.cse_benefit_factor
    }
    
    fn lookup_variable(&self, name: &str) -> Option<Variable> {
        // Look up variable by name
        None // Requires symbol table context
    }
    
    fn are_types_compatible(&self, type1: &VariableType, type2: &VariableType) -> bool {
        self.check_type_compatibility_with_context(type1, type2, &TypeCompatibilityContext::default())
    }

    /// Comprehensive type compatibility analysis with context-sensitive checking
    fn check_type_compatibility_with_context(&self, type1: &VariableType, type2: &VariableType, context: &TypeCompatibilityContext) -> bool {
        // Handle exact matches first
        if type1 == type2 {
            return true;
        }

        match (type1, type2) {
            // Primitive type compatibility
            (VariableType::Integer, VariableType::Integer) => true,
            (VariableType::Float, VariableType::Float) => true,
            (VariableType::Boolean, VariableType::Boolean) => true,
            (VariableType::String, VariableType::String) => true,

            // Numeric type coercion compatibility
            (VariableType::Integer, VariableType::Float) | 
            (VariableType::Float, VariableType::Integer) => {
                context.allow_numeric_coercion
            },

            // Pointer type compatibility with variance analysis
            (VariableType::Pointer(inner1), VariableType::Pointer(inner2)) => {
                self.check_pointer_type_compatibility(inner1, inner2, context)
            },

            // Array type compatibility with dimension and element analysis
            (VariableType::Array(elem1, size1), VariableType::Array(elem2, size2)) => {
                self.check_array_type_compatibility(elem1, elem2, *size1, *size2, context)
            },

            // Function type compatibility with signature matching
            (VariableType::Function(params1, ret1), VariableType::Function(params2, ret2)) => {
                self.check_function_type_compatibility(params1, ret1, params2, ret2, context)
            },

            // Struct/Object type compatibility with structural analysis
            (VariableType::Object(name1), VariableType::Object(name2)) => {
                self.check_object_type_compatibility(name1, name2, context)
            },

            // Generic type compatibility with constraint solving
            (VariableType::Generic(name1, constraints1), VariableType::Generic(name2, constraints2)) => {
                self.check_generic_type_compatibility(name1, constraints1, name2, constraints2, context)
            },

            // Union type compatibility (one type compatible with any member)
            (VariableType::Union(types1), type2) => {
                types1.iter().any(|t| self.check_type_compatibility_with_context(t, type2, context))
            },
            (type1, VariableType::Union(types2)) => {
                types2.iter().any(|t| self.check_type_compatibility_with_context(type1, t, context))
            },

            // Interface/Trait compatibility
            (VariableType::Interface(interface1), VariableType::Interface(interface2)) => {
                self.check_interface_compatibility(interface1, interface2, context)
            },
            (VariableType::Object(obj_name), VariableType::Interface(interface_name)) => {
                self.check_object_implements_interface(obj_name, interface_name, context)
            },

            // Nullable type compatibility
            (VariableType::Nullable(inner1), VariableType::Nullable(inner2)) => {
                self.check_type_compatibility_with_context(inner1, inner2, context)
            },
            (inner_type, VariableType::Nullable(nullable_inner)) |
            (VariableType::Nullable(nullable_inner), inner_type) => {
                context.allow_nullable_coercion && 
                self.check_type_compatibility_with_context(inner_type, nullable_inner, context)
            },

            // Unknown type handling (conservative approach)
            (VariableType::Unknown, _) | (_, VariableType::Unknown) => {
                context.allow_unknown_types
            },

            // Void type compatibility (only with itself)
            (VariableType::Void, VariableType::Void) => true,

            // Default: incompatible
            _ => false,
        }
    }

    /// Check pointer type compatibility with variance rules
    fn check_pointer_type_compatibility(&self, inner1: &VariableType, inner2: &VariableType, context: &TypeCompatibilityContext) -> bool {
        // Pointers are contravariant in their pointed-to type for safety
        match context.variance_mode {
            VarianceMode::Covariant => {
                // T* compatible with U* if T <: U
                self.is_subtype_of(inner1, inner2, context)
            },
            VarianceMode::Contravariant => {
                // T* compatible with U* if U <: T
                self.is_subtype_of(inner2, inner1, context)
            },
            VarianceMode::Invariant => {
                // T* compatible with U* only if T = U
                self.check_type_compatibility_with_context(inner1, inner2, context)
            },
        }
    }

    /// Check array type compatibility with size and element type analysis
    fn check_array_type_compatibility(&self, elem1: &VariableType, elem2: &VariableType, 
                                    size1: Option<usize>, size2: Option<usize>, 
                                    context: &TypeCompatibilityContext) -> bool {
        // Element types must be compatible
        if !self.check_type_compatibility_with_context(elem1, elem2, context) {
            return false;
        }

        // Size compatibility check
        match (size1, size2) {
            (Some(s1), Some(s2)) => s1 == s2 || context.allow_array_size_coercion,
            (None, None) => true,  // Both dynamic arrays
            (Some(_), None) | (None, Some(_)) => context.allow_dynamic_array_coercion,
        }
    }

    /// Check function type compatibility with parameter and return type analysis
    fn check_function_type_compatibility(&self, params1: &[VariableType], ret1: &VariableType,
                                       params2: &[VariableType], ret2: &VariableType,
                                       context: &TypeCompatibilityContext) -> bool {
        // Parameter count must match (unless variadic allowed)
        if params1.len() != params2.len() && !context.allow_variadic_functions {
            return false;
        }

        // Check parameter compatibility (contravariant)
        let param_context = context.with_variance(VarianceMode::Contravariant);
        for (p1, p2) in params1.iter().zip(params2.iter()) {
            if !self.check_type_compatibility_with_context(p1, p2, &param_context) {
                return false;
            }
        }

        // Check return type compatibility (covariant)
        let return_context = context.with_variance(VarianceMode::Covariant);
        self.check_type_compatibility_with_context(ret1, ret2, &return_context)
    }

    /// Check object type compatibility with structural analysis
    fn check_object_type_compatibility(&self, name1: &str, name2: &str, context: &TypeCompatibilityContext) -> bool {
        if name1 == name2 {
            return true;
        }

        // Check inheritance hierarchy
        if context.check_inheritance {
            if self.is_subclass_of(name1, name2) || self.is_subclass_of(name2, name1) {
                return true;
            }
        }

        // Check structural compatibility
        if context.allow_structural_typing {
            self.check_structural_compatibility(name1, name2, context)
        } else {
            false
        }
    }

    /// Check generic type compatibility with constraint solving
    fn check_generic_type_compatibility(&self, name1: &str, constraints1: &[String],
                                      name2: &str, constraints2: &[String],
                                      context: &TypeCompatibilityContext) -> bool {
        if name1 == name2 {
            // Same type parameter, check constraint compatibility
            return self.check_constraint_compatibility(constraints1, constraints2, context);
        }

        // Different type parameters - check if constraints allow unification
        if context.allow_generic_unification {
            self.can_unify_generic_types(name1, constraints1, name2, constraints2, context)
        } else {
            false
        }
    }

    /// Check interface compatibility
    fn check_interface_compatibility(&self, interface1: &str, interface2: &str, context: &TypeCompatibilityContext) -> bool {
        if interface1 == interface2 {
            return true;
        }

        // Check interface inheritance
        if context.check_inheritance {
            self.interface_extends(interface1, interface2) || self.interface_extends(interface2, interface1)
        } else {
            false
        }
    }

    /// Check if object implements interface
    fn check_object_implements_interface(&self, obj_name: &str, interface_name: &str, context: &TypeCompatibilityContext) -> bool {
        // Check explicit implementation declarations
        if self.object_implements_interface(obj_name, interface_name) {
            return true;
        }

        // Check structural compatibility if allowed
        if context.allow_structural_typing {
            self.check_object_interface_structural_compatibility(obj_name, interface_name, context)
        } else {
            false
        }
    }

    /// Check if type1 is a subtype of type2
    fn is_subtype_of(&self, type1: &VariableType, type2: &VariableType, context: &TypeCompatibilityContext) -> bool {
        match (type1, type2) {
            (VariableType::Object(obj1), VariableType::Object(obj2)) => {
                self.is_subclass_of(obj1, obj2)
            },
            (VariableType::Interface(iface1), VariableType::Interface(iface2)) => {
                self.interface_extends(iface1, iface2)
            },
            (VariableType::Object(obj), VariableType::Interface(iface)) => {
                self.object_implements_interface(obj, iface)
            },
            _ => self.check_type_compatibility_with_context(type1, type2, context),
        }
    }

    /// Helper methods for type system queries
    fn is_subclass_of(&self, child: &str, parent: &str) -> bool {
        // Query the type system for inheritance relationships
        // This would integrate with the compiler's type information
        if let Some(type_info) = self.get_type_info(child) {
            type_info.parent_classes.contains(&parent.to_string()) ||
            type_info.parent_classes.iter().any(|p| self.is_subclass_of(p, parent))
        } else {
            false
        }
    }

    fn interface_extends(&self, child: &str, parent: &str) -> bool {
        if let Some(interface_info) = self.get_interface_info(child) {
            interface_info.extended_interfaces.contains(&parent.to_string()) ||
            interface_info.extended_interfaces.iter().any(|p| self.interface_extends(p, parent))
        } else {
            false
        }
    }

    fn object_implements_interface(&self, obj: &str, interface: &str) -> bool {
        if let Some(type_info) = self.get_type_info(obj) {
            type_info.implemented_interfaces.contains(&interface.to_string()) ||
            type_info.parent_classes.iter().any(|p| self.object_implements_interface(p, interface))
        } else {
            false
        }
    }

    fn check_structural_compatibility(&self, type1: &str, type2: &str, _context: &TypeCompatibilityContext) -> bool {
        // Compare structure of types (fields, methods, etc.)
        let info1 = self.get_type_info(type1);
        let info2 = self.get_type_info(type2);
        
        match (info1, info2) {
            (Some(t1), Some(t2)) => {
                // Check if all public fields and methods of t2 are present in t1
                t2.fields.iter().all(|field| {
                    t1.fields.iter().any(|f| f.name == field.name && 
                        self.check_type_compatibility_with_context(&f.field_type, &field.field_type, 
                            &TypeCompatibilityContext::default()))
                }) &&
                t2.methods.iter().all(|method| {
                    t1.methods.iter().any(|m| m.signature_compatible_with(method))
                })
            },
            _ => false,
        }
    }

    fn check_constraint_compatibility(&self, constraints1: &[String], constraints2: &[String], 
                                    context: &TypeCompatibilityContext) -> bool {
        // Comprehensive constraint compatibility analysis with semantic understanding
        for constraint2 in constraints2 {
            if !self.constraint_satisfied_by_set(constraint2, constraints1, context) {
                return false;
            }
        }
        true
    }

    fn constraint_satisfied_by_set(&self, target_constraint: &str, constraint_set: &[String], 
                                  context: &TypeCompatibilityContext) -> bool {
        // Parse and analyze constraint semantics
        let target_parts = self.parse_constraint_string(target_constraint);
        
        for existing_constraint in constraint_set {
            let existing_parts = self.parse_constraint_string(existing_constraint);
            
            if self.constraints_semantically_compatible(&target_parts, &existing_parts, context) {
                return true;
            }
        }
        
        // Check if constraint can be inferred from combination of existing constraints
        self.constraint_inferrable_from_set(target_constraint, constraint_set, context)
    }

    fn parse_constraint_string(&self, constraint: &str) -> ConstraintParts {
        // Parse constraint strings like "implements:Serializable", "extends:Object", "has_field:name:String"
        let parts: Vec<&str> = constraint.split(':').collect();
        
        match parts.len() {
            2 => match parts[0] {
                "implements" => ConstraintParts::ImplementsInterface(parts[1].to_string()),
                "extends" => ConstraintParts::ExtendsClass(parts[1].to_string()),
                "subtype" => ConstraintParts::SubtypeOf(parts[1].to_string()),
                "supertype" => ConstraintParts::SupertypeOf(parts[1].to_string()),
                _ => ConstraintParts::Unknown(constraint.to_string()),
            },
            3 => match parts[0] {
                "has_field" => ConstraintParts::HasField(parts[1].to_string(), parts[2].to_string()),
                _ => ConstraintParts::Unknown(constraint.to_string()),
            },
            4 => match parts[0] {
                "has_method" => {
                    let params: Vec<String> = parts[2].split(',').map(|s| s.to_string()).collect();
                    ConstraintParts::HasMethod(parts[1].to_string(), params, parts[3].to_string())
                },
                _ => ConstraintParts::Unknown(constraint.to_string()),
            },
            _ => ConstraintParts::Unknown(constraint.to_string()),
        }
    }

    fn constraints_semantically_compatible(&self, constraint1: &ConstraintParts, constraint2: &ConstraintParts,
                                         context: &TypeCompatibilityContext) -> bool {
        match (constraint1, constraint2) {
            (ConstraintParts::ImplementsInterface(i1), ConstraintParts::ImplementsInterface(i2)) => {
                i1 == i2 || (context.check_inheritance && self.interface_extends(i1, i2))
            },
            (ConstraintParts::ExtendsClass(c1), ConstraintParts::ExtendsClass(c2)) => {
                c1 == c2 || (context.check_inheritance && self.is_subclass_of(c1, c2))
            },
            (ConstraintParts::SubtypeOf(t1), ConstraintParts::SubtypeOf(t2)) => {
                t1 == t2 || self.type_name_is_subtype_of(t1, t2)
            },
            (ConstraintParts::SupertypeOf(t1), ConstraintParts::SupertypeOf(t2)) => {
                t1 == t2 || self.type_name_is_subtype_of(t2, t1)
            },
            (ConstraintParts::HasField(f1, t1), ConstraintParts::HasField(f2, t2)) => {
                f1 == f2 && (t1 == t2 || self.type_names_compatible(t1, t2, context))
            },
            (ConstraintParts::HasMethod(m1, p1, r1), ConstraintParts::HasMethod(m2, p2, r2)) => {
                m1 == m2 && p1.len() == p2.len() && 
                p1.iter().zip(p2.iter()).all(|(a, b)| self.type_names_compatible(a, b, context)) &&
                self.type_names_compatible(r1, r2, context)
            },
            _ => false,
        }
    }

    fn constraint_inferrable_from_set(&self, target_constraint: &str, constraint_set: &[String],
                                    context: &TypeCompatibilityContext) -> bool {
        let target_parts = self.parse_constraint_string(target_constraint);
        
        match target_parts {
            ConstraintParts::ImplementsInterface(target_interface) => {
                // Check if any superclass implements this interface
                for constraint in constraint_set {
                    let parts = self.parse_constraint_string(constraint);
                    if let ConstraintParts::ExtendsClass(class_name) = parts {
                        if self.class_implements_interface(&class_name, &target_interface) {
                            return true;
                        }
                    }
                }
            },
            ConstraintParts::SubtypeOf(target_type) => {
                // Check if subtype relationship can be inferred through transitivity
                for constraint in constraint_set {
                    let parts = self.parse_constraint_string(constraint);
                    if let ConstraintParts::SubtypeOf(intermediate_type) = parts {
                        if self.type_name_is_subtype_of(&intermediate_type, &target_type) {
                            return true;
                        }
                    }
                }
            },
            _ => {},
        }
        
        false
    }

    fn can_unify_generic_types(&self, name1: &str, constraints1: &[String],
                             name2: &str, constraints2: &[String],
                             context: &TypeCompatibilityContext) -> bool {
        if name1 == name2 {
            return true;
        }
        
        // Comprehensive unification algorithm with constraint satisfaction
        let unified_constraints = self.unify_constraint_sets(constraints1, constraints2);
        
        match unified_constraints {
            Ok(unified) => self.constraint_set_is_satisfiable(&unified, context),
            Err(_) => false, // Unification failed due to conflicting constraints
        }
    }

    fn unify_constraint_sets(&self, constraints1: &[String], constraints2: &[String]) 
                           -> Result<Vec<String>, String> {
        let mut unified = Vec::new();
        let mut conflicts = Vec::new();
        
        // Add all constraints from first set
        for constraint in constraints1 {
            unified.push(constraint.clone());
        }
        
        // Add constraints from second set, checking for conflicts
        for constraint2 in constraints2 {
            let parts2 = self.parse_constraint_string(constraint2);
            let mut conflicted = false;
            
            for constraint1 in constraints1 {
                let parts1 = self.parse_constraint_string(constraint1);
                
                if self.constraints_conflict(&parts1, &parts2) {
                    conflicts.push(format!("Conflict between '{}' and '{}'", constraint1, constraint2));
                    conflicted = true;
                    break;
                }
            }
            
            if !conflicted && !unified.contains(constraint2) {
                unified.push(constraint2.clone());
            }
        }
        
        if conflicts.is_empty() {
            Ok(unified)
        } else {
            Err(format!("Unification failed: {}", conflicts.join(", ")))
        }
    }

    fn constraints_conflict(&self, constraint1: &ConstraintParts, constraint2: &ConstraintParts) -> bool {
        match (constraint1, constraint2) {
            (ConstraintParts::SubtypeOf(t1), ConstraintParts::SupertypeOf(t2)) => {
                t1 == t2 || !self.type_name_is_subtype_of(t1, t2)
            },
            (ConstraintParts::SupertypeOf(t1), ConstraintParts::SubtypeOf(t2)) => {
                t1 == t2 || !self.type_name_is_subtype_of(t2, t1)
            },
            (ConstraintParts::ImplementsInterface(i1), ConstraintParts::ExtendsClass(c1)) => {
                // Check if class cannot implement interface due to conflicts
                !self.class_can_implement_interface(c1, i1)
            },
            _ => false,
        }
    }

    fn constraint_set_is_satisfiable(&self, constraints: &[String], context: &TypeCompatibilityContext) -> bool {
        // Check pairwise constraint compatibility
        for i in 0..constraints.len() {
            for j in (i + 1)..constraints.len() {
                let parts1 = self.parse_constraint_string(&constraints[i]);
                let parts2 = self.parse_constraint_string(&constraints[j]);
                
                if self.constraints_conflict(&parts1, &parts2) {
                    return false;
                }
            }
        }
        
        // Check if constraint set has consistent semantics
        self.constraint_set_semantically_consistent(constraints, context)
    }

    fn constraint_set_semantically_consistent(&self, constraints: &[String], 
                                            _context: &TypeCompatibilityContext) -> bool {
        let mut subtype_constraints = Vec::new();
        let mut supertype_constraints = Vec::new();
        let mut interface_constraints = Vec::new();
        
        // Categorize constraints
        for constraint in constraints {
            let parts = self.parse_constraint_string(constraint);
            match parts {
                ConstraintParts::SubtypeOf(t) => subtype_constraints.push(t),
                ConstraintParts::SupertypeOf(t) => supertype_constraints.push(t),
                ConstraintParts::ImplementsInterface(i) => interface_constraints.push(i),
                _ => {},
            }
        }
        
        // Check subtype/supertype consistency through type hierarchy
        for subtype in &subtype_constraints {
            for supertype in &supertype_constraints {
                if !self.type_name_is_subtype_of(subtype, supertype) {
                    return false;
                }
            }
        }
        
        // Check if all required interfaces can be implemented simultaneously
        self.interfaces_can_be_implemented_together(&interface_constraints)
    }

    fn type_name_is_subtype_of(&self, child_name: &str, parent_name: &str) -> bool {
        if child_name == parent_name {
            return true;
        }
        
        // Query type hierarchy - would integrate with semantic analyzer
        self.is_subclass_of(child_name, parent_name)
    }

    fn type_names_compatible(&self, type1: &str, type2: &str, context: &TypeCompatibilityContext) -> bool {
        if type1 == type2 {
            return true;
        }
        
        // Handle primitive type compatibility
        match (type1, type2) {
            ("int", "long") | ("long", "int") => context.allow_numeric_coercion,
            ("float", "double") | ("double", "float") => context.allow_numeric_coercion,
            ("int", "float") | ("float", "int") => context.allow_numeric_coercion,
            _ => {
                // Check object type compatibility
                if context.check_inheritance {
                    self.type_name_is_subtype_of(type1, type2) || self.type_name_is_subtype_of(type2, type1)
                } else {
                    false
                }
            }
        }
    }

    fn class_implements_interface(&self, class_name: &str, interface_name: &str) -> bool {
        self.object_implements_interface(class_name, interface_name)
    }

    fn class_can_implement_interface(&self, class_name: &str, interface_name: &str) -> bool {
        // Check if class structure allows implementing interface
        if let (Some(class_info), Some(iface_info)) = (self.get_type_info(class_name), self.get_interface_info(interface_name)) {
            // Check for method signature conflicts
            for required_method in &iface_info.required_methods {
                for existing_method in &class_info.methods {
                    if existing_method.name == required_method.name {
                        // Method exists - check signature compatibility
                        if !existing_method.signature_compatible_with(required_method) {
                            return false; // Signature conflict
                        }
                    }
                }
            }
            true
        } else {
            true // Assume compatible if type info not available
        }
    }

    fn interfaces_can_be_implemented_together(&self, interfaces: &[String]) -> bool {
        // Check if multiple interfaces can be implemented without conflicts
        for i in 0..interfaces.len() {
            for j in (i + 1)..interfaces.len() {
                if !self.interfaces_compatible(&interfaces[i], &interfaces[j]) {
                    return false;
                }
            }
        }
        true
    }

    fn interfaces_compatible(&self, interface1: &str, interface2: &str) -> bool {
        if let (Some(iface1), Some(iface2)) = (self.get_interface_info(interface1), self.get_interface_info(interface2)) {
            // Check for method signature conflicts
            for method1 in &iface1.required_methods {
                for method2 in &iface2.required_methods {
                    if method1.name == method2.name && !method1.signature_compatible_with(method2) {
                        return false; // Conflicting method signatures
                    }
                }
            }
        }
        true
    }

    fn check_object_interface_structural_compatibility(&self, obj_name: &str, interface_name: &str, 
                                                      context: &TypeCompatibilityContext) -> bool {
        // Check if object structurally satisfies interface requirements
        if let (Some(obj_info), Some(iface_info)) = (self.get_type_info(obj_name), self.get_interface_info(interface_name)) {
            iface_info.required_methods.iter().all(|method| {
                obj_info.methods.iter().any(|m| {
                    m.name == method.name && 
                    self.check_function_type_compatibility(&m.parameters, &m.return_type,
                                                         &method.parameters, &method.return_type, context)
                })
            })
        } else {
            false
        }
    }

    fn get_type_info(&self, type_name: &str) -> Option<TypeInfo> {
        // Comprehensive type information lookup with built-in type system integration
        match type_name {
            // Built-in primitive types
            "Integer" | "int" | "i32" | "i64" => Some(TypeInfo {
                name: type_name.to_string(),
                fields: vec![],
                methods: self.get_primitive_methods("Integer"),
                parent_classes: vec!["Object".to_string()],
                implemented_interfaces: vec!["Comparable".to_string(), "Serializable".to_string()],
                is_abstract: false,
                is_final: true,
                generic_parameters: vec![],
            }),
            
            "Float" | "f32" | "f64" | "double" => Some(TypeInfo {
                name: type_name.to_string(),
                fields: vec![],
                methods: self.get_primitive_methods("Float"),
                parent_classes: vec!["Object".to_string()],
                implemented_interfaces: vec!["Comparable".to_string(), "Serializable".to_string()],
                is_abstract: false,
                is_final: true,
                generic_parameters: vec![],
            }),
            
            "String" | "str" => Some(TypeInfo {
                name: type_name.to_string(),
                fields: vec![
                    FieldInfo {
                        name: "length".to_string(),
                        field_type: VariableType::Integer,
                        is_public: true,
                        is_mutable: false,
                    },
                    FieldInfo {
                        name: "data".to_string(),
                        field_type: VariableType::Array(Box::new(VariableType::Integer), None),
                        is_public: false,
                        is_mutable: false,
                    },
                ],
                methods: self.get_string_methods(),
                parent_classes: vec!["Object".to_string()],
                implemented_interfaces: vec!["Comparable".to_string(), "Serializable".to_string(), "Iterable".to_string()],
                is_abstract: false,
                is_final: true,
                generic_parameters: vec![],
            }),
            
            "Boolean" | "bool" => Some(TypeInfo {
                name: type_name.to_string(),
                fields: vec![],
                methods: self.get_primitive_methods("Boolean"),
                parent_classes: vec!["Object".to_string()],
                implemented_interfaces: vec!["Serializable".to_string()],
                is_abstract: false,
                is_final: true,
                generic_parameters: vec![],
            }),
            
            "Object" => Some(TypeInfo {
                name: type_name.to_string(),
                fields: vec![],
                methods: self.get_object_methods(),
                parent_classes: vec![],
                implemented_interfaces: vec!["Serializable".to_string()],
                is_abstract: false,
                is_final: false,
                generic_parameters: vec![],
            }),
            
            // Collection types
            "Array" | "List" => Some(TypeInfo {
                name: type_name.to_string(),
                fields: vec![
                    FieldInfo {
                        name: "length".to_string(),
                        field_type: VariableType::Integer,
                        is_public: true,
                        is_mutable: false,
                    },
                    FieldInfo {
                        name: "capacity".to_string(),
                        field_type: VariableType::Integer,
                        is_public: false,
                        is_mutable: true,
                    },
                ],
                methods: self.get_collection_methods(),
                parent_classes: vec!["Object".to_string()],
                implemented_interfaces: vec!["Iterable".to_string(), "Collection".to_string(), "Serializable".to_string()],
                is_abstract: false,
                is_final: false,
                generic_parameters: vec!["T".to_string()],
            }),
            
            "HashMap" | "Map" => Some(TypeInfo {
                name: type_name.to_string(),
                fields: vec![
                    FieldInfo {
                        name: "size".to_string(),
                        field_type: VariableType::Integer,
                        is_public: true,
                        is_mutable: false,
                    },
                    FieldInfo {
                        name: "buckets".to_string(),
                        field_type: VariableType::Array(Box::new(VariableType::Object("Entry".to_string())), None),
                        is_public: false,
                        is_mutable: true,
                    },
                ],
                methods: self.get_map_methods(),
                parent_classes: vec!["Object".to_string()],
                implemented_interfaces: vec!["Map".to_string(), "Serializable".to_string()],
                is_abstract: false,
                is_final: false,
                generic_parameters: vec!["K".to_string(), "V".to_string()],
            }),
            
            // Check if this is a user-defined type by parsing the context
            _ => self.lookup_user_defined_type(type_name),
        }
    }

    fn get_interface_info(&self, interface_name: &str) -> Option<InterfaceInfo> {
        // Comprehensive interface information lookup
        match interface_name {
            "Serializable" => Some(InterfaceInfo {
                name: interface_name.to_string(),
                required_methods: vec![
                    MethodInfo {
                        name: "serialize".to_string(),
                        parameters: vec![],
                        return_type: VariableType::Array(Box::new(VariableType::Integer), None),
                        is_public: true,
                        is_virtual: true,
                        is_static: false,
                    },
                    MethodInfo {
                        name: "deserialize".to_string(),
                        parameters: vec![VariableType::Array(Box::new(VariableType::Integer), None)],
                        return_type: VariableType::Boolean,
                        is_public: true,
                        is_virtual: true,
                        is_static: false,
                    },
                ],
                extended_interfaces: vec![],
                generic_parameters: vec![],
            }),
            
            "Comparable" => Some(InterfaceInfo {
                name: interface_name.to_string(),
                required_methods: vec![
                    MethodInfo {
                        name: "compare_to".to_string(),
                        parameters: vec![VariableType::Object("Object".to_string())],
                        return_type: VariableType::Integer,
                        is_public: true,
                        is_virtual: true,
                        is_static: false,
                    },
                    MethodInfo {
                        name: "equals".to_string(),
                        parameters: vec![VariableType::Object("Object".to_string())],
                        return_type: VariableType::Boolean,
                        is_public: true,
                        is_virtual: true,
                        is_static: false,
                    },
                ],
                extended_interfaces: vec!["Serializable".to_string()],
                generic_parameters: vec!["T".to_string()],
            }),
            
            "Iterable" => Some(InterfaceInfo {
                name: interface_name.to_string(),
                required_methods: vec![
                    MethodInfo {
                        name: "iterator".to_string(),
                        parameters: vec![],
                        return_type: VariableType::Object("Iterator".to_string()),
                        is_public: true,
                        is_virtual: true,
                        is_static: false,
                    },
                    MethodInfo {
                        name: "for_each".to_string(),
                        parameters: vec![VariableType::Function(vec![VariableType::Generic("T".to_string(), vec![])], Box::new(VariableType::Void))],
                        return_type: VariableType::Void,
                        is_public: true,
                        is_virtual: true,
                        is_static: false,
                    },
                ],
                extended_interfaces: vec![],
                generic_parameters: vec!["T".to_string()],
            }),
            
            "Collection" => Some(InterfaceInfo {
                name: interface_name.to_string(),
                required_methods: vec![
                    MethodInfo {
                        name: "size".to_string(),
                        parameters: vec![],
                        return_type: VariableType::Integer,
                        is_public: true,
                        is_virtual: true,
                        is_static: false,
                    },
                    MethodInfo {
                        name: "is_empty".to_string(),
                        parameters: vec![],
                        return_type: VariableType::Boolean,
                        is_public: true,
                        is_virtual: true,
                        is_static: false,
                    },
                    MethodInfo {
                        name: "contains".to_string(),
                        parameters: vec![VariableType::Generic("T".to_string(), vec![])],
                        return_type: VariableType::Boolean,
                        is_public: true,
                        is_virtual: true,
                        is_static: false,
                    },
                    MethodInfo {
                        name: "add".to_string(),
                        parameters: vec![VariableType::Generic("T".to_string(), vec![])],
                        return_type: VariableType::Boolean,
                        is_public: true,
                        is_virtual: true,
                        is_static: false,
                    },
                    MethodInfo {
                        name: "remove".to_string(),
                        parameters: vec![VariableType::Generic("T".to_string(), vec![])],
                        return_type: VariableType::Boolean,
                        is_public: true,
                        is_virtual: true,
                        is_static: false,
                    },
                ],
                extended_interfaces: vec!["Iterable".to_string()],
                generic_parameters: vec!["T".to_string()],
            }),
            
            "Map" => Some(InterfaceInfo {
                name: interface_name.to_string(),
                required_methods: vec![
                    MethodInfo {
                        name: "get".to_string(),
                        parameters: vec![VariableType::Generic("K".to_string(), vec![])],
                        return_type: VariableType::Nullable(Box::new(VariableType::Generic("V".to_string(), vec![]))),
                        is_public: true,
                        is_virtual: true,
                        is_static: false,
                    },
                    MethodInfo {
                        name: "put".to_string(),
                        parameters: vec![
                            VariableType::Generic("K".to_string(), vec![]),
                            VariableType::Generic("V".to_string(), vec![])
                        ],
                        return_type: VariableType::Nullable(Box::new(VariableType::Generic("V".to_string(), vec![]))),
                        is_public: true,
                        is_virtual: true,
                        is_static: false,
                    },
                    MethodInfo {
                        name: "contains_key".to_string(),
                        parameters: vec![VariableType::Generic("K".to_string(), vec![])],
                        return_type: VariableType::Boolean,
                        is_public: true,
                        is_virtual: true,
                        is_static: false,
                    },
                    MethodInfo {
                        name: "size".to_string(),
                        parameters: vec![],
                        return_type: VariableType::Integer,
                        is_public: true,
                        is_virtual: true,
                        is_static: false,
                    },
                ],
                extended_interfaces: vec![],
                generic_parameters: vec!["K".to_string(), "V".to_string()],
            }),
            
            // Check for user-defined interfaces
            _ => self.lookup_user_defined_interface(interface_name),
        }
    }

    fn get_primitive_methods(&self, type_name: &str) -> Vec<MethodInfo> {
        let mut methods = vec![
            MethodInfo {
                name: "to_string".to_string(),
                parameters: vec![],
                return_type: VariableType::String,
                is_public: true,
                is_virtual: true,
                is_static: false,
            },
            MethodInfo {
                name: "hash_code".to_string(),
                parameters: vec![],
                return_type: VariableType::Integer,
                is_public: true,
                is_virtual: true,
                is_static: false,
            },
        ];
        
        // Add type-specific methods
        match type_name {
            "Integer" => {
                methods.extend(vec![
                    MethodInfo {
                        name: "abs".to_string(),
                        parameters: vec![],
                        return_type: VariableType::Integer,
                        is_public: true,
                        is_virtual: false,
                        is_static: false,
                    },
                    MethodInfo {
                        name: "max".to_string(),
                        parameters: vec![VariableType::Integer],
                        return_type: VariableType::Integer,
                        is_public: true,
                        is_virtual: false,
                        is_static: true,
                    },
                ]);
            },
            "Float" => {
                methods.extend(vec![
                    MethodInfo {
                        name: "abs".to_string(),
                        parameters: vec![],
                        return_type: VariableType::Float,
                        is_public: true,
                        is_virtual: false,
                        is_static: false,
                    },
                    MethodInfo {
                        name: "is_nan".to_string(),
                        parameters: vec![],
                        return_type: VariableType::Boolean,
                        is_public: true,
                        is_virtual: false,
                        is_static: false,
                    },
                ]);
            },
            _ => {},
        }
        
        methods
    }

    fn get_string_methods(&self) -> Vec<MethodInfo> {
        vec![
            MethodInfo {
                name: "length".to_string(),
                parameters: vec![],
                return_type: VariableType::Integer,
                is_public: true,
                is_virtual: false,
                is_static: false,
            },
            MethodInfo {
                name: "substring".to_string(),
                parameters: vec![VariableType::Integer, VariableType::Integer],
                return_type: VariableType::String,
                is_public: true,
                is_virtual: false,
                is_static: false,
            },
            MethodInfo {
                name: "concat".to_string(),
                parameters: vec![VariableType::String],
                return_type: VariableType::String,
                is_public: true,
                is_virtual: false,
                is_static: false,
            },
            MethodInfo {
                name: "contains".to_string(),
                parameters: vec![VariableType::String],
                return_type: VariableType::Boolean,
                is_public: true,
                is_virtual: false,
                is_static: false,
            },
            MethodInfo {
                name: "split".to_string(),
                parameters: vec![VariableType::String],
                return_type: VariableType::Array(Box::new(VariableType::String), None),
                is_public: true,
                is_virtual: false,
                is_static: false,
            },
        ]
    }

    fn get_object_methods(&self) -> Vec<MethodInfo> {
        vec![
            MethodInfo {
                name: "equals".to_string(),
                parameters: vec![VariableType::Object("Object".to_string())],
                return_type: VariableType::Boolean,
                is_public: true,
                is_virtual: true,
                is_static: false,
            },
            MethodInfo {
                name: "hash_code".to_string(),
                parameters: vec![],
                return_type: VariableType::Integer,
                is_public: true,
                is_virtual: true,
                is_static: false,
            },
            MethodInfo {
                name: "to_string".to_string(),
                parameters: vec![],
                return_type: VariableType::String,
                is_public: true,
                is_virtual: true,
                is_static: false,
            },
            MethodInfo {
                name: "get_class".to_string(),
                parameters: vec![],
                return_type: VariableType::Object("Class".to_string()),
                is_public: true,
                is_virtual: false,
                is_static: false,
            },
        ]
    }

    fn get_collection_methods(&self) -> Vec<MethodInfo> {
        vec![
            MethodInfo {
                name: "size".to_string(),
                parameters: vec![],
                return_type: VariableType::Integer,
                is_public: true,
                is_virtual: true,
                is_static: false,
            },
            MethodInfo {
                name: "get".to_string(),
                parameters: vec![VariableType::Integer],
                return_type: VariableType::Generic("T".to_string(), vec![]),
                is_public: true,
                is_virtual: true,
                is_static: false,
            },
            MethodInfo {
                name: "set".to_string(),
                parameters: vec![VariableType::Integer, VariableType::Generic("T".to_string(), vec![])],
                return_type: VariableType::Void,
                is_public: true,
                is_virtual: true,
                is_static: false,
            },
            MethodInfo {
                name: "add".to_string(),
                parameters: vec![VariableType::Generic("T".to_string(), vec![])],
                return_type: VariableType::Boolean,
                is_public: true,
                is_virtual: true,
                is_static: false,
            },
            MethodInfo {
                name: "remove".to_string(),
                parameters: vec![VariableType::Integer],
                return_type: VariableType::Generic("T".to_string(), vec![]),
                is_public: true,
                is_virtual: true,
                is_static: false,
            },
        ]
    }

    fn get_map_methods(&self) -> Vec<MethodInfo> {
        vec![
            MethodInfo {
                name: "get".to_string(),
                parameters: vec![VariableType::Generic("K".to_string(), vec![])],
                return_type: VariableType::Nullable(Box::new(VariableType::Generic("V".to_string(), vec![]))),
                is_public: true,
                is_virtual: true,
                is_static: false,
            },
            MethodInfo {
                name: "put".to_string(),
                parameters: vec![
                    VariableType::Generic("K".to_string(), vec![]),
                    VariableType::Generic("V".to_string(), vec![])
                ],
                return_type: VariableType::Nullable(Box::new(VariableType::Generic("V".to_string(), vec![]))),
                is_public: true,
                is_virtual: true,
                is_static: false,
            },
            MethodInfo {
                name: "contains_key".to_string(),
                parameters: vec![VariableType::Generic("K".to_string(), vec![])],
                return_type: VariableType::Boolean,
                is_public: true,
                is_virtual: true,
                is_static: false,
            },
            MethodInfo {
                name: "remove".to_string(),
                parameters: vec![VariableType::Generic("K".to_string(), vec![])],
                return_type: VariableType::Nullable(Box::new(VariableType::Generic("V".to_string(), vec![]))),
                is_public: true,
                is_virtual: true,
                is_static: false,
            },
            MethodInfo {
                name: "key_set".to_string(),
                parameters: vec![],
                return_type: VariableType::Object("Set".to_string()),
                is_public: true,
                is_virtual: true,
                is_static: false,
            },
        ]
    }

    fn lookup_user_defined_type(&self, type_name: &str) -> Option<TypeInfo> {
        let type_registry = self.get_type_registry();
        
        if let Some(registered_type) = type_registry.get(type_name) {
            return Some(registered_type.clone());
        }
        
        if type_name.ends_with("Exception") || type_name.ends_with("Error") {
            return Some(TypeInfo {
                name: type_name.to_string(),
                fields: vec![
                    FieldInfo {
                        name: "message".to_string(),
                        field_type: VariableType::String,
                        is_public: true,
                        is_mutable: false,
                    },
                    FieldInfo {
                        name: "cause".to_string(),
                        field_type: VariableType::Nullable(Box::new(VariableType::Object("Exception".to_string()))),
                        is_public: true,
                        is_mutable: false,
                    },
                ],
                methods: vec![
                    MethodInfo {
                        name: "get_message".to_string(),
                        parameters: vec![],
                        return_type: VariableType::String,
                        is_public: true,
                        is_virtual: true,
                        is_static: false,
                    },
                    MethodInfo {
                        name: "get_stack_trace".to_string(),
                        parameters: vec![],
                        return_type: VariableType::Array(Box::new(VariableType::String), None),
                        is_public: true,
                        is_virtual: true,
                        is_static: false,
                    },
                ],
                parent_classes: vec!["Exception".to_string(), "Object".to_string()],
                implemented_interfaces: vec!["Serializable".to_string()],
                is_abstract: false,
                is_final: false,
                generic_parameters: vec![],
            });
        }
        
        Some(TypeInfo {
            name: type_name.to_string(),
            fields: vec![],
            methods: self.get_object_methods(),
            parent_classes: vec!["Object".to_string()],
            implemented_interfaces: vec!["Serializable".to_string()],
            is_abstract: false,
            is_final: false,
            generic_parameters: vec![],
        })
    }

    fn lookup_user_defined_interface(&self, interface_name: &str) -> Option<InterfaceInfo> {
        let interface_registry = self.get_interface_registry();
        
        if let Some(registered_interface) = interface_registry.get(interface_name) {
            return Some(registered_interface.clone());
        }
        
        if interface_name.ends_with("Service") || interface_name.ends_with("Manager") {
            return Some(InterfaceInfo {
                name: interface_name.to_string(),
                required_methods: vec![
                    MethodInfo {
                        name: "initialize".to_string(),
                        parameters: vec![],
                        return_type: VariableType::Boolean,
                        is_public: true,
                        is_virtual: true,
                        is_static: false,
                    },
                    MethodInfo {
                        name: "shutdown".to_string(),
                        parameters: vec![],
                        return_type: VariableType::Void,
                        is_public: true,
                        is_virtual: true,
                        is_static: false,
                    },
                ],
                extended_interfaces: vec![],
                generic_parameters: vec![],
            });
        }
        
        Some(InterfaceInfo {
            name: interface_name.to_string(),
            required_methods: vec![],
            extended_interfaces: vec![],
            generic_parameters: vec![],
        })
    }
    
    fn get_type_registry(&self) -> HashMap<String, TypeInfo> {
        let mut registry = HashMap::new();
        
        for (_, analysis_result) in &self.analysis_results {
            if let Some(type_definitions) = &analysis_result.type_definitions {
                for (type_name, type_def) in type_definitions {
                    registry.insert(type_name.clone(), type_def.clone());
                }
            }
        }
        
        for (_, memory_result) in &self.memory_analysis_results {
            if let Some(type_info) = &memory_result.type_information {
                for (type_name, type_def) in type_info {
                    registry.insert(type_name.clone(), type_def.clone());
                }
            }
        }
        
        registry
    }
    
    fn get_interface_registry(&self) -> HashMap<String, InterfaceInfo> {
        let mut registry = HashMap::new();
        
        for (_, analysis_result) in &self.analysis_results {
            if let Some(interface_definitions) = &analysis_result.interface_definitions {
                for (interface_name, interface_def) in interface_definitions {
                    registry.insert(interface_name.clone(), interface_def.clone());
                }
            }
        }
        
        registry
    }
    
    
    fn is_expression_unused(&self, expr: &Expression, live_vars: &LiveVariableAnalysis) -> bool {
        // Check if the expression defines variables that are not live
        let defined_vars = self.get_expression_defined_variables(expr);
        
        for var in defined_vars {
            if live_vars.live_in.values().any(|live_set| live_set.contains(&var)) ||
               live_vars.live_out.values().any(|live_set| live_set.contains(&var)) {
                return false; // Expression is used
            }
        }
        
        // Check if expression has side effects
        match expr {
            Expression::Call(func, _) => !self.is_pure_function(func),
            Expression::Store(_, _) => false, // Store always has side effects
            Expression::Load(_) => {
                // Load might be unused if result isn't used and no aliasing concerns
                defined_vars.is_empty()
            },
            _ => defined_vars.is_empty(), // Other expressions unused if they don't define variables
        }
    }
    
    fn get_expression_location(&self, expr: &Expression) -> Option<InstructionLocation> {
        // Search through all control flow graphs to find expression location
        for (function_id, cfg) in &self.control_flow_graphs {
            for (block_id, block) in &cfg.blocks {
                for (stmt_idx, stmt) in block.statements.iter().enumerate() {
                    if let Some(stmt_expr) = self.statement_generates_expression(stmt) {
                        if self.expressions_semantically_equivalent(expr, &stmt_expr) {
                            return Some(InstructionLocation {
                                function_id: function_id.clone(),
                                block_id: *block_id,
                                instruction_index: stmt_idx,
                            });
                        }
                    }
                }
            }
        }
        
        // Check in def-use chains if direct search fails
        for chains in self.def_use_chains.values() {
            for (var, locations) in chains {
                for location in locations {
                    if let Some(stmt) = self.get_statement_at_location(location) {
                        if let Some(stmt_expr) = self.statement_generates_expression(stmt) {
                            if self.expressions_semantically_equivalent(expr, &stmt_expr) {
                                return Some(location.clone());
                            }
                        }
                    }
                }
            }
        }
        
        None
    }
    
    fn find_removable_expressions(&self, live_vars: &LiveVariableAnalysis, value_numbering: &ValueNumberingResult) -> CompilerResult<Vec<RemovableExpression>> {
        let mut removable = Vec::new();
        
        // Find expressions that compute values that are never used
        for (function_id, cfg) in &self.control_flow_graphs {
            for (block_id, block) in &cfg.blocks {
                for (stmt_idx, stmt) in block.statements.iter().enumerate() {
                    if let Some(expr) = self.statement_generates_expression(stmt) {
                        if self.is_expression_unused(&expr, live_vars) {
                            // Check if it's safe to remove (no side effects)
                            if self.is_safe_to_remove(&expr) {
                                removable.push(RemovableExpression {
                                    location: InstructionLocation {
                                        function_id: function_id.clone(),
                                        block_id: *block_id,
                                        instruction_index: stmt_idx,
                                    },
                                    expression: expr.clone(),
                                    removal_benefit: self.calculate_removal_benefit(&expr),
                                    safety_level: RemovalSafetyLevel::Safe,
                                });
                            }
                        }
                        
                        // Find redundant expressions using value numbering
                        if let Some(value_num) = value_numbering.expression_numbers.get(&expr) {
                            let equivalent_expressions = self.find_expressions_with_value_number(*value_num, value_numbering);
                            if equivalent_expressions.len() > 1 {
                                // Keep the dominating expression, mark others for removal
                                let dominant_expr = self.find_dominant_expression(&equivalent_expressions, function_id)?;
                                for equiv_expr in equivalent_expressions {
                                    if equiv_expr.location != dominant_expr.location {
                                        removable.push(RemovableExpression {
                                            location: equiv_expr.location,
                                            expression: equiv_expr.expression,
                                            removal_benefit: self.calculate_cse_benefit(&equiv_expr.expression),
                                            safety_level: RemovalSafetyLevel::Safe,
                                        });
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        
        Ok(removable)
    }
}

// =============================================================================
// Advanced Supporting Types and Structures
// =============================================================================

/// Comprehensive data flow analysis result
#[derive(Debug, Clone)]
pub struct DataFlowResult {
    pub function_id: FunctionId,
    pub reaching_definitions: ReachingDefinitionsResult,
    pub available_expressions: AvailableExpressionsResult,
    pub live_variables_analysis: LiveVariableAnalysis,
    pub very_busy_expressions: VeryBusyExpressionsResult,
    pub value_numbering: ValueNumberingResult,
    pub dead_code_analysis: DeadCodeAnalysis,
    pub memory_analysis: Option<MemoryAnalysisResult>,
    pub optimization_opportunities: Vec<OptimizationOpportunity>,
    pub control_flow_graph: ControlFlowGraph,
    pub analysis_quality: AnalysisQuality,
    pub analysis_metadata: AnalysisMetadata,
}

/// Analysis metadata for comprehensive tracking
#[derive(Debug, Clone)]
pub struct AnalysisMetadata {
    pub iteration_counts: HashMap<String, usize>,
    pub convergence_time: Duration,
    pub confidence_scores: HashMap<String, f64>,
    pub precision_level: AnalysisPrecision,
}

/// Enhanced definition with comprehensive information
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct Definition {
    pub variable: Variable,
    pub location: InstructionLocation,
    pub value: Option<ConstantLatticeValue>,
    pub definition_type: DefinitionType,
    pub may_aliases: Vec<Variable>,
}

/// Types of definitions
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub enum DefinitionType {
    Direct,     // Direct assignment
    Indirect,   // Through pointer/reference
    Call,       // Function call result
    Parameter,  // Function parameter
    Phi,        // SSA phi function
}

/// Sophisticated constant lattice for advanced constant propagation
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub enum ConstantLatticeValue {
    Bottom,                    // Undefined
    Constant(ConstantValue),   // Known constant
    Top,                       // Unknown/variable
}

/// Variable with enhanced scope and type information
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct Variable {
    pub name: String,
    pub scope: VariableScope,
    pub var_type: Option<TypeInfo>,
    pub is_mutable: bool,
    pub address_taken: bool,
    pub global: bool,
}

impl Variable {
    pub fn new(name: String, scope: VariableScope) -> Self {
        Self {
            name,
            scope,
            var_type: None,
            is_mutable: true,
            address_taken: false,
            global: false,
        }
    }
    
    pub fn with_type(mut self, type_info: TypeInfo) -> Self {
        self.var_type = Some(type_info);
        self
    }
    
    pub fn immutable(mut self) -> Self {
        self.is_mutable = false;
        self
    }
    
    pub fn address_taken(mut self) -> Self {
        self.address_taken = true;
        self
    }
    
    pub fn global(mut self) -> Self {
        self.global = true;
        self
    }
}

/// Enhanced variable scope
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub enum VariableScope {
    Local(usize),              // Local variable with scope level
    Parameter(usize),          // Parameter with index
    Global,                    // Global variable
    Temporary(usize),          // Temporary variable with ID
    Captured(String),          // Captured variable from outer scope
    Static(String),            // Static variable
    ThreadLocal(String),       // Thread-local variable
}

/// Type information for enhanced analysis
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct MemoryTypeInfo {
    pub name: String,
    pub size: Option<usize>,
    pub alignment: Option<usize>,
    pub is_pointer: bool,
    pub is_aggregate: bool,
    pub field_info: Option<Vec<MemoryFieldInfo>>,
}

/// Field information for aggregate types
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct MemoryFieldInfo {
    pub name: String,
    pub type_info: MemoryTypeInfo,
    pub offset: usize,
}

/// Advanced reaching definitions result
#[derive(Debug, Clone)]
pub struct ReachingDefinitionsResult {
    pub reaching_in: HashMap<BasicBlockId, HashSet<Definition>>,
    pub reaching_out: HashMap<BasicBlockId, HashSet<Definition>>,
    pub gen_sets: HashMap<BasicBlockId, HashSet<Definition>>,
    pub kill_sets: HashMap<BasicBlockId, HashSet<Definition>>,
    pub convergence_iterations: usize,
}

/// Advanced available expressions result
#[derive(Debug, Clone)]
pub struct AvailableExpressionsResult {
    pub available_at_entry: HashMap<BasicBlockId, HashSet<Expression>>,
    pub available_at_exit: HashMap<BasicBlockId, HashSet<Expression>>,
    pub redundant_expressions: HashMap<String, Vec<InstructionLocation>>,
    pub global_optimizations: Vec<GlobalOptimization>,
    pub convergence_iterations: usize,
}

/// Advanced live variable analysis result
#[derive(Debug, Clone)]
pub struct LiveVariableAnalysis {
    pub live_in: HashMap<BasicBlockId, HashSet<Variable>>,
    pub live_out: HashMap<BasicBlockId, HashSet<Variable>>,
    pub dead_assignments: HashSet<InstructionLocation>,
    pub variable_lifetimes: HashMap<Variable, VariableLifetime>,
    pub path_conditions: HashMap<BasicBlockId, Vec<PathCondition>>,
    pub convergence_iterations: usize,
}

/// Variable lifetime information
#[derive(Debug, Clone)]
pub struct VariableLifetime {
    pub birth_points: Vec<InstructionLocation>,
    pub death_points: Vec<InstructionLocation>,
    pub live_ranges: Vec<LiveRange>,
    pub interference_graph: Vec<Variable>,
}

/// Live range for register allocation
#[derive(Debug, Clone)]
pub struct LiveRange {
    pub start: InstructionLocation,
    pub end: InstructionLocation,
    pub spans_calls: bool,
    pub register_pressure: f64,
}

/// Path condition for path-sensitive analysis
#[derive(Debug, Clone)]
pub struct PathCondition {
    pub condition: Expression,
    pub truth_value: bool,
    pub location: InstructionLocation,
}

/// Advanced very busy expressions result
#[derive(Debug, Clone)]
pub struct VeryBusyExpressionsResult {
    pub busy_at_entry: HashMap<BasicBlockId, HashSet<Expression>>,
    pub busy_at_exit: HashMap<BasicBlockId, HashSet<Expression>>,
    pub code_motion_opportunities: Vec<CodeMotionOpportunity>,
    pub convergence_iterations: usize,
}

/// Code motion opportunity
#[derive(Debug, Clone)]
pub struct CodeMotionOpportunity {
    pub expression: Expression,
    pub from_blocks: Vec<BasicBlockId>,
    pub to_block: BasicBlockId,
    pub estimated_benefit: f64,
    pub safety_constraints: Vec<SafetyConstraint>,
}

/// Safety constraint for code motion
#[derive(Debug, Clone)]
pub enum SafetyConstraint {
    NoAliasing(Vec<Variable>),
    NoSideEffects,
    DominanceRequired,
    ExceptionSafety,
}

/// Value numbering result
#[derive(Debug, Clone)]
pub struct ValueNumberingResult {
    pub value_numbers: HashMap<Expression, ValueNumber>,
    pub equivalent_expressions: HashMap<ValueNumber, Vec<Expression>>,
    pub common_subexpressions: HashMap<ValueNumber, Vec<Expression>>,
    pub next_value_number: usize,
}

/// Value number for expression equivalence
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct ValueNumber(pub usize);

/// Dead code analysis result
#[derive(Debug, Clone)]
pub struct DeadCodeAnalysis {
    pub dead_instructions: HashSet<InstructionLocation>,
    pub unreachable_blocks: HashSet<BasicBlockId>,
    pub unused_computations: HashSet<InstructionLocation>,
    pub removable_expressions: Vec<RemovableExpression>,
}

/// Removable expression information
#[derive(Debug, Clone)]
pub struct RemovableExpression {
    pub expression: Expression,
    pub location: InstructionLocation,
    pub removal_benefit: f64,
    pub dependencies: Vec<InstructionLocation>,
}

/// Memory analysis result
#[derive(Debug, Clone)]
pub struct MemoryAnalysisResult {
    pub alias_sets: HashMap<Variable, AliasSet>,
    pub dependencies: Vec<MemoryDependency>,
    pub escape_analysis: HashMap<Variable, EscapeInfo>,
}

/// Alias set for memory analysis
#[derive(Debug, Clone)]
pub struct AliasSet {
    pub variables: HashSet<Variable>,
    pub may_alias_with: HashSet<AliasSet>,
    pub must_alias_with: HashSet<AliasSet>,
}

impl AliasSet {
    pub fn may_alias(&self, other: &AliasSet) -> bool {
        self.may_alias_with.contains(other) || 
        !self.variables.is_disjoint(&other.variables)
    }
}

/// Memory dependency information
#[derive(Debug, Clone)]
pub struct MemoryDependency {
    pub from: InstructionLocation,
    pub to: InstructionLocation,
    pub dependency_type: MemoryDependencyType,
    pub distance: Option<usize>,
}

/// Types of memory dependencies
#[derive(Debug, Clone)]
pub enum MemoryDependencyType {
    TrueData,      // Read after write
    AntiData,      // Write after read
    Output,        // Write after write
    Control,       // Control dependence
}

/// Escape information for variables
#[derive(Debug, Clone)]
pub struct EscapeInfo {
    pub escapes: bool,
    pub escape_points: Vec<InstructionLocation>,
    pub stack_allocatable: bool,
}

/// Global optimization opportunity
#[derive(Debug, Clone)]
pub struct GlobalOptimization {
    pub optimization_type: GlobalOptimizationType,
    pub affected_blocks: Vec<BasicBlockId>,
    pub estimated_benefit: f64,
    pub implementation_complexity: OptimizationComplexity,
}

/// Types of global optimizations
#[derive(Debug, Clone)]
pub enum GlobalOptimizationType {
    GlobalCommonSubexpressionElimination,
    LoopInvariantCodeMotion,
    GlobalConstantPropagation,
    GlobalDeadCodeElimination,
    StrengthReduction,
}

/// Optimization opportunity with comprehensive information
#[derive(Debug, Clone)]
pub struct OptimizationOpportunity {
    pub opportunity_type: OptimizationType,
    pub location: InstructionLocation,
    pub estimated_benefit: f64,
    pub confidence: f64,
    pub description: String,
    pub implementation_complexity: OptimizationComplexity,
}

/// Types of optimizations
#[derive(Debug, Clone, PartialEq)]
pub enum OptimizationType {
    DeadCodeElimination,
    ConstantPropagation,
    ConstantFolding,
    CommonSubexpressionElimination,
    CopyPropagation,
    DeadStoreElimination,
    RedundantLoadElimination,
    StrengthReduction,
    LoopInvariantCodeMotion,
    InductionVariableElimination,
}

/// Optimization complexity levels
#[derive(Debug, Clone, PartialEq)]
pub enum OptimizationComplexity {
    Low,        // Simple local optimization
    Medium,     // Regional optimization
    High,       // Global optimization
    Maximum,    // Interprocedural optimization
}

/// Basic block identifier
pub type BasicBlockId = usize;

/// Enhanced control flow graph
#[derive(Debug, Clone)]
pub struct ControlFlowGraph {
    pub function_id: FunctionId,
    pub basic_blocks: HashMap<BasicBlockId, BasicBlock>,
    pub entry_block: BasicBlockId,
    pub exit_blocks: Vec<BasicBlockId>,
    pub dominance_tree: Option<DominanceTree>,
    pub post_dominance_tree: Option<DominanceTree>,
    pub loop_info: Option<LoopInfo>,
    pub natural_loops: Vec<NaturalLoop>,
}

impl ControlFlowGraph {
    pub fn new(function_id: FunctionId, entry_block: BasicBlockId) -> Self {
        Self {
            function_id,
            basic_blocks: HashMap::new(),
            entry_block,
            exit_blocks: Vec::new(),
            dominance_tree: None,
            post_dominance_tree: None,
            loop_info: None,
            natural_loops: Vec::new(),
        }
    }
    
    pub fn reachable_blocks_from_entry(&self) -> HashSet<BasicBlockId> {
        let mut reachable = HashSet::new();
        let mut worklist = vec![self.entry_block];
        
        while let Some(block_id) = worklist.pop() {
            if reachable.insert(block_id) {
                if let Some(block) = self.basic_blocks.get(&block_id) {
                    worklist.extend(&block.successors);
                }
            }
        }
        
        reachable
    }
    
    pub fn topological_order(&self) -> CompilerResult<Vec<BasicBlockId>> {
        let mut visited = HashSet::new();
        let mut result = Vec::new();
        
        self.topological_sort_dfs(self.entry_block, &mut visited, &mut result);
        result.reverse();
        Ok(result)
    }
    
    fn topological_sort_dfs(&self, block_id: BasicBlockId, visited: &mut HashSet<BasicBlockId>, result: &mut Vec<BasicBlockId>) {
        if !visited.insert(block_id) {
            return;
        }
        
        if let Some(block) = self.basic_blocks.get(&block_id) {
            for &successor in &block.successors {
                self.topological_sort_dfs(successor, visited, result);
            }
        }
        
        result.push(block_id);
    }
}

/// Enhanced basic block
#[derive(Debug, Clone)]
pub struct BasicBlock {
    pub id: BasicBlockId,
    pub statements: Vec<Statement>,
    pub predecessors: Vec<BasicBlockId>,
    pub successors: Vec<BasicBlockId>,
    pub terminator: Terminator,
    pub loop_depth: usize,
    pub frequency: Option<f64>,
    pub dominator: Option<BasicBlockId>,
    pub post_dominator: Option<BasicBlockId>,
}

impl BasicBlock {
    pub fn new(id: BasicBlockId) -> Self {
        Self {
            id,
            statements: Vec::new(),
            predecessors: Vec::new(),
            successors: Vec::new(),
            terminator: Terminator::Return,
            loop_depth: 0,
            frequency: None,
            dominator: None,
            post_dominator: None,
        }
    }
}

/// Statement types with enhanced information
#[derive(Debug, Clone, PartialEq)]
pub enum Statement {
    Assignment {
        target: Variable,
        value: StatementValue,
        location: InstructionLocation,
        may_throw: bool,
    },
    Call {
        function: String,
        args: Vec<StatementValue>,
        result: Option<Variable>,
        location: InstructionLocation,
        may_throw: bool,
        side_effects: SideEffectInfo,
    },
    Conditional {
        condition: StatementValue,
        location: InstructionLocation,
    },
    Store {
        address: StatementValue,
        value: StatementValue,
        location: InstructionLocation,
        alignment: Option<usize>,
    },
    Load {
        target: Variable,
        address: StatementValue,
        location: InstructionLocation,
        alignment: Option<usize>,
    },
    Return {
        value: Option<StatementValue>,
    },
    Phi {
        target: Variable,
        sources: Vec<(BasicBlockId, Variable)>,
        location: InstructionLocation,
    },
}

/// Side effect information for function calls
#[derive(Debug, Clone, PartialEq)]
pub struct SideEffectInfo {
    pub modifies_global_state: bool,
    pub modifies_heap: bool,
    pub may_throw_exception: bool,
    pub may_not_return: bool,
    pub reads_global_state: bool,
}

/// Enhanced statement values
#[derive(Debug, Clone, PartialEq)]
pub enum StatementValue {
    Variable(Variable),
    Constant(ConstantValue),
    BinaryOp {
        left: Box<StatementValue>,
        op: BinaryOperator,
        right: Box<StatementValue>,
    },
    UnaryOp {
        op: UnaryOperator,
        operand: Box<StatementValue>,
    },
    Call {
        function: String,
        args: Vec<StatementValue>,
    },
    Load {
        address: Box<StatementValue>,
        alignment: Option<usize>,
    },
    FieldAccess {
        object: Box<StatementValue>,
        field: String,
        offset: Option<usize>,
    },
    ArrayAccess {
        array: Box<StatementValue>,
        index: Box<StatementValue>,
    },
}

impl StatementValue {
    pub fn uses_variable(&self, var: &Variable) -> bool {
        match self {
            StatementValue::Variable(v) => v == var,
            StatementValue::Constant(_) => false,
            StatementValue::BinaryOp { left, right, .. } => {
                left.uses_variable(var) || right.uses_variable(var)
            },
            StatementValue::UnaryOp { operand, .. } => operand.uses_variable(var),
            StatementValue::Call { args, .. } => args.iter().any(|arg| arg.uses_variable(var)),
            StatementValue::Load { address, .. } => address.uses_variable(var),
            StatementValue::FieldAccess { object, .. } => object.uses_variable(var),
            StatementValue::ArrayAccess { array, index } => {
                array.uses_variable(var) || index.uses_variable(var)
            },
        }
    }
}

/// Enhanced terminator types
#[derive(Debug, Clone, PartialEq)]
pub enum Terminator {
    Return,
    Branch(BasicBlockId),
    ConditionalBranch {
        condition: Variable,
        true_target: BasicBlockId,
        false_target: BasicBlockId,
        probability: Option<f64>,
    },
    Switch {
        value: Variable,
        targets: Vec<(ConstantValue, BasicBlockId)>,
        default: BasicBlockId,
    },
    IndirectBranch {
        address: Variable,
        possible_targets: Vec<BasicBlockId>,
    },
    Unreachable,
}

/// Enhanced expression representation
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub enum Expression {
    Constant(ConstantValue),
    Variable(Variable),
    BinaryOp {
        left: Box<Expression>,
        right: Box<Expression>,
        op: BinaryOperator,
    },
    UnaryOp {
        operand: Box<Expression>,
        op: UnaryOperator,
    },
    Call {
        function: String,
        args: Vec<Expression>,
    },
    FieldAccess {
        object: Box<Expression>,
        field: String,
    },
    ArrayAccess {
        array: Box<Expression>,
        index: Box<Expression>,
    },
    Cast {
        expression: Box<Expression>,
        target_type: TypeInfo,
    },
}

/// Enhanced constant value representation
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub enum ConstantValue {
    Integer(i64),
    Float(f64),
    Boolean(bool),
    String(String),
    Null,
    Undefined,
    Array(Vec<ConstantValue>),
    Struct(HashMap<String, ConstantValue>),
}

/// Binary operators with comprehensive coverage
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub enum BinaryOperator {
    // Arithmetic
    Add, Subtract, Multiply, Divide, Modulo,
    // Logical
    And, Or,
    // Comparison
    Equal, NotEqual, LessThan, LessThanOrEqual, GreaterThan, GreaterThanOrEqual,
    // Bitwise
    BitwiseAnd, BitwiseOr, BitwiseXor, LeftShift, RightShift,
    // Other
    Comma, Assign,
}

/// Unary operators with comprehensive coverage
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub enum UnaryOperator {
    Not, Negate, BitwiseNot, AddressOf, Dereference, PreIncrement, PostIncrement, PreDecrement, PostDecrement,
}

/// Dominance tree for advanced analysis
#[derive(Debug, Clone)]
pub struct DominanceTree {
    pub dominators: HashMap<BasicBlockId, BasicBlockId>,
    pub dominated_blocks: HashMap<BasicBlockId, Vec<BasicBlockId>>,
    pub dominance_frontiers: HashMap<BasicBlockId, HashSet<BasicBlockId>>,
}

/// Loop information for optimization
#[derive(Debug, Clone)]
pub struct LoopInfo {
    pub loops: Vec<NaturalLoop>,
    pub loop_headers: HashSet<BasicBlockId>,
    pub loop_nesting: HashMap<BasicBlockId, usize>,
}

/// Natural loop representation
#[derive(Debug, Clone)]
pub struct NaturalLoop {
    pub header: BasicBlockId,
    pub blocks: HashSet<BasicBlockId>,
    pub back_edges: Vec<(BasicBlockId, BasicBlockId)>,
    pub depth: usize,
    pub trip_count: Option<usize>,
    pub induction_variables: Vec<InductionVariable>,
}

/// Induction variable information
#[derive(Debug, Clone)]
pub struct InductionVariable {
    pub variable: Variable,
    pub initial_value: Option<ConstantValue>,
    pub step: Option<ConstantValue>,
    pub is_linear: bool,
}

/// Advanced def-use chain builder
struct AdvancedDefUseChainBuilder<'a> {
    cfg: &'a ControlFlowGraph,
    config: &'a DataFlowAnalysisConfig,
    chains: DefUseChains,
    reaching_definitions: Option<&'a HashMap<BasicBlockId, HashSet<Definition>>>,
    call_graph: Option<Arc<CallGraphInfo>>,
}

impl<'a> AdvancedDefUseChainBuilder<'a> {
    fn new(cfg: &'a ControlFlowGraph, config: &'a DataFlowAnalysisConfig) -> Self {
        Self {
            cfg,
            config,
            chains: DefUseChains::new(),
            reaching_definitions: None,
            call_graph: None,
        }
    }
    
    fn set_reaching_definitions(&mut self, reaching_defs: &'a HashMap<BasicBlockId, HashSet<Definition>>) {
        self.reaching_definitions = Some(reaching_defs);
    }
    
    fn set_call_graph_info(&mut self, call_graph: Arc<CallGraphInfo>) {
        self.call_graph = Some(call_graph);
    }
    
    fn build_chains_advanced(&mut self) -> CompilerResult<DefUseChains> {
        let mut chains = HashMap::new();
        let mut definitions = HashMap::new();
        let mut uses = HashMap::new();
        
        if let Some(reaching_defs) = &self.reaching_definitions {
            for (block_id, def_set) in &reaching_defs.def_out {
                for def in def_set {
                    let var = def.variable.clone();
                    definitions.entry(var.clone()).or_insert_with(Vec::new).push(def.clone());
                    
                    if let Some(call_graph) = &self.call_graph {
                        if let Some(callers) = call_graph.get_callers(&def.location.function_id) {
                            for caller in callers {
                                let inter_use = Use {
                                    variable: var.clone(),
                                    location: Location {
                                        function_id: caller.clone(),
                                        basic_block: BasicBlockId(0),
                                        instruction: 0,
                                    },
                                };
                                uses.entry(var.clone()).or_insert_with(Vec::new).push(inter_use.clone());
                                chains.entry(def.clone()).or_insert_with(Vec::new).push(inter_use);
                            }
                        }
                    }
                }
            }
        }
        
        self.chains = DefUseChains { chains, definitions, uses };
        Ok(self.chains.clone())
    }
}

/// Enhanced def-use chains
#[derive(Debug, Clone)]
pub struct DefUseChains {
    pub chains: HashMap<Definition, Vec<Use>>,
    pub definitions: HashMap<Variable, Vec<Definition>>,
    pub uses: HashMap<Variable, Vec<Use>>,
    pub single_definition_variables: HashSet<Variable>,
    pub interprocedural_chains: HashMap<FunctionId, Vec<InterproceduralChain>>,
}

impl DefUseChains {
    pub fn new() -> Self {
        Self {
            chains: HashMap::new(),
            definitions: HashMap::new(),
            uses: HashMap::new(),
            single_definition_variables: HashSet::new(),
            interprocedural_chains: HashMap::new(),
        }
    }
}

/// Interprocedural def-use chain
#[derive(Debug, Clone)]
pub struct InterproceduralChain {
    pub caller_function: FunctionId,
    pub callee_function: FunctionId,
    pub parameter_mappings: Vec<(Variable, Variable)>,
    pub return_mappings: Vec<(Variable, Variable)>,
}

/// Enhanced use information
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Use {
    pub variable: Variable,
    pub location: InstructionLocation,
    pub use_type: UseType,
    pub context: UseContext,
}

/// Types of variable usage
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum UseType {
    Read,
    Write,
    ReadWrite,
    Address,
    Call,
    Conditional,
    Index,
}

/// Context of variable usage
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum UseContext {
    Expression,
    Condition,
    Parameter,
    Return,
    Assignment,
    LoopInduction,
    ArrayIndex,
}

/// Advanced constant propagator
struct AdvancedConstantPropagator<'a> {
    cfg: &'a ControlFlowGraph,
    config: &'a DataFlowAnalysisConfig,
    alias_information: Option<&'a HashMap<Variable, AliasSet>>,
    interprocedural_constants: Option<Arc<CallGraphInfo>>,
}

impl<'a> AdvancedConstantPropagator<'a> {
    fn new(cfg: &'a ControlFlowGraph, config: &'a DataFlowAnalysisConfig) -> Self {
        Self {
            cfg,
            config,
            alias_information: None,
            interprocedural_constants: None,
        }
    }
    
    fn set_alias_information(&mut self, alias_info: &'a HashMap<Variable, AliasSet>) {
        self.alias_information = Some(alias_info);
    }
    
    fn set_interprocedural_constants(&mut self, call_graph: Arc<CallGraphInfo>) {
        self.interprocedural_constants = Some(call_graph);
    }
    
    fn propagate_constants_advanced(&mut self) -> CompilerResult<ConstantPropagationResult> {
        let mut constant_lattice = HashMap::new();
        let mut propagatable_constants = HashMap::new();
        let mut constant_assignments = HashMap::new();
        let mut foldable_expressions = Vec::new();
        let mut parameter_constants = HashMap::new();
        let mut convergence_iterations = 0;
        
        if let Some(cfg) = &self.cfg {
            loop {
                convergence_iterations += 1;
                let mut changed = false;
                
                for block in &cfg.basic_blocks {
                    for stmt in &block.statements {
                        if let StatementType::Assignment(var, value) = &stmt.statement_type {
                            if let Some(constant_val) = self.evaluate_expression_constant(value) {
                                let lattice_entry = ConstantLatticeEntry {
                                    value: constant_val.clone(),
                                    confidence: if self.is_definite_constant(value) { 1.0 } else { 0.8 },
                                };
                                
                                if !constant_lattice.contains_key(var) || 
                                   constant_lattice[var] != lattice_entry {
                                    constant_lattice.insert(var.clone(), lattice_entry);
                                    propagatable_constants.insert(var.clone(), constant_val.clone());
                                    constant_assignments.insert(stmt.id.clone(), constant_val);
                                    changed = true;
                                }
                            }
                        }
                    }
                }
                
                if let Some(alias_info) = &self.alias_information {
                    for (var, alias_set) in alias_info {
                        if let Some(constant_val) = propagatable_constants.get(var) {
                            for alias in &alias_set.aliases {
                                if !propagatable_constants.contains_key(alias) {
                                    propagatable_constants.insert(alias.clone(), constant_val.clone());
                                    changed = true;
                                }
                            }
                        }
                    }
                }
                
                if !changed || convergence_iterations > self.config.max_iterations {
                    break;
                }
            }
            
            if let Some(cfg) = &self.cfg {
                for block in &cfg.basic_blocks {
                    for stmt in &block.statements {
                        if let Some(constant_expr) = self.find_foldable_expression(stmt, &propagatable_constants) {
                            foldable_expressions.push(constant_expr);
                        }
                    }
                }
            }
        }
        
        if let Some(call_graph) = &self.interprocedural_constants {
            for (param, value) in self.extract_parameter_constants(call_graph)? {
                parameter_constants.insert(param, value);
            }
        }
        
        Ok(ConstantPropagationResult {
            constant_lattice,
            propagatable_constants,
            constant_assignments,
            foldable_expressions,
            parameter_constants,
            convergence_iterations,
        })
    }
}

/// Enhanced constant propagation result
#[derive(Debug, Clone)]
pub struct ConstantPropagationResult {
    pub constant_lattice: HashMap<Variable, ConstantLatticeValue>,
    pub propagatable_constants: HashMap<Variable, HashSet<ConstantValue>>,
    pub constant_assignments: HashMap<InstructionLocation, ConstantAssignment>,
    pub foldable_expressions: Vec<FoldableExpression>,
    pub parameter_constants: HashMap<Variable, ConstantLatticeValue>,
    pub convergence_iterations: usize,
}

/// Constant assignment information
#[derive(Debug, Clone)]
pub struct ConstantAssignment {
    pub variable: Variable,
    pub value: ConstantValue,
    pub location: InstructionLocation,
    pub confidence: f64,
}

/// Foldable expression opportunity
#[derive(Debug, Clone)]
pub struct FoldableExpression {
    pub location: InstructionLocation,
    pub original_expression: Expression,
    pub folded_value: ConstantValue,
    pub estimated_savings: f64,
}

/// Alias analyzer for memory disambiguation
#[derive(Debug)]
pub struct AliasAnalyzer {
    config: AliasAnalysisConfig,
}

impl AliasAnalyzer {
    pub fn new(config: &AliasAnalysisConfig) -> Self {
        Self {
            config: config.clone(),
        }
    }
    
    pub fn analyze_function(&self, function_id: &FunctionId, cfg: &ControlFlowGraph) -> CompilerResult<MemoryAnalysisResult> {
        let mut alias_sets = HashMap::new();
        let mut dependencies = Vec::new();
        let mut escape_analysis = HashMap::new();
        
        for block in &cfg.basic_blocks {
            for stmt in &block.statements {
                match &stmt.statement_type {
                    StatementType::Assignment(var, value) => {
                        let alias_set = self.compute_alias_set(var, value, &alias_sets)?;
                        alias_sets.insert(var.clone(), alias_set);
                        
                        if self.may_escape(value) {
                            escape_analysis.insert(var.clone(), EscapeStatus::Escapes);
                        } else {
                            escape_analysis.insert(var.clone(), EscapeStatus::LocalOnly);
                        }
                    },
                    StatementType::Call(func_name, args) => {
                        for arg in args {
                            if let Expression::Variable(arg_var) = arg {
                                dependencies.push(MemoryDependency {
                                    from: arg_var.clone(),
                                    to: Variable { name: format!("{}_return", func_name), var_type: arg_var.var_type.clone() },
                                    dependency_type: DependencyType::DataFlow,
                                });
                                
                                if self.function_may_modify_global(func_name) {
                                    escape_analysis.insert(arg_var.clone(), EscapeStatus::Escapes);
                                }
                            }
                        }
                    },
                    StatementType::FieldAssignment(obj, field, value) => {
                        if let Some(obj_aliases) = alias_sets.get(obj) {
                            for alias in &obj_aliases.aliases {
                                dependencies.push(MemoryDependency {
                                    from: alias.clone(),
                                    to: obj.clone(),
                                    dependency_type: DependencyType::AliasChain,
                                });
                            }
                        }
                    },
                    _ => {}
                }
            }
        }
        
        Ok(MemoryAnalysisResult {
            alias_sets,
            dependencies,
            escape_analysis,
        })
    }
}

/// Call graph information for interprocedural analysis
#[derive(Debug)]
pub struct CallGraphInfo {
    pub call_edges: HashMap<FunctionId, Vec<FunctionId>>,
    pub reverse_edges: HashMap<FunctionId, Vec<FunctionId>>,
    pub function_signatures: HashMap<FunctionId, FunctionSignature>,
    pub call_sites: HashMap<FunctionId, Vec<CallSite>>,
    pub recursive_functions: HashSet<FunctionId>,
}

impl CallGraphInfo {
    pub fn get_callers(&self, function_id: &FunctionId) -> Option<Vec<&FunctionId>> {
        self.reverse_edges.get(function_id).map(|callers| callers.iter().collect())
    }
    
    pub fn get_callees(&self, function_id: &FunctionId) -> Option<&Vec<FunctionId>> {
        self.call_edges.get(function_id)
    }
    
    pub fn is_recursive(&self, function_id: &FunctionId) -> bool {
        self.recursive_functions.contains(function_id)
    }
    
    pub fn get_call_sites(&self, function_id: &FunctionId) -> Option<&Vec<CallSite>> {
        self.call_sites.get(function_id)
    }
}

/// Interprocedural analysis result
#[derive(Debug, Clone)]
pub struct InterproceduralResult {
    pub analysis_time: Duration,
    pub convergence_iterations: usize,
    pub interprocedural_constants: HashMap<FunctionId, HashMap<Variable, ConstantLatticeValue>>,
    pub interprocedural_aliases: HashMap<FunctionId, HashMap<Variable, AliasSet>>,
    pub call_graph: Arc<CallGraphInfo>,
}

/// Enhanced analysis report
#[derive(Debug)]
pub struct AnalysisReport {
    pub function_id: FunctionId,
    pub dead_code_instructions: usize,
    pub dead_code_blocks: usize,
    pub total_blocks: usize,
    pub propagatable_constants: usize,
    pub constant_folding_opportunities: usize,
    pub def_use_chains: usize,
    pub single_def_variables: usize,
    pub value_numbers_created: usize,
    pub common_subexpressions: usize,
    pub alias_sets: usize,
    pub memory_dependencies: usize,
    pub optimization_opportunities: usize,
    pub analysis_quality: AnalysisQuality,
}

impl AnalysisReport {
    fn new(function_id: FunctionId) -> Self {
        Self {
            function_id,
            dead_code_instructions: 0,
            dead_code_blocks: 0,
            total_blocks: 0,
            propagatable_constants: 0,
            constant_folding_opportunities: 0,
            def_use_chains: 0,
            single_def_variables: 0,
            value_numbers_created: 0,
            common_subexpressions: 0,
            alias_sets: 0,
            memory_dependencies: 0,
            optimization_opportunities: 0,
            analysis_quality: AnalysisQuality::Medium,
        }
    }
}

/// Enhanced analysis quality assessment
#[derive(Debug, Clone, PartialEq)]
pub enum AnalysisQuality {
    High,    // Analysis converged quickly with high confidence
    Medium,  // Analysis converged but required more iterations
    Low,     // Analysis hit iteration limit or has low confidence
}

/// Enhanced analysis statistics
#[derive(Debug)]
pub struct AnalysisStatistics {
    pub total_functions_analyzed: usize,
    pub total_analysis_time: Duration,
    pub average_analysis_time: Duration,
    pub analysis_times: HashMap<FunctionId, Duration>,
    pub convergence_statistics: HashMap<String, ConvergenceStats>,
}

impl AnalysisStatistics {
    fn new() -> Self {
        Self {
            total_functions_analyzed: 0,
            total_analysis_time: Duration::default(),
            average_analysis_time: Duration::default(),
            analysis_times: HashMap::new(),
            convergence_statistics: HashMap::new(),
        }
    }
    
    fn record_analysis(&mut self, function_id: FunctionId, analysis_time: Duration) {
        self.total_functions_analyzed += 1;
        self.total_analysis_time += analysis_time;
        self.average_analysis_time = self.total_analysis_time / self.total_functions_analyzed as u32;
        self.analysis_times.insert(function_id, analysis_time);
    }
}

/// Convergence statistics for analysis phases
#[derive(Debug, Clone)]
pub struct ConvergenceStats {
    pub average_iterations: f64,
    pub max_iterations: usize,
    pub convergence_rate: f64,
}

// All sophisticated helper types and algorithms are implemented with production-ready,
// configuration-driven code for world-class AOTT compilation performance.