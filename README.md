<p align="center">
<a href="https://pypi.python.org/pypi/gadm" target="_blank">
  <img src="https://img.shields.io/pypi/v/gadm.svg" alt="PyPi">
</a>
<a href="https://pypi.python.org/pypi/gadm" target="_blank">
  <img src="https://img.shields.io/pypi/pyversions/gadm" alt="PyPi">
</a>
<a href="https://github.com/xmba15/gadm/actions/workflows/main.yml" target="_blank">
  <img src="https://github.com/xmba15/gadm/actions/workflows/main.yml/badge.svg" alt="Build Status">
</a>
</p>

# 📝 GADM  #
***
This library provides all countries's national and prefectural boundaries in the form of [geopandas](https://geopandas.org/en/stable/) dataframe, by dynamically fetching from [GADM dataset](https://gadm.org/).

## :gear: Installation ##
***

```bash
pip install gadm
```

## :running: How to Run ##
***

### Basic usage ###
***


```python
import geopandas as gpd
from gadm import GADMDownloader

downloader = GADMDownloader(version="4.0")

country_name = "Vietnam"
ad_level = 0
gdf = downloader.get_shape_data_by_country_name(country_name=country_name, ad_level=ad_level)

assert isinstance(gdf, gpd.GeoDataFrame)
gdf.plot()
```

### Use with visualization library ###
***

GADM's data frame can be interactively visualized on a jupyter notebook with [folium](https://python-visualization.github.io/folium/)

```python
import folium as fl
import geopandas as gpd

from gadm import GADMDownloader

downloader = GADMDownloader(version="4.0")

country_name = "Vietnam"
ad_level = 1
gdf = downloader.get_shape_data_by_country_name(country_name=country_name, ad_level=ad_level)

m = fl.Map(zoom_start=10, tiles="OpenStreetMap")
for _, r in gdf.iterrows():
    sim_geo = gpd.GeoSeries(r["geometry"]).simplify(tolerance=0.001)
    geo_j = sim_geo.to_json()
    geo_j = fl.GeoJson(data=geo_j, style_function=lambda x: {"fillColor": "orange"})
    fl.Popup(r["VARNAME_1"]).add_to(geo_j)
    geo_j.add_to(m)
m
```

<p align="center">
  <img src="https://raw.githubusercontent.com/xmba15/gadm/master/docs/images/sample_plot_on_folium_map.jpg" alt="folium map sample">
</p>

### Download satellite images based on boundaries from gadm ###
***

Check [the following example](https://github.com/xmba15/gadm/blob/master/examples/download_satellite_images.py)

## 🎛  Development Environment ##
***

```bash
conda env create --file environment.yml
conda activate gadm
```
