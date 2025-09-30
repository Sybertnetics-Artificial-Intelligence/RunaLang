.PHONY: all clean stage1

all: stage1

stage1:
	@echo "=== Building v0.0.8 Stage 1 using v0.0.7.6 ==="
	@mkdir -p build stage1
	../v0.0.7.6/stage1/runac src/string_utils.runa stage1/string_utils.s
	../v0.0.7.6/stage1/runac src/hashtable.runa stage1/hashtable.s
	../v0.0.7.6/stage1/runac src/containers.runa stage1/containers.s
	../v0.0.7.6/stage1/runac src/lexer.runa stage1/lexer.s
	../v0.0.7.6/stage1/runac src/parser.runa stage1/parser.s
	../v0.0.7.6/stage1/runac src/codegen.runa stage1/codegen.s
	../v0.0.7.6/stage1/runac src/main.runa stage1/main.s
	@echo "=== Assembling all modules ==="
	@for f in stage1/*.s; do as --64 "$$f" -o "$${f%.s}.o"; done
	@echo "=== Compiling runtime ==="
	gcc -c runtime/runtime.c -o stage1/runtime.o
	@echo "=== Linking stage1/runac ==="
	gcc stage1/*.o -lm -ldl -lpthread -Wl,--export-dynamic -o stage1/runac
	@echo "✓ Stage 1 complete: stage1/runac"

clean:
	rm -rf build stage1

