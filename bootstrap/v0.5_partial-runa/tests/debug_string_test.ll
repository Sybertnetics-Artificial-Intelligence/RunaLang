; ModuleID = 'debug_string_test'
source_filename = "debug_string_test"

@str_0 = constant ptr @.str
@.str = constant [12 x i8] c"Hello World\00"

declare void @rust_print_string(ptr)

define i64 @main() {
entry:
  call void @rust_print_string(ptr @str_0)
  ret i64 0
}
