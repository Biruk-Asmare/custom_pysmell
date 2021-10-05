PAR = 5
MLOC = 38
DOC = 3
CLOC = 29
LMC = 5
NBC = 3
NOC,LPAR,NOO = 48,3,7
TNOC,TNOL = 54,3
CNOC,NOFF,CNOO = 62,3,8
LEC,DNC,NCT = 3,3,3

smells_metrics_thresholds = {'LongParameterList':[PAR],'LongMethod':[MLOC],'LongScopeChaining':[DOC],
                             'LongBaseClassList':[NBC],'LargeClass':[CLOC],'LongMessageChain':[LMC],
                             'LongLambdaFunction':[NOC,LPAR,NOO],
                             'LongTernaryConditionalExpression':[TNOC,TNOL], 
                             'ComplexContainerComprehension':[CNOC,NOFF,CNOO],
                             'MultiplyNestedContainer':[LEC,DNC,NCT]}