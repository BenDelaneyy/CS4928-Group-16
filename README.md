# FOR PROJECT
First create a python `venv` and install `requirements.txt`.
Then create a `github-token.txt` and paste your github token with public repo access in.

# Replication package for EMSE article: *"Does Microservice Adoption Impact the Velocity? A Cohort Study"*

This replication package contains all the Python code to conduct the data collection, preprocessing and analysis of this study.

## Contents

This repository contains the following

- [INSTALL](INSTALL.md): Detailed installation instructions for each of the used tools as well as the required Python dependencies.

- [analysis_figures](analysis_figures): Figures generated during the analysis
    - [ancova-assumption-visuals.pdf](analysis_figures/ancova-assumption-visuals.pdf): Visualization assesing ANCOVA assumptions.
    - [crude_analysis_normality_qq.pdf](analysis_figures/crude_analysis_normality_qq.pdf): QQ normality boxplots drom the crude analysis.
    - [endvelocity-boxplots.pdf](analysis_figures/endvelocity-boxplots.pdf): Boxplots displaying end velocity mean values distribution. 
    - [exact-matching-output-boxplots.pdf](analysis_figures/exact-matching-output-boxplots.pdf): Boxplots displaying balance after exact matching.
    - [exact-matching-output-qq.pdf](analysis_figures/exact-matching-output-qq.pdf): QQ plots displaying balance after exact matching.
    - [variables-boxplots.pdf](analysis_figures/variables-boxplots.pdf): Boxplots displaying study variables.
    - [variables-grouped-language.pdf](analysis_figures/variables-grouped-language.pdf): Variables displayed grouped by programming languages.
    - [variables-grouped-year.pdf](analysis_figures/variables-grouped-year.pdf): Variables displayed grouped by creation year.

- [Article_figures](Article_figures): Figures added in the PDF version of the manuscript.

    - [cdf-confounders](Article_figures/cdf-confounders.pdf): Cumulative Density Function plots for model confounders.
    - [confounder-boxplots](Article_figures/confounder-boxplots.pdf): Boxplots for model confounders.
    - [creation-year-confounder](Article_figures/creation-year-confounder.pdf): Balance histogram from the confounder "Creation Year"
    - [dag-diagram](Article_figures/dag-diagram.pdf): Directional Acyclic graph diagram of the confounding relationship.
    - [data-collection-vertical](Article_figures/data-collection-vertical.pdf): Data filtering stage diagram.
    - [example-velocity](Article_figures/example-velocity.pdf): Graphical example of the velocity calculation.
    - [kernel-density](Article_figures/kernel-density.pdf): Kernel density plots for model confounders.
    - [stat-analysis-short](Article_figures/stat-analysis-short.pdf): Statistical analysis process diagram.
    - [study-design-observed-project](Article_figures/study-design-observed-project.pdf): Augmented display at a project level of the follow-up period.
    - [study-design](Article_figures/study-design.pdf): Graphical representation of the overall study design
    - [velocity-boxplots](Article_figures/velocity-boxplots.pdf): Boxplots of the start and end velocity.


- [codes](codes):
    - [```analyze_repo_multi_thread_per_commit.py```](codes/analyze_repo_multi_thread_per_commit.py): Performs the monitorization of MS usage.
    - [```clone_projects.py```](codes/clone_projects.py): Performs the repostory clonning.
    - [```commons.py```](codes/commons.py): Stores the global paths and variables. 
    - [```find_ms_usage.py```](codes/find_ms_usage.py): Checks whether the MS usage doesn't respect the criteria during the follow-up period.
    - [```format_data_for_analysis.py```](codes/format_data_for_analysis.py): Making the initial raw data accessible in R.
    - [```get_confounders.py```](codes/get_confounders.py): Mines the version control history dat from the studied projects.
    - [```get_velocity.py```](codes/get_velocity.py): Calculates velocity from the studied software projects' maintenance activity.
    - [```main.py```](codes/main.py): As will be explained, coordinates the execution of the creation of the raw data doe this study.
    - [```modules.py```](codes/modules.py): Common used functions during the project execution.
    - [```trendAnalysis.py```](codes/trendAnalysis.py): Tests the trend of commit and issue maintenance activity of the studied projects.
    - [```tsanalysis.py```](codes/tsanalysis.py): COntains functions of Time Series Analysis models to assist the testing in the ```trendAnalysis.py``` script.
    - [```basic_statistics_table.py```](codes/basic_statistics_table.py): Creates the basic statistics table of the studied projects, included in this online appendix.
    - [```confounder-matching.R```](codes/confounder-matching.R): Performs different confounder matching techniques.
    - [```crude-analysis.R```](codes/crude-analysis.R): Functions to perform the crude analysis.
    - [```data-transformation.R```](codes/data-transformation.R): Functions to perform the data transformation to reach normality.
    - [```descriptive-analysis.R```](codes/descriptive-analysis.R): Functions to perform the descriptive statistics.
    - [```power-analysis.R```](codes/power_analysis.R): Functions to perform the statistical power analysis.
    - [```stat-analysis-long.R```](codes/stat-analysis-long.R): Statistical Adjustmed analysis with graphical representations.
    - [```stat-analysis.R```](codes/stat-analysis.R): Straight numerical calculations of the Statistical Adjusted analysis.

- [data](data): Contains all the required data to start, follow and finish the analysis of this study.

    - [cases](data/cases/): All the data related to the subjects within the cases group.

    - [controls](data/controls/): All the data related to the subjects within the controls group.

    - [analyzedDataset.zip](data/analyzedDataset.zip): Initial MS datasets
    - [basic_statistics_table.pdf](data/basic_statistics_table.pdf): PDF file with the basic statistics of the projects considered in the statistical analysis of this study.
    - [basic_statistics_table_extended.csv](data/basic_statistics_table_extended.csv): Same version of the PDF table in CSV format.
    - [final_data_file.csv](data/final_data_file.csv): Final data file with the raw data used in the statistical analysis section.
    - [ms_monitorization_json.json](data/ms_monitorization_json.json): JSON file with the results from the MS usage monitorization.
    - [projects.zip](data/projects.zip): Overall folder with the MS and Non-MS projects zipped.
    - [velocity_results.csv](data/): Results from the velocity calculation stage..

    Subsequently during the code execution new data directories and files will be generated.

    The source of the data is rooted on the global paths defined in [```commons.py```](codes/commons.py).

    - [requirements.txt](requirements.txt): Python dependencies to be installed.
    - [github-token.txt](github-token.txt): Insert the GitHub token as one single line in this TXT file.


## Running the code

NOTE 1: Please, find the `DATA_PATH` global variable in the [`commons.py`](codes/commons.py) script and define the path where the program should create all the needed results.

NOTE 2: The different stages of the study execution are splitted in the [```main.py```](codes/main.py) script, from the boolean definitions in
[```commons.py```](codes/commons.py) practitioners can decide which stages want to be manipulated or re-executed again without affecting the other stages.
For a complete execution, set all the boolean global variables to ```True```

The [```main.py```](codes/main.py)  file is not divided into the exclusion criteria stages but by stages of the code which required diverse logics. In the following points we briefly explain the diverse stages in the execution, and the reader can observe the involved scripts within the code.

### Python codes

#### Stage 1: ```COMPLETE ANALYSIS```

Performs the initial prefiltering of projects existing in the Microservices dataset replication package. During the process, collects commits and issues,
whose trend is analyzed in the same stage as explained in the published article.

#### Stage 2: ```MS ANALYSIS```

For the remaining Microservices projects a separated analysis of their architecture is performed. Shortly,
all the commits from the default branch are analyzed based on the criteria used in the Microservices dataset to define if the selected projects
maintain the required minimum number of microservices during the two years of observational study.

#### Stage 3: ```CLONE PROJECTS```

From the surviving projects, the cloning of the projects is performed in order to collect further variables from their repositories.

#### Stage 4: ```REPO ANALYSIS```

Based on the metrics collected from the cloned repositories further exclusions are performed.

#### Stage 5: ```FINAL FILE CREATION```

After all the exclusion criteria is performed the final csv file is generated to be used in R. Each of the scripts is called in the name of the stage title shown in these instructions. Furthermore, the used libraries are located at the top of each script so that the reader can activate them directly before executing new lines of code. If the library package is not installed previously a warning might appear, often the same IDE alerts of this before running the line of code for the library activation.

### R codes

#### Stage 6: ```CRUDE ANALYSIS```

Performs the crude analysis in its two formats. Note that for the crude analysis with transformed data the results from the data transformation must be computed beforehand.

#### Stage 7: ```MATCHING CONFOUNDERS```

The matching of confounders is done following the Exact Matching style. At the end of the script (as well as in the other scripts) new datafiles (dataframes are generated)

#### Stage 8: ```VARIABLE TRANSFORMATION```

Different techniques are used for the variable trandformation. These techniques are used based on the skewed nature of the dependent variable at the beginning. Similarly, only the results from the cube root transformation are taken into account.
Therefore, the user is free to choose if running all the script or just the section regarding te cube root transformation.

#### Stage 9: ```STATISTICAL ANALYSIS```

### R codes:

#### Stage 10: ```STATISTICAL ANALYSIS```

NOTE: The ANCOVA and Linear Regression analysis are computed.

For further questions, please do not hesitate to contact the authors once the contact details are facilitated in the paper publication.