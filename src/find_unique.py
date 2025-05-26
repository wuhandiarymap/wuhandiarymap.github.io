import json

with open("../data/ner_results.json", "r", encoding="utf-8") as file:
	results = json.loads(file.read())

unique = {}

for k, v in results.items():
	for i, j in v["locations"].items():
		mentioned = j["mentioned"]
		if i not in unique:
			unique[i] = {"valid": None, "mentioned": mentioned, "wuhan": None, "area": None, "lat": None, "lon": None, "source": None}
		else:
			unique[i]["mentioned"] += mentioned

unique = {k: v for k, v in sorted(unique.items(), key=lambda item: item[1]["mentioned"], reverse=True)}
print(len(unique))
with open("../data/locations_info.json", "w", encoding="utf-8") as file:
	file.write(json.dumps(unique))


