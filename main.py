import math
from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional, Dict


class TokenType(Enum):
    # Keywords
    FUNCTION = auto()
    EXTERN = auto()
    IF = auto()
    THEN = auto()
    ELSE = auto()
    FOR = auto()
    IN = auto()
    
    # Literals
    INTEGER = auto()
    FLOAT = auto()
    IDENTIFIER = auto()
    
    # Operators
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    MODULO = auto()
    POWER = auto()
    
    # Comparison operators
    LESS = auto()
    GREATER = auto()
    EQUAL = auto()
    NOT_EQUAL = auto()
    
    # Punctuation
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    COMMA = auto()
    SEMICOLON = auto()
    
    # Special
    EOF = auto()
    UNKNOWN = auto()


@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int
    
    def __str__(self) -> str:
        return f"Token(type={self.type.name}, value='{self.value}', position=({self.line}, {self.column}))"


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
        
        # Keywords mapping
        self.keywords: Dict[str, TokenType] = {
            "def": TokenType.FUNCTION,
            "extern": TokenType.EXTERN,
            "if": TokenType.IF,
            "then": TokenType.THEN,
            "else": TokenType.ELSE,
            "for": TokenType.FOR,
            "in": TokenType.IN,
        }
        
        # Built-in functions
        self.built_in_functions = ["sin", "cos", "tan", "sqrt", "ln", "exp"]
        
        # Single-character token mapping
        self.single_char_tokens: Dict[str, TokenType] = {
            "+": TokenType.PLUS,
            "-": TokenType.MINUS,
            "*": TokenType.MULTIPLY,
            "/": TokenType.DIVIDE,
            "%": TokenType.MODULO,
            "^": TokenType.POWER,
            "<": TokenType.LESS,
            ">": TokenType.GREATER,
            "=": TokenType.EQUAL,
            "(": TokenType.LEFT_PAREN,
            ")": TokenType.RIGHT_PAREN,
            ",": TokenType.COMMA,
            ";": TokenType.SEMICOLON,
        }
    
    def is_at_end(self) -> bool:
        """Check if we've reached the end of the source."""
        return self.position >= len(self.source)
    
    def advance(self) -> str:
        """Consume the current character and return it."""
        char = self.source[self.position]
        self.position += 1
        self.column += 1
        
        if char == '\n':
            self.line += 1
            self.column = 1
            
        return char
    
    def peek(self) -> str:
        """Look at the current character without consuming it."""
        if self.is_at_end():
            return ''
        return self.source[self.position]
    
    def peek_next(self) -> str:
        """Look at the next character without consuming it."""
        if self.position + 1 >= len(self.source):
            return ''
        return self.source[self.position + 1]
    
    def match(self, expected: str) -> bool:
        """Check if the current character matches expected and consume it if it does."""
        if self.is_at_end() or self.source[self.position] != expected:
            return False
            
        self.position += 1
        self.column += 1
        return True
    
    def add_token(self, token_type: TokenType, value: str = ""):
        """Add a token to the list."""
        if not value:
            value = token_type.name
        self.tokens.append(Token(token_type, value, self.line, self.column - len(value)))
    
    def scan_tokens(self) -> List[Token]:
        """Scan all tokens from the source."""
        while not self.is_at_end():
            self.scan_token()
            
        # Add EOF token
        self.add_token(TokenType.EOF, "")
        return self.tokens
    
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
    
    def identifier(self):
        """Process an identifier or keyword."""
        # Back up one character since we already consumed the first letter
        start_position = self.position - 1
        start_column = self.column - 1
        
        # Consume the rest of the identifier
        while (not self.is_at_end() and 
               (self.peek().isalnum() or self.peek() == '_')):
            self.advance()
            
        # Get the identifier string
        identifier = self.source[start_position:self.position]
        
        # Check if it's a keyword
        if identifier in self.keywords:
            self.add_token(self.keywords[identifier], identifier)
        else:
            self.add_token(TokenType.IDENTIFIER, identifier)
    
    def number(self, first_char: str):
        """Process a numeric literal."""
        # Back up one character since we already consumed the first digit
        start_position = self.position - 1
        start_column = self.column - 1
        
        # Flag for if we've seen a decimal point
        has_decimal = (first_char == '.')
        
        # Consume digits
        while (not self.is_at_end() and 
               (self.peek().isdigit() or (self.peek() == '.' and not has_decimal))):
            if self.peek() == '.':
                has_decimal = True
            self.advance()
            
        # Get the number string
        number_str = self.source[start_position:self.position]
        
        # Determine if it's an integer or float
        if has_decimal:
            self.add_token(TokenType.FLOAT, number_str)
        else:
            self.add_token(TokenType.INTEGER, number_str)


def print_tokens(tokens: List[Token]):
    """Print tokens in a readable format."""
    for token in tokens:
        print(token)


def calculate(tokens: List[Token]) -> Optional[float]:
    """
    Simple calculator function to demonstrate the lexer's output.
    Supports basic arithmetic and trig functions.
    """
    pos = 0
    
    def expression():
        return term()
    
    def term():
        left = factor()
        
        while pos < len(tokens) and tokens[pos].type in [TokenType.PLUS, TokenType.MINUS]:
            op = tokens[pos]
            pos_increment()
            right = factor()
            
            if op.type == TokenType.PLUS:
                left += right
            elif op.type == TokenType.MINUS:
                left -= right
                
        return left
    
    def factor():
        left = power()
        
        while pos < len(tokens) and tokens[pos].type in [TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO]:
            op = tokens[pos]
            pos_increment()
            right = power()
            
            if op.type == TokenType.MULTIPLY:
                left *= right
            elif op.type == TokenType.DIVIDE:
                left /= right
            elif op.type == TokenType.MODULO:
                left %= right
                
        return left
    
    def power():
        left = primary()
        
        if pos < len(tokens) and tokens[pos].type == TokenType.POWER:
            pos_increment()
            right = power()  # Right associative
            return left ** right
            
        return left
    
    def primary():
        token = tokens[pos]
        pos_increment()
        
        if token.type == TokenType.INTEGER:
            return int(token.value)
        elif token.type == TokenType.FLOAT:
            return float(token.value)
        elif token.type == TokenType.IDENTIFIER:
            # Handle built-in functions
            if token.value == "sin":
                # Expect a left parenthesis
                if pos < len(tokens) and tokens[pos].type == TokenType.LEFT_PAREN:
                    pos_increment()
                    arg = expression()
                    # Expect a right parenthesis
                    if pos < len(tokens) and tokens[pos].type == TokenType.RIGHT_PAREN:
                        pos_increment()
                        return math.sin(arg)
            elif token.value == "cos":
                if pos < len(tokens) and tokens[pos].type == TokenType.LEFT_PAREN:
                    pos_increment()
                    arg = expression()
                    if pos < len(tokens) and tokens[pos].type == TokenType.RIGHT_PAREN:
                        pos_increment()
                        return math.cos(arg)
            # Add more functions as needed
            
        elif token.type == TokenType.LEFT_PAREN:
            result = expression()
            # Expect a right parenthesis
            if pos < len(tokens) and tokens[pos].type == TokenType.RIGHT_PAREN:
                pos_increment()
                return result
                
        # Error handling would go here in a real implementation
        return 0
    
    def pos_increment():
        nonlocal pos
        pos += 1
    
    result = expression()
    return result


def main():
    # Test the lexer with some example code
    sample = """
    # Define a function to calculate factorial
    def factorial(n)
        if n < 2 then
            1
        else
            n * factorial(n-1)
    
    # Call the function
    factorial(5)
    
    # Use some trigonometric functions
    extern sin(x);
    extern cos(x);
    
    # Calculate an expression with trigonometric functions
    3.14159 * sin(0.5) + 2 * cos(0)
    """
    
    # Create lexer and scan tokens
    lexer = Lexer(sample)
    tokens = lexer.scan_tokens()
    
    # Print the tokens
    print("=== Tokens ===")
    print_tokens(tokens)
    
    # Test simple expression calculation
    calc_sample = "2 + 3 * 4 - 5 / 2"
    calc_lexer = Lexer(calc_sample)
    calc_tokens = calc_lexer.scan_tokens()
    
    print("\n=== Calculator Example ===")
    print(f"Expression: {calc_sample}")
    print("Tokens:")
    print_tokens(calc_tokens)
    
    # Remove the EOF token for calculation
    result = calculate(calc_tokens[:-1])
    print(f"Result: {result}")
    
    # Test with trigonometric functions
    trig_sample = "sin(0.5) + cos(0)"
    trig_lexer = Lexer(trig_sample)
    trig_tokens = trig_lexer.scan_tokens()
    
    print("\n=== Trigonometric Example ===")
    print(f"Expression: {trig_sample}")
    print("Tokens:")
    print_tokens(trig_tokens)
    
    result = calculate(trig_tokens[:-1])
    print(f"Result: {result}")


if __name__ == "__main__":
    main()