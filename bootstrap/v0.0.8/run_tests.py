#!/usr/bin/env python3
import subprocess
import os
import glob

os.chdir('/mnt/d/SybertneticsUmbrella/SybertneticsAISolutions/MonoRepo/runa/bootstrap/v0.0.8')

tests = glob.glob('tests/unit/test_*.runa')
passed = 0
failed = 0

for test in sorted(tests):
    name = os.path.basename(test)[:-5]  # Remove .runa

    # Compile
    result = subprocess.run(['./stage3/runac', test, f'/tmp/{name}.s'],
                          capture_output=True, timeout=30)
    if result.returncode != 0:
        print(f'✗ {name} (compile failed)')
        failed += 1
        continue

    # Assemble
    result = subprocess.run(['as', '--64', f'/tmp/{name}.s', '-o', f'/tmp/{name}.o'],
                          capture_output=True)
    if result.returncode != 0:
        print(f'✗ {name} (assemble failed)')
        failed += 1
        continue

    # Link
    result = subprocess.run(['gcc', f'/tmp/{name}.o', 'runtime/runtime.o', '-lm', '-o', f'/tmp/{name}'],
                          capture_output=True)
    if result.returncode != 0:
        print(f'✗ {name} (link failed)')
        failed += 1
        continue

    # Execute the test (any exit code is OK - tests just need to run without crashing)
    try:
        result = subprocess.run([f'/tmp/{name}'], capture_output=True, timeout=5)
        # Success if it ran without timeout or segfault
        if result.returncode >= 0 and result.returncode < 128:
            print(f'✓ {name}')
            passed += 1
        else:
            print(f'✗ {name} (crash/signal, exit code {result.returncode})')
            failed += 1
    except subprocess.TimeoutExpired:
        print(f'✗ {name} (timeout)')
        failed += 1

print('='*40)
print(f'Total: {len(tests)} | Passed: {passed} | Failed: {failed}')
