from pathlib import Path

import geopandas as gpd

cwd = Path.cwd()

geojson_path = cwd.joinpath("data")
dist_path = cwd.joinpath("dist")


def convert_to_shp(filepath: Path):
    if not dist_path.exists():
        dist_path.mkdir()
    subfolder = dist_path.joinpath(f"{filepath.stem}/")
    if not subfolder.exists():
        subfolder.mkdir()

    file_name = filepath.name
    if "geojson" not in file_name:
        print("未找到geojson文件")
        return
    gdf = gpd.read_file(filepath)
    multipolygons = gdf[gdf.geometry.type == "MultiPolygon"]
    multilinestring = gdf[gdf.geometry.type == "MultiLineString"]
    multipolygons.to_file(
        subfolder.joinpath(f"{filepath.stem}.shp"),
        driver="ESRI Shapefile",
        encoding="utf-8",
    )
    multilinestring.to_file(
        subfolder.joinpath(f"{filepath.stem}.境界线.shp"),
        driver="ESRI Shapefile",
        encoding="utf-8",
    )


def convert_to_gpkg(filepath: Path):
    gdf = gpd.read_file(filepath)
    multipolygons = gdf[gdf.geometry.type == "MultiPolygon"]
    multilinestring = gdf[gdf.geometry.type == "MultiLineString"]
    multipolygons.to_file(
        dist_path.joinpath("天地图-行政区划.gpkg"),
        layer=f"{filepath.stem}",
        driver="GPKG",
    )
    multilinestring.to_file(
        dist_path.joinpath("天地图-行政区划.gpkg"),
        layer=f"{filepath.stem}.境界线",
        driver="GPKG",
    )


for i in geojson_path.glob("*.geojson"):
    print(f"开始转换 {i.name}")
    convert_to_shp(i)
    print(f"{i.stem} shp 转换完成")
    convert_to_gpkg(i)
    print(f"{i.stem} gpkg 转换完成")

# print(geojson_path.glob("*.geojson"))
