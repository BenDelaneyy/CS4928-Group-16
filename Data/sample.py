"""
Creates a stratified sample of final_data_file.csv containing only entries that are viable for the R analysis.
The original file is left untouched; the sample is written to final_data_file_sample.csv.
"""
import os
import pandas as pd

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(DATA_DIR, "final_data_file.csv")
OUTPUT_FILE = os.path.join(DATA_DIR, "final_data_file_sample.csv")

N_PER_GROUP = 6  # Number of cases (MS) and of controls (~MS)
SEED = 42
GROUP_COL = "MS/NonMS"


def viable_entries(df):
    """
    Keeps only the entries the R scripts can use.
    """
    n_start = len(df)

    # No missing values in any column used by the models
    df = df.dropna()

    # End velocity is log / Box-Cox transformed (data-transformation.R, stat-analysis.R), so it must be positive
    df = df[df["velocity_mean_end"] > 0]

    # Exact matching on main_language (confounder-matching.R) needs both MS and ~MS projects for each language
    groups_per_language = df.groupby("main_language")[GROUP_COL].nunique()
    matchable_languages = groups_per_language[groups_per_language == 2].index
    df = df[df["main_language"].isin(matchable_languages)]

    print(f"> Viable entries: {len(df)}/{n_start}")
    return df


def stratified_sample(df):
    """
    Samples N_PER_GROUP cases (MS) and pairs each one with a control (~MS) with the same main_language,
    so no entry is discarded by the exact matching.
    """
    cases = df[df[GROUP_COL] == "MS"]
    controls = df[df[GROUP_COL] == "~MS"]

    sampled_cases = cases.sample(n=N_PER_GROUP, random_state=SEED)

    # One matching control per sampled case
    sampled_controls = []
    for language in sampled_cases["main_language"]:
        candidates = controls[(controls["main_language"] == language) & ~controls.index.isin(sampled_controls)]
        sampled_controls.append(candidates.sample(n=1, random_state=SEED).index[0])

    return pd.concat([sampled_cases, controls.loc[sampled_controls]])


def main():
    df = pd.read_csv(INPUT_FILE)
    df = viable_entries(df)
    sample = stratified_sample(df).sort_index()  # Keep the original row order

    sample.to_csv(OUTPUT_FILE, index=False)
    print(f"> Sample of {len(sample)} entries written to {OUTPUT_FILE}")
    print(sample[GROUP_COL].value_counts().to_string())


if __name__ == "__main__":
    main()
