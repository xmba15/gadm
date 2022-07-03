import geopandas as gpd
import pycountry as pct
import pytest

from gadm import GADMDownloader


def test_initialization_success():
    supported_versions = ["4.0"]
    for version in supported_versions:
        GADMDownloader(version=version)


def test_initialization_failure():
    not_supported_version = "2.8"
    with pytest.raises(AssertionError, match="2.8 .*"):
        GADMDownloader(version=not_supported_version)


def test_download_data_success():
    supported_versions = ["4.0"]
    country_names = ["Vietnam", "Japan", "USA"]
    for version in supported_versions:
        downloader = GADMDownloader(version=version)
        for country_name in country_names:
            gdf = downloader.get_shape_data_by_country_name(country_name=country_name, ad_level=0)
            assert isinstance(gdf, gpd.GeoDataFrame)


def test_download_data_by_country_object():
    country_name = "Vietnam"
    country = pct.countries.lookup(country_name)
    downloader = GADMDownloader(version="4.0")
    gdf = downloader.get_shape_data_by_country(country=country, ad_level=0)
    assert isinstance(gdf, gpd.GeoDataFrame)


def test_download_not_existing_country():
    not_existing_country_name = "MCU"
    downloader = GADMDownloader(version="4.0")
    gdf = downloader.get_shape_data_by_country_name(country_name=not_existing_country_name, ad_level=0)
    assert gdf is None


def test_download_invalid_ad_level():
    invalid_ad_level = 100
    with pytest.raises(AssertionError):
        downloader = GADMDownloader(version="4.0")
        downloader.get_shape_data_by_country_name(country_name="Vietnam", ad_level=invalid_ad_level)
