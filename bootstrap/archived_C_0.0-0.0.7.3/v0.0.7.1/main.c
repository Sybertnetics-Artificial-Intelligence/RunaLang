/*
 * Copyright 2025 Sybertnetics Artificial Intelligence Solutions
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
#include <stdio.h>
#include <stdlib.h>
#include "lexer.h"
#include "parser.h"
#include "codegen_x86.h"

static char* read_file(const char *filename) {
    FILE *file = fopen(filename, "r");
    if (!file) {
        fprintf(stderr, "[MAIN ERROR] Could not open input file '%s'\n", filename);
        return NULL;
    }

    fseek(file, 0, SEEK_END);
    long length = ftell(file);
    fseek(file, 0, SEEK_SET);

    char *content = malloc(length + 1);
    size_t bytes_read = fread(content, 1, length, file);
    (void)bytes_read;
    content[length] = '\0';

    fclose(file);
    return content;
}

int main(int argc, char **argv) {
    if (argc != 3) {
        fprintf(stderr, "Usage: %s <input.runa> <output.s>\n", argv[0]);
        return 1;
    }

    const char *input_filename = argv[1];
    const char *output_filename = argv[2];

    char *source_code = read_file(input_filename);
    if (!source_code) {
        return 1;
    }

    Lexer *lexer = lexer_create(source_code);
    Parser *parser = parser_create(lexer);
    Program *program = parser_parse_program(parser);

    CodeGenerator *codegen = codegen_create(output_filename);
    if (!codegen) {
        program_destroy(program);
        parser_destroy(parser);
        lexer_destroy(lexer);
        free(source_code);
        return 1;
    }

    codegen_generate(codegen, program);

    printf("Successfully compiled '%s' to '%s'\n", input_filename, output_filename);

    codegen_destroy(codegen);
    program_destroy(program);
    parser_destroy(parser);
    lexer_destroy(lexer);
    free(source_code);

    return 0;
}