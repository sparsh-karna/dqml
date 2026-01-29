# Generated from DMQL.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .DMQLParser import DMQLParser
else:
    from DMQLParser import DMQLParser

# This class defines a complete listener for a parse tree produced by DMQLParser.
class DMQLListener(ParseTreeListener):

    # Enter a parse tree produced by DMQLParser#query.
    def enterQuery(self, ctx:DMQLParser.QueryContext):
        pass

    # Exit a parse tree produced by DMQLParser#query.
    def exitQuery(self, ctx:DMQLParser.QueryContext):
        pass


    # Enter a parse tree produced by DMQLParser#useClause.
    def enterUseClause(self, ctx:DMQLParser.UseClauseContext):
        pass

    # Exit a parse tree produced by DMQLParser#useClause.
    def exitUseClause(self, ctx:DMQLParser.UseClauseContext):
        pass


    # Enter a parse tree produced by DMQLParser#relevanceClause.
    def enterRelevanceClause(self, ctx:DMQLParser.RelevanceClauseContext):
        pass

    # Exit a parse tree produced by DMQLParser#relevanceClause.
    def exitRelevanceClause(self, ctx:DMQLParser.RelevanceClauseContext):
        pass


    # Enter a parse tree produced by DMQLParser#fromClause.
    def enterFromClause(self, ctx:DMQLParser.FromClauseContext):
        pass

    # Exit a parse tree produced by DMQLParser#fromClause.
    def exitFromClause(self, ctx:DMQLParser.FromClauseContext):
        pass


    # Enter a parse tree produced by DMQLParser#whereClause.
    def enterWhereClause(self, ctx:DMQLParser.WhereClauseContext):
        pass

    # Exit a parse tree produced by DMQLParser#whereClause.
    def exitWhereClause(self, ctx:DMQLParser.WhereClauseContext):
        pass


    # Enter a parse tree produced by DMQLParser#groupByClause.
    def enterGroupByClause(self, ctx:DMQLParser.GroupByClauseContext):
        pass

    # Exit a parse tree produced by DMQLParser#groupByClause.
    def exitGroupByClause(self, ctx:DMQLParser.GroupByClauseContext):
        pass


    # Enter a parse tree produced by DMQLParser#orderByClause.
    def enterOrderByClause(self, ctx:DMQLParser.OrderByClauseContext):
        pass

    # Exit a parse tree produced by DMQLParser#orderByClause.
    def exitOrderByClause(self, ctx:DMQLParser.OrderByClauseContext):
        pass


    # Enter a parse tree produced by DMQLParser#mineClause.
    def enterMineClause(self, ctx:DMQLParser.MineClauseContext):
        pass

    # Exit a parse tree produced by DMQLParser#mineClause.
    def exitMineClause(self, ctx:DMQLParser.MineClauseContext):
        pass


    # Enter a parse tree produced by DMQLParser#withClause.
    def enterWithClause(self, ctx:DMQLParser.WithClauseContext):
        pass

    # Exit a parse tree produced by DMQLParser#withClause.
    def exitWithClause(self, ctx:DMQLParser.WithClauseContext):
        pass


    # Enter a parse tree produced by DMQLParser#displayClause.
    def enterDisplayClause(self, ctx:DMQLParser.DisplayClauseContext):
        pass

    # Exit a parse tree produced by DMQLParser#displayClause.
    def exitDisplayClause(self, ctx:DMQLParser.DisplayClauseContext):
        pass


    # Enter a parse tree produced by DMQLParser#attributeList.
    def enterAttributeList(self, ctx:DMQLParser.AttributeListContext):
        pass

    # Exit a parse tree produced by DMQLParser#attributeList.
    def exitAttributeList(self, ctx:DMQLParser.AttributeListContext):
        pass


    # Enter a parse tree produced by DMQLParser#attribute.
    def enterAttribute(self, ctx:DMQLParser.AttributeContext):
        pass

    # Exit a parse tree produced by DMQLParser#attribute.
    def exitAttribute(self, ctx:DMQLParser.AttributeContext):
        pass


    # Enter a parse tree produced by DMQLParser#relationList.
    def enterRelationList(self, ctx:DMQLParser.RelationListContext):
        pass

    # Exit a parse tree produced by DMQLParser#relationList.
    def exitRelationList(self, ctx:DMQLParser.RelationListContext):
        pass


    # Enter a parse tree produced by DMQLParser#relation.
    def enterRelation(self, ctx:DMQLParser.RelationContext):
        pass

    # Exit a parse tree produced by DMQLParser#relation.
    def exitRelation(self, ctx:DMQLParser.RelationContext):
        pass


    # Enter a parse tree produced by DMQLParser#orderList.
    def enterOrderList(self, ctx:DMQLParser.OrderListContext):
        pass

    # Exit a parse tree produced by DMQLParser#orderList.
    def exitOrderList(self, ctx:DMQLParser.OrderListContext):
        pass


    # Enter a parse tree produced by DMQLParser#orderItem.
    def enterOrderItem(self, ctx:DMQLParser.OrderItemContext):
        pass

    # Exit a parse tree produced by DMQLParser#orderItem.
    def exitOrderItem(self, ctx:DMQLParser.OrderItemContext):
        pass


    # Enter a parse tree produced by DMQLParser#BetweenCond.
    def enterBetweenCond(self, ctx:DMQLParser.BetweenCondContext):
        pass

    # Exit a parse tree produced by DMQLParser#BetweenCond.
    def exitBetweenCond(self, ctx:DMQLParser.BetweenCondContext):
        pass


    # Enter a parse tree produced by DMQLParser#IsNullCond.
    def enterIsNullCond(self, ctx:DMQLParser.IsNullCondContext):
        pass

    # Exit a parse tree produced by DMQLParser#IsNullCond.
    def exitIsNullCond(self, ctx:DMQLParser.IsNullCondContext):
        pass


    # Enter a parse tree produced by DMQLParser#NotCondition.
    def enterNotCondition(self, ctx:DMQLParser.NotConditionContext):
        pass

    # Exit a parse tree produced by DMQLParser#NotCondition.
    def exitNotCondition(self, ctx:DMQLParser.NotConditionContext):
        pass


    # Enter a parse tree produced by DMQLParser#LikeCond.
    def enterLikeCond(self, ctx:DMQLParser.LikeCondContext):
        pass

    # Exit a parse tree produced by DMQLParser#LikeCond.
    def exitLikeCond(self, ctx:DMQLParser.LikeCondContext):
        pass


    # Enter a parse tree produced by DMQLParser#ParenCondition.
    def enterParenCondition(self, ctx:DMQLParser.ParenConditionContext):
        pass

    # Exit a parse tree produced by DMQLParser#ParenCondition.
    def exitParenCondition(self, ctx:DMQLParser.ParenConditionContext):
        pass


    # Enter a parse tree produced by DMQLParser#InCond.
    def enterInCond(self, ctx:DMQLParser.InCondContext):
        pass

    # Exit a parse tree produced by DMQLParser#InCond.
    def exitInCond(self, ctx:DMQLParser.InCondContext):
        pass


    # Enter a parse tree produced by DMQLParser#CompareCondition.
    def enterCompareCondition(self, ctx:DMQLParser.CompareConditionContext):
        pass

    # Exit a parse tree produced by DMQLParser#CompareCondition.
    def exitCompareCondition(self, ctx:DMQLParser.CompareConditionContext):
        pass


    # Enter a parse tree produced by DMQLParser#OrCondition.
    def enterOrCondition(self, ctx:DMQLParser.OrConditionContext):
        pass

    # Exit a parse tree produced by DMQLParser#OrCondition.
    def exitOrCondition(self, ctx:DMQLParser.OrConditionContext):
        pass


    # Enter a parse tree produced by DMQLParser#AndCondition.
    def enterAndCondition(self, ctx:DMQLParser.AndConditionContext):
        pass

    # Exit a parse tree produced by DMQLParser#AndCondition.
    def exitAndCondition(self, ctx:DMQLParser.AndConditionContext):
        pass


    # Enter a parse tree produced by DMQLParser#comparisonCondition.
    def enterComparisonCondition(self, ctx:DMQLParser.ComparisonConditionContext):
        pass

    # Exit a parse tree produced by DMQLParser#comparisonCondition.
    def exitComparisonCondition(self, ctx:DMQLParser.ComparisonConditionContext):
        pass


    # Enter a parse tree produced by DMQLParser#inCondition.
    def enterInCondition(self, ctx:DMQLParser.InConditionContext):
        pass

    # Exit a parse tree produced by DMQLParser#inCondition.
    def exitInCondition(self, ctx:DMQLParser.InConditionContext):
        pass


    # Enter a parse tree produced by DMQLParser#betweenCondition.
    def enterBetweenCondition(self, ctx:DMQLParser.BetweenConditionContext):
        pass

    # Exit a parse tree produced by DMQLParser#betweenCondition.
    def exitBetweenCondition(self, ctx:DMQLParser.BetweenConditionContext):
        pass


    # Enter a parse tree produced by DMQLParser#likeCondition.
    def enterLikeCondition(self, ctx:DMQLParser.LikeConditionContext):
        pass

    # Exit a parse tree produced by DMQLParser#likeCondition.
    def exitLikeCondition(self, ctx:DMQLParser.LikeConditionContext):
        pass


    # Enter a parse tree produced by DMQLParser#isNullCondition.
    def enterIsNullCondition(self, ctx:DMQLParser.IsNullConditionContext):
        pass

    # Exit a parse tree produced by DMQLParser#isNullCondition.
    def exitIsNullCondition(self, ctx:DMQLParser.IsNullConditionContext):
        pass


    # Enter a parse tree produced by DMQLParser#comparisonOperator.
    def enterComparisonOperator(self, ctx:DMQLParser.ComparisonOperatorContext):
        pass

    # Exit a parse tree produced by DMQLParser#comparisonOperator.
    def exitComparisonOperator(self, ctx:DMQLParser.ComparisonOperatorContext):
        pass


    # Enter a parse tree produced by DMQLParser#ValueExpr.
    def enterValueExpr(self, ctx:DMQLParser.ValueExprContext):
        pass

    # Exit a parse tree produced by DMQLParser#ValueExpr.
    def exitValueExpr(self, ctx:DMQLParser.ValueExprContext):
        pass


    # Enter a parse tree produced by DMQLParser#MulDivExpr.
    def enterMulDivExpr(self, ctx:DMQLParser.MulDivExprContext):
        pass

    # Exit a parse tree produced by DMQLParser#MulDivExpr.
    def exitMulDivExpr(self, ctx:DMQLParser.MulDivExprContext):
        pass


    # Enter a parse tree produced by DMQLParser#IdentifierExpr.
    def enterIdentifierExpr(self, ctx:DMQLParser.IdentifierExprContext):
        pass

    # Exit a parse tree produced by DMQLParser#IdentifierExpr.
    def exitIdentifierExpr(self, ctx:DMQLParser.IdentifierExprContext):
        pass


    # Enter a parse tree produced by DMQLParser#QualifiedIdentifierExpr.
    def enterQualifiedIdentifierExpr(self, ctx:DMQLParser.QualifiedIdentifierExprContext):
        pass

    # Exit a parse tree produced by DMQLParser#QualifiedIdentifierExpr.
    def exitQualifiedIdentifierExpr(self, ctx:DMQLParser.QualifiedIdentifierExprContext):
        pass


    # Enter a parse tree produced by DMQLParser#AggregateExpr.
    def enterAggregateExpr(self, ctx:DMQLParser.AggregateExprContext):
        pass

    # Exit a parse tree produced by DMQLParser#AggregateExpr.
    def exitAggregateExpr(self, ctx:DMQLParser.AggregateExprContext):
        pass


    # Enter a parse tree produced by DMQLParser#ParenExpr.
    def enterParenExpr(self, ctx:DMQLParser.ParenExprContext):
        pass

    # Exit a parse tree produced by DMQLParser#ParenExpr.
    def exitParenExpr(self, ctx:DMQLParser.ParenExprContext):
        pass


    # Enter a parse tree produced by DMQLParser#AddSubExpr.
    def enterAddSubExpr(self, ctx:DMQLParser.AddSubExprContext):
        pass

    # Exit a parse tree produced by DMQLParser#AddSubExpr.
    def exitAddSubExpr(self, ctx:DMQLParser.AddSubExprContext):
        pass


    # Enter a parse tree produced by DMQLParser#aggregateFunction.
    def enterAggregateFunction(self, ctx:DMQLParser.AggregateFunctionContext):
        pass

    # Exit a parse tree produced by DMQLParser#aggregateFunction.
    def exitAggregateFunction(self, ctx:DMQLParser.AggregateFunctionContext):
        pass


    # Enter a parse tree produced by DMQLParser#value.
    def enterValue(self, ctx:DMQLParser.ValueContext):
        pass

    # Exit a parse tree produced by DMQLParser#value.
    def exitValue(self, ctx:DMQLParser.ValueContext):
        pass


    # Enter a parse tree produced by DMQLParser#valueList.
    def enterValueList(self, ctx:DMQLParser.ValueListContext):
        pass

    # Exit a parse tree produced by DMQLParser#valueList.
    def exitValueList(self, ctx:DMQLParser.ValueListContext):
        pass


    # Enter a parse tree produced by DMQLParser#miningOperation.
    def enterMiningOperation(self, ctx:DMQLParser.MiningOperationContext):
        pass

    # Exit a parse tree produced by DMQLParser#miningOperation.
    def exitMiningOperation(self, ctx:DMQLParser.MiningOperationContext):
        pass


    # Enter a parse tree produced by DMQLParser#clusterOperation.
    def enterClusterOperation(self, ctx:DMQLParser.ClusterOperationContext):
        pass

    # Exit a parse tree produced by DMQLParser#clusterOperation.
    def exitClusterOperation(self, ctx:DMQLParser.ClusterOperationContext):
        pass


    # Enter a parse tree produced by DMQLParser#associationRulesOperation.
    def enterAssociationRulesOperation(self, ctx:DMQLParser.AssociationRulesOperationContext):
        pass

    # Exit a parse tree produced by DMQLParser#associationRulesOperation.
    def exitAssociationRulesOperation(self, ctx:DMQLParser.AssociationRulesOperationContext):
        pass


    # Enter a parse tree produced by DMQLParser#anomalyOperation.
    def enterAnomalyOperation(self, ctx:DMQLParser.AnomalyOperationContext):
        pass

    # Exit a parse tree produced by DMQLParser#anomalyOperation.
    def exitAnomalyOperation(self, ctx:DMQLParser.AnomalyOperationContext):
        pass


    # Enter a parse tree produced by DMQLParser#statisticsOperation.
    def enterStatisticsOperation(self, ctx:DMQLParser.StatisticsOperationContext):
        pass

    # Exit a parse tree produced by DMQLParser#statisticsOperation.
    def exitStatisticsOperation(self, ctx:DMQLParser.StatisticsOperationContext):
        pass


    # Enter a parse tree produced by DMQLParser#classificationOperation.
    def enterClassificationOperation(self, ctx:DMQLParser.ClassificationOperationContext):
        pass

    # Exit a parse tree produced by DMQLParser#classificationOperation.
    def exitClassificationOperation(self, ctx:DMQLParser.ClassificationOperationContext):
        pass


    # Enter a parse tree produced by DMQLParser#regressionOperation.
    def enterRegressionOperation(self, ctx:DMQLParser.RegressionOperationContext):
        pass

    # Exit a parse tree produced by DMQLParser#regressionOperation.
    def exitRegressionOperation(self, ctx:DMQLParser.RegressionOperationContext):
        pass


    # Enter a parse tree produced by DMQLParser#interestMeasure.
    def enterInterestMeasure(self, ctx:DMQLParser.InterestMeasureContext):
        pass

    # Exit a parse tree produced by DMQLParser#interestMeasure.
    def exitInterestMeasure(self, ctx:DMQLParser.InterestMeasureContext):
        pass


    # Enter a parse tree produced by DMQLParser#measureItem.
    def enterMeasureItem(self, ctx:DMQLParser.MeasureItemContext):
        pass

    # Exit a parse tree produced by DMQLParser#measureItem.
    def exitMeasureItem(self, ctx:DMQLParser.MeasureItemContext):
        pass


    # Enter a parse tree produced by DMQLParser#displayType.
    def enterDisplayType(self, ctx:DMQLParser.DisplayTypeContext):
        pass

    # Exit a parse tree produced by DMQLParser#displayType.
    def exitDisplayType(self, ctx:DMQLParser.DisplayTypeContext):
        pass



del DMQLParser