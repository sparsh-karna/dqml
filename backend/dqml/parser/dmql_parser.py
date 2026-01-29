"""
DMQL Parser - High-level interface for parsing DMQL queries.

This module provides a clean API for parsing DMQL queries into AST representations
that can be used by the executor and other components.

Usage:
    from backend.dqml.parser import parse_query
    
    query = '''
    USE DATABASE sales_data
    FROM customers
    WHERE age > 25
    MINE STATISTICS
    '''
    
    result = parse_query(query)
    print(result.database)  # 'sales_data'
    print(result.tables)    # ['customers']
"""

from typing import Optional, List, Dict, Any, Union
from dataclasses import dataclass, field
from antlr4 import CommonTokenStream, InputStream
from antlr4.error.ErrorListener import ErrorListener

from .DMQLLexer import DMQLLexer
from .DMQLParser import DMQLParser
from .DMQLVisitor import DMQLVisitor


# ============================================================================
# DATA CLASSES FOR AST REPRESENTATION
# ============================================================================

@dataclass
class Condition:
    """Represents a WHERE clause condition."""
    left: str
    operator: str
    right: Any
    logical_op: Optional[str] = None  # AND, OR, NOT
    nested: Optional[List['Condition']] = None


@dataclass 
class MiningOperation:
    """Represents a MINE clause operation."""
    operation_type: str  # CLUSTER, STATISTICS, ANOMALIES, etc.
    parameters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class InterestMeasure:
    """Represents interest measures in WITH clause."""
    confidence: Optional[float] = None
    support: Optional[float] = None
    lift: Optional[float] = None
    threshold: Optional[float] = None
    confidence_level: Optional[float] = None


@dataclass
class DMQLQuery:
    """Complete parsed DMQL query representation."""
    database: str
    tables: List[str]
    columns: List[str] = field(default_factory=list)
    conditions: Optional[Condition] = None
    group_by: List[str] = field(default_factory=list)
    order_by: List[tuple] = field(default_factory=list)  # [(col, ASC/DESC), ...]
    mining_operation: Optional[MiningOperation] = None
    interest_measures: Optional[InterestMeasure] = None
    display_type: str = 'table'
    raw_query: str = ''
    errors: List[str] = field(default_factory=list)


# ============================================================================
# ERROR LISTENER
# ============================================================================

class DMQLErrorListener(ErrorListener):
    """Custom error listener to collect parsing errors."""
    
    def __init__(self):
        super().__init__()
        self.errors: List[str] = []
    
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.errors.append(f"Line {line}:{column} - {msg}")


# ============================================================================
# AST VISITOR
# ============================================================================

class DMQLQueryVisitor(DMQLVisitor):
    """Visitor that builds a DMQLQuery from the parse tree."""
    
    def __init__(self):
        self.query = DMQLQuery(database='', tables=[])
    
    def visitQuery(self, ctx: DMQLParser.QueryContext):
        """Visit the root query node."""
        # Visit all children
        self.visitChildren(ctx)
        return self.query
    
    def visitUseClause(self, ctx: DMQLParser.UseClauseContext):
        """Extract database name from USE clause."""
        self.query.database = ctx.IDENTIFIER().getText()
        return self.visitChildren(ctx)
    
    def visitRelevanceClause(self, ctx: DMQLParser.RelevanceClauseContext):
        """Extract columns from RELEVANCE TO clause."""
        attr_list = ctx.attributeList()
        if attr_list:
            self.query.columns = self._extractAttributeList(attr_list)
        return self.visitChildren(ctx)
    
    def visitFromClause(self, ctx: DMQLParser.FromClauseContext):
        """Extract table names from FROM clause."""
        relation_list = ctx.relationList()
        if relation_list:
            for relation in relation_list.relation():
                # Get the first identifier (table name)
                identifiers = relation.IDENTIFIER()
                if identifiers:
                    self.query.tables.append(identifiers[0].getText())
        return self.visitChildren(ctx)
    
    def visitWhereClause(self, ctx: DMQLParser.WhereClauseContext):
        """Extract conditions from WHERE clause."""
        condition_ctx = ctx.condition()
        if condition_ctx:
            self.query.conditions = self._extractCondition(condition_ctx)
        return self.visitChildren(ctx)
    
    def visitGroupByClause(self, ctx: DMQLParser.GroupByClauseContext):
        """Extract GROUP BY columns."""
        attr_list = ctx.attributeList()
        if attr_list:
            self.query.group_by = self._extractAttributeList(attr_list)
        return self.visitChildren(ctx)
    
    def visitOrderByClause(self, ctx: DMQLParser.OrderByClauseContext):
        """Extract ORDER BY columns with direction."""
        order_list = ctx.orderList()
        if order_list:
            for order_item in order_list.orderItem():
                col = order_item.IDENTIFIER().getText()
                direction = 'ASC'
                if order_item.DESC():
                    direction = 'DESC'
                self.query.order_by.append((col, direction))
        return self.visitChildren(ctx)
    
    def visitMineClause(self, ctx: DMQLParser.MineClauseContext):
        """Extract mining operation from MINE clause."""
        mining_op = ctx.miningOperation()
        if mining_op:
            self.query.mining_operation = self._extractMiningOperation(mining_op)
        return self.visitChildren(ctx)
    
    def visitWithClause(self, ctx: DMQLParser.WithClauseContext):
        """Extract interest measures from WITH clause."""
        interest = ctx.interestMeasure()
        if interest:
            self.query.interest_measures = self._extractInterestMeasures(interest)
        return self.visitChildren(ctx)
    
    def visitDisplayClause(self, ctx: DMQLParser.DisplayClauseContext):
        """Extract display type from DISPLAY AS clause."""
        display_type = ctx.displayType()
        if display_type:
            self.query.display_type = display_type.getText().lower()
        return self.visitChildren(ctx)
    
    # ========================================================================
    # HELPER METHODS
    # ========================================================================
    
    def _extractAttributeList(self, ctx) -> List[str]:
        """Extract list of attribute names."""
        attributes = []
        for attr in ctx.attribute():
            identifiers = attr.IDENTIFIER()
            if identifiers:
                if len(identifiers) == 2:
                    # table.column notation
                    attributes.append(f"{identifiers[0].getText()}.{identifiers[1].getText()}")
                else:
                    attributes.append(identifiers[0].getText())
            elif attr.STAR():
                attributes.append('*')
        return attributes
    
    def _extractCondition(self, ctx) -> Condition:
        """Recursively extract conditions from condition context."""
        # Get the text representation for simple parsing
        text = ctx.getText()
        
        # Handle different condition types based on context type
        if hasattr(ctx, 'comparisonCondition') and ctx.comparisonCondition():
            comp = ctx.comparisonCondition()
            return self._extractComparisonCondition(comp)
        
        # For AND/OR conditions
        if ctx.AND():
            conditions = ctx.condition()
            if len(conditions) >= 2:
                left = self._extractCondition(conditions[0])
                right = self._extractCondition(conditions[1])
                return Condition(
                    left='',
                    operator='AND',
                    right=None,
                    logical_op='AND',
                    nested=[left, right]
                )
        
        if ctx.OR():
            conditions = ctx.condition()
            if len(conditions) >= 2:
                left = self._extractCondition(conditions[0])
                right = self._extractCondition(conditions[1])
                return Condition(
                    left='',
                    operator='OR', 
                    right=None,
                    logical_op='OR',
                    nested=[left, right]
                )
        
        # Handle parenthesized condition
        if hasattr(ctx, 'LPAREN') and ctx.LPAREN():
            inner_conditions = ctx.condition()
            if inner_conditions:
                if isinstance(inner_conditions, list):
                    return self._extractCondition(inner_conditions[0])
                return self._extractCondition(inner_conditions)
        
        # Handle comparison condition child
        children = list(ctx.getChildren())
        for child in children:
            if hasattr(child, 'comparisonCondition'):
                return self._extractComparisonCondition(child.comparisonCondition())
            if isinstance(child, DMQLParser.ComparisonConditionContext):
                return self._extractComparisonCondition(child)
        
        # Fallback: return raw text as condition
        return Condition(left=text, operator='=', right=text)
    
    def _extractComparisonCondition(self, ctx) -> Condition:
        """Extract a simple comparison condition."""
        expressions = ctx.expression()
        op_ctx = ctx.comparisonOperator()
        
        left = expressions[0].getText() if expressions else ''
        operator = op_ctx.getText() if op_ctx else '='
        right_val = expressions[1].getText() if len(expressions) > 1 else ''
        
        # Try to convert right value to appropriate type
        right: Any = right_val
        if right_val.isdigit():
            right = int(right_val)
        elif right_val.replace('.', '').isdigit():
            right = float(right_val)
        elif right_val.startswith("'") and right_val.endswith("'"):
            right = right_val[1:-1]
        elif right_val.startswith('"') and right_val.endswith('"'):
            right = right_val[1:-1]
        
        return Condition(left=left, operator=operator, right=right)
    
    def _extractMiningOperation(self, ctx) -> MiningOperation:
        """Extract mining operation details."""
        # Check for cluster operation
        if ctx.clusterOperation():
            cluster = ctx.clusterOperation()
            k_value = int(cluster.INT().getText())
            return MiningOperation(
                operation_type='CLUSTER',
                parameters={'k': k_value}
            )
        
        # Check for statistics
        if ctx.statisticsOperation():
            return MiningOperation(operation_type='STATISTICS')
        
        # Check for anomaly detection
        if ctx.anomalyOperation():
            return MiningOperation(operation_type='ANOMALIES')
        
        # Check for association rules
        if ctx.associationRulesOperation():
            return MiningOperation(operation_type='ASSOCIATION_RULES')
        
        # Check for classification
        if ctx.classificationOperation():
            classification = ctx.classificationOperation()
            target = classification.IDENTIFIER().getText()
            return MiningOperation(
                operation_type='CLASSIFICATION',
                parameters={'target': target}
            )
        
        # Check for regression
        if ctx.regressionOperation():
            regression = ctx.regressionOperation()
            target = regression.IDENTIFIER().getText()
            return MiningOperation(
                operation_type='REGRESSION',
                parameters={'target': target}
            )
        
        return MiningOperation(operation_type='UNKNOWN')
    
    def _extractInterestMeasures(self, ctx) -> InterestMeasure:
        """Extract interest measures from WITH clause."""
        measures = InterestMeasure()
        
        for item in ctx.measureItem():
            text = item.getText().lower()
            
            # Extract the value
            float_val = item.FLOAT()
            int_val = item.INT()
            value = float(float_val.getText()) if float_val else float(int_val.getText()) if int_val else 0.0
            
            if 'confidence_level' in text:
                measures.confidence_level = value
            elif 'confidence' in text:
                measures.confidence = value
            elif 'support' in text:
                measures.support = value
            elif 'lift' in text:
                measures.lift = value
            elif 'threshold' in text:
                measures.threshold = value
        
        return measures


# ============================================================================
# PUBLIC API
# ============================================================================

def parse_query(query: str) -> DMQLQuery:
    """
    Parse a DMQL query string and return a DMQLQuery object.
    
    Args:
        query: The DMQL query string to parse
        
    Returns:
        DMQLQuery object containing parsed query components
        
    Example:
        >>> query = '''
        ... USE DATABASE sales_data
        ... FROM customers
        ... WHERE age > 25
        ... '''
        >>> result = parse_query(query)
        >>> print(result.database)
        'sales_data'
    """
    # Create input stream
    input_stream = InputStream(query)
    
    # Create lexer
    lexer = DMQLLexer(input_stream)
    lexer.removeErrorListeners()
    error_listener = DMQLErrorListener()
    lexer.addErrorListener(error_listener)
    
    # Create token stream
    stream = CommonTokenStream(lexer)
    
    # Create parser
    parser = DMQLParser(stream)
    parser.removeErrorListeners()
    parser.addErrorListener(error_listener)
    
    # Parse the query
    tree = parser.query()
    
    # Visit the parse tree to build AST
    visitor = DMQLQueryVisitor()
    result = visitor.visit(tree)
    
    # Store raw query and any errors
    result.raw_query = query
    result.errors = error_listener.errors
    
    return result


def validate_query(query: str) -> tuple[bool, List[str]]:
    """
    Validate a DMQL query without fully parsing it.
    
    Args:
        query: The DMQL query string to validate
        
    Returns:
        Tuple of (is_valid, error_messages)
    """
    result = parse_query(query)
    is_valid = len(result.errors) == 0
    return is_valid, result.errors
