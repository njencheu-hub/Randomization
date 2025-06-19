
# A fundamental assumption in A/B testing is that the only distinction between the test 
# and control groups should be the specific feature being evaluated. This necessitates 
# that the user distributions in both groups are comparable. If this condition holds true, 
# the impact of the feature change on the metric being tested can be accurately estimated.

# For instance, if 10% of users in the test group are from the US, 
# we expect approximately 10% of users in the control group to also be from the US. 
# Similarly, if 50% of users in the test group are repeat users, 
# a similar percentage should be observed in the control group.

import pandas as pd
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 350)
#read from google drive
data = pd.read_csv("https://drive.google.com/uc?export=download&id=1jYFe4qjaQ1ZZZrqJ2R8Nu-eRBjhAfsoL")
print(data.head())

# output
#    user_id source  device browser_language      browser sex  age    country  test  conversion
# 0        1    SEO     Web               EN       Chrome   M   38      Chile     0           0
# 1        2    SEO  Mobile               ES  Android_App   M   27   Colombia     0           0
# 2        3    SEO  Mobile               ES   Iphone_App   M   18  Guatemala     1           0
# 3        5    Ads     Web               ES       Chrome   M   22  Argentina     1           0
# 4        8    Ads  Mobile               ES  Android_App   M   19  Venezuela     1           0

# --------
# Check A/B Test Randomization
# --------

# Checking that randomization worked well simply means making sure that 
# all variables have the same distribution in test and control. 
# So, taking for instance the first variable, source, it would mean checking that 
# the proportion of users coming from ads, SEO, and direct is the same.

# This can easily be done the following way:

# # Check A/B randomization by 'source'
# source_counts = data.groupby(["source", "test"])["user_id"].count().unstack()

# # get relative frequencies
# source_proportions = source_counts.div(source_counts.sum(axis=1), axis=0)

# # What This Does:
# # groupby(["source", "test"])["user_id"].count(): counts users in each source/test group.
# # .unstack(): pivots the test group (0/1) into columns.
# # .div(..., axis=0): divides each row by its total to get relative frequencies.

# print("\nRaw counts by source:")
# print(source_counts)

# print("\nProportions by source:")
# print(source_proportions)

# Raw counts by source:
# test        0      1
# source
# Ads     74352  86448
# Direct  37238  43047
# SEO     73721  86279

# Proportions by source:
# test           0         1
# source
# Ads     0.462388  0.537612
# Direct  0.463823  0.536177
# SEO     0.460756  0.539244

# Interpretation:
# Balanced Randomization: All traffic sources have a very consistent distribution: 
# around 46% in control and 54% in test.
# No Major Imbalance: The differences between sources (e.g., Ads vs SEO) are minimal 
# and likely due to chance. This implies randomization worked properly.
# Slight Skew Toward Test: The test group is consistently a bit larger (~54%) than control (~46%), 
# but this is applied evenly across all sources — so it doesn't compromise randomization quality.

# Summary:
# Randomization looks successful for the source variable. 
# The proportions of users in control vs. test are nearly identical across traffic sources, 
# so we can reasonably say that traffic source is not confounding the test results.

# To ensure that the test and control groups are comparable, 
# we can analyze their distributions across all relavant columns, which can be tedious and time-consuming, 
# so we approach this as a machine learning problem.

# -------
# Machine Leraning Approach
# -------

# For this analysis, a decision tree model is suitable because it provides clear insights 
# into which variables (if any) contribute to the differentiation between test and control groups. 
# This approach helps pinpoint where randomization may not have worked as intended.


import graphviz
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_graphviz
from graphviz import Source
  
#drop user_id, not needed
data = data.drop(['user_id'], axis=1)

#make dummy vars. Don't drop one level here, keep them all. You don't want 
# to risk dropping the one level that actually creates problems with the randomization
data_dummy = pd.get_dummies(data)

#model features, test is the label and conversion is not needed here
train_cols = data_dummy.drop(['test', 'conversion'], axis=1)
  
tree=DecisionTreeClassifier(
    #change weights. Our data set is now perfectly balanced. It makes easier to look at tree output
    class_weight="balanced",
    #only split if if it's worthwhile. The default value of 0 means always split no matter what if you can increase overall performance, which creates tons of noisy and irrelevant splits
    min_impurity_decrease = 0.001
    )
tree.fit(train_cols,data_dummy['test'])
  
# export_graphviz(tree, out_file="tree_test.dot", feature_names=train_cols.columns, proportion=True, rotate=True)
# s = Source.from_file("tree_test.dot")
# s.view()

# --- Replace old export and s.view() with this ---
from sklearn.tree import plot_tree

import matplotlib.pyplot as plt

# Make a figure
plt.figure(figsize=(20, 20))

# Plot the tree using sklearn's plot_tree (better integration with matplotlib)
plot_tree(
    tree,
    feature_names=train_cols.columns,
    class_names=["Control", "Test"],
    filled=True,
    proportion=True,
    rounded=True,
    max_depth=3  # Limit depth to keep it readable; adjust as needed
)

# Save to file
plt.savefig("randomization_tree.png", bbox_inches='tight')
plt.close()

# We can see that the test and control are not the same. 
# Users from Argentina and Uruguay are way more likely to be in the test than the control. 
# When country_Argentina is 1, the tree shows that users in control are ~23% and 
# in test 73% instead of 50/50. For Uruguay, the proportions are even more extreme: 
# 11% in control and 89% in test! Not good!

# Let’s double check this manually in our dataset.

print(data_dummy.groupby("test")[["country_Argentina", "country_Uruguay"]].mean())

#         country_Argentina  country_Uruguay
# test
# 0              0.050488         0.002239
# 1              0.173223         0.017236

# Our tree was right! In test, 17% of users are from Argentina, 
# but in control only 5% of users are from Argentina. 
# Uruguay is even more extreme: 
# test has 1.7% of users from Uruguay and control has just 0.2% of Uruguayan users

# And this is a big problem because that means we are not comparing anymore 
# apples to apples in our A/B test. The difference we might see in conversion rate might 
# very well depend on the fact that users between the two groups are different.

# Let’s check it in practice:

from scipy import stats
  
#this is the test results using the orginal dataset
original_data = stats.ttest_ind(data_dummy.loc[data['test'] == 1]['conversion'], 
                                data_dummy.loc[data['test'] == 0]['conversion'], 
                                equal_var=False)
  
#this is after removing Argentina and Uruguay
data_no_AR_UR = stats.ttest_ind(data_dummy.loc[(data['test'] == 1) & (data_dummy['country_Argentina'] ==  0) & (data_dummy['country_Uruguay'] ==  0)]['conversion'], 
                                data_dummy.loc[(data['test'] == 0) & (data_dummy['country_Argentina'] ==  0) & (data_dummy['country_Uruguay'] ==  0)]['conversion'], 
                                equal_var=False)
  
print(pd.DataFrame( {"data_type" : ["Full", "Removed_Argentina_Uruguay"], 
                         "p_value" : [original_data.pvalue, data_no_AR_UR.pvalue],
                         "t_statistic" : [original_data.statistic, data_no_AR_UR.statistic]
                         }))

# output
#                    data_type       p_value  t_statistic
# 0                       Full  1.928918e-13    -7.353895
# 1  Removed_Argentina_Uruguay  7.200849e-01     0.358346

# There's a significant discrepancy observed in the test results where certain countries 
# were either overrepresented or underrepresented, leading to a statistically significant 
# negative t-statistic indicating that the test performed worse than the control. 
# Upon removing data from these two countries, the results become non-significant.

# At this juncture, you have two main courses of action:
# 1. Recognize the presence of a bug and engage with the software engineer responsible 
# for the randomization process. Investigate the root cause of the issue, rectify it, 
# and then rerun the test. It's essential to delve deeper into the bug's discovery, 
# as it may hint at broader underlying issues beyond just the identified issue.

# 2. If investigation reveals that everything else was functioning correctly except for 
# the disparity in those two countries, you could consider adjusting the weights or distribution 
# for these segments. This adjustment aims to align the relative frequencies of these countries 
# with others, thereby restoring balance. Subsequently, you can rerun the test to ensure a fair comparison.

# These steps are crucial to maintain the integrity and reliability of A/B test results, 
# ensuring that decisions based on testing outcomes are sound and accurate.
