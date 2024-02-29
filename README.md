# github-report
Generate files for github reports

Example of the file generated:
```
CORE 2024-02-01..2024-02-29

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

This code depends on git hub api and python. Ensure your machine have both installed
DOCS: https://cli.github.com/manual/gh_api

First install gh api

```powershell
snap install gh
```

After you install, login in gh with the command

```powershell
gh auth login
```

After you finish the authentication you are read to go.

Command example:

```powershell
python3 gh_report.py AGX-Software indiky-server "2024-05-01..2024-05-31"
```

"""
    Argswith open(file_name, 'w') as file:
    # Write the content to the file
    file.write(content):
        repo_owner (str): The owner or organization of the repository.
        repo_name (str): The name of the repository.
        date (str): The date range which the report will be generated. Should be a date range following the example 2024-05-01..2024-05-31

    example: python3 gh_report.py AGX-Software indiky-server "2024-05-01..2024-05-31"
    example 2: python3 gh_report.py AGX-Software indiky-web "2024-05-01..2024-05-31"
"""
