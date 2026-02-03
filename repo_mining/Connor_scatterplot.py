import csv
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np


intut = "data/output.csv"
rows = []
with open(input, newline='') as f:
     reader = csv.DictReader(f)
     for row in reader:
          rows.append(row)

dates = [datetime.fromisoformat(r['date'].replace('Z', '')) for r in rows]
project_start = min(dates)

files = sorted(set(r['file'] for r in rows))
authors = sorted(set(r['author'] for r in rows))

file_index = {f: i for i, f in enumerate(files)}
author_index = {a: i for i, a in enumerate(authors)}
num_authors = len(authors)

cmap = cm.get_cmap('tab20', num_authors)
author_colors = {a: cmap(i) for a, i in author_index.items()}

x_files = []
y_weeks = []
point_colors = []

for r in rows:
     date = datetime.fromisoformat(r['date'].replace('Z', ''))
     weeks = (date - project_start).days / 7

     x_files.append(file_index[r['file']])
     y_weeks.append(weeks)
     point_colors.append(author_colors[r['author']])


plt.figure(figsize=(12, 7))

plt.scatter(
     x_files,
     y_weeks,
     c=point_colors,
     alpha=0.75,
     edgecolors='black',
     linewidths=0.3
)

plt.xlabel("Files")
plt.ylabel("Weeks Since Project Start")
plt.title("Author Activity Over Time")

legend_handles = [
     plt.Line2D(
          [0], 
          [0], 
          marker='o', 
          color='w',
          markerfacecolor=author_colors[a], 
          markeredgecolor='black',
          markersize=8, 
          label=a
     )
     for a in authors
]

plt.legend(
    handles=legend_handles,
    title="Authors",
    bbox_to_anchor=(1.05, 1),
    loc="upper left"
)

plt.tight_layout()
plt.show()
