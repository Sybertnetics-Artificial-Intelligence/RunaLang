#include "vm.h"
#include <algorithm>
#include <sstream>
#include <stdexcept>
#include <set>

namespace runa {

// VMValue implementation
VMValue::VMValue() : type_(ValueType::NULL_VALUE), value_(std::monostate{}) {}

VMValue::VMValue(int64_t value) : type_(ValueType::INTEGER), value_(value) {}

VMValue::VMValue(double value) : type_(ValueType::FLOAT), value_(value) {}

VMValue::VMValue(const std::string& value) : type_(ValueType::STRING), value_(value) {}

VMValue::VMValue(bool value) : type_(ValueType::BOOLEAN), value_(value) {}

VMValue::VMValue(std::nullptr_t) : type_(ValueType::NULL_VALUE), value_(std::monostate{}) {}

VMValue::VMValue(const std::vector<VMValue>& value) : type_(ValueType::LIST), value_(value) {}

VMValue::VMValue(const std::map<std::string, VMValue>& value) : type_(ValueType::DICTIONARY), value_(value) {}

int64_t VMValue::asInteger() const {
    if (type_ == ValueType::INTEGER) {
        return std::get<int64_t>(value_);
    }
    throw std::runtime_error("Value is not an integer");
}

double VMValue::asFloat() const {
    if (type_ == ValueType::FLOAT) {
        return std::get<double>(value_);
    }
    throw std::runtime_error("Value is not a float");
}

const std::string& VMValue::asString() const {
    if (type_ == ValueType::STRING) {
        return std::get<std::string>(value_);
    }
    throw std::runtime_error("Value is not a string");
}

bool VMValue::asBoolean() const {
    if (type_ == ValueType::BOOLEAN) {
        return std::get<bool>(value_);
    }
    throw std::runtime_error("Value is not a boolean");
}

const std::vector<VMValue>& VMValue::asList() const {
    if (type_ == ValueType::LIST) {
        return std::get<std::vector<VMValue>>(value_);
    }
    throw std::runtime_error("Value is not a list");
}

const std::map<std::string, VMValue>& VMValue::asDictionary() const {
    if (type_ == ValueType::DICTIONARY) {
        return std::get<std::map<std::string, VMValue>>(value_);
    }
    throw std::runtime_error("Value is not a dictionary");
}

bool VMValue::isTruthy() const {
    switch (type_) {
        case ValueType::NULL_VALUE:
            return false;
        case ValueType::BOOLEAN:
            return asBoolean();
        case ValueType::INTEGER:
            return asInteger() != 0;
        case ValueType::FLOAT:
            return asFloat() != 0.0;
        case ValueType::STRING:
            return !asString().empty();
        case ValueType::LIST:
            return !asList().empty();
        case ValueType::DICTIONARY:
            return !asDictionary().empty();
        default:
            return true;
    }
}

std::string VMValue::toString() const {
    switch (type_) {
        case ValueType::NULL_VALUE:
            return "null";
        case ValueType::INTEGER:
            return std::to_string(asInteger());
        case ValueType::FLOAT:
            return std::to_string(asFloat());
        case ValueType::STRING:
            return asString();
        case ValueType::BOOLEAN:
            return asBoolean() ? "true" : "false";
        case ValueType::LIST:
            return "[list]";
        case ValueType::DICTIONARY:
            return "{dictionary}";
        case ValueType::FUNCTION:
            return "[function]";
        default:
            return "[unknown]";
    }
}

// VMFunction implementation
VMFunction::VMFunction(const std::string& name, 
                       const std::vector<std::string>& parameters,
                       int localsCount,
                       const std::vector<Instruction>& instructions,
                       int lineNumber,
                       const std::string& sourceFile)
    : name_(name), parameters_(parameters), localsCount_(localsCount),
      instructions_(instructions), lineNumber_(lineNumber), sourceFile_(sourceFile) {}

// Instruction implementation
Instruction::Instruction(Opcode opcode, 
                         const std::map<std::string, VMValue>& args,
                         int lineNumber,
                         const std::string& sourceInfo)
    : opcode_(opcode), args_(args), lineNumber_(lineNumber), sourceInfo_(sourceInfo) {}

// CallFrame implementation
CallFrame::CallFrame(const VMFunction& function, int basePointer)
    : function_(function), instructionPointer_(0), basePointer_(basePointer) {}

std::optional<VMValue> CallFrame::getLocal(const std::string& name) const {
    auto it = locals_.find(name);
    if (it != locals_.end()) {
        return it->second;
    }
    return std::nullopt;
}

// RunaVM implementation
RunaVM::RunaVM() 
    : state_(VMState::READY), nextHeapId_(1), gcThreshold_(1000),
      instructionCount_(0), debugMode_(false) {
    initializeBuiltins();
}

RunaVM::~RunaVM() = default;

VMValue RunaVM::execute(const std::vector<std::map<std::string, VMValue>>& bytecode, bool debug) {
    auto startTime = std::chrono::high_resolution_clock::now();
    
    try {
        // Reset VM state
        state_ = VMState::RUNNING;
        callStack_.clear();
        operandStack_.clear();
        globals_.clear();
        constants_.clear();
        heap_.clear();
        nextHeapId_ = 1;
        instructionCount_ = 0;
        debugMode_ = debug;
        
        // Parse bytecode
        auto functions = parseBytecode(bytecode);
        
        // Find main function
        auto mainIt = functions.find("main");
        if (mainIt == functions.end()) {
            throw std::runtime_error("No main function found in bytecode");
        }
        
        // Create initial call frame
        CallFrame initialFrame(mainIt->second);
        callStack_.push_back(initialFrame);
        
        // Execute
        VMValue result = executeLoop();
        
        // Update execution statistics
        auto endTime = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::microseconds>(endTime - startTime);
        double executionTimeMs = duration.count() / 1000.0;
        updateExecutionStats(executionTimeMs);
        
        state_ = VMState::STOPPED;
        return result;
        
    } catch (const std::exception& e) {
        state_ = VMState::ERROR;
        throw;
    }
}

std::map<std::string, VMFunction> RunaVM::parseBytecode(const std::vector<std::map<std::string, VMValue>>& bytecode) {
    std::map<std::string, VMFunction> functions;
    
    for (const auto& instructionData : bytecode) {
        auto typeIt = instructionData.find("type");
        if (typeIt == instructionData.end()) continue;
        
        if (typeIt->second.asString() == "function") {
            auto nameIt = instructionData.find("name");
            auto paramsIt = instructionData.find("parameters");
            auto localsIt = instructionData.find("locals_count");
            auto lineIt = instructionData.find("line_number");
            auto sourceIt = instructionData.find("source_file");
            
            std::string name = nameIt != instructionData.end() ? nameIt->second.asString() : "";
            std::vector<std::string> parameters;
            if (paramsIt != instructionData.end() && paramsIt->second.isList()) {
                for (const auto& param : paramsIt->second.asList()) {
                    parameters.push_back(param.asString());
                }
            }
            int localsCount = localsIt != instructionData.end() ? localsIt->second.asInteger() : 0;
            int lineNumber = lineIt != instructionData.end() ? lineIt->second.asInteger() : 0;
            std::string sourceFile = sourceIt != instructionData.end() ? sourceIt->second.asString() : "";
            
            std::vector<Instruction> instructions;
            VMFunction function(name, parameters, localsCount, instructions, lineNumber, sourceFile);
            functions[name] = function;
        }
    }
    
    return functions;
}

VMValue RunaVM::executeLoop() {
    while (state_ == VMState::RUNNING && !callStack_.empty()) {
        CallFrame& currentFrame = callStack_.back();
        
        // Check for breakpoint
        if (debugMode_ && breakpoints_.find(currentFrame.getInstructionPointer()) != breakpoints_.end()) {
            state_ = VMState::PAUSED;
            break;
        }
        
        // Execute next instruction
        if (currentFrame.getInstructionPointer() >= currentFrame.getFunction().getInstructions().size()) {
            // Function completed
            VMValue result = operandStack_.empty() ? VMValue(nullptr) : operandStack_.back();
            if (!operandStack_.empty()) operandStack_.pop_back();
            callStack_.pop_back();
            
            if (!callStack_.empty()) {
                // Return to caller
                operandStack_.push_back(result);
            } else {
                // Program completed
                return result;
            }
        } else {
            // Execute instruction
            const Instruction& instruction = currentFrame.getFunction().getInstructions()[currentFrame.getInstructionPointer()];
            executeInstruction(instruction, currentFrame);
            currentFrame.setInstructionPointer(currentFrame.getInstructionPointer() + 1);
            instructionCount_++;
        }
    }
    
    // Return top of stack or null
    return operandStack_.empty() ? VMValue(nullptr) : operandStack_.back();
}

void RunaVM::executeInstruction(const Instruction& instruction, CallFrame& frame) {
    switch (instruction.getOpcode()) {
        case Opcode::LOAD_CONST:
            executeLoadConst(instruction, frame);
            break;
        case Opcode::LOAD_VAR:
            executeLoadVar(instruction, frame);
            break;
        case Opcode::STORE_VAR:
            executeStoreVar(instruction, frame);
            break;
        case Opcode::BINARY_OP:
            executeBinaryOp(instruction, frame);
            break;
        case Opcode::UNARY_OP:
            executeUnaryOp(instruction, frame);
            break;
        case Opcode::CALL:
            executeCall(instruction, frame);
            break;
        case Opcode::RETURN:
            executeReturn(instruction, frame);
            break;
        case Opcode::JUMP:
            executeJump(instruction, frame);
            break;
        case Opcode::JUMP_IF_FALSE:
            executeJumpIfFalse(instruction, frame);
            break;
        case Opcode::BUILD_LIST:
            executeBuildList(instruction, frame);
            break;
        case Opcode::BUILD_DICT:
            executeBuildDict(instruction, frame);
            break;
        case Opcode::GET_ITEM:
            executeGetItem(instruction, frame);
            break;
        case Opcode::SET_ITEM:
            executeSetItem(instruction, frame);
            break;
        case Opcode::DUP:
            executeDup(instruction, frame);
            break;
        case Opcode::POP:
            executePop(instruction, frame);
            break;
        default:
            throw std::runtime_error("Unsupported opcode: " + std::to_string(static_cast<int>(instruction.getOpcode())));
    }
}

void RunaVM::executeLoadConst(const Instruction& instruction, CallFrame& frame) {
    auto valueIt = instruction.getArgs().find("value");
    if (valueIt != instruction.getArgs().end()) {
        operandStack_.push_back(valueIt->second);
    }
}

void RunaVM::executeLoadVar(const Instruction& instruction, CallFrame& frame) {
    auto nameIt = instruction.getArgs().find("name");
    if (nameIt == instruction.getArgs().end()) {
        throw std::runtime_error("LOAD_VAR missing name argument");
    }
    
    std::string varName = nameIt->second.asString();
    
    // Check locals first
    auto localValue = frame.getLocal(varName);
    if (localValue) {
        operandStack_.push_back(*localValue);
        return;
    }
    
    // Check globals
    auto globalIt = globals_.find(varName);
    if (globalIt != globals_.end()) {
        operandStack_.push_back(globalIt->second);
        return;
    }
    
    throw std::runtime_error("Undefined variable: " + varName);
}

void RunaVM::executeStoreVar(const Instruction& instruction, CallFrame& frame) {
    auto nameIt = instruction.getArgs().find("name");
    if (nameIt == instruction.getArgs().end()) {
        throw std::runtime_error("STORE_VAR missing name argument");
    }
    
    if (operandStack_.empty()) {
        throw std::runtime_error("STORE_VAR: operand stack empty");
    }
    
    std::string varName = nameIt->second.asString();
    VMValue value = operandStack_.back();
    operandStack_.pop_back();
    
    frame.setLocal(varName, value);
}

void RunaVM::executeBinaryOp(const Instruction& instruction, CallFrame& frame) {
    if (operandStack_.size() < 2) {
        throw std::runtime_error("BINARY_OP: insufficient operands");
    }
    
    VMValue right = operandStack_.back();
    operandStack_.pop_back();
    VMValue left = operandStack_.back();
    operandStack_.pop_back();
    
    auto operatorIt = instruction.getArgs().find("operator");
    std::string op = operatorIt != instruction.getArgs().end() ? operatorIt->second.asString() : "+";
    
    VMValue result = applyBinaryOperator(left, right, op);
    operandStack_.push_back(result);
}

void RunaVM::executeUnaryOp(const Instruction& instruction, CallFrame& frame) {
    if (operandStack_.empty()) {
        throw std::runtime_error("UNARY_OP: operand stack empty");
    }
    
    VMValue operand = operandStack_.back();
    operandStack_.pop_back();
    
    auto operatorIt = instruction.getArgs().find("operator");
    std::string op = operatorIt != instruction.getArgs().end() ? operatorIt->second.asString() : "-";
    
    VMValue result = applyUnaryOperator(operand, op);
    operandStack_.push_back(result);
}

void RunaVM::executeCall(const Instruction& instruction, CallFrame& frame) {
    auto functionIt = instruction.getArgs().find("function");
    if (functionIt == instruction.getArgs().end()) {
        throw std::runtime_error("CALL missing function argument");
    }
    
    std::string functionName = functionIt->second.asString();
    
    // Check built-in functions
    auto builtinIt = builtins_.find(functionName);
    if (builtinIt != builtins_.end()) {
        VMValue result = builtinIt->second(this);
        operandStack_.push_back(result);
        return;
    }
    
    // For now, just pop the function and arguments
    // Full function call implementation would go here
    throw std::runtime_error("Function call not implemented: " + functionName);
}

void RunaVM::executeReturn(const Instruction& instruction, CallFrame& frame) {
    // Return value is already on the stack
}

void RunaVM::executeJump(const Instruction& instruction, CallFrame& frame) {
    auto targetIt = instruction.getArgs().find("target");
    if (targetIt == instruction.getArgs().end()) {
        throw std::runtime_error("JUMP missing target argument");
    }
    
    int target = targetIt->second.asInteger();
    frame.setInstructionPointer(target - 1); // -1 because ip will be incremented after
}

void RunaVM::executeJumpIfFalse(const Instruction& instruction, CallFrame& frame) {
    if (operandStack_.empty()) {
        throw std::runtime_error("JUMP_IF_FALSE: operand stack empty");
    }
    
    VMValue condition = operandStack_.back();
    operandStack_.pop_back();
    
    auto targetIt = instruction.getArgs().find("target");
    if (targetIt == instruction.getArgs().end()) {
        throw std::runtime_error("JUMP_IF_FALSE missing target argument");
    }
    
    int target = targetIt->second.asInteger();
    
    if (!condition.isTruthy()) {
        frame.setInstructionPointer(target - 1); // -1 because ip will be incremented after
    }
}

void RunaVM::executeBuildList(const Instruction& instruction, CallFrame& frame) {
    auto countIt = instruction.getArgs().find("count");
    int count = countIt != instruction.getArgs().end() ? countIt->second.asInteger() : 0;
    
    std::vector<VMValue> elements;
    for (int i = 0; i < count; ++i) {
        if (operandStack_.empty()) {
            throw std::runtime_error("BUILD_LIST: insufficient operands");
        }
        elements.insert(elements.begin(), operandStack_.back());
        operandStack_.pop_back();
    }
    
    operandStack_.push_back(VMValue(elements));
}

void RunaVM::executeBuildDict(const Instruction& instruction, CallFrame& frame) {
    auto countIt = instruction.getArgs().find("count");
    int count = countIt != instruction.getArgs().end() ? countIt->second.asInteger() : 0;
    
    std::map<std::string, VMValue> items;
    for (int i = 0; i < count; ++i) {
        if (operandStack_.size() < 2) {
            throw std::runtime_error("BUILD_DICT: insufficient operands");
        }
        VMValue value = operandStack_.back();
        operandStack_.pop_back();
        VMValue key = operandStack_.back();
        operandStack_.pop_back();
        items[key.asString()] = value;
    }
    
    operandStack_.push_back(VMValue(items));
}

void RunaVM::executeGetItem(const Instruction& instruction, CallFrame& frame) {
    if (operandStack_.size() < 2) {
        throw std::runtime_error("GET_ITEM: insufficient operands");
    }
    
    VMValue key = operandStack_.back();
    operandStack_.pop_back();
    VMValue container = operandStack_.back();
    operandStack_.pop_back();
    
    if (container.isList()) {
        int64_t index = key.asInteger();
        const auto& list = container.asList();
        if (index >= 0 && index < static_cast<int64_t>(list.size())) {
            operandStack_.push_back(list[index]);
        } else {
            throw std::runtime_error("List index out of range: " + std::to_string(index));
        }
    } else if (container.isDictionary()) {
        const auto& dict = container.asDictionary();
        auto it = dict.find(key.asString());
        if (it != dict.end()) {
            operandStack_.push_back(it->second);
        } else {
            throw std::runtime_error("Dictionary key not found: " + key.asString());
        }
    } else {
        throw std::runtime_error("Cannot get item from " + container.toString());
    }
}

void RunaVM::executeSetItem(const Instruction& instruction, CallFrame& frame) {
    if (operandStack_.size() < 3) {
        throw std::runtime_error("SET_ITEM: insufficient operands");
    }
    
    VMValue value = operandStack_.back();
    operandStack_.pop_back();
    VMValue key = operandStack_.back();
    operandStack_.pop_back();
    VMValue container = operandStack_.back();
    operandStack_.pop_back();
    
    // Note: This is a simplified implementation
    // In a real implementation, you'd need to handle mutable containers properly
    operandStack_.push_back(container);
}

void RunaVM::executeDup(const Instruction& instruction, CallFrame& frame) {
    if (operandStack_.empty()) {
        throw std::runtime_error("DUP: operand stack empty");
    }
    operandStack_.push_back(operandStack_.back());
}

void RunaVM::executePop(const Instruction& instruction, CallFrame& frame) {
    if (operandStack_.empty()) {
        throw std::runtime_error("POP: operand stack empty");
    }
    operandStack_.pop_back();
}

VMValue RunaVM::applyBinaryOperator(const VMValue& left, const VMValue& right, const std::string& operator_) {
    if (operator_ == "+") {
        if (left.isInteger() && right.isInteger()) {
            return VMValue(left.asInteger() + right.asInteger());
        } else if (left.isString() && right.isString()) {
            return VMValue(left.asString() + right.asString());
        } else {
            throw std::runtime_error("Cannot add " + left.toString() + " and " + right.toString());
        }
    } else if (operator_ == "-") {
        if (left.isInteger() && right.isInteger()) {
            return VMValue(left.asInteger() - right.asInteger());
        } else {
            throw std::runtime_error("Cannot subtract " + left.toString() + " and " + right.toString());
        }
    } else if (operator_ == "*") {
        if (left.isInteger() && right.isInteger()) {
            return VMValue(left.asInteger() * right.asInteger());
        } else {
            throw std::runtime_error("Cannot multiply " + left.toString() + " and " + right.toString());
        }
    } else if (operator_ == "/") {
        if (left.isInteger() && right.isInteger()) {
            return VMValue(static_cast<double>(left.asInteger()) / right.asInteger());
        } else {
            throw std::runtime_error("Cannot divide " + left.toString() + " and " + right.toString());
        }
    } else {
        throw std::runtime_error("Unsupported binary operator: " + operator_);
    }
}

VMValue RunaVM::applyUnaryOperator(const VMValue& operand, const std::string& operator_) {
    if (operator_ == "-") {
        if (operand.isInteger()) {
            return VMValue(-operand.asInteger());
        } else if (operand.isFloat()) {
            return VMValue(-operand.asFloat());
        } else {
            throw std::runtime_error("Cannot negate " + operand.toString());
        }
    } else if (operator_ == "!") {
        if (operand.isBoolean()) {
            return VMValue(!operand.asBoolean());
        } else {
            throw std::runtime_error("Cannot negate " + operand.toString());
        }
    } else {
        throw std::runtime_error("Unsupported unary operator: " + operator_);
    }
}

void RunaVM::initializeBuiltins() {
    builtins_["print"] = [this](RunaVM* vm) { return builtinPrint(); };
    builtins_["len"] = [this](RunaVM* vm) { return builtinLen(); };
    builtins_["str"] = [this](RunaVM* vm) { return builtinStr(); };
    builtins_["int"] = [this](RunaVM* vm) { return builtinInt(); };
    builtins_["float"] = [this](RunaVM* vm) { return builtinFloat(); };
    builtins_["bool"] = [this](RunaVM* vm) { return builtinBool(); };
}

VMValue RunaVM::builtinPrint() {
    if (operandStack_.empty()) {
        throw std::runtime_error("print: operand stack empty");
    }
    VMValue value = operandStack_.back();
    operandStack_.pop_back();
    std::cout << value.toString() << std::endl;
    return VMValue(nullptr);
}

VMValue RunaVM::builtinLen() {
    if (operandStack_.empty()) {
        throw std::runtime_error("len: operand stack empty");
    }
    VMValue value = operandStack_.back();
    operandStack_.pop_back();
    
    if (value.isString()) {
        return VMValue(static_cast<int64_t>(value.asString().length()));
    } else if (value.isList()) {
        return VMValue(static_cast<int64_t>(value.asList().size()));
    } else if (value.isDictionary()) {
        return VMValue(static_cast<int64_t>(value.asDictionary().size()));
    } else {
        throw std::runtime_error("Cannot get length of " + value.toString());
    }
}

VMValue RunaVM::builtinStr() {
    if (operandStack_.empty()) {
        throw std::runtime_error("str: operand stack empty");
    }
    VMValue value = operandStack_.back();
    operandStack_.pop_back();
    return VMValue(value.toString());
}

VMValue RunaVM::builtinInt() {
    if (operandStack_.empty()) {
        throw std::runtime_error("int: operand stack empty");
    }
    VMValue value = operandStack_.back();
    operandStack_.pop_back();
    
    try {
        if (value.isInteger()) {
            return value;
        } else if (value.isString()) {
            return VMValue(std::stoll(value.asString()));
        } else {
            throw std::runtime_error("Cannot convert " + value.toString() + " to integer");
        }
    } catch (const std::exception& e) {
        throw std::runtime_error("Cannot convert " + value.toString() + " to integer");
    }
}

VMValue RunaVM::builtinFloat() {
    if (operandStack_.empty()) {
        throw std::runtime_error("float: operand stack empty");
    }
    VMValue value = operandStack_.back();
    operandStack_.pop_back();
    
    try {
        if (value.isFloat()) {
            return value;
        } else if (value.isInteger()) {
            return VMValue(static_cast<double>(value.asInteger()));
        } else if (value.isString()) {
            return VMValue(std::stod(value.asString()));
        } else {
            throw std::runtime_error("Cannot convert " + value.toString() + " to float");
        }
    } catch (const std::exception& e) {
        throw std::runtime_error("Cannot convert " + value.toString() + " to float");
    }
}

VMValue RunaVM::builtinBool() {
    if (operandStack_.empty()) {
        throw std::runtime_error("bool: operand stack empty");
    }
    VMValue value = operandStack_.back();
    operandStack_.pop_back();
    return VMValue(value.isTruthy());
}

void RunaVM::updateExecutionStats(double executionTimeMs) {
    executionStats_.totalInstructions += instructionCount_;
    executionStats_.totalExecutions++;
    
    // Update average execution time
    double currentAvg = executionStats_.averageExecutionTimeMs;
    uint64_t totalExecutions = executionStats_.totalExecutions;
    executionStats_.averageExecutionTimeMs = (currentAvg * (totalExecutions - 1) + executionTimeMs) / totalExecutions;
    
    // Update memory usage
    executionStats_.memoryUsageBytes = getMemoryUsage();
}

size_t RunaVM::getMemoryUsage() const {
    // Simplified memory usage calculation
    size_t usage = 0;
    usage += heap_.size() * sizeof(VMValue);
    usage += globals_.size() * sizeof(VMValue);
    usage += operandStack_.size() * sizeof(VMValue);
    usage += callStack_.size() * sizeof(CallFrame);
    return usage;
}

void RunaVM::resetStats() {
    executionStats_ = ExecutionStats{};
}

void RunaVM::forceGC() {
    // Simplified garbage collection
    // In a real implementation, this would mark and sweep unreachable objects
    executionStats_.gcCollections++;
}

} // namespace runa 