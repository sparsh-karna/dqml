# Generated from DMQL.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .DMQLParser import DMQLParser
else:
    from DMQLParser import DMQLParser

# This class defines a complete generic visitor for a parse tree produced by DMQLParser.

class DMQLVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by DMQLParser#query.
    def visitQuery(self, ctx:DMQLParser.QueryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMQLParser#useClause.
    def visitUseClause(self, ctx:DMQLParser.UseClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMQLParser#relevanceClause.
    def visitRelevanceClause(self, ctx:DMQLParser.RelevanceClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMQLParser#fromClause.
    def visitFromClause(self, ctx:DMQLParser.FromClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMQLParser#whereClause.
    def visitWhereClause(self, ctx:DMQLParser.WhereClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMQLParser#groupByClause.
    def visitGroupByClause(self, ctx:DMQLParser.GroupByClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMQLParser#orderByClause.
    def visitOrderByClause(self, ctx:DMQLParser.OrderByClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMQLParser#mineClause.
    def visitMineClause(self, ctx:DMQLParser.MineClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMQLParser#withClause.
    def visitWithClause(self, ctx:DMQLParser.WithClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMQLParser#displayClause.
    def visitDisplayClause(self, ctx:DMQLParser.DisplayClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMQLParser#attributeList.
    def visitAttributeList(self, ctx:DMQLParser.AttributeListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMQLParser#attribute.
    def visitAttribute(self, ctx:DMQLParser.AttributeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMQLParser#relationList.
    def visitRelationList(self, ctx:DMQLParser.RelationListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMQLParser#relation.
    def visitRelation(self, ctx:DMQLParser.RelationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMQLParser#orderList.
    def visitOrderList(self, ctx:DMQLParser.OrderListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMQLParser#orderItem.
    def visitOrderItem(self, ctx:DMQLParser.OrderItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMQLParser#BetweenCond.
    def visitBetweenCond(self, ctx:DMQLParser.BetweenCondContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMQLParser#IsNullCond.
    def visitIsNullCond(self, ctx:DMQLParser.IsNullCondContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMQLParser#NotCondition.
    def visitNotCondition(self, ctx:DMQLParser.NotConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMQLParser#LikeCond.
    def visitLikeCond(self, ctx:DMQLParser.LikeCondContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMQLParser#ParenCondition.
    def visitParenCondition(self, ctx:DMQLParser.ParenConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMQLParser#InCond.
    def visitInCond(self, ctx:DMQLParser.InCondContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMQLParser#CompareCondition.
    def visitCompareCondition(self, ctx:DMQLParser.CompareConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMQLParser#OrCondition.
    def visitOrCondition(self, ctx:DMQLParser.OrConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMQLParser#AndCondition.
    def visitAndCondition(self, ctx:DMQLParser.AndConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMQLParser#comparisonCondition.
    def visitComparisonCondition(self, ctx:DMQLParser.ComparisonConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMQLParser#inCondition.
    def visitInCondition(self, ctx:DMQLParser.InConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMQLParser#betweenCondition.
    def visitBetweenCondition(self, ctx:DMQLParser.BetweenConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMQLParser#likeCondition.
    def visitLikeCondition(self, ctx:DMQLParser.LikeConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMQLParser#isNullCondition.
    def visitIsNullCondition(self, ctx:DMQLParser.IsNullConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMQLParser#comparisonOperator.
    def visitComparisonOperator(self, ctx:DMQLParser.ComparisonOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMQLParser#ValueExpr.
    def visitValueExpr(self, ctx:DMQLParser.ValueExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMQLParser#MulDivExpr.
    def visitMulDivExpr(self, ctx:DMQLParser.MulDivExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMQLParser#IdentifierExpr.
    def visitIdentifierExpr(self, ctx:DMQLParser.IdentifierExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMQLParser#QualifiedIdentifierExpr.
    def visitQualifiedIdentifierExpr(self, ctx:DMQLParser.QualifiedIdentifierExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMQLParser#AggregateExpr.
    def visitAggregateExpr(self, ctx:DMQLParser.AggregateExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMQLParser#ParenExpr.
    def visitParenExpr(self, ctx:DMQLParser.ParenExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMQLParser#AddSubExpr.
    def visitAddSubExpr(self, ctx:DMQLParser.AddSubExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMQLParser#aggregateFunction.
    def visitAggregateFunction(self, ctx:DMQLParser.AggregateFunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMQLParser#value.
    def visitValue(self, ctx:DMQLParser.ValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMQLParser#valueList.
    def visitValueList(self, ctx:DMQLParser.ValueListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMQLParser#miningOperation.
    def visitMiningOperation(self, ctx:DMQLParser.MiningOperationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMQLParser#clusterOperation.
    def visitClusterOperation(self, ctx:DMQLParser.ClusterOperationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMQLParser#associationRulesOperation.
    def visitAssociationRulesOperation(self, ctx:DMQLParser.AssociationRulesOperationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMQLParser#anomalyOperation.
    def visitAnomalyOperation(self, ctx:DMQLParser.AnomalyOperationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMQLParser#statisticsOperation.
    def visitStatisticsOperation(self, ctx:DMQLParser.StatisticsOperationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMQLParser#classificationOperation.
    def visitClassificationOperation(self, ctx:DMQLParser.ClassificationOperationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMQLParser#regressionOperation.
    def visitRegressionOperation(self, ctx:DMQLParser.RegressionOperationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMQLParser#interestMeasure.
    def visitInterestMeasure(self, ctx:DMQLParser.InterestMeasureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMQLParser#measureItem.
    def visitMeasureItem(self, ctx:DMQLParser.MeasureItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMQLParser#displayType.
    def visitDisplayType(self, ctx:DMQLParser.DisplayTypeContext):
        return self.visitChildren(ctx)



del DMQLParser