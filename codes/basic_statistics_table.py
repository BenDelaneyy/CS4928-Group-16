"""
basic statistics regarding the selected projects should be reported to help readers better understand the dataset.
This includes information on project size, the number of MS components, stars, and the number of issues and commits.
"""

import os
import subprocess
import sys
import requests
from commons import DATA_PATH, CASES_PATH, CONTROLS_PATH, SCC_PATH, TIOBE_LIST
import pandas as pd
from utils import read_token
from dateutil.relativedelta import relativedelta
from datetime import datetime
import json
import random
from git import Repo


def read_csv_to_dict(save_path):
    """
    Loads an existing CSV file into a dictionary matching the changes_data format.
    If the file does not exist, returns an empty dictionary.

    :param save_path: Path to the CSV file.
    :return: Dictionary with existing data or an empty initialized dictionary.
    """
    df = pd.read_csv(save_path)

    # Convert the DataFrame into a dictionary with lists
    existing_data = df.to_dict(orient="list")
    #print(f"Loaded existing data from {save_path}")
    return existing_data


def get_stars(project_name, project_type):

    stargazers_url = f"https://api.github.com/repos/{project_name}/stargazers"
    github_token = read_token()
    headers = {'Accept': 'application/vnd.github.v3.star+json', 'Authorization': f'token {github_token}'}
    page_num = 1

    project_filename = project_name.replace("/", "#", 1)
    # Get first commit crawled from GitHub
    if project_type == "cases":
        df = pd.read_csv(os.path.join(CASES_PATH, "commits", f"{project_filename}.csv"))
    else:
        df = pd.read_csv(os.path.join(CONTROLS_PATH, "commits", f"{project_filename}.csv"))
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%dT%H:%M:%SZ')
    creation_datetime = df['date'].min()

    #creation_datetime = datetime.strptime(, "%Y-%m-%dT%H:%M:%SZ")
    followup_start_date = creation_datetime + relativedelta(months=12)
    followup_end_date = creation_datetime + relativedelta(months=24)
    stargazers_beginning = 0
    stargazers_end = 0
    while True:

        params = {'per_page': 100, 'state': 'all', 'page': page_num}

        repo_response = requests.get(stargazers_url, headers=headers, params=params)
        if repo_response.status_code != 200:
            return 0, 0, followup_start_date, followup_end_date
        response_json = repo_response.json()
        if len(response_json) == 0:
            return stargazers_beginning, stargazers_end, followup_start_date, followup_end_date

        for stargazer in response_json:
            try:
                star_datetime = datetime.strptime(stargazer["starred_at"], "%Y-%m-%dT%H:%M:%SZ")
            except TypeError:
                return "*", followup_start_date
            if star_datetime <= followup_start_date:
                stargazers_beginning += 1
                stargazers_end += 1
            elif followup_start_date < star_datetime <= followup_end_date:
                stargazers_end += 1
            else:
                return stargazers_beginning, stargazers_end, followup_start_date, followup_end_date

        page_num += 1


def get_microservices(project_name, period, follow_up_start_datetime, follow_up_end_datetime):

    ms_analysis_path = os.path.join("/Users/mrobredo23/OULU/docker_cohort-24/data/ms_analysis_files", project_name)
    list_files = os.listdir(ms_analysis_path)


    ordered_analysis_dates = [datetime.strptime(analysis_file.removesuffix(".json"), "%Y-%m-%dT%H:%M:%SZ") for analysis_file in list_files]
    sorted_analysis_dates = sorted(ordered_analysis_dates)
    previous_datetime = None

    if period == "start":
        print("Project name: ", project_name, "follow_up_start_datetime: ", follow_up_start_datetime)
        for analysis_datetime in sorted_analysis_dates:
            if analysis_datetime > follow_up_start_datetime:
                break
            previous_datetime = analysis_datetime

        if previous_datetime is None:
            previous_datetime = sorted_analysis_dates[0]
        with open(os.path.join(ms_analysis_path, f"{previous_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")}.json"), mode="r", encoding="utf-8") as json_file:
            ms_analysis_dict = json.load(json_file)

        return ms_analysis_dict["num_services"]
    else:
        print("Project name: ", project_name, "follow_up_end_datetime: ", follow_up_end_datetime)
        for analysis_datetime in sorted_analysis_dates:
            if analysis_datetime > follow_up_end_datetime:
                break
            previous_datetime = analysis_datetime

        with open(os.path.join(ms_analysis_path, f"{previous_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")}.json"), mode="r",
                  encoding="utf-8") as json_file:
            ms_analysis_dict = json.load(json_file)

        return ms_analysis_dict["num_services"]


def write_csv_from_dict(dictionary, path):
    """
    Writes in an scalable format all dictionaries
    :param dictionary:
    :param path:
    """

    data_df = pd.DataFrame.from_dict(dictionary)
    data_df.to_csv(path, index=False)


def checkout_git_repo(project_path, git_hash):

    repo = Repo(project_path)
    try:
        repo.git.checkout(git_hash, force=True)
        #print(f"Checkout repo {os.path.basename(project_path)} at {git_hash}")
    except Exception as e:
        print(f"Failed to checkout {git_hash}: {e}")


def is_directory_empty(dir_path):
    """
    Check if a directory is empty, ignoring hidden files and folders.
    """

    return not any(
        entry for entry in os.scandir(dir_path)
        if not entry.name.startswith('.')  # Ignore hidden files/folders
    )


def clone_repo(repo_name):
    """
    Clone repository into the specified path

    :param repo_name: Short name of the repository
    :return: The path of the repository clonned
    """
    repo_name_clean = repo_name.replace("#", "/", 1)
    clone_url = f"https://github.com/{repo_name_clean}.git"
    repos_path = os.path.join(DATA_PATH, "repos")
    os.makedirs(repos_path, exist_ok=True)
    print(f"Cloning {repo_name} repository...")
    try:
        repo_path = os.path.join(repos_path, repo_name)
        if os.path.exists(repo_path) and is_directory_empty(repo_path) is False:
            print(f"The repository {repo_name} already exists in path {repo_path}, skipping.")
            return repo_path
        subprocess.run(["git", "config", "--global", "core.longpaths", "true"])
        subprocess.run(['git', 'clone', clone_url, repo_path], check=True)
        print(f"Repository {repo_name} successfully cloned!")
        return repo_path
    except subprocess.CalledProcessError as e:
        print(f"Error at clonning the repository: {e}")
        sys.exit(e.returncode)


def open_json_file(json_file):
    '''
    Open a json file and return the data
    '''
    with open(json_file, "r", encoding='utf-8') as f:
        data1 = json.load(f)
    return data1


def process_language_data(temp_csv_path):
    """
        Processes the CSV file to check languages in a given list, sum the Code column for matched languages,
        and find the language(s) with the highest Code value.

        :param csv_file: Path to the CSV file.
        :return: Tuple (matched_languages_count, total_code_sum, highest_code_languages)
        """

    # Load the CSV into a DataFrame
    df = pd.read_csv(temp_csv_path)

    # Convert provided language list to lowercase for case-insensitive comparison
    language_set = {lang.lower() for lang in TIOBE_LIST}

    # Filter the DataFrame for languages that exist in the given list (case insensitive)
    df["Language_lower"] = df["Language"].str.lower()
    matched_df = df[df["Language_lower"].isin(language_set)]

    # Count matched languages
    matched_languages_count = matched_df.shape[0]

    # Sum of Code column for matched languages
    total_code_sum = matched_df["Code"].sum()

    # Find the highest Code value among matched languages
    max_code_value = matched_df["Code"].max()

    # Get the language(s) with the highest Code value
    highest_code_languages = matched_df[matched_df["Code"] == max_code_value]["Language"].tolist()

    return matched_languages_count, total_code_sum, highest_code_languages[0]


def get_sloc_variables(repo_name, current_hash):
    """
    Gets the effective lines of code (ELOC) from the specified file path at the stage of the current commit

    :param file_path:
    :param repo_path:
    :param c_hash:
    :return: ELOC
    """

    if not os.path.exists(os.path.join(DATA_PATH, "repos")):
        os.makedirs(os.path.join(DATA_PATH, "repos"), exist_ok=True)
    if not os.path.exists(os.path.join(DATA_PATH, "repos", repo_name)):
        repo_path = clone_repo(repo_name)
    else:
        repo_path = os.path.join(DATA_PATH, "repos", repo_name)

    checkout_git_repo(project_path=repo_path, git_hash=current_hash)
    temp_csv_path = os.path.normpath(os.path.join(str(DATA_PATH), "temp.csv"))
    subprocess.run(["scc", repo_path, "-f", "csv", "-o", temp_csv_path], shell=False, check=True)
    matched_languages_count, total_code_sum, highest_code_language = process_language_data(temp_csv_path)
    os.remove(temp_csv_path)
    return matched_languages_count, total_code_sum, highest_code_language


# Helper function to sort CSV file by date column
def sort_csv_by_date(input_csv_path, date_column, output_csv_path):
    if os.path.exists(input_csv_path):
        df = pd.read_csv(input_csv_path)
        df[date_column] = pd.to_datetime(df[date_column], utc=True)  # Convert to datetime
        df.sort_values(by=date_column, inplace=True)  # Sort by date
        df.to_csv(output_csv_path, index=False)  # Save sorted CSV
    else:
        raise FileNotFoundError(f"❌ File not found: {input_csv_path}")


def get_end_vch_data(project_name, project_type, follow_up_end_datetime):
    """
    Counts total commits, contributors, and issues for a project up until a given datetime.
    Ensures that the commits and issues CSV files are sorted by date before processing.

    :param project_name: Name of the project.
    :param project_type: Type of project (used to locate files).
    :param follow_up_end_datetime: Datetime object to filter data.
    :return: Tuple (total_commits, total_contributors, total_issues, last_commit_hash)
    """

    follow_up_end_datetime = follow_up_end_datetime.to_pydatetime()

    # Define the paths to the CSV files
    assert isinstance(project_type, str)
    project_type_path = os.path.join(DATA_PATH, project_type)
    csv_file_path = os.path.join(project_type_path, "commits", f"{project_name}.csv")
    issues_csv_path = os.path.join(project_type_path, "issues", f"{project_name}.csv")

    # Initialize counters
    total_commits = 0
    total_issues = 0
    unique_contributors = set()  # Use a set to track unique emails
    last_commit_hash = None

    # Process sorted commits file
    df_commits = pd.read_csv(csv_file_path)
    df_commits["date"] = pd.to_datetime(df_commits["date"], format="%Y-%m-%dT%H:%M:%SZ", utc=True)
    df_commits.sort_values(by="date", inplace=True)

    # Process sorted commits
    for _, row in df_commits.iterrows():
        commit_date = row["date"].replace(tzinfo=None)
        author_email = str(row["author_email"]).lower()

        if commit_date <= follow_up_end_datetime and "bot" not in author_email:
            total_commits += 1
            unique_contributors.add(author_email)
            last_commit_hash = row["sha"]
    total_contributors = len(unique_contributors)

    # Process sorted issues file
    df_issues = pd.read_csv(issues_csv_path)
    df_issues["created_at"] = pd.to_datetime(df_issues["created_at"], utc=True)
    df_issues.sort_values(by="created_at", inplace=True)

    # Process sorted issues
    for _, row in df_issues.iterrows():
        issue_date = row["created_at"].replace(tzinfo=None)
        user_login = str(row["user_login"]).lower()

        if issue_date <= follow_up_end_datetime and "bot" not in user_login:
            total_issues += 1

    print(f"\n🔹 Project: {project_name}")
    print(f"📅 Commits up to {follow_up_end_datetime}: {total_commits}")
    print(f"👥 Unique contributors up to {follow_up_end_datetime}: {total_contributors}")
    print(f"🐞 Issues up to {follow_up_end_datetime}: {total_issues}")

    return total_commits, total_contributors, total_issues, last_commit_hash


def get_start_size(project_name, project_type, follow_up_start_datetime):

    if project_name in ["pagarme#tldr", "hashgraph#hedera-mirror-node"]:
        return None

    follow_up_start_datetime = follow_up_start_datetime.to_pydatetime()
    # Define the paths to the CSV files
    assert isinstance(project_type, str)
    project_type_path = os.path.join(DATA_PATH, project_type)
    csv_file_path = os.path.join(project_type_path, "commits", f"{project_name}.csv")
    df_commits = pd.read_csv(csv_file_path)
    df_commits["date"] = pd.to_datetime(df_commits["date"], format="%Y-%m-%dT%H:%M:%SZ", utc=True)
    df_commits.sort_values(by="date", inplace=True)
    last_commit_hash = None
    # Process sorted commits
    for _, row in df_commits.iterrows():
        commit_date = row["date"].replace(tzinfo=None)
        author_email = str(row["author_email"]).lower()

        if commit_date <= follow_up_start_datetime and "bot" not in author_email:
            last_commit_hash = row["sha"]

    # Getting the size value.
    if not os.path.exists(os.path.join(DATA_PATH, "repos")):
        os.makedirs(os.path.join(DATA_PATH, "repos"), exist_ok=True)
    if not os.path.exists(os.path.join(DATA_PATH, "repos", project_name)):
        repo_path = clone_repo(project_name)
    else:
        repo_path = os.path.join(DATA_PATH, "repos", project_name)

    checkout_git_repo(project_path=repo_path, git_hash=last_commit_hash)
    temp_csv_path = os.path.normpath(os.path.join(str(DATA_PATH), "temp.csv"))
    # /opt/homebrew/bin/scc
    subprocess.run(["scc", repo_path, "-f", "csv", "-o", temp_csv_path], shell=False, check=True)
    matched_languages_count, total_code_sum, highest_code_language = process_language_data(temp_csv_path)
    os.remove(temp_csv_path)

    return total_code_sum


def make_table():
    # Define the new dictionary structure with nested columns
    table_dict = {
        "Project": [],
        "Creation year": [],
        "Subject Type": [],
        "Size_FU_start": [],
        "Size_FU_end": [],
        "Microservices_FU_start": [],
        "Microservices_FU_end": [],
        "Main Language_FU_start": [],
        "Main Language_FU_end": [],
        "Stars_FU_start": [],
        "Stars_FU_end": [],
        "Issues_FU_start": [],
        "Issues_FU_end": [],
        "Commits_FU_start": [],
        "Commits_FU_end": [],
        "Contributors_FU_start": [],
        "Contributors_FU_end": [],
        "Languages_FU_start": [],
        "Languages_FU_end": []
    }

    output_path = os.path.join(DATA_PATH, "basic_statistics_table_extended.csv")
    final_projects_path = os.path.join(DATA_PATH, "final_data_file.csv")
    final_projects_dict = read_csv_to_dict(final_projects_path)

    # Load existing CSV if it exists and populate table_dict
    existing_projects = set()
    if os.path.exists(output_path):
        existing_df = pd.read_csv(output_path)
        existing_projects = set(existing_df["Project"].tolist())  # Get existing projects
        for column in existing_df.columns:
            if column in table_dict:
                table_dict[column] = existing_df[column].tolist()

    for i in range(0, len(final_projects_dict["full_name"])):

        project_name = final_projects_dict["full_name"][i].replace("#", "/")

        # Skip project if it's already in the output CSV
        if project_name in existing_projects:
            print(f"Skipping existing project: {project_name}")
            continue

        print(f"Starting processing of project: {final_projects_dict["full_name"][i]}")
        table_dict["Project"].append(final_projects_dict["full_name"][i].replace("#", "/"))
        table_dict["Creation year"].append(final_projects_dict["creation_year"][i])

        # Determine subject type
        is_microservices = final_projects_dict["MS/NonMS"][i] == "MS"
        table_dict["Subject Type"].append("Case" if is_microservices else "Control")

        # Get GitHub stars
        project_type = "cases" if is_microservices else "controls"
        num_stars_beginning, num_stars_end, follow_up_start_datetime, follow_up_end_datetime = get_stars(
            project_name=final_projects_dict["full_name"][i].replace("#", "/"),
            project_type=project_type
        )

        start_size = get_start_size(project_name=final_projects_dict["full_name"][i], project_type=project_type,
                                    follow_up_start_datetime=follow_up_start_datetime)

        # Assign FU_start values
        table_dict["Size_FU_start"].append(start_size)
        table_dict["Main Language_FU_start"].append(final_projects_dict["main_language"][i])
        table_dict["Stars_FU_start"].append(num_stars_beginning)
        table_dict["Issues_FU_start"].append(final_projects_dict["n_issues"][i])
        table_dict["Commits_FU_start"].append(final_projects_dict["n_commits"][i])
        table_dict["Contributors_FU_start"].append(final_projects_dict["n_contributors"][i])
        table_dict["Languages_FU_start"].append(final_projects_dict["n_languages"][i])

        if is_microservices:
            num_microservices = get_microservices(
                project_name=final_projects_dict["full_name"][i],
                period="start",
                follow_up_start_datetime=follow_up_start_datetime,
                follow_up_end_datetime=follow_up_end_datetime
            )
            table_dict["Microservices_FU_start"].append(num_microservices)
        else:
            table_dict["Microservices_FU_start"].append("-")

        # Fitting end of follow-up information into the dictionary
        end_commits, end_contributors, end_issues, last_commit_hash = get_end_vch_data(project_name=final_projects_dict["full_name"][i],
                                                                                       project_type=project_type,
                                                                                       follow_up_end_datetime=follow_up_end_datetime)
        table_dict["Issues_FU_end"].append(end_issues)  # Placeholder
        table_dict["Commits_FU_end"].append(end_commits)  # Placeholder

        # The repository no longer exists
        if final_projects_dict["full_name"][i] not in ["pagarme#tldr", "hashgraph#hedera-mirror-node"]:
            end_fu_num_languages, end_fu_size, end_fu_main_language  = get_sloc_variables(repo_name=final_projects_dict["full_name"][i],
                                                                                          current_hash=str(last_commit_hash))
        else:
            end_fu_num_languages, end_fu_size, end_fu_main_language = None, None, None

        table_dict["Size_FU_end"].append(end_fu_size)  # Placeholder
        table_dict["Main Language_FU_end"].append(end_fu_main_language)  # Placeholder
        table_dict["Stars_FU_end"].append(num_stars_end)  # Placeholder
        table_dict["Contributors_FU_end"].append(end_contributors)  # Placeholder
        table_dict["Languages_FU_end"].append(end_fu_num_languages)  # Placeholder

        if is_microservices:
            num_microservices_end = get_microservices(
                project_name=final_projects_dict["full_name"][i],
                period="end",
                follow_up_start_datetime=follow_up_start_datetime,
                follow_up_end_datetime=follow_up_end_datetime
            )
            table_dict["Microservices_FU_end"].append(num_microservices_end)  # Placeholder
        else:
            table_dict["Microservices_FU_end"].append("-")

        print(
            f"Project {final_projects_dict['full_name'][i]} completed - {i + 1}/{len(final_projects_dict['full_name'])}")

        # Convert new row into DataFrame and append to CSV
        new_row = {
            "Project": project_name,
            "Creation year": final_projects_dict["creation_year"][i],
            "Subject Type": "Case" if is_microservices else "Control",
            "Size_FU_start": table_dict["Size_FU_start"][-1],
            "Size_FU_end": table_dict["Size_FU_end"][-1],
            "Microservices_FU_start":  table_dict["Microservices_FU_start"][-1],
            "Microservices_FU_end": table_dict["Microservices_FU_end"][-1],
            "Main Language_FU_start": table_dict["Main Language_FU_start"][-1],
            "Main Language_FU_end": table_dict["Main Language_FU_end"][-1],
            "Stars_FU_start": table_dict["Stars_FU_start"][-1],
            "Stars_FU_end": table_dict["Stars_FU_end"][-1],
            "Issues_FU_start": table_dict["Issues_FU_start"][-1],
            "Issues_FU_end": table_dict["Issues_FU_end"][-1],
            "Commits_FU_start": table_dict["Commits_FU_start"][-1],
            "Commits_FU_end": table_dict["Commits_FU_end"][-1],
            "Contributors_FU_start": table_dict["Contributors_FU_start"][-1],
            "Contributors_FU_end": table_dict["Contributors_FU_end"][-1],
            "Languages_FU_start": table_dict["Languages_FU_start"][-1],
            "Languages_FU_end": table_dict["Languages_FU_end"][-1]
        }

        final_df = pd.DataFrame([new_row])
        # Append row to CSV
        final_df.to_csv(output_path, mode='a', header=not os.path.exists(output_path), index=False)

    print(f"> Table saved at {output_path}")
