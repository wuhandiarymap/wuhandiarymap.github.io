import glob
from locations import FindLocations
from tqdm import tqdm
from datetime import datetime
import json


def get_entries():
	entries = []
	for file in glob.glob("**/*.txt", recursive=True):
		entries.append(file)

	return entries

def process():
	entries = get_entries()
	fl = FindLocations(verbose=False)
	results = {}
	for i in tqdm(entries):
		with open(i, "r", encoding="utf-8") as file:
			date = str(datetime.strptime(i.split("\\")[1].replace(".txt", ""), "%Y%m%d").date())
			text = ""
			for line in file:
				if "Source" in line:
					source = line.replace("Source: ", "").strip("\n")
				elif "Title" in line:
					title = line.replace("Title: ", "").strip("\n")
				elif "Text" in line:
					continue
				else:
					text += line


			locations = fl.find_locations(f"{title}\n{text}")
			
			results[date] = {"source": source, "title": title, "locations": locations}

	with open("../data/ner_results.json", "w", encoding="utf-8") as file:
		file.write(json.dumps(results))

process()

