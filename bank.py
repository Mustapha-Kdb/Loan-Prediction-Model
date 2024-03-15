#!/usr/bin/env python
# coding: utf-8

from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD


# Defining the model structure. We can define the network by just passing a list of edges.
model = BayesianNetwork(
    [
        ('DebtIncomeRatio', 'PaymentHistory'),
        ('PaymentHistory', 'Age'),
        ('PaymentHistory', 'Reliability'),
        ('Age', 'Reliability'),
        ('Income','Assets'), 
        ('Income', 'FutureIncome'),
        ('Assets', 'FutureIncome'),
        ('DebtIncomeRatio', 'BankLoan'),
        ('Reliability', 'BankLoan'),
        ('FutureIncome', 'BankLoan')
    ]
)

# Defining individual CPDs.
cpd_DebtIncomeRatio = TabularCPD(variable='DebtIncomeRatio', variable_card=2, values=[[0.5], [0.5]], state_names={'DebtIncomeRatio': ['Low', 'High']})
cpd_Income = TabularCPD(variable='Income', variable_card=3, values=[[0.333], [0.333], [0.334]], state_names={'Income': ['High', 'Medium', 'Low']})


# The representation of CPD in pgmpy is a bit different than the CPD shown in the above picture. In pgmpy the colums
# are the evidences and rows are the states of the variable. So the grade CPD is represented like this:
#
#    +----------------+----------------+----------------+-----------+----------------+----------------+------------+----------------+----------------+--------------+
#    | PaymentHistory |   Excellent    |    Excellent   | Excellent |   Acceptable   |   Acceptable   | Acceptable |  Unacceptable  |  Unacceptable  | Unacceptable |
#    +----------------+----------------+----------------+-----------+----------------+----------------+------------+----------------+----------------+--------------+
#    | Age            | Between16and25 | Between26and64 |   Over65  | Between16and25 | Between26and64 |   Over65   | Between16and25 | Between26and64 |    Over65    |
#    +----------------+----------------+----------------+-----------+----------------+----------------+------------+----------------+----------------+--------------+
#    | Reliability_0  |       0.7      |       0.8      |    0.9    |       0.6      |       0.7      |     0.8    |       0.5      |       0.6      |      0.7     |
#    +----------------+----------------+----------------+-----------+----------------+----------------+------------+----------------+----------------+--------------+
#    | Reliability_1  |       0.3      |       0.2      |    0.1    |       0.4      |       0.3      |     0.2    |       0.5      |       0.4      |      0.3     |
#    +----------------+----------------+----------------+-----------+----------------+----------------+------------+----------------+----------------+--------------+


cpd_Reliability = TabularCPD(variable='Reliability', variable_card=2,
                      values=[[0.7, 0.8, 0.9, 0.6, 0.7, 0.8, 0.5, 0.6, 0.7],
                              [0.3, 0.2, 0.1, 0.4, 0.3, 0.2, 0.5, 0.4, 0.3],],
                      evidence=['PaymentHistory','Age'],
                      evidence_card=[3,3],
                      state_names={'Reliability': ['Reliable', 'Unreliable'],
                                   'PaymentHistory': ['Excellent', 'Acceptable', 'Unacceptable'],
                                   'Age': ['Between16and25', 'Between26and64', 'Over65']})

cpd_Age = TabularCPD(variable='Age', variable_card=3, 
                      values=[[0.1, 0.333, 0.6],
                              [0.3, 0.333, 0.3],
                              [0.6, 0.334, 0.1]],
                      evidence=['PaymentHistory'],
                      evidence_card=[3],
                      state_names={'Age': ['Between16and25', 'Between26and64', 'Over65'],
                                   'PaymentHistory': ['Excellent', 'Acceptable', 'Unacceptable']})


cpd_PaymentHistory = TabularCPD(variable='PaymentHistory', variable_card=3, 
                      values=[[0.6, 0.1],
                              [0.3, 0.3],
                              [0.1, 0.6]],
                      evidence=['DebtIncomeRatio'],
                      evidence_card=[2],
                      state_names={'PaymentHistory': ['Excellent', 'Acceptable', 'Unacceptable'],
                                   'DebtIncomeRatio': ['Low', 'High']})

cpd_BankLoan = TabularCPD(variable='BankLoan', variable_card=2, 
                      values=[[0.8, 0.6, 0.6, 0.4, 0.6, 0.4, 0.4, 0.2],
                              [0.2, 0.4, 0.4, 0.6, 0.4, 0.6, 0.6, 0.8]],
                      evidence=['DebtIncomeRatio','Reliability','FutureIncome'],
                      evidence_card=[2,2,2],
                      state_names={'BankLoan': ['Positive', 'Negative'],
                                   'DebtIncomeRatio': ['Low', 'High'],
                                   'Reliability': ['Reliable', 'Unreliable'],
                                   'FutureIncome': ['Promising', 'Not_promising']})

# {'DebtIncomeRatio': ['Low', 'High']})
# {'Income': ['High', 'Medium', 'Low']})
# {'PaymentHistory': ['Excellent', 'Acceptable', 'Unacceptable']}
# {'Age': ['Between16and25', 'Between26and64', 'Over65']}
# {'Reliability': ['Reliable', 'Unreliable']}
# {'Assets': ['High', 'Medium', 'Low']}
# {'FutureIncome': ['Promising', 'Not_promising']}
# {'BankLoan': ['Positive', 'Negative']}

# To complete
# cpd_Assets =

# cpd_FutureIncome =

# model.add_cpds(cpd_DebtIncomeRatio, cpd_Income, cpd_PaymentHistory, cpd_Age, cpd_Reliability, cpd_Assets, cpd_FutureIncome, cpd_BankLoan)
# model.check_model()
