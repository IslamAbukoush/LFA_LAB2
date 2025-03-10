# Lexer Implementation for Programming Language Analysis

## Overview

This project implements a lexical analyzer (lexer) for a simple programming language, designed as part of the "Formal Languages & Finite Automata" course. The lexer converts source code text into a sequence of tokens that can be further processed by a parser in a compiler or interpreter pipeline.

The implementation is written in Python and features support for various programming language constructs including control flow statements, arithmetic operations, functions, and trigonometric operations.

## Table of Contents

- [Introduction to Lexical Analysis](#introduction-to-lexical-analysis)
- [Features](#features)
- [Implementation Details](#implementation-details)
  - [Token Types](#token-types)
  - [Lexer Architecture](#lexer-architecture)
  - [Token Scanning Process](#token-scanning-process)
- [Usage Examples](#usage-examples)
- [Testing and Results](#testing-and-results)
- [Conclusions](#conclusions)

## Introduction to Lexical Analysis

Lexical analysis is the first phase in a compiler or interpreter, responsible for breaking down source code text into meaningful lexemes and categorizing them as tokens. This process:

1. Reads the input characters from source code
2. Groups them into lexemes (meaningful sequences)
3. Categorizes each lexeme as a specific token type
4. Passes the tokens to the parser for syntactic analysis

The lexer essentially serves as a scanner that transforms raw text into structured data that can be more easily processed by subsequent compilation phases.

## Features

This lexer implementation includes the following features:

- **Comprehensive Token Recognition**:
  - Keywords: `def`, `extern`, `if`, `then`, `else`, `for`, `in`
  - Numeric literals (both integers and floating-point numbers)
  - Identifiers (variable and function names)
  - Operators (arithmetic, comparison)
  - Special symbols and punctuation

- **Advanced Functionality**:
  - Comment handling (lines beginning with `#`)
  - Position tracking (line and column numbers for error reporting)
  - Support for mathematical and trigonometric functions
  - Decimal number recognition

- **Demonstration Features**:
  - Token visualization for debugging
  - Simple expression evaluation for calculator functionality
  - Support for basic and trigonometric operations

## Implementation Details

### Token Types

The lexer categorizes source code into the following token types:

```python
class TokenType(Enum):
    # Keywords
    FUNCTION = auto()   # 'def'
    EXTERN = auto()     # 'extern'
    IF = auto()         # 'if'
    THEN = auto()       # 'then'
    ELSE = auto()       # 'else'
    FOR = auto()        # 'for'
    IN = auto()         # 'in'
    
    # Literals
    INTEGER = auto()    # e.g., 123
    FLOAT = auto()      # e.g., 123.456
    IDENTIFIER = auto() # e.g., variable_name
    
    # Operators
    PLUS = auto()       # '+'
    MINUS = auto()      # '-'
    MULTIPLY = auto()   # '*'
    DIVIDE = auto()     # '/'
    MODULO = auto()     # '%'
    POWER = auto()      # '^'
    
    # Comparison operators
    LESS = auto()       # '<'
    GREATER = auto()    # '>'
    EQUAL = auto()      # '='
    NOT_EQUAL = auto()  # '!='
    
    # Punctuation
    LEFT_PAREN = auto() # '('
    RIGHT_PAREN = auto()# ')'
    COMMA = auto()      # ','
    SEMICOLON = auto()  # ';'
    
    # Special
    EOF = auto()        # End of file
    UNKNOWN = auto()    # Unrecognized character
```

Each token contains:
- The token type (from the `TokenType` enum)
- The actual string value from the source code
- Line and column position information

### Lexer Architecture

The lexer is implemented as a class with the following main components:

1. **State Management**:
   - Source code text storage
   - Current position tracking
   - Line and column counters for error reporting

2. **Token Mapping Tables**:
   - Keywords mapping (e.g., `"def"` → `TokenType.FUNCTION`)
   - Single-character token mapping (e.g., `"+"` → `TokenType.PLUS`)
   - Built-in function recognition

3. **Helper Methods**:
   - `advance()` - Consumes the current character
   - `peek()` - Looks at the current character without consuming it
   - `match()` - Conditionally consumes a character
   - `add_token()` - Adds a token to the result list

4. **Token Recognition Methods**:
   - `identifier()` - Processes identifiers and keywords
   - `number()` - Processes numeric literals
   - `scan_token()` - Dispatches to appropriate recognition method

### Token Scanning Process

The lexer follows this process to scan tokens:

1. **Initialization**: Create a new `Lexer` instance with the source code
2. **Main Loop**: Call `scan_tokens()` which repeatedly calls `scan_token()` until reaching the end of input
3. **Character Analysis**:
   - Skip whitespace
   - Handle comments (lines starting with `#`)
   - Recognize single-character tokens
   - Identify keywords and identifiers
   - Process numeric literals
   - Flag unknown characters
4. **Token Collection**: Build a list of tokens with their types and positions
5. **Finalization**: Add an EOF token at the end

#### Key Scanning Logic

```python
def scan_token(self):
    """Scan a single token."""
    char = self.advance()
    
    # Skip whitespace
    if char.isspace():
        return
        
    # Comments
    if char == '#':
        # Comment runs until end of line
        while self.peek() != '\n' and not self.is_at_end():
            self.advance()
        return
        
    # Check single character tokens
    if char in self.single_char_tokens:
        # Check for two-character operators
        if char == '!' and self.match('='):
            self.add_token(TokenType.NOT_EQUAL, "!=")
        else:
            self.add_token(self.single_char_tokens[char], char)
        return
        
    # Identifiers and keywords
    if char.isalpha() or char == '_':
        self.identifier()
        return
        
    # Numbers
    if char.isdigit() or (char == '.' and self.peek().isdigit()):
        self.number(char)
        return
        
    # Unknown character
    self.add_token(TokenType.UNKNOWN, char)
```

## Usage Examples

### Basic Usage

```python
# Initialize the lexer with source code
lexer = Lexer("x = 5 + 3 * 2")

# Scan all tokens
tokens = lexer.scan_tokens()

# Print the tokens
for token in tokens:
    print(token)
```

### Example With Function Definitions

```python
sample = """
# Define a function to calculate factorial
def factorial(n)
    if n < 2 then
        1
    else
        n * factorial(n-1)

# Call the function
factorial(5)
"""

lexer = Lexer(sample)
tokens = lexer.scan_tokens()
print_tokens(tokens)
```

### Mathematical Expressions With Trigonometric Functions

```python
trig_sample = "sin(0.5) + cos(0)"
trig_lexer = Lexer(trig_sample)
trig_tokens = trig_lexer.scan_tokens()
```

## Testing and Results

The implementation includes several test cases to demonstrate the lexer's functionality:

1. **Function Definition Example**:
   - Correctly identifies keywords (`def`, `if`, `then`, `else`)
   - Processes nested function calls
   - Handles comments properly

2. **Calculator Example**:
   - Tokenizes arithmetic expressions
   - Supports operator precedence
   - Processes integers and floating-point numbers

3. **Trigonometric Function Example**:
   - Recognizes function names as identifiers
   - Properly handles nested expressions
   - Supports mathematical constants and operations

### Sample Output

For the expression `2 + 3 * 4 - 5 / 2`, the lexer produces:

```
Token(type=INTEGER, value='2', position=(1, 1))
Token(type=PLUS, value='+', position=(1, 3))
Token(type=INTEGER, value='3', position=(1, 5))
Token(type=MULTIPLY, value='*', position=(1, 7))
Token(type=INTEGER, value='4', position=(1, 9))
Token(type=MINUS, value='-', position=(1, 11))
Token(type=INTEGER, value='5', position=(1, 13))
Token(type=DIVIDE, value='/', position=(1, 15))
Token(type=INTEGER, value='2', position=(1, 17))
Token(type=EOF, value='', position=(1, 18))
```

## Conclusions

This lexer implementation demonstrates the fundamental concepts of lexical analysis:

1. **Token Recognition**: The lexer successfully identifies and categorizes tokens from source code.
2. **Positional Information**: The implementation tracks line and column numbers, which is crucial for error reporting.
3. **Language Features**: Support for various language constructs makes the lexer flexible and extensible.

The lexer serves as a first step in a compiler pipeline, transforming raw text into structured tokens that can be processed by a parser. While this implementation is focused on a specific subset of language features, the design allows for easy extension to support additional token types and language constructs.

Future enhancements could include:
- Support for string literals
- More complex operator recognition
- Error recovery mechanisms
- Performance optimizations for large source files

## References

1. Compilers: Principles, Techniques, and Tools (Dragon Book)
2. [LLVM Kaleidoscope Tutorial](https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/LangImpl01.html)
3. [Lexical Analysis on Wikipedia](https://en.wikipedia.org/wiki/Lexical_analysis)
