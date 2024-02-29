from datetime import datetime, timedelta
from collections import defaultdict
import calendar
import subprocess
import json
import sys


def format_month(month: int):
    year = datetime.now().year

    first_day = datetime(year, month, 1)
    if month == 12:
        last_day = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        last_day = datetime(year, month + 1, 1) - timedelta(days=1)

    start_date_str = first_day.strftime("%Y-%m-%d")
    end_date_str = last_day.strftime("%Y-%m-%d")

    return start_date_str, end_date_str


def format_month_dot(month: int):
    start_date_str, end_date_str = format_month(month)
    return f"{start_date_str}..{end_date_str}"


def format_month_since_until(month: int):
    start_date_str, end_date_str = format_month(month)
    return f"since={start_date_str}&until={end_date_str}"


def month_name(month: int):
    return calendar.month_name[month]


class GenerateReport:
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

    def sum_by_author(self):
        print(f"generating report from {self.date} for {self.repo_name}\n")

        commits_by_author = defaultdict(int)
        deletions_by_author = defaultdict(int)
        additions_by_author = defaultdict(int)
        count_by_author = defaultdict(int)
        request_changes_by_author = defaultdict(int)

        prs_result = self.generate_pr_json(self.date)

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

        file_name = f"prs_report_{self.repo_name}_{self.repo_owner}_{self.date}.txt"
        with open(file_name, "w") as file:
            repo_name = self.repo_name.upper() + f" {self.date}" + "\n"
            print(repo_name)
            file.write(repo_name)
            file.write("\n")

            self.one_line_result(count_by_author, "PR COUNT:", file)
            self.one_line_result(commits_by_author, "COMMIT COUNT:", file)
            self.one_line_result(additions_by_author, "LINES ADD:", file)
            self.one_line_result(deletions_by_author, "LINES DELETED:", file)
            self.one_line_result(request_changes_by_author, "PR CHANGE_REQUESTS:", file)

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


if __name__ == "__main__":
    GenerateReport(*sys.argv[1:4]).sum_by_author()
