#ifndef RUNA_VM_H
#define RUNA_VM_H

#include <vector>
#include <map>
#include <string>
#include <memory>
#include <variant>
#include <functional>
#include <chrono>
#include <iostream>
#include <deque>
#include <optional>

namespace runa {

// Forward declarations
class VMValue;
class VMFunction;
class CallFrame;
class Instruction;

// Value types for the VM
enum class ValueType {
    INTEGER,
    FLOAT,
    STRING,
    BOOLEAN,
    NULL_VALUE,
    LIST,
    DICTIONARY,
    FUNCTION,
    CLOSURE,
    BUILTIN
};

// VM execution states
enum class VMState {
    READY,
    RUNNING,
    PAUSED,
    STOPPED,
    ERROR
};

// Bytecode operation codes
enum class Opcode {
    LOAD_CONST,
    LOAD_VAR,
    STORE_VAR,
    DUP,
    POP,
    SWAP,
    BINARY_OP,
    UNARY_OP,
    JUMP,
    JUMP_IF_FALSE,
    JUMP_IF_TRUE,
    RETURN,
    CALL,
    CALL_BUILTIN,
    BUILD_LIST,
    BUILD_DICT,
    GET_ITEM,
    SET_ITEM,
    TYPE_CHECK,
    TYPE_CAST,
    AI_THINK,
    AI_LEARN,
    AI_COMMUNICATE,
    AI_TRANSLATE,
    AI_ANALYZE,
    MATCH_START,
    MATCH_CASE,
    MATCH_END,
    AWAIT,
    ASYNC_CALL,
    ALLOCATE,
    DEALLOCATE,
    PROFILE_START,
    PROFILE_END
};

// VM value representation
class VMValue {
public:
    using ValueVariant = std::variant<int64_t, double, std::string, bool, 
                                     std::vector<VMValue>, std::map<std::string, VMValue>>;

    VMValue();
    VMValue(int64_t value);
    VMValue(double value);
    VMValue(const std::string& value);
    VMValue(bool value);
    VMValue(std::nullptr_t);
    VMValue(const std::vector<VMValue>& value);
    VMValue(const std::map<std::string, VMValue>& value);

    ValueType getType() const { return type_; }
    const ValueVariant& getValue() const { return value_; }
    
    // Type-specific getters
    int64_t asInteger() const;
    double asFloat() const;
    const std::string& asString() const;
    bool asBoolean() const;
    const std::vector<VMValue>& asList() const;
    const std::map<std::string, VMValue>& asDictionary() const;
    
    // Type checking
    bool isInteger() const { return type_ == ValueType::INTEGER; }
    bool isFloat() const { return type_ == ValueType::FLOAT; }
    bool isString() const { return type_ == ValueType::STRING; }
    bool isBoolean() const { return type_ == ValueType::BOOLEAN; }
    bool isNull() const { return type_ == ValueType::NULL_VALUE; }
    bool isList() const { return type_ == ValueType::LIST; }
    bool isDictionary() const { return type_ == ValueType::DICTIONARY; }
    bool isFunction() const { return type_ == ValueType::FUNCTION; }
    
    // Truthiness check
    bool isTruthy() const;
    
    // String representation
    std::string toString() const;

private:
    ValueType type_;
    ValueVariant value_;
};

// Function representation
class VMFunction {
public:
    VMFunction(const std::string& name, 
               const std::vector<std::string>& parameters,
               int localsCount,
               const std::vector<Instruction>& instructions,
               int lineNumber = 0,
               const std::string& sourceFile = "");

    const std::string& getName() const { return name_; }
    const std::vector<std::string>& getParameters() const { return parameters_; }
    int getLocalsCount() const { return localsCount_; }
    const std::vector<Instruction>& getInstructions() const { return instructions_; }
    int getLineNumber() const { return lineNumber_; }
    const std::string& getSourceFile() const { return sourceFile_; }

private:
    std::string name_;
    std::vector<std::string> parameters_;
    int localsCount_;
    std::vector<Instruction> instructions_;
    int lineNumber_;
    std::string sourceFile_;
};

// Instruction representation
class Instruction {
public:
    Instruction(Opcode opcode, 
                const std::map<std::string, VMValue>& args = {},
                int lineNumber = 0,
                const std::string& sourceInfo = "");

    Opcode getOpcode() const { return opcode_; }
    const std::map<std::string, VMValue>& getArgs() const { return args_; }
    int getLineNumber() const { return lineNumber_; }
    const std::string& getSourceInfo() const { return sourceInfo_; }

private:
    Opcode opcode_;
    std::map<std::string, VMValue> args_;
    int lineNumber_;
    std::string sourceInfo_;
};

// Call frame for function execution
class CallFrame {
public:
    CallFrame(const VMFunction& function, int basePointer = 0);

    const VMFunction& getFunction() const { return function_; }
    int getInstructionPointer() const { return instructionPointer_; }
    int getBasePointer() const { return basePointer_; }
    std::optional<int> getReturnAddress() const { return returnAddress_; }
    const std::map<std::string, VMValue>& getLocals() const { return locals_; }

    void setInstructionPointer(int ip) { instructionPointer_ = ip; }
    void setReturnAddress(int address) { returnAddress_ = address; }
    void setLocal(const std::string& name, const VMValue& value) { locals_[name] = value; }
    std::optional<VMValue> getLocal(const std::string& name) const;

private:
    const VMFunction& function_;
    int instructionPointer_;
    int basePointer_;
    std::optional<int> returnAddress_;
    std::map<std::string, VMValue> locals_;
};

// Performance monitoring
struct ExecutionStats {
    uint64_t totalInstructions = 0;
    uint64_t totalExecutions = 0;
    double averageExecutionTimeMs = 0.0;
    size_t memoryUsageBytes = 0;
    uint64_t gcCollections = 0;
    std::map<std::string, uint64_t> instructionCounts;
};

// Main VM class
class RunaVM {
public:
    RunaVM();
    ~RunaVM();

    // Main execution interface
    VMValue execute(const std::vector<std::map<std::string, VMValue>>& bytecode, bool debug = false);
    
    // State management
    VMState getState() const { return state_; }
    void pause() { if (state_ == VMState::RUNNING) state_ = VMState::PAUSED; }
    void resume() { if (state_ == VMState::PAUSED) state_ = VMState::RUNNING; }
    void stop() { state_ = VMState::STOPPED; }

    // Memory management
    void setGCThreshold(size_t threshold) { gcThreshold_ = threshold; }
    void forceGC();

    // Debugging support
    void setDebugMode(bool debug) { debugMode_ = debug; }
    void setBreakpoint(int instructionIndex) { breakpoints_[instructionIndex] = true; }
    void clearBreakpoint(int instructionIndex) { breakpoints_.erase(instructionIndex); }
    void addWatchVariable(const std::string& name) { watchVariables_.insert(name); }
    void removeWatchVariable(const std::string& name) { watchVariables_.erase(name); }

    // Statistics
    const ExecutionStats& getExecutionStats() const { return executionStats_; }
    void resetStats();

    // Built-in functions
    using BuiltinFunction = std::function<VMValue(RunaVM*)>;
    void registerBuiltin(const std::string& name, BuiltinFunction func);

private:
    // VM state
    VMState state_;
    std::deque<CallFrame> callStack_;
    std::deque<VMValue> operandStack_;
    std::map<std::string, VMValue> globals_;
    std::vector<VMValue> constants_;

    // Memory management
    std::map<int, VMValue> heap_;
    int nextHeapId_;
    size_t gcThreshold_;

    // Performance tracking
    uint64_t instructionCount_;
    std::chrono::high_resolution_clock::time_point startTime_;
    ExecutionStats executionStats_;

    // Built-in functions
    std::map<std::string, BuiltinFunction> builtins_;

    // Debugging support
    bool debugMode_;
    std::map<int, bool> breakpoints_;
    std::set<std::string> watchVariables_;

    // Internal methods
    std::map<std::string, VMFunction> parseBytecode(const std::vector<std::map<std::string, VMValue>>& bytecode);
    VMValue executeLoop();
    void executeInstruction(const Instruction& instruction, CallFrame& frame);
    
    // Instruction execution methods
    void executeLoadConst(const Instruction& instruction, CallFrame& frame);
    void executeLoadVar(const Instruction& instruction, CallFrame& frame);
    void executeStoreVar(const Instruction& instruction, CallFrame& frame);
    void executeBinaryOp(const Instruction& instruction, CallFrame& frame);
    void executeUnaryOp(const Instruction& instruction, CallFrame& frame);
    void executeCall(const Instruction& instruction, CallFrame& frame);
    void executeReturn(const Instruction& instruction, CallFrame& frame);
    void executeJump(const Instruction& instruction, CallFrame& frame);
    void executeJumpIfFalse(const Instruction& instruction, CallFrame& frame);
    void executeBuildList(const Instruction& instruction, CallFrame& frame);
    void executeBuildDict(const Instruction& instruction, CallFrame& frame);
    void executeGetItem(const Instruction& instruction, CallFrame& frame);
    void executeSetItem(const Instruction& instruction, CallFrame& frame);
    void executeDup(const Instruction& instruction, CallFrame& frame);
    void executePop(const Instruction& instruction, CallFrame& frame);

    // Helper methods
    VMValue applyBinaryOperator(const VMValue& left, const VMValue& right, const std::string& operator_);
    VMValue applyUnaryOperator(const VMValue& operand, const std::string& operator_);
    VMValue pythonToVMValue(const std::map<std::string, VMValue>& value);
    
    // Built-in function implementations
    VMValue builtinPrint();
    VMValue builtinLen();
    VMValue builtinStr();
    VMValue builtinInt();
    VMValue builtinFloat();
    VMValue builtinBool();
    
    // Performance monitoring
    void updateExecutionStats(double executionTimeMs);
    size_t getMemoryUsage() const;
    
    // Initialization
    void initializeBuiltins();
};

} // namespace runa

#endif // RUNA_VM_H 