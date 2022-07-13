"""
Download satellite images of based on the boundary obtained by gadm
"""
import os
import sys

from gadm import GADMDownloader

try:
    import tqdm
    from pystac_client import Client
    import rioxarray
except ImportError:
    print("Please install the following dependencies to run this example")
    print("\tpip install pystac_client")
    print("\tpip install rioxarray")
    print("\tpip install tqdm\n")
    sys.exit(1)


def get_args():
    import argparse

    parser = argparse.ArgumentParser("sample of downloading satellite images based on the gadm boundary")
    parser.add_argument("--output_dir", "-o", type=str, required=True)

    return parser.parse_args()


def main(args):
    downloader = GADMDownloader(version="4.0")
    country_name = "Japan"
    ad_level = 2
    gdf = downloader.get_shape_data_by_country_name(country_name=country_name, ad_level=ad_level)
    gdf = gdf[gdf["NAME_1"] == "Tokyo"]
    gdf = gdf[gdf["NAME_2"] == "Shibuya"]
    assert len(gdf) == 1

    boundary = gdf.iloc[0]["geometry"]
    url = "https://earth-search.aws.element84.com/v0"
    client = Client.open(url)

    collections = ["sentinel-s2-l2a-cogs"]
    time_range = "2022-01-01/2022-07-14"
    max_item = 5

    search = client.search(
        max_items=max_item,
        collections=collections,
        intersects=boundary,
        query={"eo:cloud_cover": {"lt": 10}, "sentinel:valid_cloud_cover": {"eq": True}},
        datetime=time_range,
    )

    for item in tqdm.tqdm(search.items(), total=min(search.matched(), max_item)):
        visual_href = item.assets["visual"].href
        output_file = "_".join(visual_href.split("/")[-2:])
        print("downloading {}".format(output_file))
        visual = rioxarray.open_rasterio(visual_href)
        visual.rio.to_raster(os.path.join(args.output_dir, output_file), driver="COG")


if __name__ == "__main__":
    main(get_args())
