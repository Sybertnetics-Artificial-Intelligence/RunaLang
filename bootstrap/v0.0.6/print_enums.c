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
#include "lexer.h"

int main() {
    printf("TOKEN_EOF = %d\n", TOKEN_EOF);
    printf("TOKEN_TYPE = %d\n", TOKEN_TYPE);
    printf("TOKEN_DOT = %d\n", TOKEN_DOT);
    printf("TOKEN_IDENTIFIER = %d\n", TOKEN_IDENTIFIER);
    printf("TOKEN_AS = %d\n", TOKEN_AS);
    printf("TOKEN_BY = %d\n", TOKEN_BY);
    printf("TOKEN_PRINT = %d\n", TOKEN_PRINT);
    return 0;
}