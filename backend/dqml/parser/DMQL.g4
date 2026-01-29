/**
 * DMQL (Data Mining Query Language) Grammar
 * 
 * A SQL-like language for data mining operations.
 * Based on Han et al. (1996) DMQL specification, modernized for DQML Platform.
 * 
 * Author: DQML Platform Team
 * Date: January 30, 2026
 */

grammar DMQL;

// ============================================================================
// PARSER RULES
// ============================================================================

// Entry point - a complete DMQL query
query
    : useClause
      (relevanceClause)?
      fromClause
      (whereClause)?
      (groupByClause)?
      (orderByClause)?
      (mineClause)?
      (withClause)?
      (displayClause)?
      EOF
    ;

// USE DATABASE database_name
useClause
    : USE DATABASE IDENTIFIER
    ;

// RELEVANCE TO attribute_list
relevanceClause
    : RELEVANCE TO attributeList
    ;

// FROM relation(s)
fromClause
    : FROM relationList
    ;

// WHERE condition
whereClause
    : WHERE condition
    ;

// GROUP BY attribute_list
groupByClause
    : GROUP BY attributeList
    ;

// ORDER BY attribute_list (ASC|DESC)?
orderByClause
    : ORDER BY orderList
    ;

// MINE mining_operation
mineClause
    : MINE miningOperation
    ;

// WITH interest_measure THRESHOLD = value
withClause
    : WITH interestMeasure
    ;

// DISPLAY AS visualization_type
displayClause
    : DISPLAY AS displayType
    ;

// ============================================================================
// ATTRIBUTE AND RELATION LISTS
// ============================================================================

attributeList
    : attribute (COMMA attribute)*
    ;

attribute
    : IDENTIFIER
    | IDENTIFIER DOT IDENTIFIER    // table.column notation
    | STAR                          // wildcard *
    ;

relationList
    : relation (COMMA relation)*
    ;

relation
    : IDENTIFIER (AS IDENTIFIER)?   // table with optional alias
    ;

orderList
    : orderItem (COMMA orderItem)*
    ;

orderItem
    : IDENTIFIER (ASC | DESC)?
    ;

// ============================================================================
// CONDITIONS (WHERE clause expressions)
// ============================================================================

condition
    : condition AND condition                           # AndCondition
    | condition OR condition                            # OrCondition
    | NOT condition                                     # NotCondition
    | LPAREN condition RPAREN                           # ParenCondition
    | comparisonCondition                               # CompareCondition
    | inCondition                                       # InCond
    | betweenCondition                                  # BetweenCond
    | likeCondition                                     # LikeCond
    | isNullCondition                                   # IsNullCond
    ;

comparisonCondition
    : expression comparisonOperator expression
    ;

inCondition
    : IDENTIFIER IN LPAREN valueList RPAREN
    | IDENTIFIER NOT IN LPAREN valueList RPAREN
    ;

betweenCondition
    : IDENTIFIER BETWEEN value AND value
    | IDENTIFIER NOT BETWEEN value AND value
    ;

likeCondition
    : IDENTIFIER LIKE STRING
    | IDENTIFIER NOT LIKE STRING
    ;

isNullCondition
    : IDENTIFIER IS NULL
    | IDENTIFIER IS NOT NULL
    ;

comparisonOperator
    : EQ | NEQ | GT | LT | GTE | LTE
    ;

expression
    : value                                             # ValueExpr
    | IDENTIFIER                                        # IdentifierExpr
    | IDENTIFIER DOT IDENTIFIER                         # QualifiedIdentifierExpr
    | aggregateFunction                                 # AggregateExpr
    | LPAREN expression RPAREN                          # ParenExpr
    | expression (STAR | SLASH) expression              # MulDivExpr
    | expression (PLUS | MINUS) expression              # AddSubExpr
    ;

aggregateFunction
    : (COUNT | SUM | AVG | MIN | MAX) LPAREN (STAR | IDENTIFIER) RPAREN
    ;

// ============================================================================
// VALUES
// ============================================================================

value
    : INT
    | FLOAT
    | STRING
    | TRUE
    | FALSE
    | NULL
    ;

valueList
    : value (COMMA value)*
    ;

// ============================================================================
// MINING OPERATIONS
// ============================================================================

miningOperation
    : clusterOperation
    | associationRulesOperation
    | anomalyOperation
    | statisticsOperation
    | classificationOperation
    | regressionOperation
    ;

// CLUSTER K = n
clusterOperation
    : CLUSTER KPARAM EQ INT
    ;

// ASSOCIATION_RULES
associationRulesOperation
    : ASSOCIATION_RULES
    ;

// ANOMALIES or ANOMALY_DETECTION
anomalyOperation
    : ANOMALIES
    | ANOMALY_DETECTION
    ;

// STATISTICS
statisticsOperation
    : STATISTICS
    ;

// CLASSIFICATION TARGET = column
classificationOperation
    : CLASSIFICATION TARGET EQ IDENTIFIER
    ;

// REGRESSION TARGET = column
regressionOperation
    : REGRESSION TARGET EQ IDENTIFIER
    ;

// ============================================================================
// INTEREST MEASURES (WITH clause)
// ============================================================================

interestMeasure
    : measureItem (COMMA measureItem)*
    ;

measureItem
    : CONFIDENCE EQ (FLOAT | INT)
    | SUPPORT EQ (FLOAT | INT)
    | LIFT EQ (FLOAT | INT)
    | THRESHOLD EQ (FLOAT | INT)
    | CONFIDENCE_LEVEL EQ (FLOAT | INT)
    ;

// ============================================================================
// DISPLAY/VISUALIZATION TYPES
// ============================================================================

displayType
    : TABLE
    | BAR_CHART
    | LINE_CHART
    | SCATTER_PLOT
    | HEATMAP
    | PIE_CHART
    | HISTOGRAM
    | BOX_PLOT
    | IDENTIFIER                    // Allow custom visualization types
    ;

// ============================================================================
// LEXER RULES (TOKENS)
// ============================================================================

// Keywords
USE             : U S E ;
DATABASE        : D A T A B A S E ;
RELEVANCE       : R E L E V A N C E ;
TO              : T O ;
FROM            : F R O M ;
WHERE           : W H E R E ;
GROUP           : G R O U P ;
BY              : B Y ;
ORDER           : O R D E R ;
ASC             : A S C ;
DESC            : D E S C ;
MINE            : M I N E ;
WITH            : W I T H ;
DISPLAY         : D I S P L A Y ;
AS              : A S ;

// Boolean operators
AND             : A N D ;
OR              : O R ;
NOT             : N O T ;
IN              : I N ;
BETWEEN         : B E T W E E N ;
LIKE            : L I K E ;
IS              : I S ;

// Boolean values
TRUE            : T R U E ;
FALSE           : F A L S E ;
NULL            : N U L L ;

// Mining operations
CLUSTER         : C L U S T E R ;
ASSOCIATION_RULES : A S S O C I A T I O N '_' R U L E S ;
ANOMALIES       : A N O M A L I E S ;
ANOMALY_DETECTION : A N O M A L Y '_' D E T E C T I O N ;
STATISTICS      : S T A T I S T I C S ;
CLASSIFICATION  : C L A S S I F I C A T I O N ;
REGRESSION      : R E G R E S S I O N ;
TARGET          : T A R G E T ;

// Interest measures
KPARAM          : K ;
CONFIDENCE      : C O N F I D E N C E ;
SUPPORT         : S U P P O R T ;
LIFT            : L I F T ;
THRESHOLD       : T H R E S H O L D ;
CONFIDENCE_LEVEL : C O N F I D E N C E '_' L E V E L ;

// Aggregate functions
COUNT           : C O U N T ;
SUM             : S U M ;
AVG             : A V G ;
MIN             : M I N ;
MAX             : M A X ;

// Display types
TABLE           : T A B L E ;
BAR_CHART       : B A R '_' C H A R T ;
LINE_CHART      : L I N E '_' C H A R T ;
SCATTER_PLOT    : S C A T T E R '_' P L O T ;
HEATMAP         : H E A T M A P ;
PIE_CHART       : P I E '_' C H A R T ;
HISTOGRAM       : H I S T O G R A M ;
BOX_PLOT        : B O X '_' P L O T ;

// Comparison operators
EQ              : '=' ;
NEQ             : '!=' | '<>' ;
GT              : '>' ;
LT              : '<' ;
GTE             : '>=' ;
LTE             : '<=' ;

// Arithmetic operators
PLUS            : '+' ;
MINUS           : '-' ;
STAR            : '*' ;
SLASH           : '/' ;

// Punctuation
LPAREN          : '(' ;
RPAREN          : ')' ;
COMMA           : ',' ;
DOT             : '.' ;
SEMICOLON       : ';' ;

// Literals
INT             : DIGIT+ ;
FLOAT           : DIGIT+ '.' DIGIT+ ;
STRING          : '\'' (~['\r\n] | '\'\'')* '\''
                | '"' (~["\r\n] | '""')* '"'
                ;

// Identifiers
IDENTIFIER      : LETTER (LETTER | DIGIT | '_')* ;

// Whitespace and comments
WS              : [ \t\r\n]+ -> skip ;
LINE_COMMENT    : '--' ~[\r\n]* -> skip ;
BLOCK_COMMENT   : '/*' .*? '*/' -> skip ;

// ============================================================================
// FRAGMENT RULES (helpers for lexer)
// ============================================================================

fragment DIGIT  : [0-9] ;
fragment LETTER : [a-zA-Z_] ;

// Case-insensitive letter fragments
fragment A : [aA] ;
fragment B : [bB] ;
fragment C : [cC] ;
fragment D : [dD] ;
fragment E : [eE] ;
fragment F : [fF] ;
fragment G : [gG] ;
fragment H : [hH] ;
fragment I : [iI] ;
fragment J : [jJ] ;
fragment K : [kK] ;
fragment L : [lL] ;
fragment M : [mM] ;
fragment N : [nN] ;
fragment O : [oO] ;
fragment P : [pP] ;
fragment Q : [qQ] ;
fragment R : [rR] ;
fragment S : [sS] ;
fragment T : [tT] ;
fragment U : [uU] ;
fragment V : [vV] ;
fragment W : [wW] ;
fragment X : [xX] ;
fragment Y : [yY] ;
fragment Z : [zZ] ;
