#!/bin/bash

# Copyright 2025 Sybertnetics Artificial Intelligence Solutions
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
echo 'Process called "main" takes argc as Integer, argv as Integer returns Integer:' > test_input.runa
echo '    Return 42' >> test_input.runa
echo 'End Process' >> test_input.runa

echo "Trying to compile with runac_test (expect errors but check if file is created):"
./runac_test test_input.runa test_output.s 2>&1 || true
echo "Checking if output file was created:"
if [ -f test_output.s ]; then
    echo "SUCCESS: Output file created"
    head -10 test_output.s
else
    echo "FAILED: No output file created"
fi
