CC = gcc
CFLAGS = -Wall -Wextra -std=c99 -O2
TARGET = runac
SOURCES = main.c lexer.c parser.c codegen_x86.c
OBJECTS = $(SOURCES:.c=.o)

.PHONY: all clean test test2 test3 test4

all: $(TARGET)

$(TARGET): $(OBJECTS)
	$(CC) $(OBJECTS) -o $(TARGET)

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

help:
	@echo "Available targets:"
	@echo "  all      - Build the compiler"
	@echo "  clean    - Remove build artifacts"
	@echo "  test     - Test with variables and arithmetic (x=40, y=2, return x+y)"
	@echo "  test2    - Test with Set statement (x=10, x=x+32, return x)"
	@echo "  test3    - Test with If/Otherwise conditional (if x==5 set result=42 else 0)"
	@echo "  test4    - Test with While loop (count from 0 to 5)"
	@echo "  help     - Show this help"