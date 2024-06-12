import shutil
import zipfile
from pathlib import Path

import geopandas as gpd

cwd = Path.cwd()

geojson_path = cwd.joinpath("data")
dist_path = cwd.joinpath("dist")


def convert_to_shp(filepath: Path):
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
    # 打包为zip
    # with zipfile.ZipFile(
    #     dist_path.joinpath(f"{filepath.stem}.zip"), "w", zipfile.ZIP_DEFLATED
    # ) as zipf:
    #     for file in subfolder.glob("**/*"):
    #         zipf.write(file, file.relative_to(subfolder.parent))


def convert_to_gpkg(filepath: Path):
    gdf = gpd.read_file(filepath)
    gpkg_file_path = dist_path.joinpath("天地图-行政区划.gpkg")
    multipolygons = gdf[gdf.geometry.type == "MultiPolygon"]
    multilinestring = gdf[gdf.geometry.type == "MultiLineString"]
    multipolygons.to_file(
        gpkg_file_path,
        layer=f"{filepath.stem}",
        driver="GPKG",
    )
    multilinestring.to_file(
        gpkg_file_path,
        layer=f"{filepath.stem}.境界线",
        driver="GPKG",
    )


def main():
    # 删除 dist 文件夹
    if dist_path.exists():
        shutil.rmtree(dist_path)
    # 创建 dist 文件夹
    if not dist_path.exists():
        dist_path.mkdir()

    for i in geojson_path.glob("*.geojson"):
        print(f"开始转换 {i.name}")
        convert_to_shp(i)
        print(f"{i.stem} shp 转换完成")
        convert_to_gpkg(i)
        print(f"{i.stem} gpkg 转换完成")

    # 打包 gpkg 文件为 zip
    gpkg_file_path = dist_path.joinpath("天地图-行政区划.gpkg")
    with zipfile.ZipFile(
        dist_path.joinpath("行政区划.gpkg.zip"), "w", zipfile.ZIP_DEFLATED
    ) as zipf:
        zipf.write(gpkg_file_path, gpkg_file_path.relative_to(dist_path))

    # 打包 shp 文件 为 zip

    with zipfile.ZipFile(
        dist_path.joinpath("行政区划.shp.zip"), "w", zipfile.ZIP_DEFLATED
    ) as zipf:
        directories = [p for p in dist_path.glob("*") if p.is_dir()]
        for directory in directories:
            for file in directory.glob("**/*"):
                zipf.write(file, file.relative_to(directory.parent))
    # 打包 geojson 文件 为 zip
    with zipfile.ZipFile(
        dist_path.joinpath("行政区划.geojson.zip"), "w", zipfile.ZIP_DEFLATED
    ) as zipf:
        for file in geojson_path.glob("**/*"):
            zipf.write(file, file.relative_to(geojson_path))


if __name__ == "__main__":
    main()
