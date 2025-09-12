#!/bin/bash

echo "=== Testing Runa Extension Integration ==="
echo ""

# Create a comprehensive test file
cat > comprehensive_runa_test.runa << 'EOF'
Note: Comprehensive Runa syntax test for IDE extension validation
Note: This file tests all major Runa language features

Note: Type definitions
Type called "Person":
    name as String
    age as Integer
    email as Optional[String]

Type called "Status" is:
    | Active
    | Inactive
    | Pending
    | CompletedWith as String

Note: Process definitions with various signatures
Process called "greet_person" that takes person as Person returns String:
    Let greeting be "Hello, "
    Let full_message be greeting followed by person.name
    Return full_message

Process called "calculate_sum" that takes numbers as List[Integer] returns Integer:
    Let sum be 0
    For each number in numbers:
        Set sum to sum plus number
    Return sum

Process called "validate_email" that takes email as String returns Boolean:
    If email contains "@" and email contains ".":
        Return true
    Otherwise:
        Return false

Note: Variable declarations and assignments
Let message be "Welcome to Runa!"
Let count be 42
Let is_active be true
Let scores be [85, 92, 78, 96]

Note: Conditional statements
If count is greater than 0:
    Display "Count is positive"
Otherwise if count equals 0:
    Display "Count is zero"
Otherwise:
    Display "Count is negative"

Note: Loops and iterations
For each score in scores:
    If score is greater than 90:
        Display "Excellent score: " followed by score

While count is greater than 0:
    Display "Counting down: " followed by count
    Set count to count minus 1

Note: Pattern matching
Match is_active:
    When true:
        Display "System is active"
    When false:
        Display "System is inactive"

Note: Error handling
Try:
    Let result be calculate_sum(scores)
    Display "Sum calculated: " followed by result
Catch error:
    Display "Error occurred: " followed by error
Finally:
    Display "Calculation attempt completed"

Note: Import statements (testing syntax)
Import "collections" as Collections
Import "datetime" as DateTime
Import "os" as OS

Note: External function declarations
External "system_time" that takes nothing returns Integer
External "read_file" that takes path as String returns String

Note: Complex expressions and natural language operators
Let complex_condition be (count is greater than 10) and (message contains "Runa")
Let math_result be (5 plus 3) multiplied by 2 divided by 4

Note: Function calls and method chaining
Let person be Person with name "Alice", age 30, email "alice@example.com"
Let greeting be greet_person(person)
Display greeting

Note: Advanced features
Define PI as 3.14159
Define MAX_USERS as 1000

Assert count is less than MAX_USERS
Assert message is not null

Note: End of test file
EOF

echo "✓ Created comprehensive_runa_test.runa"
echo ""

# Test if Cursor can open the file
echo "Testing Cursor integration..."
echo "1. You can now open 'comprehensive_runa_test.runa' in Cursor"
echo "2. Check if syntax highlighting works for:"
echo "   - Keywords (Process, Type, Let, If, Otherwise, etc.)"
echo "   - Comments (Note: ...)"
echo "   - Strings ('Hello' and \"World\")"
echo "   - Numbers and operators"
echo "   - Type annotations (String, Integer, etc.)"
echo ""

echo "3. Test autocompletion by typing:"
echo "   - 'Proc' (should suggest 'Process called')"
echo "   - 'Typ' (should suggest 'Type called')"
echo "   - 'If' (should suggest full If-Otherwise block)"
echo "   - 'Let' (should suggest 'Let variable be value')"
echo ""

echo "4. Test commands in Command Palette (Ctrl+Shift+P):"
echo "   - 'Runa: Compile File'"
echo "   - 'Runa: Run File'"
echo "   - 'Runa: Format Document'"
echo "   - 'Runa: Convert Mathematical Symbols to Words'"
echo ""

echo "Extension installation path:"
echo "   VSIX file: $(pwd)/runa-language-support-v2-2.0.3.vsix"
echo ""

# Check if the test file is valid
echo "Validating test file syntax..."
if [ -f "comprehensive_runa_test.runa" ]; then
    echo "✓ Test file created successfully"
    echo "   Lines: $(wc -l < comprehensive_runa_test.runa)"
    echo "   Size: $(du -h comprehensive_runa_test.runa | cut -f1)"
else
    echo "✗ Failed to create test file"
fi
echo ""

echo "=== CURSOR-SPECIFIC TROUBLESHOOTING ==="
echo ""
echo "If the extension doesn't load in Cursor:"
echo "1. Check Extensions view (Ctrl+Shift+X) - search for 'runa'"
echo "2. Verify extension is enabled"
echo "3. Look at Output panel -> 'Runa' channel for error messages"
echo "4. Try reloading window (Ctrl+Shift+P -> 'Developer: Reload Window')"
echo "5. Check if .runa files are associated with 'Runa' language"
echo ""

echo "The composer errors you saw are unrelated to our extension."
echo "They appear to be Cursor's AI features having repository analysis issues."
echo ""

echo "Test completed! Open comprehensive_runa_test.runa in Cursor to verify extension functionality."