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
CC = gcc
CFLAGS = -Wall -Wextra -std=c99 -O2
TARGET = runac
SOURCES = main.c lexer.c parser.c codegen_x86.c
OBJECTS = $(SOURCES:.c=.o)

.PHONY: all clean test test2

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

help:
	@echo "Available targets:"
	@echo "  all      - Build the compiler"
	@echo "  clean    - Remove build artifacts"
	@echo "  test     - Test with variables and arithmetic (x=40, y=2, return x+y)"
	@echo "  test2    - Test with Set statement (x=10, x=x+32, return x)"
	@echo "  help     - Show this help"