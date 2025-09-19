set pagination off
set disassemble-next-line on
break runa_function_main
run sample.runa
p (int)get_argc()
x/wd runa_argc
x/gx runa_argv
x/s *(char**)runa_argv
x/s *((char**)runa_argv+1)
bt full
info registers
x/32i quit
