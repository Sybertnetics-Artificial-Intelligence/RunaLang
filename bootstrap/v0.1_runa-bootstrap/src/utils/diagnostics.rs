use std::fmt;

#[derive(Debug, Clone)]
pub enum DiagnosticLevel {
    Error,
    Warning,
    Info,
    Note,
}

#[derive(Debug, Clone)]
pub struct SourceLocation {
    pub file: String,
    pub line: usize,
    pub column: usize,
    pub length: usize,
}

#[derive(Debug, Clone)]
pub struct Diagnostic {
    pub level: DiagnosticLevel,
    pub message: String,
    pub location: Option<SourceLocation>,
    pub code: Option<String>,
}

pub struct DiagnosticEngine {
    diagnostics: Vec<Diagnostic>,
}

impl DiagnosticEngine {
    pub fn new() -> Self {
        Self {
            diagnostics: Vec::new(),
        }
    }
    
    pub fn error(&mut self, message: String, location: Option<SourceLocation>) {
        self.diagnostics.push(Diagnostic {
            level: DiagnosticLevel::Error,
            message,
            location,
            code: None,
        });
    }
    
    pub fn warning(&mut self, message: String, location: Option<SourceLocation>) {
        self.diagnostics.push(Diagnostic {
            level: DiagnosticLevel::Warning,
            message,
            location,
            code: None,
        });
    }
    
    pub fn info(&mut self, message: String, location: Option<SourceLocation>) {
        self.diagnostics.push(Diagnostic {
            level: DiagnosticLevel::Info,
            message,
            location,
            code: None,
        });
    }
    
    pub fn note(&mut self, message: String, location: Option<SourceLocation>) {
        self.diagnostics.push(Diagnostic {
            level: DiagnosticLevel::Note,
            message,
            location,
            code: None,
        });
    }
    
    pub fn has_errors(&self) -> bool {
        self.diagnostics.iter().any(|d| matches!(d.level, DiagnosticLevel::Error))
    }
    
    pub fn has_warnings(&self) -> bool {
        self.diagnostics.iter().any(|d| matches!(d.level, DiagnosticLevel::Warning))
    }
    
    pub fn error_count(&self) -> usize {
        self.diagnostics.iter().filter(|d| matches!(d.level, DiagnosticLevel::Error)).count()
    }
    
    pub fn warning_count(&self) -> usize {
        self.diagnostics.iter().filter(|d| matches!(d.level, DiagnosticLevel::Warning)).count()
    }
    
    pub fn emit_all(&self) {
        for diagnostic in &self.diagnostics {
            eprintln!("{}", diagnostic);
        }
    }
    
    pub fn clear(&mut self) {
        self.diagnostics.clear();
    }
    
    pub fn diagnostics(&self) -> &[Diagnostic] {
        &self.diagnostics
    }
}

impl fmt::Display for DiagnosticLevel {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            DiagnosticLevel::Error => write!(f, "error"),
            DiagnosticLevel::Warning => write!(f, "warning"),
            DiagnosticLevel::Info => write!(f, "info"),
            DiagnosticLevel::Note => write!(f, "note"),
        }
    }
}

impl fmt::Display for Diagnostic {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match &self.location {
            Some(loc) => {
                write!(f, "{}:{}:{}: {}: {}", 
                    loc.file, loc.line, loc.column, self.level, self.message)
            }
            None => {
                write!(f, "{}: {}", self.level, self.message)
            }
        }
    }
}