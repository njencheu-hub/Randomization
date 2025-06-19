import pandas
#read from google drive
data = pandas.read_csv("https://drive.google.com/uc?export=download&id=1E8aYgxZpYXO_HxLgQPAGMUS1_fbfTW5d")
# print(data.head())

# output
#   user_id  conversion  test
# 0   860955           0     0
# 1   911569           0     1
# 2   673989           0     0
# 3   562761           0     0
# 4    64288           0     0

# user_id: Identifies each user uniquely
# conversion: This metric is the focus of the test, specifically the conversion rate. 
# The objective of the test was to increase the rate at which users perform a desired action.
# test: Indicates whether the user was assigned to the test group (1) or the control group (0). 
# Users in the test group experienced the new version of the site, 
# while those in the control group experienced the old version.

# A/B Test:
# This table represents the typical format for storing A/B test results. 
# Once results are compiled in a table like this, the standard procedure 
# involves conducting a t-test to determine if the average conversion rate 
# significantly differs between users exposed to the site change and those who were not.

# In practice, it would simply be something like this:

from scipy import stats
#check conversion rate for both groups
print(data.groupby('test')['conversion'].mean())

# output
# test              Interpretation
# 0    0.043707   ← Control group (no site change): ~4.37% conversion rate
# 1    0.055598   ← Test group (new site version): ~5.56% conversion rate

#perform a statistical test between the two groups
# Perform Welch’s t-test (recommended when variances are unequal)

print("----- Test Result Summary -----")

test_result = stats.ttest_ind(
    data.loc[data['test'] == 1]['conversion'], 
    data.loc[data['test'] == 0]['conversion'], 
    equal_var=False
    )
#t statistics
print("t-statistic n/", test_result.statistic)

#p value
print("p-value:", test_result.pvalue)

#print test results
if (test_result.pvalue > 0.05):
    print("Non-significant results")
elif (test_result.statistic > 0):
    print("Statistically better results")
else:
    print("Statistically worse results")

# T-Test Results Summary
# T-statistic: 7.71 (large non-zero value)=> big difference between the groups, 
# relative to the variation (or noise) in the data.
# P-value: 1.32e-14 (much smaller than 0.05) 
# =>The difference in conversion rates between the test and control groups is statistically significant.
# A test is winning if the test group is statistically significantly better. 
# With regards to better, you need to make sure that the t-statistic is positive

# Conclusion:
# We have very strong evidence to reject the null hypothesis. 
# The new version of the site (test group) significantly 
# improved conversion rates compared to the old version (control group).

# So in this case, the test is winning. Conversion rate is higher (from 4.3% to 5.5%) and the p-value 
# is super low, suggesting to us that the difference is extremely unlikely to be by chance. 
# So we can be pretty confident that the new version is better and we should roll it out for all users.

#  A/B Testing Complexity
# While analyzing A/B test results may seem straightforward once data is organized into a clean table, 
# the complexity lies in ensuring that certain assumptions are met throughout the testing process. 
# These assumptions are crucial for conducting a reliable t-test: 
# Sample Size, Randomization, Independence & Generalization of Test Results


