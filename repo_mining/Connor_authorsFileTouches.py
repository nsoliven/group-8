import os
import csv
import json
import requests

def fetch_json(url, tokens, token_index):
     headers = {"Authorization": f"Bearer {tokens[token_index % len(tokens)]}"}

     response = requests.get(url, headers=headers)
     response.raise_for_status()

     data = response.json()
     return data, token_index + 1

def collect_file_touches(repository, tokens, valid_exts):
     page_num = 1
     token_idx = 0
     results = []

     while True:
          commits_url = (
               f"https://api.github.com/repos/{repository}/commits"
               f"?page={page_num}&per_page=100"
          )

          commits, token_idx = fetch_json(commits_url, tokens, token_idx)

          if not commits:
               break

          for commit in commits:
               sha = commit["sha"]
               author = commit["commit"]["author"]["name"]
               date = commit["commit"]["author"]["date"]

               detail_url = f"https://api.github.com/repos/{repository}/commits/{sha}"
               details, token_idx = fetch_json(detail_url, tokens, token_idx)

               for changed_file in details.get("files", []):
                    filename = changed_file.get("filename", "")
                    if filename.endswith(valid_exts):
                         results.append([filename, author, date])

          page_num += 1

     return results

def write_csv(rows, output_path):
     os.makedirs(os.path.dirname(output_path), exist_ok=True)

     with open(output_path, "w", newline="", encoding="utf-8") as f:
          writer = csv.writer(f)
          writer.writerow(["file", "author", "date"])
          writer.writerows(rows)



repo = "scottyab/rootbeer"
token = ["Fake000Token"]
ext = (".java", ".c", ".cpp", ".h", ".sh", ".py", ".kt", ".kts")

try:
     touches = collect_file_touches(repo, token, ext)
     write_csv(touches, "data/output.csv")
     print("Done")
except Exception as err:
     print(f"Error: {err}")