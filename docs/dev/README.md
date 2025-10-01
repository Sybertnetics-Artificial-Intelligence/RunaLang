# Runa Development Documentation

Welcome to the Runa compiler development documentation. This directory contains technical documentation for contributors and core developers.

---

## 📚 Quick Navigation

### Planning & Roadmap
- **[Development Roadmap](./DEVELOPMENT_ROADMAP.md)** - Complete plan from v0.0.8 to v1.0
- **[Version Comparison](./VERSION_COMPARISON.md)** - Quick reference chart of features per version

### Current Milestone
- **[v0.0.8: Inline Assembly](./milestones/V0.0.8_INLINE_ASSEMBLY.md)** - Next milestone (starts after v0.0.7.5)

### Completed Milestones
- ✅ **v0.0.7.5: Self-Hosting** - Runa compiler written in Runa (COMPLETE)

---

## 🎯 Current Status

**Latest Release:** v0.0.7.5
**Status:** Self-hosting achieved ✅
**Next Milestone:** v0.0.8 (Inline Assembly)

### What Works Today (v0.0.7.5):
- ✅ Self-hosting compiler (Runa compiles Runa)
- ✅ Full language features (variables, functions, types, modules)
- ✅ Bootstrap test passes (Stage 2 = Stage 3 = Stage 4)
- ✅ Performance: 2-4x slower than C, 6-18x faster than Python
- ✅ Binary size: 198KB
- ✅ Benchmarks against C, Rust, Java, Python

### What's Next (v0.0.8):
- 🔄 Inline assembly support
- 🔄 Eliminate dependency on GNU assembler (`as`)
- 🔄 Prepare for native object file generation

---

## 🗺️ Project Structure

```
runa/docs/dev/
├── README.md                      # This file
├── DEVELOPMENT_ROADMAP.md         # Complete v0.0.8 → v1.0 plan
├── VERSION_COMPARISON.md          # Feature matrix
├── milestones/
│   ├── V0.0.8_INLINE_ASSEMBLY.md # Next milestone
│   └── ...                        # Future milestones
├── dev_tools/                     # Developer tools docs
└── Sybertnetics_Roadmap/          # Strategic planning
```

---

## 📖 Key Documents

### For New Contributors:
1. Start with [Version Comparison](./VERSION_COMPARISON.md) to understand where we are
2. Read [Development Roadmap](./DEVELOPMENT_ROADMAP.md) to see the big picture
3. Check current [Milestone](./milestones/) to see what's being worked on

### For Core Developers:
1. [Development Roadmap](./DEVELOPMENT_ROADMAP.md) - Detailed implementation plans
2. [Milestone Documents](./milestones/) - Task breakdowns per version
3. Bootstrap validation procedures (in milestone docs)

---

## 🚀 Development Phases

### Phase 1: Foundation (COMPLETE)
- v0.0.0 → v0.0.7.5: Basic compiler, self-hosting

### Phase 2: Independence (3 months)
- v0.0.8: Inline assembly
- v0.0.9: Native object writer & linker
- v0.1.0: Beta release (no external dependencies)

### Phase 3: Production Features (18 months)
- v0.2.0: Standard library
- v0.3.0: Type system enhancements
- v0.4.0: Module system & packages
- v0.5.0: Error handling & debugging
- v0.6.0: Memory management
- v0.7.0: Optimization passes
- v0.8.0: Concurrency
- v0.9.0: Advanced optimization

### Phase 4: v1.0 Release (6 months polish)
- Complete documentation
- Ecosystem tooling
- Community building
- Production readiness


---

## 🎯 Milestone Quick Reference

| Version | Goal | Timeline | Status |
|---------|------|----------|--------|
| v0.0.7.5 | Self-hosting | - | ✅ Complete |
| v0.0.8 | Inline Assembly | 2-3 weeks | 🔄 Next |
| v0.0.9 | Native Object/Linker | 4-6 weeks | 📋 Planned |
| v0.1.0 | Beta Release | 2-3 weeks | 🎯 Milestone |
| v0.2.0 | Standard Library | 6-8 weeks | 📋 Planned |
| v0.3.0 | Type System | 8-10 weeks | 📋 Planned |
| v0.4.0 | Modules & Packages | 10-12 weeks | 📋 Planned |
| v0.5.0 | Error Handling | 6-8 weeks | 📋 Planned |
| v0.6.0 | Memory Safety | 10-12 weeks | 📋 Planned |
| v0.7.0 | Optimization L1 | 8-10 weeks | 📋 Planned |
| v0.8.0 | Concurrency | 10-12 weeks | 📋 Planned |
| v0.9.0 | Advanced Optimization | 12-14 weeks | 📋 Planned |
| v1.0.0 | Production Release | 16-20 weeks | 🎯 Goal |

---

## 🛠️ Development Workflow

### Starting a New Milestone:
1. Read the milestone document (e.g., `V0.0.8_INLINE_ASSEMBLY.md`)
2. Create feature branch: `git checkout -b feature/v0.0.8-inline-asm`
3. Follow task breakdown in milestone doc
4. Run tests frequently: `./run_tests.sh`
5. Update milestone doc with progress

### Before Completing a Milestone:
1. ✅ All tasks in milestone doc complete
2. ✅ Bootstrap test passes
3. ✅ All regression tests pass
4. ✅ Documentation updated
5. ✅ Benchmarks run and recorded
6. ✅ Version tag created: `git tag v0.0.8`

### Testing Requirements:
- **Unit tests:** All new features
- **Integration tests:** End-to-end compilation
- **Bootstrap test:** Self-compilation produces identical binary
- **Regression tests:** All previous tests still pass
- **Performance tests:** No >5% performance degradation

---

## 📊 Success Metrics

### Technical Metrics:
- **Compilation speed:** Should not degrade >20% per version
- **Binary size:** Target <500KB by v1.0
- **Performance vs C:** Goal is 0.8-1.2x by v1.0
- **Test coverage:** Aim for 80%+ coverage
- **Bootstrap stability:** Must produce identical binary

### Community Metrics (v1.0 goals):
- 1000+ GitHub stars
- 50+ contributors
- 100+ packages in repository
- Active community (Discord/forum)
- 10+ production users

---

## 🔗 External Resources

### Learning Compiler Development:
- [Crafting Interpreters](https://craftinginterpreters.com/)
- [Modern Compiler Implementation in ML](https://www.cs.princeton.edu/~appel/modern/)
- [Engineering a Compiler (Cooper & Torczon)](https://www.elsevier.com/books/engineering-a-compiler/cooper/978-0-12-088478-0)

### x86-64 Reference:
- [x86-64 ABI](https://refspecs.linuxbase.org/elf/x86_64-abi-0.99.pdf)
- [Intel Software Developer Manual](https://software.intel.com/content/www/us/en/develop/articles/intel-sdm.html)
- [Linux System Call Table](https://filippo.io/linux-syscall-table/)

### ELF Format:
- [ELF Specification](https://refspecs.linuxfoundation.org/elf/elf.pdf)
- [Linkers and Loaders (Levine)](https://www.iecc.com/linker/)

---

## 🤝 Contributing

### Areas We Need Help:
1. **Core Compiler:** Parser, codegen, optimization
2. **Standard Library:** Data structures, algorithms
3. **Tooling:** IDE extensions, debugger, profiler
4. **Documentation:** Tutorials, examples, guides
5. **Testing:** Test cases, fuzzing, benchmarking

### Communication:
- **GitHub Issues:** Bug reports, feature requests
- **Pull Requests:** Code contributions
- **Discussions:** Design decisions, questions

---

## 📝 Document Maintenance

This documentation is maintained by the Runa core team and should be updated:
- **After each milestone:** Update status, add lessons learned
- **When plans change:** Update roadmap, notify team
- **With new features:** Add to version comparison chart
- **For breaking changes:** Document migration path

---

## 🎓 Philosophy

**Runa's Mission:**
> "Write code your manager can read, with the speed of C"

**Core Values:**
1. **Readability:** Code should read like English prose
2. **Performance:** Compiled speed competitive with C/Rust
3. **Safety:** Prevent bugs at compile time
4. **Simplicity:** Small, understandable compiler
5. **Self-hosting:** Compiler written in the language itself

---

**Maintained by:** Runa Core Team

---

## Quick Links

- [Main Repository](../../../)
- [User Documentation](../user/)
- [Language Specification](../user/language-specification/)
- [Bootstrap Compiler](../../bootstrap/)
- [Benchmarks](../../bootstrap/v0.0.7.5/benchmarks/)
