#!/bin/bash

# Script to replace all parser_eat(parser, TOKEN_X) calls with parser_eat(parser, X)
# where X is the hardcoded token number

cp src/parser.runa src/parser.runa.backup

sed -i 's/parser_eat(parser, TOKEN_EOF)/parser_eat(parser, 0)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_PROCESS)/parser_eat(parser, 1)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_CALLED)/parser_eat(parser, 2)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_RETURNS)/parser_eat(parser, 3)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_INTEGER_TYPE)/parser_eat(parser, 4)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_STRING_TYPE)/parser_eat(parser, 5)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_CHARACTER_TYPE)/parser_eat(parser, 6)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_RETURN)/parser_eat(parser, 7)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_END)/parser_eat(parser, 8)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_COLON)/parser_eat(parser, 9)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_STRING_LITERAL)/parser_eat(parser, 10)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_INTEGER)/parser_eat(parser, 11)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_LET)/parser_eat(parser, 12)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_BE)/parser_eat(parser, 13)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_SET)/parser_eat(parser, 14)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_TO)/parser_eat(parser, 15)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_PLUS)/parser_eat(parser, 16)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_MINUS)/parser_eat(parser, 17)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_IF)/parser_eat(parser, 18)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_OTHERWISE)/parser_eat(parser, 19)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_WHILE)/parser_eat(parser, 20)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_IS)/parser_eat(parser, 21)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_EQUAL)/parser_eat(parser, 22)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_NOT_EQUAL)/parser_eat(parser, 23)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_LESS)/parser_eat(parser, 24)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_GREATER)/parser_eat(parser, 25)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_GREATER_EQUAL)/parser_eat(parser, 26)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_LESS_EQUAL)/parser_eat(parser, 27)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_THAN)/parser_eat(parser, 28)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_NOT)/parser_eat(parser, 29)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_AND)/parser_eat(parser, 30)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_OR)/parser_eat(parser, 31)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_THAT)/parser_eat(parser, 32)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_TAKES)/parser_eat(parser, 33)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_AS)/parser_eat(parser, 34)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_MULTIPLIED)/parser_eat(parser, 35)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_DIVIDED)/parser_eat(parser, 36)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_MODULO)/parser_eat(parser, 37)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_BY)/parser_eat(parser, 38)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_BIT_AND)/parser_eat(parser, 39)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_BIT_OR)/parser_eat(parser, 40)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_BIT_XOR)/parser_eat(parser, 41)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_BIT_SHIFT_LEFT)/parser_eat(parser, 42)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_BIT_SHIFT_RIGHT)/parser_eat(parser, 43)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_BREAK)/parser_eat(parser, 44)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_CONTINUE)/parser_eat(parser, 45)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_OTHERWISE_IF)/parser_eat(parser, 46)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_PRINT)/parser_eat(parser, 47)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_LPAREN)/parser_eat(parser, 48)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_RPAREN)/parser_eat(parser, 49)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_TYPE)/parser_eat(parser, 50)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_DOT)/parser_eat(parser, 51)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_COMMA)/parser_eat(parser, 52)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_IDENTIFIER)/parser_eat(parser, 53)/g' src/parser.runa

# Continue with remaining tokens...
sed -i 's/parser_eat(parser, TOKEN_READ_FILE)/parser_eat(parser, 54)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_WRITE_FILE)/parser_eat(parser, 55)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_IMPORT)/parser_eat(parser, 56)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_STRING_LENGTH)/parser_eat(parser, 57)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_STRING_CHAR_AT)/parser_eat(parser, 58)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_STRING_SUBSTRING)/parser_eat(parser, 59)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_STRING_EQUALS)/parser_eat(parser, 60)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_ASCII_VALUE_OF)/parser_eat(parser, 61)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_IS_DIGIT)/parser_eat(parser, 62)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_IS_ALPHA)/parser_eat(parser, 63)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_IS_WHITESPACE)/parser_eat(parser, 64)/g' src/parser.runa

# List operations
sed -i 's/parser_eat(parser, TOKEN_LIST_CREATE)/parser_eat(parser, 65)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_LIST_APPEND)/parser_eat(parser, 66)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_LIST_GET)/parser_eat(parser, 67)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_LIST_GET_INTEGER)/parser_eat(parser, 68)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_LIST_LENGTH)/parser_eat(parser, 69)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_LIST_DESTROY)/parser_eat(parser, 70)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_LIST_SET)/parser_eat(parser, 71)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_LIST_INSERT)/parser_eat(parser, 72)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_LIST_REMOVE)/parser_eat(parser, 73)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_LIST_CLEAR)/parser_eat(parser, 74)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_LIST_FIND)/parser_eat(parser, 75)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_LIST_SORT)/parser_eat(parser, 76)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_LIST_REVERSE)/parser_eat(parser, 77)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_LIST_COPY)/parser_eat(parser, 78)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_LIST_MERGE)/parser_eat(parser, 79)/g' src/parser.runa

# String operations
sed -i 's/parser_eat(parser, TOKEN_STRING_CONCAT)/parser_eat(parser, 80)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_STRING_COMPARE)/parser_eat(parser, 81)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_STRING_TO_INTEGER)/parser_eat(parser, 82)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_INTEGER_TO_STRING)/parser_eat(parser, 83)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_STRING_FIND)/parser_eat(parser, 84)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_STRING_REPLACE)/parser_eat(parser, 85)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_STRING_TRIM)/parser_eat(parser, 86)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_STRING_SPLIT)/parser_eat(parser, 87)/g' src/parser.runa

# File operations
sed -i 's/parser_eat(parser, TOKEN_FILE_OPEN)/parser_eat(parser, 88)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_FILE_CLOSE)/parser_eat(parser, 89)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_FILE_READ_LINE)/parser_eat(parser, 90)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_FILE_WRITE_LINE)/parser_eat(parser, 91)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_FILE_EXISTS)/parser_eat(parser, 92)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_FILE_DELETE)/parser_eat(parser, 93)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_FILE_SIZE)/parser_eat(parser, 94)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_FILE_SEEK)/parser_eat(parser, 95)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_FILE_TELL)/parser_eat(parser, 96)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_FILE_EOF)/parser_eat(parser, 97)/g' src/parser.runa

# Math operations
sed -i 's/parser_eat(parser, TOKEN_SIN)/parser_eat(parser, 98)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_COS)/parser_eat(parser, 99)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_TAN)/parser_eat(parser, 100)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_SQRT)/parser_eat(parser, 101)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_POW)/parser_eat(parser, 102)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_ABS)/parser_eat(parser, 103)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_FLOOR)/parser_eat(parser, 104)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_CEIL)/parser_eat(parser, 105)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_MIN)/parser_eat(parser, 106)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_MAX)/parser_eat(parser, 107)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_RANDOM)/parser_eat(parser, 108)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_LOG)/parser_eat(parser, 109)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_EXP)/parser_eat(parser, 110)/g' src/parser.runa

# Remaining tokens
sed -i 's/parser_eat(parser, TOKEN_PIPE)/parser_eat(parser, 111)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_MATCH)/parser_eat(parser, 112)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_WHEN)/parser_eat(parser, 113)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_WITH)/parser_eat(parser, 114)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_GET_COMMAND_LINE_ARGS)/parser_eat(parser, 115)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_EXIT_WITH_CODE)/parser_eat(parser, 116)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_PANIC)/parser_eat(parser, 117)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_ASSERT)/parser_eat(parser, 118)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_ALLOCATE)/parser_eat(parser, 119)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_DEALLOCATE)/parser_eat(parser, 120)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_INLINE)/parser_eat(parser, 121)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_ASSEMBLY)/parser_eat(parser, 122)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_NOTE)/parser_eat(parser, 123)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_POINTER)/parser_eat(parser, 124)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_OF)/parser_eat(parser, 125)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_ARRAY)/parser_eat(parser, 126)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_LBRACKET)/parser_eat(parser, 127)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_RBRACKET)/parser_eat(parser, 128)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_ERROR)/parser_eat(parser, 129)/g' src/parser.runa
sed -i 's/parser_eat(parser, TOKEN_COUNT)/parser_eat(parser, 130)/g' src/parser.runa

echo "All parser_eat calls have been replaced with hardcoded numbers"