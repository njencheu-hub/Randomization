import statsmodels.stats.api as sms

#Firstly, we need to define the two conversion rates via proportion_effectsize. 
#The first element here (0.1) is simply the conversion rate of the site prior to 
# running the test. Aka control conversion rate
#The second one (0.11) is the minimum conversion rate of the test that would 
# make it worth it to make the change

p1_and_p2 = sms.proportion_effectsize(0.1, 0.11)

# This calculates the effect size for a comparison between two proportions:
# 0.10 = baseline conversion rate (control group)
# 0.11 = expected improved conversion rate (test group)

# print(proportion_effectsize(0.1, 0.11))  # Output: ~0.031
# So here, p1_and_p2 ≈ 0.031 → a small effect size

#Now we can run the function that after passing the two conversion rates above 
# + power and significance, returns sample size

sample_size = sms.NormalIndPower().solve_power(p1_and_p2, power=0.8, alpha=0.05)

# This is performing power analysis — it's calculating the sample size required 
# per group to detect that small effect size (~0.031) with:
# Power = 0.8 → 80% chance of detecting a true effect (standard benchmark)
# Alpha = 0.05 → 5% significance level (false positive risk)

# solve_power(...) says:
# “How many people do I need in each group to confidently detect a difference 
# between 10% and 11% conversion?”
# Because the effect size is small, this will return a large sample size — maybe 25,000+ per group.

print("The required sample size per group is ~", round(sample_size))

# This prints the final result — the rounded sample size needed per group (control and test) 
# to detect a 1% uplift with 80% power and 5% significance level.

# Summary
# We're calculating how many users you need in an A/B test to detect a change 
# from 10% → 11% conversion rate with good confidence.

# Result:
# The required sample size per group is ~ 14744
# The result is straightforward: it indicates that approximately 15,000 users are needed in 
# both the test and control groups to reliably detect a minimum 1% increase in our metric

# Additionally, we can input a range of values for p2 
# (the minimum conversion rate improvement required for making the change) as a vector. 
# This allows you to visualize how the required sample size varies with different thresholds for p2. 
# This flexibility enables you to present various scenarios to the product manager, assisting them 
# in selecting the most suitable minimum effect level for the test. This approach helps align the 
# A/B testing objectives closely with business priorities and resource allocation decisions.

import numpy as np
import matplotlib.pyplot as plt

#Possible p2 values. We choose from 10.5% to 15% with 0.5% increments

possible_p2 = np.arange(.105, .155, .005)

print(possible_p2)
# [0.105 0.11  0.115 0.12  0.125 0.13  0.135 0.14  0.145 0.15 ]

#now let's estimate sample size for all those values and plot them
sample_size = []
for i in possible_p2:
   p1_and_p2 = sms.proportion_effectsize(0.1, i)
   sample_size.append(sms.NormalIndPower().solve_power(p1_and_p2, power=0.8, alpha=0.05))
plt.plot(sample_size, possible_p2)
plt.title("Sample size vs Minimum Effect size")
plt.xlabel("Sample Size")
plt.ylabel("Minimum Test Conversion rate")
plt.savefig("sample_size_vs_conversion_rate.png", dpi=300, bbox_inches='tight')
# plt.show()
