# Runa Standard Library: CSV Module

## Overview

The CSV module provides production-grade capabilities for reading, writing, and processing Comma-Separated Values (CSV) files. Built with performance, reliability, and ease of use in mind, it supports advanced features like streaming processing, automatic dialect detection, schema validation, and custom formatting.

## Architecture

The CSV module is organized into three core components:

- **`csv/csv.runa`**: Core types, utilities, and foundational CSV operations
- **`csv/reader.runa`**: Advanced CSV reading with streaming and validation
- **`csv/writer.runa`**: High-performance CSV writing with formatting options

## Key Features

### Core Capabilities
- **High-Performance I/O**: Streaming support for processing large CSV files without memory constraints
- **Dialect Detection**: Automatic detection of CSV dialects (delimiters, quote characters, line terminators)
- **Schema Validation**: Type checking and data validation against predefined schemas
- **Custom Formatting**: Advanced output formatting with type-specific conversion
- **Error Recovery**: Comprehensive error handling with detailed diagnostic information

### Production Features
- **Memory Efficiency**: Streaming APIs for processing files larger than available memory
- **Cross-Platform**: Handles different line terminators and encoding formats
- **AI/ML Integration**: Specialized interfaces for machine learning data pipelines
- **Type Safety**: Strong typing with comprehensive validation
- **Performance Optimization**: Buffered I/O and batch processing capabilities

## Basic Usage

### Reading CSV Files

```runa
Import "csv/reader" as csv_reader
Import "csv/csv" as csv_core

Note: Read entire CSV file
Let result be csv_reader.read_csv with file_path as "data.csv"
Match result:
    When csv_core.CSVSuccess with rows as data_rows and row_count as count:
        Display "Loaded " plus (count as String) plus " rows"
        For each row in data_rows:
            Let name be row["name"] if row contains key "name" else ""
            Let age be row["age"] if row contains key "age" else ""
            Display "Name: " plus name plus ", Age: " plus age
    
    When csv_core.CSVFailure with error as csv_error:
        Display "Error reading CSV: " plus csv_error.message
```

### Writing CSV Files

```runa
Import "csv/writer" as csv_writer
Import "csv/csv" as csv_core

Note: Create sample data
Let headers be list containing "name", "age", "city"
Let data be list containing:
    list containing "Alice", "30", "New York",
    list containing "Bob", "25", "San Francisco",
    list containing "Charlie", "35", "Chicago"

Note: Write CSV file
Let success be csv_writer.write_csv_with_headers with:
    file_path as "output.csv"
    headers as headers
    data as data

If success:
    Display "CSV file written successfully"
Otherwise:
    Display "Failed to write CSV file"
```

### Streaming Large Files

```runa
Import "csv/reader" as csv_reader

Note: Create streaming reader for large files
Let reader_options be csv_core.create_csv_reader_options
Set reader_options.chunk_size to Some with value as 1024
Set reader_options.has_header to true

Let stream_result be csv_reader.create_stream_reader with:
    file_path as "large_dataset.csv"
    options as reader_options

Match stream_result:
    When csv_reader.ReaderSuccess with data as reader:
        Let total_processed be 0
        
        While reader.is_open:
            Let chunk_result be csv_reader.read_next_chunk with reader as reader
            Match chunk_result:
                When csv_reader.ReaderSuccess with data as chunk_data:
                    Let chunk_rows be chunk_data["rows"] as List[csv_core.CSVRow]
                    Set total_processed to total_processed plus length of chunk_rows
                    
                    Note: Process each row in the chunk
                    For each row in chunk_rows:
                        Note: Your processing logic here
                        Pass
                
                When csv_reader.ReaderFailure with error as chunk_error:
                    Display "Chunk processing error: " plus chunk_error.message
                    Break
        
        Let close_result be csv_reader.close_stream_reader with reader as reader
        Display "Processed " plus (total_processed as String) plus " rows total"
    
    When csv_reader.ReaderFailure with error as reader_error:
        Display "Failed to create stream reader: " plus reader_error.message
```

## Advanced Features

### Automatic Dialect Detection

```runa
Import "csv/reader" as csv_reader

Note: Detect CSV dialect automatically
Let dialect_result be csv_reader.detect_csv_dialect with file_path as "unknown_format.csv"
Match dialect_result:
    When csv_reader.ReaderSuccess with data as detected_dialect:
        Display "Detected delimiter: " plus detected_dialect.delimiter
        Display "Detected quote character: " plus detected_dialect.quotechar
        Display "Detected line terminator: " plus detected_dialect.lineterminator
        
        Note: Use detected dialect for reading
        Let options be csv_core.create_csv_reader_options
        Set options.dialect to detected_dialect
        
        Let read_result be csv_reader.read_csv_with_options with:
            file_path as "unknown_format.csv"
            options as options
    
    When csv_reader.ReaderFailure with error as detection_error:
        Display "Dialect detection failed: " plus detection_error.message
```

### Schema Validation

```runa
Import "csv/reader" as csv_reader

Note: Define data schema
Let schema be Dictionary with:
    "id" as "integer"
    "name" as "string"
    "email" as "string"
    "age" as "integer"
    "salary" as "float"
    "active" as "boolean"

Note: Read CSV with schema validation
Let result be csv_reader.read_csv_with_schema with:
    file_path as "employees.csv"
    schema as schema

Match result:
    When csv_core.CSVSuccess with rows as validated_rows:
        Display "All rows passed schema validation"
        Note: Process validated data with confidence
        
    When csv_core.CSVFailure with error as validation_error:
        Match validation_error:
            When csv_core.ValidationError with field_name as field and message as msg:
                Display "Validation failed for field '" plus field plus "': " plus msg
            Otherwise:
                Display "Schema validation error: " plus validation_error.message
```

### Custom Output Formatting

```runa
Import "csv/writer" as csv_writer

Note: Define formatting specifications
Let format_config be Dictionary with:
    "salary" as Dictionary with:
        "type" as "currency"
        "symbol" as "$"
    "bonus_percentage" as Dictionary with:
        "type" as "percentage"
        "decimal_places" as 1
    "hire_date" as Dictionary with:
        "type" as "date"
        "format" as "YYYY-MM-DD"
    "employee_id" as Dictionary with:
        "type" as "integer"
        "padding" as Dictionary with:
            "length" as 8
            "character" as "0"
            "align" as "right"

Note: Write CSV with custom formatting
Let success be csv_writer.write_csv_with_custom_formatting with:
    file_path as "formatted_employees.csv"
    rows as employee_data
    format_config as format_config

If success:
    Display "Formatted CSV written successfully"
```

## Configuration Options

### CSV Dialect Configuration

```runa
Import "csv/csv" as csv_core

Note: Create custom CSV dialect
Let custom_dialect be csv_core.CSVDialect with:
    delimiter as ";"
    quotechar as "'"
    escapechar as "\\"
    lineterminator as "\r\n"
    doublequote as false
    skipinitialspace as true
    strict as true
    metadata as Dictionary with "source" as "custom"

Note: Configure reader options
Let reader_options be csv_core.CSVReaderOptions with:
    dialect as custom_dialect
    has_header as true
    encoding as "utf-8"
    chunk_size as Some with value as 2048
    schema as None
    ai_mode as false

Note: Configure writer options  
Let writer_options be csv_core.CSVWriterOptions with:
    dialect as custom_dialect
    write_header as true
    encoding as "utf-8"
    ai_mode as false
```

### AI/ML Integration Mode

```runa
Note: Enable AI mode for enhanced validation and consistency checking
Let ai_options be csv_core.create_csv_reader_options
Set ai_options.ai_mode to true
Set ai_options.schema to Some with value as ml_schema

Note: AI mode provides:
Note: - Enhanced row structure consistency validation
Note: - Automatic data type inference and validation
Note: - Better error reporting for data quality issues
Note: - Optimized data structures for ML processing

Let ml_result be csv_reader.read_csv_with_options with:
    file_path as "training_data.csv"
    options as ai_options
```

## Error Handling

### Comprehensive Error Types

```runa
Import "csv/csv" as csv_core

Process called "handle_csv_error" that takes error as csv_core.CSVError returns String:
    Match error:
        When csv_core.ParseError with line_number as line and message as msg and field_index as field:
            Return "Parse error at line " plus (line as String) plus ", field " plus (field as String) plus ": " plus msg
        
        When csv_core.FileError with path as file_path and message as msg and operation as op:
            Return "File error during " plus op plus " of '" plus file_path plus "': " plus msg
        
        When csv_core.ValidationError with field_name as field and message as msg and value as val:
            Return "Validation error in field '" plus field plus "' with value '" plus val plus "': " plus msg
        
        When csv_core.EncodingError with message as msg and encoding as enc:
            Return "Encoding error with " plus enc plus ": " plus msg

Note: Usage example
Let result be csv_reader.read_csv with file_path as "problematic.csv"
Match result:
    When csv_core.CSVFailure with error as csv_error:
        Let error_message be handle_csv_error with error as csv_error
        Display "CSV processing failed: " plus error_message
```

## Performance Optimization

### Streaming for Large Files

```runa
Note: For files larger than available memory, use streaming APIs
Import "csv/reader" as csv_reader
Import "csv/writer" as csv_writer

Process called "process_large_csv" that takes input_path as String and output_path as String returns Boolean:
    Note: Stream processing for memory efficiency
    Try:
        Let reader_result be csv_reader.create_stream_reader with:
            file_path as input_path
            options as csv_core.create_csv_reader_options
        
        Let writer_result be csv_writer.create_stream_writer with:
            file_path as output_path
            options as csv_core.create_csv_writer_options
        
        Match reader_result:
            When csv_reader.ReaderSuccess with data as reader:
                Match writer_result:
                    When csv_writer.WriterSuccess with data as writer:
                        Let processed_count be 0
                        
                        While reader.is_open:
                            Let chunk_result be csv_reader.read_next_chunk with reader as reader
                            Match chunk_result:
                                When csv_reader.ReaderSuccess with data as chunk_data:
                                    Let chunk_rows be chunk_data["rows"] as List[csv_core.CSVRow]
                                    
                                    Note: Process and transform rows
                                    Let transformed_rows be empty list
                                    For each row in chunk_rows:
                                        Let transformed_row be transform_row with row as row
                                        Add transformed_row to transformed_rows
                                    
                                    Note: Write transformed batch
                                    Let write_result be csv_writer.write_rows_batch with:
                                        writer as writer
                                        rows as transformed_rows
                                    
                                    Match write_result:
                                        When csv_writer.WriterSuccess:
                                            Set processed_count to processed_count plus length of chunk_rows
                                        When csv_writer.WriterFailure:
                                            Return false
                                
                                When csv_reader.ReaderFailure:
                                    Break
                        
                        Let close_reader_result be csv_reader.close_stream_reader with reader as reader
                        Let close_writer_result be csv_writer.close_stream_writer with writer as writer
                        
                        Display "Processed " plus (processed_count as String) plus " rows"
                        Return true
        
        Return false
    
    Catch error:
        Return false
```

### Batch Processing

```runa
Import "csv/writer" as csv_writer

Note: Batch writing for better performance
Let batch_size be 1000
Let current_batch be empty list

Process called "write_data_in_batches" that takes writer as csv_writer.CSVStreamWriter and all_data as List[csv_core.CSVRow] returns Boolean:
    Try:
        Let batch_count be 0
        
        For each row in all_data:
            Add row to current_batch
            
            If length of current_batch is greater than or equal to batch_size:
                Let batch_result be csv_writer.write_rows_batch with:
                    writer as writer
                    rows as current_batch
                
                Match batch_result:
                    When csv_writer.WriterSuccess:
                        Set batch_count to batch_count plus 1
                        Set current_batch to empty list
                    When csv_writer.WriterFailure:
                        Return false
        
        Note: Write remaining rows
        If length of current_batch is greater than 0:
            Let final_batch_result be csv_writer.write_rows_batch with:
                writer as writer
                rows as current_batch
        
        Display "Wrote " plus (batch_count as String) plus " batches"
        Return true
    
    Catch error:
        Return false
```

## Data Validation and Quality

### Type Validation

```runa
Import "csv/csv" as csv_core

Note: Comprehensive type validation
Process called "validate_csv_data_quality" that takes rows as List[csv_core.CSVRow] returns Dictionary[String, Any]:
    Let validation_summary be Dictionary with:
        "total_rows" as length of rows
        "valid_rows" as 0
        "invalid_rows" as 0
        "field_errors" as empty list
        "type_errors" as empty list
    
    For each row in rows:
        Let row_valid be true
        
        Note: Check required fields
        Let required_fields be list containing "id", "name", "email"
        For each required_field in required_fields:
            If not row contains key required_field:
                Set row_valid to false
                Add "Missing required field: " plus required_field to validation_summary["field_errors"]
        
        Note: Validate field types
        If row contains key "id":
            Let id_value be row["id"] as String
            If not csv_core.is_valid_integer with text as id_value:
                Set row_valid to false
                Add "Invalid integer for id: " plus id_value to validation_summary["type_errors"]
        
        If row contains key "email":
            Let email_value be row["email"] as String
            If not is_valid_email with email as email_value:
                Set row_valid to false
                Add "Invalid email format: " plus email_value to validation_summary["type_errors"]
        
        If row_valid:
            Set validation_summary["valid_rows"] to validation_summary["valid_rows"] plus 1
        Otherwise:
            Set validation_summary["invalid_rows"] to validation_summary["invalid_rows"] plus 1
    
    Return validation_summary

Process called "is_valid_email" that takes email as String returns Boolean:
    Note: Basic email validation
    Return csv_core.string_contains with text as email and pattern as "@" and 
           csv_core.string_contains with text as email and pattern as "."
```

## Integration Examples

### Database Export/Import

```runa
Import "csv/writer" as csv_writer
Import "csv/reader" as csv_reader

Process called "export_database_to_csv" that takes table_name as String and output_path as String returns Boolean:
    Note: Export database table to CSV
    Try:
        Note: Fetch data from database (simplified)
        Let db_rows be fetch_table_data with table as table_name
        
        Note: Convert database rows to CSV format
        Let csv_rows be empty list
        For each db_row in db_rows:
            Let csv_row be convert_db_row_to_csv with db_row as db_row
            Add csv_row to csv_rows
        
        Note: Write to CSV with metadata
        Let metadata be Dictionary with:
            "source_table" as table_name
            "export_date" as get_current_date
            "record_count" as length of csv_rows
        
        Return csv_writer.export_csv_with_metadata with:
            file_path as output_path
            rows as csv_rows
            metadata as metadata
    
    Catch error:
        Return false

Process called "import_csv_to_database" that takes csv_path as String and table_name as String returns Boolean:
    Note: Import CSV data to database table
    Try:
        Let read_result be csv_reader.read_csv with file_path as csv_path
        Match read_result:
            When csv_core.CSVSuccess with rows as csv_rows:
                Let import_count be 0
                
                For each csv_row in csv_rows:
                    Let db_insert_result be insert_row_to_database with:
                        table as table_name
                        row_data as csv_row
                    
                    If db_insert_result:
                        Set import_count to import_count plus 1
                
                Display "Imported " plus (import_count as String) plus " records to " plus table_name
                Return true
            
            When csv_core.CSVFailure with error as import_error:
                Display "CSV import failed: " plus import_error.message
                Return false
    
    Catch error:
        Return false
```

### JSON Interoperability

```runa
Import "csv/reader" as csv_reader
Import "csv/writer" as csv_writer
Import "json/json" as json_utils

Process called "convert_csv_to_json" that takes csv_path as String and json_path as String returns Boolean:
    Try:
        Let csv_result be csv_reader.read_csv with file_path as csv_path
        Match csv_result:
            When csv_core.CSVSuccess with rows as csv_rows:
                Let json_array be empty list
                
                For each csv_row in csv_rows:
                    Let json_object be Dictionary with empty entries
                    Let field_keys be csv_core.get_csv_row_keys with row as csv_row
                    
                    For each field_key in field_keys:
                        Let field_value be csv_row at key field_key
                        Set json_object at key field_key to field_value
                    
                    Add json_object to json_array
                
                Let json_content be json_utils.serialize with data as json_array
                Return write_file with path as json_path and content as json_content
            
            When csv_core.CSVFailure:
                Return false
    
    Catch error:
        Return false

Process called "convert_json_to_csv" that takes json_path as String and csv_path as String returns Boolean:
    Try:
        Let json_content be read_file with path as json_path
        Let json_data be json_utils.parse with content as json_content
        
        Note: Convert JSON objects to CSV rows
        Let csv_rows be empty list
        Let headers be extract_headers_from_json with json_data as json_data
        
        For each json_object in json_data:
            Let csv_row be convert_json_object_to_csv_row with:
                json_obj as json_object
                headers as headers
            
            Add csv_row to csv_rows
        
        Return csv_writer.write_csv_with_headers with:
            file_path as csv_path
            headers as headers
            data as convert_csv_rows_to_data with rows as csv_rows
    
    Catch error:
        Return false
```

## Best Practices

### Memory Management

```runa
Note: For large files, always use streaming APIs
Note: ✅ Good: Streaming processing
Let stream_reader be csv_reader.create_stream_reader with file_path as "large.csv"

Note: ❌ Bad: Loading entire file into memory
Let all_data be csv_reader.read_csv with file_path as "large.csv"
```

### Error Handling

```runa
Note: Always handle CSV errors explicitly
Let result be csv_reader.read_csv with file_path as input_path
Match result:
    When csv_core.CSVSuccess with rows as data:
        Note: Process successful result
        Pass
    When csv_core.CSVFailure with error as csv_error:
        Note: Handle specific error types
        Match csv_error:
            When csv_core.FileError:
                Note: Handle file access issues
                Pass
            When csv_core.ParseError:
                Note: Handle data format issues
                Pass
            When csv_core.ValidationError:
                Note: Handle data validation issues
                Pass
```

### Performance Optimization

```runa
Note: Use appropriate chunk sizes for streaming
Let options be csv_core.create_csv_reader_options
Set options.chunk_size to Some with value as 8192  Note: 8KB chunks for balanced performance

Note: Enable buffering for writers
Let writer_options be csv_core.create_csv_writer_options
Let writer be csv_writer.create_stream_writer with options as writer_options
Set writer.auto_flush to false  Note: Manual flush control for better performance
```

## Troubleshooting

### Common Issues

**Memory Issues with Large Files**
```runa
Note: Solution: Use streaming APIs instead of loading entire file
Let reader_result be csv_reader.create_stream_reader with file_path as large_file
Note: Process in chunks instead of loading all at once
```

**Encoding Problems**
```runa
Note: Solution: Specify encoding explicitly
Let options be csv_core.create_csv_reader_options
Set options.encoding to "utf-8"  Note: or "latin1", "cp1252", etc.
```

**Dialect Detection Failures**
```runa
Note: Solution: Manually specify dialect parameters
Let custom_dialect be csv_core.CSVDialect with:
    delimiter as "\t"  Note: Tab-separated
    quotechar as "\""
    escapechar as "\\"
    lineterminator as "\n"
```

**Schema Validation Errors**
```runa
Note: Solution: Validate data incrementally and handle errors gracefully
Let validation_result be csv_reader.validate_csv_file with:
    file_path as input_file
    schema as data_schema

Match validation_result:
    When csv_reader.ReaderSuccess with data as validation_summary:
        If not validation_summary["is_valid"] as Boolean:
            Let errors be validation_summary["validation_errors"]
            Note: Process validation errors individually
```

## Module Integration

The CSV module integrates seamlessly with other Runa standard library modules:

- **`io/file`**: File system operations and encoding support
- **`text/text`**: String processing and text manipulation utilities  
- **`json/json`**: JSON interoperability for data format conversion
- **`collections`**: Advanced data structures for processing CSV data
- **`async`**: Asynchronous CSV processing for high-performance applications

## API Reference

### Core Types

- **`CSVDialect`**: CSV format configuration (delimiter, quotes, etc.)
- **`CSVReaderOptions`**: Configuration for CSV reading operations
- **`CSVWriterOptions`**: Configuration for CSV writing operations
- **`CSVRow`**: Dictionary representing a single CSV row
- **`CSVResult`**: Result type for CSV operations (Success/Failure)
- **`CSVError`**: Comprehensive error types for diagnostics

### Reader Functions

- **`read_csv(file_path)`**: Read entire CSV file with default options
- **`read_csv_with_options(file_path, options)`**: Read with custom configuration
- **`read_csv_with_schema(file_path, schema)`**: Read with data validation
- **`create_stream_reader(file_path, options)`**: Create streaming reader
- **`detect_csv_dialect(file_path)`**: Automatic dialect detection

### Writer Functions

- **`write_csv(file_path, rows)`**: Write CSV with default options
- **`write_csv_with_headers(file_path, headers, data)`**: Write with explicit headers
- **`create_stream_writer(file_path, options)`**: Create streaming writer
- **`write_csv_with_custom_formatting(file_path, rows, format_config)`**: Advanced formatting

### Utility Functions

- **`validate_csv_file(file_path, schema)`**: Validate CSV against schema
- **`analyze_csv_structure(file_path)`**: Analyze CSV file structure
- **`convert_data_to_csv_rows(headers, data)`**: Convert data arrays to CSV rows

The Runa CSV module provides enterprise-grade CSV processing capabilities with comprehensive error handling, performance optimization, and extensive customization options, making it suitable for both simple data processing tasks and complex data pipeline implementations.