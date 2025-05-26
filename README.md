# Wuhan Diary on a Map

## Overview
Between January 25 and March 24 in 2020, Fang Fang (方方) wrote daily diary entries about the situation in Wuhan and published them online. This project is an effort to visualize the locations she mentioned each day.

The locations were automatically identified using [HanLP](https://hanlp.hankcs.com/docs/index.html), and the coordinates were looked up manually. The maps were generated using [Plotly](https://plotly.com/). You can find all the diary posts on [Caixin](https://fangfang.blog.caixin.com/).

## Data and Code
The code used for identifying the locations can be found in `src/locations.py`. `src/process_diary.py` generates a json file with the initial results (`data/ner_results.json`). `src/find_unique.py` is used to find all unique locations (`data/locations_info.json`). The missing data was then filled out manually. Contributions to this file are welcome. Locations where `valid=false` are currently not being considered locations; locations where `valid=null` are also not being mapped because the location could not be identified so far. `src/merge.py` applies the data in `data/locations_info.json` to `data/ner_results.json` in `data/locations_to_map.json`. This file is used by `src/make_map.py` to create a map for each day, which can be found in `website/maps`.