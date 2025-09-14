use runa_bootstrap::lexer::tokenize;
use runa_bootstrap::parser::parse;
use runa_bootstrap::types::{Statement, Expression, BinOp};

#[test]
fn test_type_definition_parsing() {
    let source = r#"
Type called "Point":
    x as Integer
    y as Integer
End Type
"#;
    
    let tokens = tokenize(source).expect("Tokenization should succeed");
    let program = parse(tokens).expect("Parsing should succeed");
    
    assert_eq!(program.types.len(), 1);
    let point_type = &program.types[0];
    assert_eq!(point_type.name, "Point");
    assert_eq!(point_type.fields.len(), 2);
    assert_eq!(point_type.fields[0].0, "x");
    assert_eq!(point_type.fields[1].0, "y");
}

#[test]
fn test_multiple_type_definitions() {
    let source = r#"
Type called "Point":
    x as Integer
    y as Integer
End Type

Type called "Person":
    name as String
    age as Integer
End Type
"#;
    
    let tokens = tokenize(source).expect("Tokenization should succeed");
    let program = parse(tokens).expect("Parsing should succeed");
    
    assert_eq!(program.types.len(), 2);
    assert_eq!(program.types[0].name, "Point");
    assert_eq!(program.types[1].name, "Person");
}

#[test]
fn test_field_access_parsing() {
    let source = r#"
Type called "Point":
    x as Integer
    y as Integer
End Type

Process called "get_x" that takes point as Point returns Integer:
    Let result be point.x
    Return result
End Process
"#;
    
    let tokens = tokenize(source).expect("Tokenization should succeed");
    let program = parse(tokens).expect("Parsing should succeed");
    
    assert_eq!(program.types.len(), 1);
    assert_eq!(program.functions.len(), 1);
    
    let func = &program.functions[0];
    assert_eq!(func.name, "get_x");
    assert_eq!(func.body.len(), 2);
    
    // Check the Let statement contains field access
    match &func.body[0] {
        Statement::Let { name, value } => {
            assert_eq!(name, "result");
            match value {
                Expression::FieldAccess { object, field } => {
                    assert_eq!(field, "x");
                    match object.as_ref() {
                        Expression::Variable(var_name) => {
                            assert_eq!(var_name, "point");
                        }
                        _ => panic!("Expected variable in field access object"),
                    }
                }
                _ => panic!("Expected field access in Let statement"),
            }
        }
        _ => panic!("Expected Let statement"),
    }
}

#[test]
fn test_chained_field_access_parsing() {
    let source = r#"
Type called "Address":
    street as String
End Type

Type called "Person":
    address as Address
End Type

Process called "get_street" that takes person as Person returns String:
    Return person.address.street
End Process
"#;
    
    let tokens = tokenize(source).expect("Tokenization should succeed");
    let program = parse(tokens).expect("Parsing should succeed");
    
    assert_eq!(program.types.len(), 2);
    assert_eq!(program.functions.len(), 1);
    
    let func = &program.functions[0];
    match &func.body[0] {
        Statement::Return { value: Some(expr) } => {
            match expr {
                Expression::FieldAccess { object, field } => {
                    assert_eq!(field, "street");
                    match object.as_ref() {
                        Expression::FieldAccess { object: inner_object, field: inner_field } => {
                            assert_eq!(inner_field, "address");
                            match inner_object.as_ref() {
                                Expression::Variable(var_name) => {
                                    assert_eq!(var_name, "person");
                                }
                                _ => panic!("Expected variable in chained field access"),
                            }
                        }
                        _ => panic!("Expected field access in chained field access"),
                    }
                }
                _ => panic!("Expected field access in return statement"),
            }
        }
        _ => panic!("Expected Return statement"),
    }
}

#[test]
fn test_import_parsing() {
    let source = r#"
Import "geometry" as Geometry

Type called "Point":
    x as Integer
    y as Integer
End Type
"#;
    
    let tokens = tokenize(source).expect("Tokenization should succeed");
    let program = parse(tokens).expect("Parsing should succeed");
    
    assert_eq!(program.imports.len(), 1);
    let import = &program.imports[0];
    assert_eq!(import.module_name, "geometry");
    assert_eq!(import.alias, "Geometry");
    
    assert_eq!(program.types.len(), 1);
}

#[test]
fn test_multiple_imports() {
    let source = r#"
Import "math" as Math
Import "geometry" as Geometry
Import "utils" as Utils
"#;
    
    let tokens = tokenize(source).expect("Tokenization should succeed");
    let program = parse(tokens).expect("Parsing should succeed");
    
    assert_eq!(program.imports.len(), 3);
    
    assert_eq!(program.imports[0].module_name, "math");
    assert_eq!(program.imports[0].alias, "Math");
    
    assert_eq!(program.imports[1].module_name, "geometry");
    assert_eq!(program.imports[1].alias, "Geometry");
    
    assert_eq!(program.imports[2].module_name, "utils");
    assert_eq!(program.imports[2].alias, "Utils");
}

#[test]
fn test_import_with_types_and_functions() {
    let source = r#"
Import "stdlib" as Std

Type called "Application":
    name as String
    version as Integer
End Type

Process called "run" that takes app as Application returns Integer:
    Return app.version
End Process
"#;
    
    let tokens = tokenize(source).expect("Tokenization should succeed");
    let program = parse(tokens).expect("Parsing should succeed");
    
    assert_eq!(program.imports.len(), 1);
    assert_eq!(program.imports[0].module_name, "stdlib");
    assert_eq!(program.imports[0].alias, "Std");
    
    assert_eq!(program.types.len(), 1);
    assert_eq!(program.types[0].name, "Application");
    
    assert_eq!(program.functions.len(), 1);
    assert_eq!(program.functions[0].name, "run");
}

#[test]
fn test_parse_constructor_basic() {
    let source = r#"
Type called "Point":
    x as Integer
    y as Integer
End Type

Process called "test" returns Integer:
    Let origin be a value of type Point with x as 0, y as 0
    Return 0
End Process
"#;

    let tokens = tokenize(source).unwrap();
    let program = parse(tokens).unwrap();
    
    assert_eq!(program.functions.len(), 1);
    let func = &program.functions[0];
    assert_eq!(func.body.len(), 2);
    
    if let Statement::Let { name, value } = &func.body[0] {
        assert_eq!(name, "origin");
        if let Expression::Constructor { type_name, fields } = value {
            assert_eq!(type_name, "Point");
            assert_eq!(fields.len(), 2);
            assert_eq!(fields[0].0, "x");
            assert_eq!(fields[1].0, "y");
        } else {
            panic!("Expected Constructor expression");
        }
    } else {
        panic!("Expected Let statement");
    }
}

#[test]
fn test_parse_constructor_complex() {
    let source = r#"
Type called "Rectangle":
    width as Integer
    height as Integer
    color as String
End Type

Process called "test" returns Integer:
    Let box be a value of type Rectangle with width as 100, height as 50, color as "red"
    Return 0
End Process
"#;

    let tokens = tokenize(source).unwrap();
    let program = parse(tokens).unwrap();
    
    assert_eq!(program.functions.len(), 1);
    let func = &program.functions[0];
    
    if let Statement::Let { name, value } = &func.body[0] {
        assert_eq!(name, "box");
        if let Expression::Constructor { type_name, fields } = value {
            assert_eq!(type_name, "Rectangle");
            assert_eq!(fields.len(), 3);
            assert_eq!(fields[0].0, "width");
            assert_eq!(fields[1].0, "height");
            assert_eq!(fields[2].0, "color");
            
            // Check field values
            if let Expression::Integer(100) = &fields[0].1 {
                // Correct
            } else {
                panic!("Expected width to be 100");
            }
            if let Expression::Integer(50) = &fields[1].1 {
                // Correct
            } else {
                panic!("Expected height to be 50");
            }
            if let Expression::String(s) = &fields[2].1 {
                assert_eq!(s, "red");
            } else {
                panic!("Expected color to be string 'red'");
            }
        } else {
            panic!("Expected Constructor expression");
        }
    } else {
        panic!("Expected Let statement");
    }
}

#[test]
fn test_parse_if_statement() {
    let source = r#"
Process called "test" returns Integer:
    If x is greater than 0:
        Return 1
    End If
    Return 0
End Process
"#;

    let tokens = tokenize(source).unwrap();
    let program = parse(tokens).unwrap();
    
    assert_eq!(program.functions.len(), 1);
    let func = &program.functions[0];
    assert_eq!(func.body.len(), 2);
    
    // Check the If statement
    if let Statement::If { condition, then_body, else_ifs, else_body } = &func.body[0] {
        // Check condition is a comparison
        if let Expression::Binary { op, .. } = condition {
            assert!(matches!(op, BinOp::Greater));
        } else {
            panic!("Expected binary comparison in if condition");
        }
        
        assert_eq!(then_body.len(), 1);
        assert_eq!(else_ifs.len(), 0);
        assert!(else_body.is_none());
    } else {
        panic!("Expected If statement");
    }
}

#[test]
fn test_parse_if_otherwise_statement() {
    let source = r#"
Process called "test" returns Integer:
    If x is equal to 0:
        Return 0
    Otherwise:
        Return 1
    End If
End Process
"#;

    let tokens = tokenize(source).unwrap();
    let program = parse(tokens).unwrap();
    
    let func = &program.functions[0];
    
    if let Statement::If { condition, then_body, else_ifs, else_body } = &func.body[0] {
        // Check condition
        if let Expression::Binary { op, .. } = condition {
            assert!(matches!(op, BinOp::Equal));
        } else {
            panic!("Expected binary comparison");
        }
        
        assert_eq!(then_body.len(), 1);
        assert_eq!(else_ifs.len(), 0);
        assert!(else_body.is_some());
        assert_eq!(else_body.as_ref().unwrap().len(), 1);
    } else {
        panic!("Expected If statement");
    }
}

#[test]
fn test_parse_while_statement() {
    let source = r#"
Process called "test" returns Integer:
    Let i be 0
    While i is less than 10:
        Set i to i plus 1
    End While
    Return i
End Process
"#;

    let tokens = tokenize(source).unwrap();
    let program = parse(tokens).unwrap();
    
    let func = &program.functions[0];
    assert_eq!(func.body.len(), 3);
    
    // Check the While statement
    if let Statement::While { condition, body } = &func.body[1] {
        // Check condition
        if let Expression::Binary { op, .. } = condition {
            assert!(matches!(op, BinOp::Less));
        } else {
            panic!("Expected binary comparison in while condition");
        }
        
        assert_eq!(body.len(), 1);
        
        // Check the Set statement in the body
        if let Statement::Set { name, .. } = &body[0] {
            assert_eq!(name, "i");
        } else {
            panic!("Expected Set statement in while body");
        }
    } else {
        panic!("Expected While statement");
    }
}

#[test]
fn test_parse_for_each_statement() {
    let source = r#"
Process called "test" returns Integer:
    Let total be 0
    For Each item in collection:
        Set total to total plus item
    End For
    Return total
End Process
"#;

    let tokens = tokenize(source).unwrap();
    let program = parse(tokens).unwrap();
    
    let func = &program.functions[0];
    assert_eq!(func.body.len(), 3);
    
    // Check the ForEach statement
    if let Statement::ForEach { variable, collection, body } = &func.body[1] {
        assert_eq!(variable, "item");
        
        // Check collection is a variable
        if let Expression::Variable(name) = collection {
            assert_eq!(name, "collection");
        } else {
            panic!("Expected Variable expression for collection");
        }
        
        assert_eq!(body.len(), 1);
        
        // Check the Set statement in the body
        if let Statement::Set { name, .. } = &body[0] {
            assert_eq!(name, "total");
        } else {
            panic!("Expected Set statement in for each body");
        }
    } else {
        panic!("Expected ForEach statement");
    }
}

#[test]
fn test_parse_constructor_empty() {
    let source = r#"
Type called "Empty":
End Type

Process called "test" returns Integer:
    Let e be a value of type Empty
    Return 0
End Process
"#;

    let tokens = tokenize(source).unwrap();
    let program = parse(tokens).unwrap();
    
    assert_eq!(program.functions.len(), 1);
    let func = &program.functions[0];
    
    if let Statement::Let { name, value } = &func.body[0] {
        assert_eq!(name, "e");
        if let Expression::Constructor { type_name, fields } = value {
            assert_eq!(type_name, "Empty");
            assert_eq!(fields.len(), 0);
        } else {
            panic!("Expected Constructor expression");
        }
    } else {
        panic!("Expected Let statement");
    }
}

#[test]
fn test_parse_inline_assembly_basic() {
    let source = r#"
Process called "syscall_exit" that takes code as Integer returns Integer:
    Inline Assembly:
        "mov %0, %%eax"
        "int $0x80"
        : "=r"(result)
        : "r"(code)
        : "eax"
    End Assembly
    Return 0
End Process
"#;

    let tokens = tokenize(source).unwrap();
    let program = parse(tokens).unwrap();
    
    assert_eq!(program.functions.len(), 1);
    let func = &program.functions[0];
    assert_eq!(func.body.len(), 2);
    
    // Check the InlineAssembly statement
    if let Statement::InlineAssembly { instructions, output_constraints, input_constraints, clobbers } = &func.body[0] {
        assert_eq!(instructions.len(), 2);
        assert_eq!(instructions[0], "mov %0, %%eax");
        assert_eq!(instructions[1], "int $0x80");
        
        assert_eq!(output_constraints.len(), 1);
        assert_eq!(output_constraints[0].0, "=r");
        assert_eq!(output_constraints[0].1, "result");
        
        assert_eq!(input_constraints.len(), 1);
        assert_eq!(input_constraints[0].0, "r");
        assert_eq!(input_constraints[0].1, "code");
        
        assert_eq!(clobbers.len(), 1);
        assert_eq!(clobbers[0], "eax");
    } else {
        panic!("Expected InlineAssembly statement");
    }
}

#[test]
fn test_parse_inline_assembly_no_constraints() {
    let source = r#"
Process called "nop_test" returns Integer:
    Inline Assembly:
        "nop"
        "nop"
    End Assembly
    Return 0
End Process
"#;

    let tokens = tokenize(source).unwrap();
    let program = parse(tokens).unwrap();
    
    let func = &program.functions[0];
    
    if let Statement::InlineAssembly { instructions, output_constraints, input_constraints, clobbers } = &func.body[0] {
        assert_eq!(instructions.len(), 2);
        assert_eq!(instructions[0], "nop");
        assert_eq!(instructions[1], "nop");
        
        assert_eq!(output_constraints.len(), 0);
        assert_eq!(input_constraints.len(), 0);
        assert_eq!(clobbers.len(), 0);
    } else {
        panic!("Expected InlineAssembly statement");
    }
}

#[test]
fn test_parse_inline_assembly_multiple_constraints() {
    let source = r#"
Process called "complex_asm" that takes a as Integer, b as Integer returns Integer:
    Inline Assembly:
        "add %1, %0"
        "mul %2, %0"
        : "=r"(result), "=r"(overflow)
        : "r"(a), "r"(b)
        : "cc", "memory"
    End Assembly
    Return result
End Process
"#;

    let tokens = tokenize(source).unwrap();
    let program = parse(tokens).unwrap();
    
    let func = &program.functions[0];
    
    if let Statement::InlineAssembly { instructions, output_constraints, input_constraints, clobbers } = &func.body[0] {
        assert_eq!(instructions.len(), 2);
        assert_eq!(instructions[0], "add %1, %0");
        assert_eq!(instructions[1], "mul %2, %0");
        
        assert_eq!(output_constraints.len(), 2);
        assert_eq!(output_constraints[0], ("=r".to_string(), "result".to_string()));
        assert_eq!(output_constraints[1], ("=r".to_string(), "overflow".to_string()));
        
        assert_eq!(input_constraints.len(), 2);
        assert_eq!(input_constraints[0], ("r".to_string(), "a".to_string()));
        assert_eq!(input_constraints[1], ("r".to_string(), "b".to_string()));
        
        assert_eq!(clobbers.len(), 2);
        assert_eq!(clobbers[0], "cc");
        assert_eq!(clobbers[1], "memory");
    } else {
        panic!("Expected InlineAssembly statement");
    }
}

#[test]
fn test_parse_inline_assembly_only_output() {
    let source = r#"
Process called "get_cpuid" returns Integer:
    Inline Assembly:
        "cpuid"
        : "=a"(eax_val), "=b"(ebx_val), "=c"(ecx_val), "=d"(edx_val)
    End Assembly
    Return eax_val
End Process
"#;

    let tokens = tokenize(source).unwrap();
    let program = parse(tokens).unwrap();
    
    let func = &program.functions[0];
    
    if let Statement::InlineAssembly { instructions, output_constraints, input_constraints, clobbers } = &func.body[0] {
        assert_eq!(instructions.len(), 1);
        assert_eq!(instructions[0], "cpuid");
        
        assert_eq!(output_constraints.len(), 4);
        assert_eq!(output_constraints[0], ("=a".to_string(), "eax_val".to_string()));
        assert_eq!(output_constraints[1], ("=b".to_string(), "ebx_val".to_string()));
        assert_eq!(output_constraints[2], ("=c".to_string(), "ecx_val".to_string()));
        assert_eq!(output_constraints[3], ("=d".to_string(), "edx_val".to_string()));
        
        assert_eq!(input_constraints.len(), 0);
        assert_eq!(clobbers.len(), 0);
    } else {
        panic!("Expected InlineAssembly statement");
    }
}

#[test]
fn test_parse_inline_assembly_only_input() {
    let source = r#"
Process called "set_control_register" that takes value as Integer returns Integer:
    Inline Assembly:
        "mov %0, %%cr3"
        :
        : "r"(value)
        : "memory"
    End Assembly
    Return 0
End Process
"#;

    let tokens = tokenize(source).unwrap();
    let program = parse(tokens).unwrap();
    
    let func = &program.functions[0];
    
    if let Statement::InlineAssembly { instructions, output_constraints, input_constraints, clobbers } = &func.body[0] {
        assert_eq!(instructions.len(), 1);
        assert_eq!(instructions[0], "mov %0, %%cr3");
        
        assert_eq!(output_constraints.len(), 0);
        
        assert_eq!(input_constraints.len(), 1);
        assert_eq!(input_constraints[0], ("r".to_string(), "value".to_string()));
        
        assert_eq!(clobbers.len(), 1);
        assert_eq!(clobbers[0], "memory");
    } else {
        panic!("Expected InlineAssembly statement");
    }
}

#[test]
fn test_parse_inline_assembly_only_clobbers() {
    let source = r#"
Process called "memory_barrier" returns Integer:
    Inline Assembly:
        "mfence"
        :
        :
        : "memory"
    End Assembly
    Return 0
End Process
"#;

    let tokens = tokenize(source).unwrap();
    let program = parse(tokens).unwrap();
    
    let func = &program.functions[0];
    
    if let Statement::InlineAssembly { instructions, output_constraints, input_constraints, clobbers } = &func.body[0] {
        assert_eq!(instructions.len(), 1);
        assert_eq!(instructions[0], "mfence");
        
        assert_eq!(output_constraints.len(), 0);
        assert_eq!(input_constraints.len(), 0);
        
        assert_eq!(clobbers.len(), 1);
        assert_eq!(clobbers[0], "memory");
    } else {
        panic!("Expected InlineAssembly statement");
    }
}