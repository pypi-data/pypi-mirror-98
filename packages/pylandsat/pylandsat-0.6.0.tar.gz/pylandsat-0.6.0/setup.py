# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pylandsat']

package_data = \
{'': ['*']}

install_requires = \
['appdirs',
 'click',
 'fiona',
 'geopy',
 'numpy',
 'python-dateutil',
 'rasterio>=1.0,<2.0',
 'requests>=2.20,<3.0',
 'shapely',
 'tqdm']

entry_points = \
{'console_scripts': ['pylandsat = pylandsat.cli:cli']}

setup_kwargs = {
    'name': 'pylandsat',
    'version': '0.6.0',
    'description': 'Search, download and preprocess Landsat imagery',
    'long_description': '# Description\n\n**pylandsat** is a Python package that allows you to search and download\nLandsat scenes from the public dataset hosted on\n[Google Cloud](https://cloud.google.com/storage/docs/public-datasets/landsat).\nAdditionally, it includes a set of classes and methods to access and\npreprocess the downloaded scenes.\n\nOnly Landsat [Collection 1](https://landsat.usgs.gov/landsat-collections) is supported, i.e. level-1 data products from the following sensors and satellite missions:\n\n* Landsat 8 OLI/TIRS\n* Landsat 7 ETM+\n* Landsat 4-5 TM\n* Landsat 1-5 MSS\n\n# Installation\n\n`pip install pylandsat`\n\n# Command-line interface\n\n## Download one or multiple scenes\n\n### Usage\n\n```bash\nUsage: pylandsat download [OPTIONS] [PRODUCTS]...\n\n  Download a Landsat product according to its identifier.\n\nOptions:\n  -d, --output-dir PATH  Output directory.\n  -f, --files TEXT       Comma-separated list of files to download.\n  --help                 Show this message and exit.\n```\n\n### Examples\n\n```bash\n# Download an entire product in the current directory\npylandsat download LE07_L1TP_205050_19991104_20170216_01_T1\n\n# Download multiple products\npylandsat download \\\n    LE07_L1TP_205050_19991104_20170216_01_T1 \\\n    LE07_L1TP_206050_19991111_20170216_01_T1\n\n# Download only the blue, green and red bands\npylandsat download --files B1.TIF,B2.TIF,B3.TIF \\\n    LE07_L1TP_205050_19991104_20170216_01_T1\n\n# Download only quality band\npylandsat download --files BQA.TIF \\\n    LE07_L1TP_205050_19991104_20170216_01_T1\n```\n\n## Search for scenes\n\nTo allow large and fast queries, **pylandsat** works with a local dump of the Landsat catalog hosted on Google Cloud. As such, an initial sync is required :\n\n```bash\n# Sync local Landsat catalog\npylandsat sync-database\n\n# Force update\npylandsat sync-database -f\n```\n\nThe database is stored in a local directory that can be displayed using the following command :\n\n```bash\npylandsat print-datadir\n```\n\nOnce the database has been created, the local catalog can be queried.\n\n### Usage\n\n```bash\nUsage: pylandsat search [OPTIONS]\n\n  Search for scenes in the Google Landsat Public Dataset catalog.\n\nOptions:\n  -b, --begin TEXT       Begin search date (YYYY-MM-DD).\n  -e, --end TEXT         End search date (YYYY-MM-DD).\n  -g, --geojson PATH     Area of interest (GeoJSON file).\n  -l, --latlon FLOAT...  Point of interest (decimal lat/lon).\n  -p, --path INTEGER     WRS2 path.\n  -r, --row INTEGER      WRS2 row.\n  -c, --clouds FLOAT     Max. cloud cover percentage.\n  -s, --sensors TEXT     Comma-separated list of possible sensors.\n  -t, --tiers TEXT       Comma-separated list of possible collection tiers.\n  --slcoff               Include SLC-off LE7 scenes.\n  -o, --output PATH      Output CSV file.\n  --help                 Show this message and exit.\n```\n\nAt least three options must be provided: `--begin` and `--end` (i.e. the period of interest), and a geographic extent (`--path` and `--row`, `--latlon`, `--address` or `--geojson`). By default, **pylandsat** lists all the product IDs matching the query. The full response can be exported to a CSV file using the `--output` option. Note that is the spatial extent is provided as a GeoJSON file, only the first feature will be considered.\n\n### Examples\n\n```bash\n# If only the year is provided, date is set to January 1st\npylandsat search \\\n    --begin 1999 --end 2000 \\\n    --path 206 --row 50 \\\n    --clouds 0\n\n# Using latitude and longitude\npylandsat search \\\n    --begin 2000 --end 2010 \\\n    --latlon 50.85 4.34\n\n# Using a polygon in a GeoJSON file\npylandsat search \\\n    --begin 2000 --end 2010 \\\n    --geojson brussels.geojson\n\n# Using an address that will be geocoded\npylandsat search \\\n    --begin 2000 --end 2010 \\\n    --address \'Brussels, Belgium\'\n\n# Limit to TM and ETM sensors\npylandsat search \\\n    --begin 1990 --end 2010 \\\n    --address \'Brussels, Belgium\' \\\n    --sensors LT04,LT05,LE07\n\n# Export results into a CSV file\npylandsat search \\\n    --begin 1990 --end 2010 \\\n    --address \'Brussels, Belgium\' \\\n    --sensors LT04,LT05,LE07 \\\n    --output scenes.csv\n```\n\n```bash\n# List available sensors, i.e. possible values\n# for the `--sensors` option\npylandsat list-sensors\n\n# List available files for a given sensor\npylandsat list-available-files LT05\n```\n\n# Python API\n\n## Search the catalog\n\n``` python\nfrom datetime import datetime\n\nfrom shapely.geometry import Point\nfrom pylandsat import Catalog, Product\n\ncatalog = Catalog()\n\nbegin = datetime(2010, 1, 1)\nend = datetime(2020, 1, 1)\ngeom = Point(4.34, 50.85)\n\n# Results are returned as a list\nscenes = catalog.search(\n    begin=begin,\n    end=end,\n    geom=geom,\n    sensors=[\'LE07\', \'LC08\']\n)\n\n# Get the product ID of the first scene\nproduct_id = scenes[0].get("product_id")\n\n# Download the scene\nproduct = Product(product_id)\nproduct.download(out_dir=\'data\')\n\n# The output of catalog.search() can be converted to a DataFrame\n# for further processing. For instance:\n# Get the product ID of the scene with the lowest cloud cover\nimport pandas as pd\n\ndf = pd.DataFrame.from_dict(scenes)\ndf.set_index(["product_id"], inplace=True)\ndf = df.sort_values(by=\'cloud_cover\', ascending=True)\nproduct_id = df.index[0]\n```\n\n## Load and preprocess data\n\n``` python\nimport numpy as np\nimport rasterio\nimport matplotlib.pyplot as plt\nfrom pylandsat import Scene\n\n# Access data\nscene = Scene(\'data/LE07_L1TP_205050_19991104_20170216_01_T1\')\nprint(scene.available_bands())\nprint(scene.product_id)\nprint(scene.sensor)\nprint(scene.date)\n\n# Access MTL metadata\nprint(scene.mtl[\'IMAGE_ATTRIBUTES\'][\'CLOUD_COVER_LAND\'])\n\n# Quality band\nplt.imshow(scene.quality.read())\n\n# Access band data\nnir = scene.nir.read(1)\nred = scene.red.read(1)\nndvi = (nir + red) / (nir - red)\n\n# Access band metadata\nprint(scene.nir.bname)\nprint(scene.nir.fname)\nprint(scene.nir.profile)\nprint(scene.nir.width, scene.nir.height)\nprint(scene.nir.crs)\n\n# Use reflectance values instead of DN\nnir = scene.nir.to_reflectance()\n\n# ..or brightness temperature\ntirs = scene.tirs.to_brightness_temperature()\n\n# Save file to disk\nwith rasterio.open(\'temperature.tif\', \'w\', **scene.tirs.profile) as dst:\n    dst.write(tirs, 1)\n```\n',
    'author': 'Yann Forget',
    'author_email': 'yannforget@mailbox.org',
    'maintainer': 'Yann Forget',
    'maintainer_email': 'yannforget@mailbox.org',
    'url': 'https://github.com/yannforget/pylandsat',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
