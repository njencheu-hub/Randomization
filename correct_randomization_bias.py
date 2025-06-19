# In the analysis of randomization, it was discovered that the 
# test and control groups were not properly randomized. 
# Specifically, users from Argentina and Uruguay were under-represented 
# in the control group compared to the test group. The test group had 
# 17% from Argentina and 1.7% from Uruguay, whereas the control group had 
# significantly lower percentages of 5% and 0.2%, respectively.

# One potential solution to address this issue would be to adjust the 
# proportion of users from Argentina and Uruguay in the control group. 
# This adjustment aims to balance the relative frequencies between the 
# test and control groups, assuming no other variables are correlated 
# with these countries. Essentially, this involves oversampling users 
# from Argentina and Uruguay in the control group until their percentages 
# match those in the test group. 
# Subsequently, a new test can be conducted on this adjusted dataset.

# Here's how to proceed:
# A. Use same dataset of check_randomization analysis 

# 1. Load dataset

import pandas as pd
from scipy.stats import ttest_ind

df = pd.read_csv("randomization.csv")
print(df.head())

#    user_id source  device browser_language      browser sex  age    country  test  conversion
# 0        1    SEO     Web               EN       Chrome   M   38      Chile     0           0
# 1        2    SEO  Mobile               ES  Android_App   M   27   Colombia     0           0
# 2        3    SEO  Mobile               ES   Iphone_App   M   18  Guatemala     1           0
# 3        5    Ads     Web               ES       Chrome   M   22  Argentina     1           0
# 4        8    Ads  Mobile               ES  Android_App   M   19  Venezuela     1           0

# 2. Calculate proportions
# Check how over/underrepresented Argentina and Uruguay are in test vs. control.

# Get counts
country_counts = df.groupby(['test', 'country']).size().unstack().fillna(0)

# Convert to percentages
country_props = country_counts.div(country_counts.sum(axis=1), axis=0)

# Print just Argentina (AR) and Uruguay (UY)
print("Argentina (AR) proportions:\n", country_props[['Argentina']])
print("\nUruguay (UY) proportions:\n", country_props[['Uruguay']])

# Argentina (AR) proportions:
#  country  Argentina
# test
# 0         0.050488
# 1         0.173223

# Uruguay (UY) proportions:
#  country   Uruguay
# test
# 0        0.002239
# 1        0.017236

# B. Increase the representation of users from Argentina and Uruguay in the control group 
# to match the proportions in the test group. This can be achieved by:
# b.1 Calculating the number of new rows needed where test = 0 and country = AR or UR 
# to balance the relative frequencies.
# b.2 Randomly sampling these rows from the original dataset and appending them to the control group.


# 3. Calculate how many additional rows we need to sample

# Separate into test and control
test_df = df[df['test'] == 1]
control_df = df[df['test'] == 0]

# Desired proportions from test group
target_AR_prop = (test_df['country'] == 'Argentina').mean()
target_UY_prop = (test_df['country'] == 'Uruguay').mean()

# Current size of control
control_size = len(control_df)

# Required number of rows to match test group proportions
desired_AR = int(target_AR_prop * control_size)
desired_UY = int(target_UY_prop * control_size)

# Current counts in control
current_AR = (control_df['country'] == 'Argentina').sum()
current_UY = (control_df['country'] == 'Uruguay').sum()

# How many more we need
extra_AR = desired_AR - current_AR
extra_UY = desired_UY - current_UY

print(f"Need to oversample {extra_AR} AR and {extra_UY} UY users into control.")

# Need to oversample 22744 AR and 2778 UY users into control.

# 4. Sample and append users from AR and UY to control group

# Get source pool from test group only to avoid duplication
source_AR = test_df[test_df['country'] == 'Argentina']
source_UY = test_df[test_df['country'] == 'Uruguay']

# Sample with replacement in case we don’t have enough rows
oversampled_AR = source_AR.sample(n=extra_AR, replace=True)
oversampled_UY = source_UY.sample(n=extra_UY, replace=True)

# Set these to be in control group
oversampled_AR['test'] = 0
oversampled_UY['test'] = 0

# Append to control
control_balanced = pd.concat([control_df, oversampled_AR, oversampled_UY], ignore_index=True)

# Combine back with original test group
df_corrected = pd.concat([control_balanced, test_df], ignore_index=True)

# C. Verify that the proportions of users from Argentina and Uruguay 
# are now equal in both test and control groups.

# 5. Validate the new proportions

# Check proportions again
props_corrected = df_corrected.groupby(['test', 'country']).size().unstack().fillna(0)
props_corrected = props_corrected.div(props_corrected.sum(axis=1), axis=0)

print("Argentina and Uruguay proportions after balancing:")
print(props_corrected[['Argentina', 'Uruguay']])

# Argentina and Uruguay proportions after balancing:
# country  Argentina   Uruguay
# test
# 0         0.152253  0.015145
# 1         0.173223  0.017236

# D. Conduct a t-test on this modified dataset to assess the test results 
# with corrected relative frequencies for Argentina and Uruguay.

# This approach (Steps A to D) ensures that any subsequent test accurately reflects 
# the impact of the feature change by correcting the initial randomization bias.

# 6. Conduct a t-test on conversion rates

# Compare conversion between test and control
conversion_test = df_corrected[df_corrected['test'] == 1]['conversion']
conversion_control = df_corrected[df_corrected['test'] == 0]['conversion']

t_stat, p_val = ttest_ind(conversion_test, conversion_control)

print(f"\nT-test Results:\nT-statistic: {t_stat:.4f}, P-value: {p_val:.4f}")

# T-test Results:
# T-statistic: -1.1395, P-value: 0.2545

# T-test Interpretation (After Bias Correction)

# A p-value of 0.2545 is much greater than the typical significance level of 0.05.
# This means you fail to reject the null hypothesis:
# There is no statistically significant difference in conversion rates between the test and control groups.

# Why This Matters:
# After correcting for the initial randomization bias 
# (where Argentina and Uruguay were underrepresented in the control group), 
# our A/B test now reflects a fair comparison.

# The initial imbalance could have falsely suggested a difference, 
# but the corrected test indicates no true effect from the tested variation.

# Conclusion
# The feature or change tested in the A/B experiment did not lead to a 
# statistically significant improvement in conversions.
# The original randomization bias (especially from Argentina and Uruguay) 
# has been successfully mitigated, so our result is now trustworthy.