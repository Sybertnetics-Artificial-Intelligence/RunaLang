; ModuleID = 'test_runtime'
source_filename = "test_runtime"

@str_0 = constant ptr @.str
@.str = constant [22 x i8] c"Testing runtime FFI: \00"
@str_1 = constant ptr @.str.1
@.str.1 = constant [3 x i8] c"\\n\00"

declare void @rust_print_string(ptr)

declare ptr @rust_integer_to_string(i64)

define i64 @main() {
entry:
  call void @rust_print_string(ptr @str_0)
  %alloca = alloca i64, align 8
  store i64 42, ptr %alloca, align 4
  %load = load i64, ptr %alloca, align 4
  %call = call ptr @rust_integer_to_string(i64 %load)
  %alloca1 = alloca ptr, align 8
  store ptr %call, ptr %alloca1, align 8
  %load2 = load ptr, ptr %alloca1, align 8
  call void @rust_print_string(ptr %load2)
  call void @rust_print_string(ptr @str_1)
  ret i64 0
}
