# Runa Development Phase Roadmap

## 🎉 **Current Status: Phase 1.5 COMPLETE**
✅ Full compilation pipeline (Phase 1.4)
✅ Foundation fixes (Phase 1.5): conditionals, loops, display, function calls, process definitions

---

## 🚀 **Next Major Milestone: Phase 2.0 – Jump to Self-Hosting**
**Timeline: 2-3 months**

What We'll Build:
1. 🔥 Rewrite `lexer.py` in Runa – Natural-language lexer written in Runa itself
2. 🔥 Rewrite `parser.py` in Runa – Full parser in Runa
3. 🔥 Rewrite `semantic.py` / IR visitor in Runa – core of the compiler in its own language
4. 🔥 Bootstrap Compiler – Runa compiler compiles itself (self-hosting!)
5. 🎯 CI pipeline to compile the Runa compiler using the existing Python implementation and then recompile itself for verification.

**Success Criteria**
- The Runa compiler written in Runa produces identical Python output as the reference compiler for the full test-suite.
- All current 60+ tests run against the self-hosted compiler.
- Build process integrated into `make self-host` & `runa-dev.bat self-host` commands.

---

## 🗺️ **High-Level Phase Timeline**

| Phase | Duration | Key Deliverables |
|-------|----------|------------------|
| 2.0-A | 2 weeks  | Minimal Runa standard library, I/O helpers in Runa |
| 2.0-B | 3 weeks  | Lexer in Runa + tests |
| 2.0-C | 3 weeks  | Parser in Runa + tests |
| 2.0-D | 3 weeks  | Semantic + IR visitor in Runa |
| 2.0-E | 1 week   | Bootstrap script & CI, self-hosting demo |

> ⚠️  Prerequisite: keep Phase 1.5 green; any regression blocks the branch.

---

## ✅ **Completed Phases Recap**
- Phase 1.1 Lexer ✅
- Phase 1.2 Parser ✅
- Phase 1.3 Semantic Analyzer ✅
- Phase 1.4 IR & Python Code Gen ✅
- Phase 1.5 Foundation Fixes ✅

---

## **🔥 DECISION POINT: What Should Phase 1.5 Be?**

We have two paths forward:

### **Option A: Phase 1.5 - Solidify Foundation** ⚡ (RECOMMENDED FIRST)
**Timeline: 1-2 weeks**  
**Goal: Fix current issues, complete Runa language features**

#### **Immediate Fixes Needed:**
1. **Fix Conditional Control Flow** - If/Otherwise statements not generating proper Python control flow
2. **Function Call Arguments** - Complex named parameter handling broken  
3. **Display Statement Formatting** - Message prefix/suffix handling incorrect
4. **Loop Constructs** - Add While/For loop compilation support
5. **Process Definitions** - Implement Runa function/process definitions

#### **Why This First:**
- 🎯 Completes the Runa language implementation
- 🎯 Provides solid foundation for bigger goals  
- 🎯 Quick wins that prove concept fully
- 🎯 Essential for self-hosting (we need working control flow!)

### **Option B: Phase 2.0 - Universal Translation** 🚀 (THE BIG VISION)
**Timeline: 2-3 months**  
**Goal: True universal translation platform**

#### **The Big Goals You're Excited About:**
1. **Self-Hosting Runa Compiler** - Write Runa compiler in Runa itself
2. **Multi-Target Code Generation** - JavaScript, C++, WebAssembly outputs  
3. **AI-First Universal Translation** - Cross-language intelligent translation
4. **Multiple Input Languages** - Parse JavaScript, Python, C++ → IR

---

## **🎯 RECOMMENDED APPROACH:**

### **Phase 1.5: Solidify Foundation** (Do This First!)
**Goal: Complete working Runa language compiler**

```
Week 1-2: Fix Core Issues
✅ Fix conditional control flow generation
✅ Fix function call argument handling  
✅ Fix display statement formatting
✅ Add loop constructs compilation
✅ Add process/function definitions

Result: 100% working Runa language compiler
```

### **Phase 2.0: Self-Hosting** (Then This!)
**Goal: Write Runa compiler in Runa itself**

```
Week 3-6: Self-Hosting Implementation
🔥 Rewrite lexer.py in Runa natural language
🔥 Rewrite parser.py in Runa natural language  
🔥 Rewrite semantic.py in Runa natural language
🔥 Bootstrap: Runa compiler compiles itself!

Result: Self-hosting Runa compiler (MASSIVE milestone!)
```

### **Phase 2.1: Multi-Target Generation** 
**Goal: Multiple output languages**

```
Week 7-10: Additional Code Generators
🔥 IR → JavaScript generator
🔥 IR → C++ generator  
🔥 IR → WebAssembly generator
🔥 Runa programs run on any platform

Result: True multi-target compilation
```

### **Phase 2.2: Universal Input** 
**Goal: Multiple input languages**

```
Week 11-14: Universal Input Parsing
🔥 JavaScript → IR parser
🔥 Python → IR parser
🔥 C++ → IR parser  
🔥 Cross-language translation working

Result: True universal translation platform
```

### **Phase 3.0: AI Integration**
**Goal: AI-powered intelligent translation**

```
Month 4+: AI-First Features
🔥 LLM integration for semantic understanding
🔥 Context-aware cross-language translation
🔥 Intelligent code optimization
🔥 Natural language code generation

Result: AI-First Universal Translation Platform
```

---

## **🎯 MY RECOMMENDATION:**

**Start with Phase 1.5 (1-2 weeks)** to solidify our foundation, THEN jump into the exciting Phase 2.0+ goals!

**Why?**
- 🎯 We need working control flow for self-hosting
- 🎯 Quick wins build momentum  
- 🎯 Solid foundation prevents technical debt
- 🎯 Phase 2.0 will be much easier with complete Runa implementation

**The exciting stuff (self-hosting, multi-target, AI) is Phase 2.0+!**

---

## **🔥 WHAT DO YOU WANT TO TACKLE?**

**Option 1:** Phase 1.5 first (recommended) - Fix the foundation, then go big  
**Option 2:** Jump straight to Phase 2.0 - Start self-hosting now (risky but exciting!)  
**Option 3:** Phase 2.1 - Start building JavaScript/C++ generators immediately  

Which path excites you most? We can dive into any of these! 🚀 