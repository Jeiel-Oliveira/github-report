# GitHub Report Generator

This script generates a report for a GitHub repository, including various statistics such as pull request count, commit count, lines added/deleted, and pull request change requests. The report is based on data retrieved from the GitHub API.

## Installation

Before using the script, ensure you have Python installed on your machine. Additionally, you'll need to install the GitHub CLI (gh) using the following command:

```powershell
snap install gh
```

After installing gh, authenticate with your GitHub account using the following command:

```powershell
gh auth login
```

## Usage

Run the script with the following command:

```powershell
python3 gh_report.py REPO_OWNER REPO_NAME "DATE_RANGE"
```

## Where:

- REPO_OWNER is the owner or organization of the repository.
- REPO_NAME is the name of the repository.
- DATE_RANGE is the date range for which the report will be generated. This should be in the format "YYYY-MM-DD..YYYY-MM-DD".

## Examples

### One repository

```powershell
python3 gh_report.py AGX-Software indiky-server "2024-05-01..2024-05-31"
```

### Multiple repositories

```powershell
python3 gh_report.py AGX-Software "indiky-server:core" "2024-05-01..2024-05-31"
```

## Output

The script generates a report similar to the following example:

```
YOUR_REPOSITORY 2024-02-01..2024-02-29

PR COUNT:
Das_pistas: 6
oliver: 12
JackOlive: 8
Dimitri: 9
EternoOliver: 7
jack: 3
app/dependabot: 1
TOTAL: 46

COMMIT COUNT:
Das_pistas: 34
oliver: 220
EternoOliver: 54
JackOlive: 77
Dimitri: 74
jack: 24
dependabot[bot]: 1
RelampagoMarcos: 6
TOTAL: 490

LINES ADD:
Das_pistas: 1817
oliver: 5159
JackOlive: 2905
Dimitri: 1627
EternoOliver: 2261
jack: 160
app/dependabot: 3
TOTAL: 13932

LINES DELETED:
Das_pistas: 485
oliver: 1021
JackOlive: 676
Dimitri: 252
EternoOliver: 970
jack: 19
app/dependabot: 3
TOTAL: 3426

PR CHANGE_REQUESTS:
JackOlive: 3
oliver: 4
jack: 1
TOTAL: 8
```

## Notes

- Ensure you have the necessary permissions to access the repository.
- The script depends on the GitHub API and Python. Make sure both are installed and configured correctly.
- For more information on the GitHub CLI and API, refer to the official documentation.
