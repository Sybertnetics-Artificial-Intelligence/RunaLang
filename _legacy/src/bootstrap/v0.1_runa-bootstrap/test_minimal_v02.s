; ModuleID = 'test_minimal_v02.s'
source_filename = "test_minimal_v02.s"
target triple = "x86_64-pc-linux-gnu"

@read_mode = private unnamed_addr constant [2 x i8] c"r\00", align 1
@empty = private unnamed_addr constant [1 x i8] zeroinitializer, align 1
@write_mode = private unnamed_addr constant [2 x i8] c"w\00", align 1

declare i32 @printf(ptr, ...)

declare ptr @malloc(i64)

declare void @free(ptr)

declare ptr @fopen(ptr, ptr)

declare i32 @fclose(ptr)

declare i64 @fread(ptr, i64, i64, ptr)

declare i64 @fwrite(ptr, i64, i64, ptr)

declare i32 @fseek(ptr, i64, i32)

declare i64 @ftell(ptr)

declare i64 @strlen(ptr)

define ptr @ReadFile(ptr %0) {
entry:
  %file = call ptr @fopen(ptr %0, ptr @read_mode)
  %is_null = icmp eq ptr %file, null
  br i1 %is_null, label %error, label %open_success

open_success:                                     ; preds = %entry
  %1 = call i32 @fseek(ptr %file, i64 0, i32 2)
  %file_size = call i64 @ftell(ptr %file)
  %2 = call i32 @fseek(ptr %file, i64 0, i32 0)
  %buffer_size = add i64 %file_size, 1
  %buffer = call ptr @malloc(i64 %buffer_size)
  %3 = call i64 @fread(ptr %buffer, i64 1, i64 %file_size, ptr %file)
  %buffer_end = getelementptr i8, ptr %buffer, i64 %file_size
  store i8 0, ptr %buffer_end, align 1
  %4 = call i32 @fclose(ptr %file)
  br label %read_done

read_done:                                        ; preds = %error, %open_success
  %result = phi ptr [ %buffer, %open_success ], [ @empty, %error ]
  ret ptr %result

error:                                            ; preds = %entry
  br label %read_done
}

define void @WriteFile(ptr %0, ptr %1) {
entry:
  %file = call ptr @fopen(ptr %1, ptr @write_mode)
  %is_null = icmp eq ptr %file, null
  br i1 %is_null, label %done, label %write

write:                                            ; preds = %entry
  %content_len = call i64 @strlen(ptr %0)
  %2 = call i64 @fwrite(ptr %0, i64 1, i64 %content_len, ptr %file)
  %3 = call i32 @fclose(ptr %file)
  br label %done

done:                                             ; preds = %write, %entry
  ret void
}

define ptr @string_concat(ptr %0, ptr %1) {
entry:
  %len1 = call i64 @strlen(ptr %0)
  %len2 = call i64 @strlen(ptr %1)
  %total_len = add i64 %len1, %len2
  %buffer_size = add i64 %total_len, 1
  %buffer = call ptr @malloc(i64 %buffer_size)
  call void @memcpy(ptr %buffer, ptr %0, i64 %len1)
  %offset = getelementptr i8, ptr %buffer, i64 %len1
  call void @memcpy(ptr %offset, ptr %1, i64 %len2)
  %end_offset = getelementptr i8, ptr %buffer, i64 %total_len
  store i8 0, ptr %end_offset, align 1
  ret ptr %buffer
}

declare ptr @memcpy(ptr, ptr, i64)

define i64 @string_length(ptr %0) {
entry:
  %length = call i64 @strlen(ptr %0)
  ret i64 %length
}

define i64 @string_char_at(ptr %0, i64 %1) {
entry:
  %str_len = call i64 @strlen(ptr %0)
  %in_bounds = icmp ult i64 %1, %str_len
  br i1 %in_bounds, label %bounds_ok, label %out_of_bounds

bounds_ok:                                        ; preds = %entry
  %char_ptr = getelementptr i8, ptr %0, i64 %1
  %char_value = load i8, ptr %char_ptr, align 1
  %char_as_int = zext i8 %char_value to i64
  br label %return

out_of_bounds:                                    ; preds = %entry
  br label %return

return:                                           ; preds = %out_of_bounds, %bounds_ok
  %result = phi i64 [ %char_as_int, %bounds_ok ], [ -1, %out_of_bounds ]
  ret i64 %result
}

define ptr @string_substring(ptr %0, i64 %1, i64 %2) {
entry:
  %sub_len = sub i64 %2, %1
  %buffer_size = add i64 %sub_len, 1
  %buffer = call ptr @malloc(i64 %buffer_size)
  %src_ptr = getelementptr i8, ptr %0, i64 %1
  call void @memcpy(ptr %buffer, ptr %src_ptr, i64 %sub_len)
  %end_ptr = getelementptr i8, ptr %buffer, i64 %sub_len
  store i8 0, ptr %end_ptr, align 1
  ret ptr %buffer
}

define ptr @list_create() {
entry:
  %list_ptr = call ptr @malloc(i64 24)
  %capacity_ptr = getelementptr i64, ptr %list_ptr, i64 0
  store i64 10, ptr %capacity_ptr, align 4
  %size_ptr = getelementptr i64, ptr %list_ptr, i64 1
  store i64 0, ptr %size_ptr, align 4
  %data_ptr = call ptr @malloc(i64 80)
  %data_field_ptr = getelementptr i64, ptr %list_ptr, i64 2
  %data_as_i64 = ptrtoint ptr %data_ptr to i64
  store i64 %data_as_i64, ptr %data_field_ptr, align 4
  ret ptr %list_ptr
}

define void @list_append(ptr %0, i64 %1) {
entry:
  %size_ptr = getelementptr i64, ptr %0, i64 1
  %current_size = load i64, ptr %size_ptr, align 4
  %data_field_ptr = getelementptr i64, ptr %0, i64 2
  %data_as_i64 = load i64, ptr %data_field_ptr, align 4
  %data_ptr = inttoptr i64 %data_as_i64 to ptr
  %element_ptr = getelementptr i64, ptr %data_ptr, i64 %current_size
  store i64 %1, ptr %element_ptr, align 4
  %new_size = add i64 %current_size, 1
  store i64 %new_size, ptr %size_ptr, align 4
  ret void
}

define i64 @list_get(ptr %0, i64 %1) {
entry:
  %data_field_ptr = getelementptr i64, ptr %0, i64 2
  %data_as_i64 = load i64, ptr %data_field_ptr, align 4
  %data_ptr = inttoptr i64 %data_as_i64 to ptr
  %element_ptr = getelementptr i64, ptr %data_ptr, i64 %1
  %value = load i64, ptr %element_ptr, align 4
  ret i64 %value
}

define i64 @list_length(ptr %0) {
entry:
  %size_ptr = getelementptr i64, ptr %0, i64 1
  %size = load i64, ptr %size_ptr, align 4
  ret i64 %size
}

define i1 @is_digit(i8 %0) {
entry:
  %ge_zero = icmp uge i8 %0, 48
  %le_nine = icmp ule i8 %0, 57
  %is_digit_result = and i1 %ge_zero, %le_nine
  ret i1 %is_digit_result
}

define i1 @is_letter(i8 %0) {
entry:
  %ge_a_lower = icmp uge i8 %0, 97
  %le_z_lower = icmp ule i8 %0, 122
  %is_lower = and i1 %ge_a_lower, %le_z_lower
  %ge_a_upper = icmp uge i8 %0, 65
  %le_z_upper = icmp ule i8 %0, 90
  %is_upper = and i1 %ge_a_upper, %le_z_upper
  %is_letter_result = or i1 %is_lower, %is_upper
  ret i1 %is_letter_result
}

define i64 @main() {
entry:
  ret i64 42
}
