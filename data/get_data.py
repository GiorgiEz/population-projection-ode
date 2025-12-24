from bs4 import BeautifulSoup
import csv
import re

def remove_brackets(value):
    if not value:
        return value
    value = re.sub(r"\[[^\]]*\]", "", value)
    value = re.sub(r"\([^\)]*\)", "", value)
    return value.strip()

# ---------- Load HTML ----------
with open("table.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

table = soup.find("table")
rows = table.find("tbody").find_all("tr")

# ---------- Columns ----------
header = [
    "year",
    "avg_population",
    "live_births",
    "deaths",
    "natural_change",
    "crude_birth_rate",
    "crude_death_rate",
    "natural_change_per_1000",
    "crude_migration_change",
    "total_fertility_rate",
]

# ---------- Write CSV ----------
with open("population_data.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(header)

    for row in rows[1:-2]:
        cells = [td.get_text(strip=True) for td in row.find_all("td")]
        cleaned = [remove_brackets(cell) for cell in cells]
        writer.writerow(cleaned)

print("Saved population_data.csv")
