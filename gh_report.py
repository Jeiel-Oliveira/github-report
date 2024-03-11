from datetime import datetime, timedelta
from collections import defaultdict
import calendar
import subprocess
import json
import sys

def month_name(month: int):
    return calendar.month_name[month]

class Report:
    def sum_defaultdict(self, d):
        total = 0
        for _, v in d.items():
            total += v
        return total

    def one_line_result(self, d, title, file):
        title = f"{title}\n"
        print(title)
        file.write(title)

        for key, value in d.items():
            key_pair = f"""{key}: {value}"""
            file.write(key_pair + "\n")
            print(key_pair)

        total = f"TOTAL: {self.sum_defaultdict(d)}"
        file.write(total)
        print(total)
        print("\n")
        file.write("\n")
        file.write("\n")

class GenerateReport(Report):
    repo_owner: str
    repo_name: str
    date: int

    def __init__(self, repo_owner: str, repo_name: str, date: str):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.date = date

    def base_cmd(self):
        return [
            "gh",
            "pr",
            "list",
            "-R",
            f"{self.repo_owner}/{self.repo_name}",
            "--state",
            "closed",
            "-L",
            "100",
        ]

    def commit_cmd(self, number: str):
        return [
            "gh",
            "pr",
            "view",
            str(number),
            "-R",
            f"{self.repo_owner}/{self.repo_name}",
        ]

    def generate_pr_json(self, date_range: str):
        cmd = self.base_cmd() + [
            "--json",
            "author,number,title,mergedAt,additions,deletions,reviews",
            "-S",
            f"merged:{date_range}",
        ]

        result = subprocess.run(cmd, stdout=subprocess.PIPE)
        return json.loads(result.stdout)

    def generate_commit_json(self, number: int):
        cmd = self.commit_cmd(number) + ["--json", "commits"]

        result = subprocess.run(cmd, stdout=subprocess.PIPE)
        return json.loads(result.stdout)

    def pr_results(self):
        prs_result = self.generate_pr_json(self.date)

        commits_by_author = defaultdict(int)
        deletions_by_author = defaultdict(int)
        additions_by_author = defaultdict(int)
        count_by_author = defaultdict(int)
        request_changes_by_author = defaultdict(int)

        total = len(prs_result)
        count = 1

        print(f"Total PRs: {total} from {self.repo_owner}/{self.repo_name}\n")

        for pr in prs_result:
            print(f"Processing {count} of {total}")

            deletions_by_author[pr["author"]["login"]] += pr["deletions"]
            additions_by_author[pr["author"]["login"]] += pr["additions"]
            count_by_author[pr["author"]["login"]] += 1

            commits = self.generate_commit_json(pr["number"])
            for commit in commits["commits"]:
                for author in commit["authors"]:
                    commits_by_author[author["login"]] += 1

            for review in pr["reviews"]:
                if review["state"] == "CHANGES_REQUESTED":
                    request_changes_by_author[pr["author"]["login"]] += 1

            count += 1

        return {
            "commits_by_author": commits_by_author,
            "deletions_by_author": deletions_by_author,
            "additions_by_author": additions_by_author,
            "count_by_author": count_by_author,
            "request_changes_by_author": request_changes_by_author
        }

class GenerateTotalReport(Report):
    repo_owner: str
    repos_name: str
    date: int

    def __init__(self, repo_owner: str, repos_name: str, date: str):
        self.repo_owner = repo_owner
        self.repos_name = repos_name
        self.date = date

    def sum_by_author(self):
        repos = self.repos_name.split(":")

        commits_by_author = defaultdict(int)
        deletions_by_author = defaultdict(int)
        additions_by_author = defaultdict(int)
        count_by_author = defaultdict(int)
        request_changes_by_author = defaultdict(int)

        for repo in repos:
            generate_report = GenerateReport(self.repo_owner, repo, self.date)
            prs_result = generate_report.pr_results()

            for key, value in prs_result["commits_by_author"].items():
                commits_by_author[key] += value

            for key, value in prs_result["deletions_by_author"].items():
                deletions_by_author[key] += value

            for key, value in prs_result["additions_by_author"].items():
                additions_by_author[key] += value

            for key, value in prs_result["count_by_author"].items():
                count_by_author[key] += value

            for key, value in prs_result["request_changes_by_author"].items():
                request_changes_by_author[key] += value

        return {
            "commits_by_author": commits_by_author,
            "deletions_by_author": deletions_by_author,
            "additions_by_author": additions_by_author,
            "count_by_author": count_by_author,
            "request_changes_by_author": request_changes_by_author
        }

    def generate_file(self):
        print(f"generating report from {self.date} for {self.repos_name}\n")

        prs_result = self.sum_by_author()

        file_name = f"prs_report_{self.repos_name}_{self.repo_owner}_{self.date}.txt"
        with open(file_name, "w") as file:
            repo_name = self.repos_name.upper() + f" {self.date}" + "\n"
            print(repo_name)
            file.write(repo_name)
            file.write("\n")

            self.one_line_result(prs_result["count_by_author"], "PR COUNT:", file)
            self.one_line_result(prs_result["commits_by_author"], "COMMIT COUNT:", file)
            self.one_line_result(prs_result["additions_by_author"], "LINES ADD:", file)
            self.one_line_result(prs_result["deletions_by_author"], "LINES DELETED:", file)
            self.one_line_result(prs_result["request_changes_by_author"], "PR CHANGE_REQUESTS:", file)

"""
    Argswith open(file_name, 'w') as file:
    # Write the content to the file
    file.write(content):
        repo_owner (str): The owner or organization of the repository.
        repo_name (str): The name of the repository.
        date (str): The date range which the report will be generated. Should be a date range following the example 2024-05-01..2024-05-31

    example: python3 gh_report.py AGX-Software "indiky-server:core" "2024-05-01..2024-05-31"
    example 2: python3 gh_report.py AGX-Software indiky-web "2024-05-01..2024-05-31"
"""
if __name__ == "__main__":
    GenerateTotalReport(*sys.argv[1:4]).generate_file()
