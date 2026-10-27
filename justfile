# 以 data/raw 为源，格式化后输出到 data/formatted
format:
    mkdir -p data/formatted
    cp data/raw/*.geojson data/formatted/
    npx --yes prettier@3 --parser json --write "data/formatted/*.geojson"
# 只格式化 data/formatted 中已有的指定文件，例如 just format-file data/formatted/中国_县.geojson
format-file file:
    npx --yes prettier@3 --parser json --write "{{ file }}"
# 将 data/raw 的 GeoJSON 转换为 Shapefile/GeoPackage，并打包到 dist/
convert:
    uv run script/convert.py
