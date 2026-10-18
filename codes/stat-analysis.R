###########################################
# STATISTICAL ANALYSISANALYSIS
###########################################

library(car)
library(corrplot)
library(RColorBrewer)
library(rstatix)
library(bestglm)
library(xtable)
library(effectsize)
library(lm.beta)
library(sensemakr)


###########################################
# 1.WITHOUT MATCHING

###########################################
# 1.1 WITH TRANSFORMATION 

df_log <- df
df_log$velocity_mean_end <- log(df_log$velocity_mean_end)
df_cube <- df
df_cube$velocity_mean_end <- (df_cube$velocity_mean_end)^(1/3)

normality_plot(df_log$velocity_mean_end, df_cube$velocity_mean_end, "LOG", 
               "CUBE", "cube transformation")

###########################################
# 1.2.1 ANCOVA (We use the cube)


model_aov <- aov(velocity_mean_end ~ factor(MS.NonMS) + velocity_mean_start + size + n_contributors + n_languages + 
                   factor(creation_year) + n_commits + n_issues + factor(main_language), data = df_cube)
summary(model_aov)
print(xtable(summary(model_aov), type="latex"))


# 1. Linearity assumption (Residuals vs Fitted values)
# The blue line should go approximately horizontal and next to 0. If there is
# Some pronounced pattern then means  there is no perfect linearity
autoplot(model_aov)
# After fitting the ancova model, there's no clear pattern within the residuals appart from some outliers, which confirms the
# linear relationship among the dependent and the independent variables.
corrplot(cor(df_cube[header_names]))

# 2. Homogeneity of Variance (Scale-location)
leveneTest(velocity_mean_end ~ as.factor(MS.NonMS), data = df_cube)
# p-value=0.8354 (We don't have enough evidence to reject the null hypothesis, therefore 
# the difference among the variances of the two groups is not statistically significant.

# 3. Normality of residuals (Normal Q-Q plot)
# The residuals should follow the diagonal line.
shapiro.test(model$residuals) 

# 4. Homogeneity of regression slopes
anova.test <- anova_test(velocity_mean_end ~ factor(MS.NonMS) + velocity_mean_start +
                           size + n_languages + factor(creation_year) + n_commits + n_issues +
                           n_contributors, data = df_cube)
anova.test


###########################################
# 1.2.2 Linear Regression (We use the cube)
model_lm <- lm(velocity_mean_end ~ factor(MS.NonMS) + velocity_mean_start + size + n_contributors + n_languages + 
                 factor(creation_year) + n_commits + n_issues + factor(main_language), data = df_cube)
summary(model_lm)
vif_values <- vif(model_lm)
vif_values # No multicollinearity so far.
print(xtable(summary(model_lm), type="latex"))

model_lm_0 <- lm(velocity_mean_end ~ velocity_mean_start + size*n_contributors + n_languages + 
                   factor(creation_year) + n_commits + n_issues + factor(main_language), data = df_cube)

# We test the impact of the 
anova(model_lm_0,model_lm) # 0.7451 We cannot reject the null hypothesis, therefore the implication of the variance in the
# addition of the independent variable is not statistically signigicant to say that it improvers the model.

autoplot(model_lm)


######################################################################################
######################################################################################
######################################################################################


###########################################
# 2.WITH MATCHING (exact matching)

###########################################
# 2.2 WITH TRANSFORMATION 

data.exactMatching_log <- data.exactMatching
data.exactMatching_log$velocity_mean_end <- log(data.exactMatching_log$velocity_mean_end)
data.exactMatching_cube <- data.exactMatching
data.exactMatching_cube$velocity_mean_end <- (data.exactMatching_cube$velocity_mean_end)^(1/3)

normality_plot(data.exactMatching_log$velocity_mean_end, data.exactMatching_cube$velocity_mean_end, "LOG", 
               "CUBE", "cube transformation")

shapiro.test(data.exactMatching_log$velocity_mean_end)
shapiro.test(data.exactMatching_cube$velocity_mean_end) # Almost normally distributed

###########################################
# 2.2.1 ANCOVA (We use the cube)


model_aov <- aov(velocity_mean_end ~ factor(MS.NonMS) + velocity_mean_start + size + n_contributors + n_languages + 
                   factor(creation_year) + n_commits + n_issues, data = data.exactMatching_cube, weights = data.exactMatching_cube$weights)
summary(model_aov)
print(xtable(summary(model_aov), type="latex"))
# Effect size of the model.
eta_squared(model_aov)
partial_eta_squared(model_aov)
omega_squared(model_aov)
epsilon_squared(model_aov)



# 1. Linearity assumption (Residuals vs Fitted values)
# The blue line should go approximately horizontal and next to 0. If there is
# Some pronounced pattern then means  there is no perfect linearity
autoplot(model_aov)
# After fitting the ancova model, there's no clear pattern within the residuals appart from some outliers, which confirms the
# linear relationship among the dependent and the independent variables.
corrplot(cor(numeric_df[header_names]))

# 2. Homogeneity of Variance (Scale-location)
leveneTest(velocity_mean_end ~ factor(MS.NonMS), data = data.exactMatching_cube)
# p-value=0.4523 (We don't have enough evidence to reject the null hypothesis, therefore 
# the difference among the variances of the two groups is not statistically significant.

# 3. Normality of residuals (Normal Q-Q plot)
# The residuals should follow the diagonal line.
shapiro.test(model_aov$residuals) 
qqnorm(model_aov$residuals)
qqline(model_aov$residuals)

# 4. Homogeneity of regression slopes
anova.test <- anova_test(velocity_mean_end ~ factor(MS.NonMS) + velocity_mean_start +
                           size + n_languages + factor(creation_year) + n_commits + n_issues +
                           n_contributors, data = data.exactMatching_cube, weights=data.exactMatching_cube$weights)
anova.test


###########################################
# 2.2.2 Linear Regression (We use the cube)
model_lm <- lm(velocity_mean_end ~ factor(MS.NonMS) + velocity_mean_start + size + n_contributors + n_languages + 
                 factor(creation_year) + n_commits + n_issues, 
               data = data.exactMatching_cube, weights = data.exactMatching_cube$weights)
summary(model_lm)
print(xtable(summary(model_lm), type="latex"))
# Effect size
f2_values <- f2(model_lm) # Cohen's f2
print(f2_values)

summary(model_lm)$r.squared      # R-squared (overall effect size)
summary(model_lm)$adj.r.squared  # Adjusted R-squared (more reliable for multiple predictors)
partial_r2(model_lm)
partial_f2(model_lm)
partial_f(model_lm)


# Standardized beta coefficients
model_lm_beta <- lm.beta(model_lm)
summary(model_lm_beta)

model_lm_0 <- lm(velocity_mean_end ~ velocity_mean_start + size*n_contributors + n_languages + 
                   factor(creation_year) + n_commits + n_issues + factor(main_language), 
                 data = data.exactMatching_cube, weights = data.exactMatching_cube$weights)

# We test the impact of the 
anova(model_lm_0,model_lm) # 0.8763 We cannot reject the null hypothesis, therefore the implication of the variance in the
# addition of the independent variable is not statistically signigicant to say that it improvers the model.

autoplot(model_lm)
