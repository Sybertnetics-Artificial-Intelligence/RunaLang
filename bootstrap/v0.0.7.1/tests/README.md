# v0.0.7.1 Test Suite

This directory contains test programs for the v0.0.7.1 Runa compiler.

## Running Tests

To run a test:
```bash
../runac test_name.runa test_name.s
gcc -o test_name test_name.s ../runtime_*.o -no-pie
./test_name
```
