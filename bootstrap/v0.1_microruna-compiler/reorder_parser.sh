#!/bin/bash
# Extract functions and reorder them

# Extract parse_list_literal (lines 369-417)
sed -n '369,417p' src/parser.runa > list_literal.tmp

# Extract parse_struct_creation (lines 419-506)  
sed -n '419,506p' src/parser.runa > struct_creation.tmp

# Create new file with proper order:
# 1. First 109 lines (up to end of parse_function_call)
sed -n '1,109p' src/parser.runa > parser_new.runa

# 2. Add empty line
echo "" >> parser_new.runa

# 3. Insert parse_list_literal
cat list_literal.tmp >> parser_new.runa
echo "" >> parser_new.runa

# 4. Insert parse_struct_creation
cat struct_creation.tmp >> parser_new.runa
echo "" >> parser_new.runa

# 5. Add lines 111-368 (parse_primary_expression through parse_comparison_expression)
sed -n '111,368p' src/parser.runa >> parser_new.runa

# 6. Skip the functions we moved and add the rest (from line 507 onwards)
sed -n '507,$p' src/parser.runa >> parser_new.runa

# Clean up
rm list_literal.tmp struct_creation.tmp

echo "Reordered parser created as parser_new.runa"
