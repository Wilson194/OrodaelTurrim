grammar Rules;

/* Lexical rules */

// Language symbols definition
IF   : 'IF';
THEN : 'THEN';
WITH : 'WITH';

AND : 'AND' ;
OR : 'OR';

TRUE: 'TRUE';
FALSE: 'FALSE';

// Operators
GT : '>';
GE : '>=';
LT : '<';
LE : '<=';
EQ : '==';
NE : '!=';

// Parenthese
LPAREN: '(';
RPAREN : ')';

LSPAREN : '[';
RSPAREN : ']';

// Float number
DECIMAL : '-'?[0-9]+('.'[0-9]+)? ;

// Identifier (Characters, undescrope and number)
IDENTIFIER : [a-zA-Z_][a-zA-Z_0-9]* ;


SEMI : ';' ;

// Hashtag comments
COMMENT : '#' .+? ('\n'|EOF) -> skip ;
WS : [ \r\t\u000C\n]+ -> skip ;


/* Grammar rules */

rules_set : single_rule* EOF;

single_rule: IF condition THEN conclusion SEMI | IF condition THEN conclusion WITH DECIMAL SEMI;

condition: left_logical_expr;
conclusion: right_logical_expr;

left_logical_expr
 : left_logical_expr AND left_logical_expr  # LogicalExpressionAnd
 | left_logical_expr OR left_logical_expr   # LogicalExpressionOr
 | function_expr                            # ComparisonExpression
 | function_expr LSPAREN DECIMAL RSPAREN    # ComparisonExpression
 | LPAREN left_logical_expr RPAREN          # LogicalExpressionInParen
 ;

function_expr
            : IDENTIFIER args
            | IDENTIFIER args comp_operator DECIMAL
            | IDENTIFIER
            | IDENTIFIER comp_operator DECIMAL
            | IDENTIFIER comp_operator IDENTIFIER
            | IDENTIFIER args comp_operator IDENTIFIER
            | (TRUE | FALSE);

args : arg args | arg;

arg : DECIMAL | IDENTIFIER;

comp_operator : GT |GE | LT | LE | EQ | NE;


right_logical_expr
 : right_logical_expr AND right_logical_expr    # RLogicalExpressionAnd
 | LPAREN right_logical_expr RPAREN             # RLogicalExpressionInParen
 | r_function_expr                              # RLogicalExpression
 ;

r_function_expr : IDENTIFIER | IDENTIFIER args;

