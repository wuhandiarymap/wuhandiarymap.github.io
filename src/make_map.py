import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd
import json
from tqdm import tqdm

class MapMaker():
	def __init__(self):
		super(MapMaker, self).__init__()
		
	def base_map(self, districts):
		geojson = open("../data/wuhan.geojson", encoding="utf-8")
		gdf = gpd.read_file(geojson)
		
		gdf["name"] = gdf["name"].str[:-1]
		gdf["info"] = gdf["name"].map(districts)
		
		# print(districts)
		# print(gdf)
		# print(gdf["info"])
		# input()
		
		if districts:
			gdf["highlight"] = gdf["name"].apply(lambda x: 1 if x.replace("区", "") in districts.keys() else 0)

		else:
			gdf["highlight"] = 0
		
		self.fig = px.choropleth_map(
			gdf,
			geojson=gdf.geometry,
			locations=gdf.index,
			center={"lat": 30.5928, "lon": 114.3052}, 
			map_style="open-street-map", #"carto-positron-nolabels",
			color="highlight",
			hover_name="name",
			hover_data={"highlight": False},
			custom_data="info",
			color_continuous_scale=[[0, "#ed8a9c"], [1, "#2feb64"]],
			range_color=[0, 1],
			opacity=0.2,
			width=750,
			height=800,
		)
		
		self.fig.update_coloraxes(showscale=False)
		self.fig.update_traces(hovertemplate="<b>%{hovertext}<b><extra></extra>")

	def add_marker(self, lat, lon, name, wuhan, data):
		hover_text = f"<b>{name}</b><br><i>Click for more info</i><extra></extra>"

		if wuhan:
			self.fig.add_trace(
				go.Scattermap(
					lat=[lat],
					lon=[lon],
					hovertemplate=hover_text,
					mode="markers",
					marker=dict(
						size=12,
						opacity=1,
						color="#fa3f32"
					),
					customdata=data
				)
			)
		else:
			self.fig.add_trace(
				go.Scattermap(
					lat=[lat],
					lon=[lon],
					hovertemplate=hover_text,
					mode="text+markers",
					text=name,
					textposition="top center",
					marker=dict(
						size=12,
						opacity=1,
						color="#fa3f32"
					),
					textfont=dict(
						size=20,
						color="black",
					),
					customdata=data
				)
			)

	def save_map(self, fname):
		self.fig.update_layout(
			margin=dict(
				l=0,
				r=0,
				b=0,
				t=0,
				pad=0
			),
			showlegend=False,
		)
		self.fig.write_html(f"../website/maps/{fname}.html", config={"displayModeBar": False}, div_id=f"{fname}")


def process_data():
	with open("../data/locations_to_map.json", "r", encoding="utf-8") as file:
		data = json.loads(file.read())

	for k, v in tqdm(data.items()):
	#for k, v in data.items():
		mm = MapMaker()
		locations = v["locations"]
		districts = {}
		
		for i, j in locations.items():
			if j["description"] == "District":
				districts[i.replace("区", "")] = [i, j["mentioned_this_day"], j["mentioned_total"], j["context"], j["description"]]
			if i == "汉口":
				districts["江汉"] = [i, j["mentioned_this_day"], j["mentioned_total"], j["context"], j["description"]]
				districts["硚口"] = [i, j["mentioned_this_day"], j["mentioned_total"], j["context"], j["description"]]
				districts["江岸"] = [i, j["mentioned_this_day"], j["mentioned_total"], j["context"], j["description"]]

		mm.base_map(districts)
		
		mapped_wuhan = False

		for i, j in locations.items():
			lat = j["lat"]
			lon = j["lon"]
			data = [i, j["mentioned_this_day"], j["mentioned_total"], j["context"], j["description"]]

			if j["description"] != "District" and j["valid"]:
				if j["wuhan"]:
					if (i == "武汉市" or i == "武汉" or i == "汉") and not mapped_wuhan:
						mm.add_marker(lat, lon, "武汉", False, data)
						mapped_wuhan = True

					if (i != "武汉市" and i != "武汉" and i != "汉"):
						mm.add_marker(lat, lon, i, True, data)
				
				if not j["wuhan"]:
					mm.add_marker(lat, lon, i, False, data)
		
		mm.save_map(k)


if __name__ == "__main__":
	process_data()

