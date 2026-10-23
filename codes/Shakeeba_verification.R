# M2 sample verification — Shakeeba Hamdam
# 23 October 2026
# Run with the working directory set to the repository root.
# Checks one bounded-sample test, not the full study.

sample_data <- read.csv("Data/final_data_file_sample.csv")

# Check sample counts, duplicate IDs and missing velocity values.
print(nrow(sample_data))
print(table(sample_data$MS.NonMS))
print(sum(duplicated(sample_data$full_name)))

print(colSums(is.na(sample_data[c(
  "velocity_mean_start",
  "velocity_mean_end"
)])))

# Follow the preparation used in crude-analysis.R:
# add 0.01 to end velocity, then take the absolute value.
ms_velocity <- abs(
  sample_data$velocity_mean_end[sample_data$MS.NonMS == "MS"] + 0.01
)

nonms_velocity <- abs(
  sample_data$velocity_mean_end[sample_data$MS.NonMS == "~MS"] + 0.01
)

# Recalculate the one-sided Wilcoxon rank-sum test.
# Reference result already inspected: W = 10, p approximately 0.1201.
verification_result <- wilcox.test(
  ms_velocity,
  nonms_velocity,
  alternative = "less",
  conf.int = TRUE
)

print(verification_result)

# Record the R version and session details.
print(sessionInfo())

