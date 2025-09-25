CC = gcc
CFLAGS = -Wall -Wextra -std=c99 -g -O0
TARGET = runac
SOURCES = main.c lexer.c parser.c codegen_x86.c runtime_list.c runtime_io.c runtime_string.c runtime_math.c runtime_system.c hashtable.c containers.c string_utils.c
OBJECTS = $(SOURCES:.c=.o)
RUNTIME_OBJ = runtime_list.o runtime_io.o runtime_string.o runtime_math.o runtime_system.o
ENHANCED_OBJ = hashtable.o containers.o string_utils.o

.PHONY: all clean test test2 test3 test4 test5 test6 test7 test8 test9 test10

all: $(TARGET)

$(TARGET): $(OBJECTS)
	$(CC) $(OBJECTS) -o $(TARGET) -lm

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJECTS) $(TARGET) *.s *_program

test: $(TARGET)
	echo 'Process called "main" returns Integer:' > test.runa
	echo '    Let x be 40' >> test.runa
	echo '    Let y be 2' >> test.runa
	echo '    Return x plus y' >> test.runa
	echo 'End Process' >> test.runa
	./$(TARGET) test.runa test.s
	@echo ""
	@echo "Generated assembly:"
	@cat test.s
	@echo ""
	gcc test.s -o test_program
	./test_program; echo "Exit code: $$?"
	rm -f test.runa test.s test_program

test2: $(TARGET)
	echo 'Process called "main" returns Integer:' > test2.runa
	echo '    Let x be 10' >> test2.runa
	echo '    Set x to x plus 32' >> test2.runa
	echo '    Return x' >> test2.runa
	echo 'End Process' >> test2.runa
	./$(TARGET) test2.runa test2.s
	@echo ""
	@echo "Generated assembly:"
	@cat test2.s
	@echo ""
	gcc test2.s -o test2_program
	./test2_program; echo "Exit code: $$?"
	rm -f test2.runa test2.s test2_program

test3: $(TARGET)
	echo 'Process called "main" returns Integer:' > test3.runa
	echo '    Let x be 5' >> test3.runa
	echo '    Let result be 0' >> test3.runa
	echo '    If x is equal to 5:' >> test3.runa
	echo '        Set result to 42' >> test3.runa
	echo '    Otherwise:' >> test3.runa
	echo '        Set result to 0' >> test3.runa
	echo '    End If' >> test3.runa
	echo '    Return result' >> test3.runa
	echo 'End Process' >> test3.runa
	./$(TARGET) test3.runa test3.s
	@echo ""
	@echo "Generated assembly:"
	@cat test3.s
	@echo ""
	gcc test3.s -o test3_program
	./test3_program; echo "Exit code: $$?"
	rm -f test3.runa test3.s test3_program

test4: $(TARGET)
	echo 'Process called "main" returns Integer:' > test4.runa
	echo '    Let x be 0' >> test4.runa
	echo '    While x is less than 5:' >> test4.runa
	echo '        Set x to x plus 1' >> test4.runa
	echo '    End While' >> test4.runa
	echo '    Return x' >> test4.runa
	echo 'End Process' >> test4.runa
	./$(TARGET) test4.runa test4.s
	@echo ""
	@echo "Generated assembly:"
	@cat test4.s
	@echo ""
	gcc test4.s -o test4_program
	./test4_program; echo "Exit code: $$?"
	rm -f test4.runa test4.s test4_program

test5: $(TARGET)
	echo 'Process called "double" that takes n as Integer returns Integer:' > test5.runa
	echo '    Return n multiplied by 2' >> test5.runa
	echo 'End Process' >> test5.runa
	echo '' >> test5.runa
	echo 'Process called "main" returns Integer:' >> test5.runa
	echo '    Return double(21)' >> test5.runa
	echo 'End Process' >> test5.runa
	./$(TARGET) test5.runa test5.s
	@echo ""
	@echo "Generated assembly:"
	@cat test5.s
	@echo ""
	gcc test5.s -o test5_program
	./test5_program; echo "Exit code: $$?"
	rm -f test5.runa test5.s test5_program

test6: $(TARGET)
	echo 'Process called "factorial" that takes n as Integer returns Integer:' > test6.runa
	echo '    If n is equal to 0:' >> test6.runa
	echo '        Return 1' >> test6.runa
	echo '    Otherwise:' >> test6.runa
	echo '        Return n multiplied by factorial(n minus 1)' >> test6.runa
	echo '    End If' >> test6.runa
	echo 'End Process' >> test6.runa
	echo '' >> test6.runa
	echo 'Process called "main" returns Integer:' >> test6.runa
	echo '    Return factorial(5)' >> test6.runa
	echo 'End Process' >> test6.runa
	./$(TARGET) test6.runa test6.s
	@echo ""
	@echo "Generated assembly:"
	@cat test6.s
	@echo ""
	gcc test6.s -o test6_program
	./test6_program; echo "Exit code: $$?"
	rm -f test6.runa test6.s test6_program

test7: $(TARGET)
	echo 'Process called "main" returns Integer:' > test7.runa
	echo '    Print "Hello, Runa!"' >> test7.runa
	echo '    Return 0' >> test7.runa
	echo 'End Process' >> test7.runa
	./$(TARGET) test7.runa test7.s
	@echo ""
	@echo "Generated assembly:"
	@cat test7.s
	@echo ""
	gcc test7.s -o test7_program
	./test7_program; echo "Exit code: $$?"
	rm -f test7.runa test7.s test7_program

test8: $(TARGET)
	echo 'Process called "main" returns Integer:' > test8.runa
	echo '    Let msg be "Hello, Runa!"' >> test8.runa
	echo '    Print msg' >> test8.runa
	echo '    Return 0' >> test8.runa
	echo 'End Process' >> test8.runa
	./$(TARGET) test8.runa test8.s
	@echo ""
	@echo "Generated assembly:"
	@cat test8.s
	@echo ""
	gcc test8.s -o test8_program
	./test8_program; echo "Exit code: $$?"
	rm -f test8.runa test8.s test8_program

test9: $(TARGET) $(RUNTIME_OBJ)
	echo 'Process called "main" returns Integer:' > test9.runa
	echo '    Let nums be list_create()' >> test9.runa
	echo '    list_append(nums, 1)' >> test9.runa
	echo '    list_append(nums, 2)' >> test9.runa
	echo '    Return list_get(nums, 1)' >> test9.runa
	echo 'End Process' >> test9.runa
	./$(TARGET) test9.runa test9.s
	@echo ""
	@echo "Generated assembly:"
	@cat test9.s
	@echo ""
	gcc test9.s $(RUNTIME_OBJ) -o test9_program
	./test9_program; echo "Exit code: $$?"
	rm -f test9.runa test9.s test9_program

test10: $(TARGET) $(RUNTIME_OBJ)
	echo 'Process called "main" returns Integer:' > test10.runa
	echo '    Let xs be list_create()' >> test10.runa
	echo '    list_append(xs, 10)' >> test10.runa
	echo '    list_append(xs, 20)' >> test10.runa
	echo '    Return list_get_integer(xs, 0) plus list_get_integer(xs, 1)' >> test10.runa
	echo 'End Process' >> test10.runa
	./$(TARGET) test10.runa test10.s
	@echo ""
	@echo "Generated assembly:"
	@cat test10.s
	@echo ""
	gcc test10.s $(RUNTIME_OBJ) -o test10_program
	./test10_program; echo "Exit code: $$?"
	rm -f test10.runa test10.s test10_program

help:
	@echo "Available targets:"
	@echo "  all      - Build the compiler"
	@echo "  clean    - Remove build artifacts"
	@echo "  test     - Test with variables and arithmetic (x=40, y=2, return x+y)"
	@echo "  test2    - Test with Set statement (x=10, x=x+32, return x)"
	@echo "  test3    - Test with If/Otherwise conditional (if x==5 set result=42 else 0)"
	@echo "  test4    - Test with While loop (count from 0 to 5)"
	@echo "  test5    - Test with function definition and call (double function)"
	@echo "  test6    - Test with recursive function (factorial)"
	@echo "  test7    - Test with Print statement and string literal"
	@echo "  test8    - Test with string variable and Print statement"
	@echo "  test9    - Test with list creation and access (list_get)"
	@echo "  test10   - Test with list operations and arithmetic"
	@echo "  help     - Show this help"