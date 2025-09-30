# Runa v0.0.7.5 Documentation

This directory contains comprehensive documentation for the Runa v0.0.7.5 self-hosting compiler.

## Quick Start

1. **New Users:** Start with [COMPILER_USAGE.md](COMPILER_USAGE.md) for installation and basic usage
2. **Language Reference:** See [LANGUAGE_FEATURES.md](LANGUAGE_FEATURES.md) for implemented features
3. **Technical Details:** Read [ACHIEVEMENT.md](ACHIEVEMENT.md) for bootstrap verification and metrics

## Document Overview

### ACHIEVEMENT.md
Documents the successful self-hosting milestone achieved on September 30, 2025. Includes:
- Technical verification methodology
- 5-stage bootstrap process
- Fixed-point proof
- Performance metrics
- Validation criteria

### COMPILER_USAGE.md
Complete user guide for the Runa compiler. Covers:
- Installation and setup
- Command-line usage
- Compilation workflow
- Supported features
- Example programs
- Troubleshooting

### LANGUAGE_FEATURES.md
Detailed breakdown of language feature implementation status. Documents:
- Fully implemented features
- Partially implemented features
- Not yet implemented features
- Specification compliance
- Differences from full spec

### runa-language-specification-v0.0.7.3.md
Historical language specification from v0.0.7.3 (C bootstrap). Reference for transliteration fidelity.

## Version Information

**Compiler Version:** v0.0.7.5
**Release Date:** September 30, 2025
**Status:** Self-hosting, production-ready
**Target Platform:** Linux x86-64

## Additional Resources

### User Documentation
Complete language specification available at:
- `runa/docs/user/language-specification/`

### Developer Documentation
Internal architecture and development guides at:
- `runa/docs/dev/`

### Test Suite
Example programs and test cases in:
- `tests/` directory

## Getting Help

For issues or questions:
1. Check COMPILER_USAGE.md for common problems
2. Review example programs in tests/
3. Consult the complete language specification
4. Report issues via GitHub

## Contributing

When contributing to v0.0.7.5:
1. Maintain self-hosting capability
2. Update relevant documentation
3. Add test cases for new features
4. Verify bootstrap still works

## Roadmap

### Next Versions
- **v0.0.8:** Inline assembly support
- **v0.0.9:** Native object generation and linking
- **v0.1.0+:** Feature expansion and multi-platform support

See the main repository README for the complete roadmap.