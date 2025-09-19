#!/bin/bash

# Script to combine v0.1 modules into a single compilable file

echo "Note: Combined v0.1 MicroRuna compiler modules for v0.0 bootstrap compilation" > v0.1_combined.runa
echo "" >> v0.1_combined.runa

# Add lexer functions
echo "Note: === LEXER FUNCTIONS ===" >> v0.1_combined.runa
cat ../v0.1_microruna-compiler/src/lexer.runa | grep -v "^Note:" >> v0.1_combined.runa
echo "" >> v0.1_combined.runa

# Add parser functions
echo "Note: === PARSER FUNCTIONS ===" >> v0.1_combined.runa
cat ../v0.1_microruna-compiler/src/parser.runa | grep -v "^Note:" >> v0.1_combined.runa
echo "" >> v0.1_combined.runa

# Add main entry point (but skip functions that conflict)
echo "Note: === MAIN FUNCTIONS ===" >> v0.1_combined.runa
cat ../v0.1_microruna-compiler/src/main.runa | grep -v "^Note:" >> v0.1_combined.runa

echo "Combined file created: v0.1_combined.runa"