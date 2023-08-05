# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ohsome', 'ohsome.test']

package_data = \
{'': ['*'], 'ohsome': ['ohsome_log/*'], 'ohsome.test': ['data/*']}

install_requires = \
['geopandas>=0.9.0,<0.10.0',
 'multidict>=5.1.0,<6.0.0',
 'pip>=21.0.1',
 'pyproj>=3.0.0,<4.0.0',
 'requests>=2.25.1,<3.0.0']

extras_require = \
{':python_version < "3.7"': ['pandas<0.25.3'],
 ':python_version >= "3.0" and python_version < "3.7"': ['numpy<1.20.1'],
 ':python_version >= "3.7" and python_version < "4"': ['pandas>=0.25.3',
                                                       'numpy>=1.20.1']}

setup_kwargs = {
    'name': 'ohsome',
    'version': '0.1.0b0',
    'description': 'A Python client for the ohsome API',
    'long_description': '# ohsome-py: A Python client for the ohsome API\n\n[![status: experimental](https://github.com/GIScience/badges/raw/master/status/experimental.svg)](https://github.com/GIScience/badges#experimental)\n\nThe *ohsome-py* package helps you extract and analyse OpenStreetMap history data using the [ohsome API](https://docs.ohsome.org/ohsome-api/v1/) and Python. It handles queries to the [ohsome API](https://docs.ohsome.org/ohsome-api/v1/) and converts its responses to [Pandas](https://pandas.pydata.org/) and [GeoPandas](https://geopandas.org/) data frames to facilitate easy data handling and analysis.\n\nThe ohsome API provides various endpoints for [data aggregation](https://api.ohsome.org/v1/swagger-ui.html?urls.primaryName=Data%20Aggregation), [data extraction](https://api.ohsome.org/v1/swagger-ui.html?urls.primaryName=dataExtraction) and [contributions](https://api.ohsome.org/v1/swagger-ui.html?urls.primaryName=Contributions). Take a look at the [documentation of the ohsome API](https://docs.ohsome.org/ohsome-api/stable) to learn more about the endpoints and query parameters or go through the [Tutorial](https://github.com/GIScience/ohsome-py/blob/master/notebooks/Tutorial.ipynb) to get started.\n\n\n## Installation\n\nThe easiest way to install *ohsome-py* is using pip:\n\n```\n$ pip install ohsome\n```\n\nTo install the latest *ohsome-py* version from GitHub:\n\n```\n$ pip install git+https://github.com/giscience/ohsome-py\n```\n\nIf you want to run the Juypter Notebook [Tutorial](https://github.com/GIScience/ohsome-py/blob/master/notebooks/Tutorial.ipynb) you also need to install `jupyter` and `matplotlib`:\n\n```\n$ pip install jupyter matplotlib\n```\n\n## Usage\n\nAll queries are handled by an `OhsomeClient` object, which also provides information about the current ohsome API instance, e.g. `start_timestamp` and `end_timestamp` indicate the earliest and the latest possible dates for a query.\n\n``` python\nfrom ohsome import OhsomeClient\nclient = OhsomeClient()\nclient.start_timestamp # --> \'2007-10-08T00:00:00Z\'\nclient.end_timestamp # --> \'2021-01-23T03:00Z\'\n```\n\n### 1. Data Aggregation\n\n**Example:** The Number of OSM ways tagged as _landuse=farmland_ using the [/elements/count](https://api.ohsome.org/v1/swagger-ui.html?urls.primaryName=Data%20Aggregation#/Count/count_1) endpoint:\n\n``` python\nresponse = client.elements.count.post(bboxes=[8.625,49.3711,8.7334,49.4397],\n\t\t\t\t      time="2014-01-01",\n\t\t\t\t      filter="landuse=farmland and type:way")\n```\n\nThe single components of the endpoint URL are appended as method calls to the `OhsomeClient` object. Use automatic code completion to find valid endpoints. Alternatively, you can define the endpoint as argument in the `.post()` method.\n\n``` python\nresponse = client.post(endpoint="elements/count",\n\t\t       bboxes=[8.625,49.3711,8.7334,49.4397],\n\t\t       time="2020-01-01",\n\t\t       filter="landuse=farmland and type:way")\n```\n\nResponses from the data aggregation endpoints can be converted to a `pandas.DataFrame` object using the `OhsomeResponse.as_dataframe()` method.\n\n```\nresponse_df = response.as_dataframe()\n```\n\n### 2. Data Extraction\n\n**Example:** OSM ways tagged as _landuse=farmland_ including their geometry and tags using the [/elements/geometry](https://api.ohsome.org/v1/swagger-ui.html?urls.primaryName=Data%20Extraction#/Data%20Extraction/elementsGeometry_1) endpoint:\n\n``` python\nclient = OhsomeClient()\nresponse = client.elements.geometry.post(bboxes=[8.625,49.3711,8.7334,49.4397],\n\t\t\t\t\t time="2020-01-01",\n\t\t\t\t\t filter="landuse=farmland and type:way",\n\t\t\t\t\t properties="tags")\nresponse_gdf = response.as_geodataframe()\n```\n\nResponses from the data extraction endpoint can be converted to a `geopandas.GeoDataFrame`  using the `OhsomeResponse.as_geodataframe()` method, since the data contains geometries.\n\n### Query Parameters\n\nAll query parameters are described in the [ohsome API documentation](https://docs.ohsome.org/ohsome-api/stable) and can be passed as `string` objects to the `post()` method. Other Python data types are accepted as well. \n\n#### Boundary\n\nThe [boundary](https://docs.ohsome.org/ohsome-api/stable/boundaries.html) of the query can be defined using the `bpolys`, `bboxes` and `bcircles` parameters. The coordinates have to be given in WGS 84 (EPSG:4326).\n\n##### bpolys\n\nThe `bpolys` parameter can be passed as a `geopandas.GeoDataFrame` containing the polygon features.\n\n``` python\nbpolys = gpd.read_file("./data/polygons.geojson")\nclient.elements.count.groupByBoundary.post(bpolys=bpolys, filter="amenity=restaurant")\n```\n\n##### bboxes\n\nThe `bboxes` parameter contains the coordinates of one or several bounding boxes.\n\n``` python\nbboxes = [8.7137,49.4096,8.717,49.4119] # one bounding box\nbboxes = [[8.7137,49.4096,8.717,49.4119], [8.7137,49.4096,8.717,49.4119]]\nbboxes = {"A": [8.67066, 49.41423, 8.68177, 49.4204],\n\t  "B": [8.67066, 49.41423, 8.68177, 49.4204]}\n```\n\n##### bcircles\n\nThe `bcircles` parameter contains one or several circles defined through the coordinates of the centroids and the radius in meters.\n\n```python\nbcircles = [8.7137,49.4096, 100]\nbcircles = [[8.7137,49.4096, 100], [8.7137,49.4096, 300]]\nbcircles = {"Circle1": [8.695, 49.41, 200],\n\t    "Circle2": [8.696, 49.41, 200]}\n```\n\n#### Time\n\nThe [time](https://docs.ohsome.org/ohsome-api/stable/time.html) parameter must be ISO-8601 conform can be passed in several ways\n\n```python\ntime = \'2018-01-01/2018-03-01/P1M\'\ntime = [\'2018-01-01\', \'2018-02-01\', \'2018-03-01\']\ntime = datetime.datetime(year=2018, month=3, day=1)\ntime = pandas.date_range("2018-01-01", periods=3, freq="M")\n```\n\n## Contribution Guidelines\n\nIf you want to contribute to this project, please fork the repository or create a new branch containing your changes.\n\n**Install the pre-commit hooks** in our local git repo before commiting to ensure homogenous code style.\n\n```\n$ pre-commit install\n```\n\n**Run the tests** inside the repo using `pytest` (and `poetry` if you like) to make sure everything works.\n\n```\n$ poetry run pytest\n```\n\nRunning the tests in a docker container containing an ohsome API instance is faster, but not mandatory. To set up and start such a docker container run the following command before running the tests.\n\n```\n$ docker run -t -i --name ohsome-api -p 8080:8080 julianpsotta/ohsome-api:latest\n```\n\n\nCreate a **pull request to the development** branch once it is ready to be merged.\n\n## References\n\nThe design of this package was inspired by the blog post [Using Python to Implement a Fluent Interface to Any REST API](https://sendgrid.com/blog/using-python-to-implement-a-fluent-interface-to-any-rest-api/) by Elmer Thomas.\n',
    'author': 'Christina Ludwig',
    'author_email': 'christina.ludwig@uni-heidelberg.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
