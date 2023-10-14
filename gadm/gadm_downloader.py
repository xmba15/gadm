"""
Module to download GADM data, the database of global Administrative Areas.
"""

import logging
import os
from typing import List, Optional

import fiona
import geopandas as gpd
import pycountry as pct

from gadm.custom_types import AdministrativeDivisionLevel as ADLevel
from gadm.utils import download_url

__all__ = ["GADMDownloader"]


class GADMDownloader:
    """
    Data downloader of GADM, the database of global Administrative Areas.
    Official Website: https://gadm.org/
    """

    __SUPPORTED_VERSIONS = {"4.0": "40"}
    __ROOT_URL_TEMPLATE = "https://geodata.ucdavis.edu/gadm/gadm{version}/gpkg/"
    __DATA_PATH_TEMPLATE = "gadm{version_wo_dot}_{country_alpha_3}.gpkg"
    __CACHED_DIR = os.path.join(os.path.expanduser("~"), ".gadm")

    def __init__(
        self,
        version: str = "4.0",
        timeout_sec: float = 60,
        logger: logging.Logger = logging.getLogger("gadm_downloader.db"),
    ):
        """
        Parameters
        ----------
        version : str
            version of gadm data, currently only support version 4.0
        logger : logging.Logger
            logger instance
        """
        assert version in GADMDownloader.__SUPPORTED_VERSIONS, f"{version} is not a supported version"
        self._version = version
        self._url_root_dir = GADMDownloader.__ROOT_URL_TEMPLATE.format(
            version=self._version,
        )
        self._timeout_sec = timeout_sec
        self._logger = logger

        if not os.path.isdir(GADMDownloader.__CACHED_DIR):
            os.makedirs(GADMDownloader.__CACHED_DIR)

    def get_shape_data_by_country(
        self, country: pct.ExistingCountries.data_class_base, ad_level: int
    ) -> Optional[gpd.GeoDataFrame]:
        """get shape data as a GeoDataFrame by country object

        Parameters
        ----------
        country : Country
            object of Country defined in pycountry library
        ad_level : int
            administrative division level

        Returns
        -------
        Optional[gpd.GeoDataFrame]
            optional GeoDataFrame shape
        """

        if not os.path.isdir(GADMDownloader.__CACHED_DIR):
            os.makedirs(GADMDownloader.__CACHED_DIR)

        data_path = GADMDownloader.__DATA_PATH_TEMPLATE.format(
            version_wo_dot=GADMDownloader.__SUPPORTED_VERSIONS[self._version], country_alpha_3=country.alpha_3
        )
        abs_data_path = os.path.join(GADMDownloader.__CACHED_DIR, data_path)
        try:
            download_url(
                self._url_root_dir + data_path,
                abs_data_path,
                timeout_sec=self._timeout_sec,
                logger=self._logger,
            )
        except Exception as e:
            self._logger.exception(f"failed to fetch data for {country.common_name} with error {e}")
            return None

        layers: List[str] = sorted(fiona.listlayers(abs_data_path))
        if len(layers) < ad_level:
            self._logger.info("gadm does not have data for level {ad_level} of {country.common_name}")
            return None

        return gpd.read_file(abs_data_path, layer=layers[ad_level])

    def get_shape_data_by_country_name(self, country_name: str, ad_level: int) -> Optional[gpd.GeoDataFrame]:
        """get shape data as a GeoDataFrame by country name

        Parameters
        ----------
        country_name : str
            country name
        ad_level : int
            administrative division level

        Returns
        -------
        Optional[gpd.GeoDataFrame]
            optional GeoDataFrame shape
        """

        assert ADLevel.MIN <= ad_level <= ADLevel.MAX
        try:
            country = pct.countries.lookup(country_name)
        except LookupError:
            self._logger.exception(f"could not find data for {country_name}")
            return None

        return self.get_shape_data_by_country(country, ad_level)
