import json

locations_to_map = {}

with open("../data/ner_results.json", "r", encoding="utf-8") as file:
	results = json.loads(file.read())

with open("../data/locations_info.json", "r", encoding="utf-8") as file:
	info = json.loads(file.read())

for k, v in results.items():
	source = v["source"]
	title = v["title"]
	locations = v["locations"]

	locations_to_map[k] = {
		"source": source,
		"title": title,
		"locations": None
	}

	location_info = {}

	for i, j in locations.items():
		mentioned = j["mentioned"]
		label = j["label"]
		context = j["context"]
		valid = info[i]["valid"]
		mentioned_total = info[i]["mentioned"]
		wuhan = info[i]["wuhan"]
		area = info[i]["area"]
		lat = info[i]["lat"]
		lon = info[i]["lon"]
		description = info[i]["description"]
		info_source = info[i]["source"]

		location_info[i] = {
			"mentioned_this_day": mentioned,
			"mentioned_total": mentioned_total,
			"label": label,
			"context": context,
			"valid": valid,
			"wuhan": wuhan,
			"area": area,
			"lat": lat,
			"lon": lon,
			"description": description,
			"info_source": info_source
		}

	locations_to_map[k]["locations"] = location_info


with open("../data/locations_to_map.json", "w", encoding="utf-8") as file:
	info = file.write(json.dumps(locations_to_map))

		



