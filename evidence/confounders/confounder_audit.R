###########################################
# CONFOUNDER AUDIT on the 12-project bounded sample (P22 pack: "Audit at least two potential confounders").
# Added 2026-11-24 (the FINAL tag was moved to include it). Exploratory and descriptive: it does NOT change the frozen M2 test or result.
# Confounders are the covariates the original study adjusts for (columns of Data/final_data_file.csv,
# used in codes/stat-analysis.R): size, n_languages, creation_year, n_commits, n_issues, n_contributors.
# main_language is matched exactly by Data/sample.py (one ~MS project per MS project, same language).
# Base R only. Run from the repository root:
#   Rscript evidence/confounders/confounder_audit.R
###########################################

options(width = 200)
output_file <- "evidence/confounders/confounder_audit_output.txt"
sink(output_file, split = TRUE)

cat("Confounder audit -", format(Sys.time()), "-", R.version.string, "\n")
cat("Data: Data/final_data_file_sample.csv (12 projects, 6 MS / 6 ~MS)\n\n")

df <- read.csv("Data/final_data_file_sample.csv", check.names = FALSE)
grp <- df[["MS/NonMS"]]
ms <- grp == "MS"
nonms <- grp == "~MS"

# 1. Language matching (by construction)
cat("1. main_language per group (should be identical multisets):\n")
print(table(df$main_language, grp))
cat("\n")

# 2. Balance of each confounder between groups
confounders <- c("size", "n_languages", "creation_year", "n_commits", "n_issues", "n_contributors")
smd <- function(x, y) (mean(x) - mean(y)) / sqrt((var(x) + var(y)) / 2)  # standardised mean difference

bal <- do.call(rbind, lapply(confounders, function(v) {
  x <- df[[v]][ms]; y <- df[[v]][nonms]
  p <- suppressWarnings(wilcox.test(x, y, alternative = "two.sided", exact = FALSE)$p.value)
  data.frame(confounder = v,
             median_MS = median(x), median_nonMS = median(y),
             SMD = round(smd(x, y), 3),
             imbalanced_SMD_gt_0.25 = abs(smd(x, y)) > 0.25,
             wilcox_p_two_sided = round(p, 4))
}))
cat("2. Balance between MS and ~MS (SMD = standardised mean difference; |SMD| > 0.25 is a common imbalance threshold;\n",
    "   Wilcoxon p uses the normal approximation because of ties; with n = 6 per group it has very little power):\n", sep = "")
print(bal, row.names = FALSE)
cat("\n")

# 3. Association of each confounder with the outcome (end velocity), all 12 projects
vel <- df$velocity_mean_end
assoc <- do.call(rbind, lapply(confounders, function(v) {
  ct <- suppressWarnings(cor.test(df[[v]], vel, method = "spearman", exact = FALSE))
  data.frame(confounder = v, spearman_rho_with_end_velocity = round(unname(ct$estimate), 3),
             p = round(ct$p.value, 4))
}))
cat("3. Spearman correlation of each confounder with velocity_mean_end (n = 12):\n")
print(assoc, row.names = FALSE)
cat("\n")

# 4. Flag: a confounder matters for the M2 comparison if it is imbalanced AND related to the outcome
flag <- merge(bal[, c("confounder", "SMD", "imbalanced_SMD_gt_0.25")], assoc, by = "confounder")
flag <- flag[order(flag$confounder), ]
flag$potential_confounding <- flag$imbalanced_SMD_gt_0.25 & abs(flag$spearman_rho_with_end_velocity) >= 0.3
cat("4. Potential confounding (|SMD| > 0.25 and |rho| >= 0.3):\n")
print(flag[, c("confounder", "SMD", "spearman_rho_with_end_velocity", "potential_confounding")], row.names = FALSE)

sink()
