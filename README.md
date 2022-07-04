# 📝 GADM  #
***

## 🎛  Dependencies ##
***

```bash
conda env create --file environment.yml
conda activate gadm
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
```

## :gem: References ##
***
