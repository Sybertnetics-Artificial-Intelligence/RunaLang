#!/bin/bash
cd /mnt/d/SybertneticsUmbrella/SybertneticsAISolutions/MonoRepo/runa/bootstrap/v0.0.7.5/stage1
for obj in string_utils.o hashtable.o containers.o lexer.o parser.o codegen.o; do
    objcopy --redefine-sym main=_unused_main_${obj} ${obj}
done
echo "Renamed conflicting main symbols"