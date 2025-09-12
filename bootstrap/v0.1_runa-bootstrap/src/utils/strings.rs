use string_cache::DefaultAtom;
use std::collections::HashMap;

// String interning for performance
pub type InternedString = DefaultAtom;

pub struct StringInterner {
    strings: HashMap<String, InternedString>,
}

impl StringInterner {
    pub fn new() -> Self {
        Self {
            strings: HashMap::new(),
        }
    }
    
    pub fn intern(&mut self, s: &str) -> InternedString {
        if let Some(interned) = self.strings.get(s) {
            interned.clone()
        } else {
            let interned = InternedString::from(s);
            self.strings.insert(s.to_string(), interned.clone());
            interned
        }
    }
    
    pub fn get(&self, s: &str) -> Option<InternedString> {
        self.strings.get(s).cloned()
    }
}

// String utilities
pub fn escape_string(s: &str) -> String {
    s.chars()
        .map(|c| match c {
            '\n' => "\\n".to_string(),
            '\r' => "\\r".to_string(),
            '\t' => "\\t".to_string(),
            '\\' => "\\\\".to_string(),
            '"' => "\\\"".to_string(),
            c => c.to_string(),
        })
        .collect()
}

pub fn unescape_string(s: &str) -> Result<String, String> {
    let mut result = String::new();
    let mut chars = s.chars();
    
    while let Some(c) = chars.next() {
        if c == '\\' {
            match chars.next() {
                Some('n') => result.push('\n'),
                Some('r') => result.push('\r'),
                Some('t') => result.push('\t'),
                Some('\\') => result.push('\\'),
                Some('"') => result.push('"'),
                Some(other) => return Err(format!("Invalid escape sequence: \\{}", other)),
                None => return Err("Incomplete escape sequence".to_string()),
            }
        } else {
            result.push(c);
        }
    }
    
    Ok(result)
}

pub fn is_valid_identifier(s: &str) -> bool {
    if s.is_empty() {
        return false;
    }
    
    let mut chars = s.chars();
    
    // First character must be letter or underscore
    if let Some(first) = chars.next() {
        if !first.is_alphabetic() && first != '_' {
            return false;
        }
    }
    
    // Remaining characters must be alphanumeric or underscore
    chars.all(|c| c.is_alphanumeric() || c == '_')
}

pub fn normalize_line_endings(s: &str) -> String {
    s.replace("\r\n", "\n").replace('\r', "\n")
}