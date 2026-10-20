# Installation guide:

This files contains instructions on how to install and run each tool used in the data gathering process.

## SCC

Download ```SCC``` from its official [repository](https://github.com/boyter/scc/tree/master). 

Data presented in this replication package/paper were generated with the [v3.5.0](https://github.com/boyter/scc/releases/tag/v3.5.0) version of the tool.

The tool can be executed as
```
scc [flags] [files or directories]
```

where:
- ```flags```: offered modifications of the expected output. Further information can be found in the ```SCC``` [documentation](https://github.com/boyter/scc/blob/master/README.md).
- ```[files or directories]```: whether entire repository is to be analysed, a subdirectory or a single file.

The results from the tool are done at a file level, and our implementation creates and removes the created outcome, fetching only the required content.


## Creating Python virtual environment and installing dependencies.

Instructions on the required dependencies to run the scripts. Running the code requires Python3.9. See more details about the installation instructions [here](https://www.python.org/downloads/). The dependencies needed to run the code are all listed in the file ```requirements.txt```. They can be installed using pip as:
```
python -m pip install -r requirements.txt
```
Such requirements include packages such as ```pandas```, ```statsmodels```, or ```PyDriller``` among others.

You might also want to consider using [virtual env](https://packaging.python.org/guides/installing-using-pip-and-virtualenv/).

## Setting up R Software and R Studio.
Running the Crude Analysis, Matching and Statistical Adjustment requires running diverse R codes. The execution of this code works
line-wise. Therefore, the user will have to run the code in a text editor, e.g. R Studio where the same IDE asks you to install (```install.packages(*)``` in the R console) the libraries based in the 
commands of type ```library(*)``` it reads. Hence, the user is safe to start running the code as they wish.

Install R Software into your machine through the download process [here](https://www.r-project.org). Similarly, for an easy use of the provided codes, we recommend downloading and running the scripts in [R Studio](https://posit.co/download/rstudio-desktop/).


Follow the instructions in [README](README.md) to replicate each step of the data collection.