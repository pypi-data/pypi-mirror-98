# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stackstac']

package_data = \
{'': ['*']}

install_requires = \
['dask[array]>=2021.2.0,<2022.0.0',
 'numpy>=1.20.0,<2.0.0',
 'pyproj>=3.0.0,<4.0.0',
 'rasterio>=1.2.0,<2.0.0',
 'xarray>=0.17.0,<0.18.0']

extras_require = \
{'docs': ['Sphinx>=3.5.2,<4.0.0',
          'numpydoc>=1.1.0,<2.0.0',
          'pandoc>=1.0.2,<2.0.0',
          'insipid-sphinx-theme>=0.2.3,<0.3.0',
          'nbsphinx>=0.8.2,<0.9.0',
          'sphinx-autodoc-typehints>=1.11.1,<2.0.0']}

setup_kwargs = {
    'name': 'stackstac',
    'version': '0.1.0',
    'description': 'Load a STAC collection into xarray with dask',
    'long_description': '# StackSTAC\n\n[![Documentation Status](https://readthedocs.org/projects/stackstac/badge/?version=latest)](https://stackstac.readthedocs.io/en/latest/?badge=latest)\n\nTurn a list of [STAC](http://stacspec.org) items into a 4D [xarray](http://xarray.pydata.org/en/stable/) DataArray (dims: `time, band, y, x`), including reprojection to a common grid. The array is a lazy [Dask array](https://docs.dask.org/en/latest/array.html), so loading and processing the data in parallel—locally or [on a cluster](https://coiled.io/)—is just a `compute()` call away.\n\nFor more information and examples, please [see the documentation](https://stackstac.readthedocs.io).\n\n```python\nimport stackstac\nimport satsearch\n\nstac_items = satsearch.Search(\n    url="https://earth-search.aws.element84.com/v0",\n    intersects=dict(type="Point", coordinates=[-105.78, 35.79]),\n    collections=["sentinel-s2-l2a-cogs"],\n    datetime="2020-04-01/2020-05-01"\n).items()\n\nstack = stackstac.stack(stac_items)\nprint(stack)\n```\n```\n<xarray.DataArray \'stackstac-f350f6bfc3213d7eee2e6cb159246d88\' (time: 13, band: 17, y: 10980, x: 10980)>\ndask.array<fetch_raster_window, shape=(13, 17, 10980, 10980), dtype=float64, chunksize=(1, 1, 1024, 1024), chunktype=numpy.ndarray>\nCoordinates: (12/23)\n  * time                        (time) datetime64[ns] 2020-04-01T18:04:04 ......\n    id                          (time) <U24 \'S2B_13SDV_20200401_0_L2A\' ... \'S...\n  * band                        (band) <U8 \'overview\' \'visual\' ... \'WVP\' \'SCL\'\n  * x                           (x) float64 4e+05 4e+05 ... 5.097e+05 5.098e+05\n  * y                           (y) float64 4e+06 4e+06 ... 3.89e+06 3.89e+06\n    eo:cloud_cover              (time) float64 29.24 1.16 27.26 ... 87.33 5.41\n    ...                          ...\n    data_coverage               (time) object 33.85 100 33.9 ... 32.84 100 34.29\n    platform                    (time) <U11 \'sentinel-2b\' ... \'sentinel-2b\'\n    sentinel:sequence           <U1 \'0\'\n    proj:epsg                   int64 32613\n    sentinel:data_coverage      (time) float64 33.85 100.0 33.9 ... 100.0 34.29\n    title                       (band) object None ... \'Scene Classification ...\nAttributes:\n    spec:        RasterSpec(epsg=32613, bounds=(399960.0, 3890220.0, 509760.0...\n    crs:         epsg:32613\n    transform:   | 10.00, 0.00, 399960.00|\\n| 0.00,-10.00, 4000020.00|\\n| 0.0...\n    resolution:  10.0\n```\n\nOnce in xarray form, many operations become easy. For example, we can compute a low-cloud weekly mean-NDVI timeseries:\n\n```python\nlowcloud = stack[stack["eo:cloud_cover"] < 40]\nnir, red = lowcloud.sel(band="B08"), lowcloud.sel(band="B04")\nndvi = (nir - red) / (nir + red)\nweekly_ndvi = ndvi.resample(time="1w").mean(dim=("time", "x", "y")).rename("NDVI")\n# Call `weekly_ndvi.compute()` to process ~25GiB of raster data in parallel. Might want a dask cluster for that!\n```\n\n## Installation\n\n```\npip install stackstac\n```\n\n## Things `stackstac` does for you:\n\n* Figure out the geospatial parameters from the STAC metadata (if possible): a coordinate reference system, resolution, and bounding box.\n* Transfer the STAC metadata into [xarray coordinates](http://xarray.pydata.org/en/stable/data-structures.html#coordinates) for easy indexing, filtering, and provenance of metadata.\n* Efficiently generate a Dask graph for loading the data in parallel.\n* Mediate between Dask\'s parallelism and GDAL\'s aversion to it, allowing for fast, multi-threaded reads when possible, and at least preventing segfaults when not.\n* Mask nodata and rescale by dataset-level scales/offsets.\n\n## Limitations:\n\n* **Raster data only!** We are currently ignoring other types of assets you might find in a STAC (XML/JSON metadata, point clouds, video, etc.).\n* **Single-band raster data only!** Each band has to be a separate STAC asset—a separate `red`, `green`, and `blue` asset on each Item is great, but a single `RGB` asset containing a 3-band GeoTIFF is not supported yet.\n* [COG](https://www.cogeo.org)s work best. "Normal" GeoTIFFs that aren\'t internally tiled, or don\'t have overviews, will see much worse performance. Sidecar files (like `.msk` files) are ignored for performace. JPEG2000 will probably work, but probably be slow unless you buy kakadu. [Formats make a big difference](https://medium.com/@_VincentS_/do-you-really-want-people-using-your-data-ec94cd94dc3f).\n* BYOBlocksize. STAC doesn\'t offer any metadata about the internal tiling scheme of the data. Knowing it can make IO more efficient, but actually reading the data to figure it out is slow. So it\'s on you to set this parameter. (But if you don\'t, things should be fine for any reasonable COG.)\n* Doesn\'t make geospatial data any easier to work with in xarray. Common operations (picking bands, clipping to bounds, etc.) are tedious to type out. Real geospatial operations (shapestats on a GeoDataFrame, reprojection, etc.) aren\'t supported at all. [rioxarray](https://corteva.github.io/rioxarray/stable/readme.html) might help with some of these, but it has limited support for Dask, so be careful you don\'t kick off a huge computation accidentally.\n* I haven\'t even written tests yet! Don\'t use this in production. Or do, I guess. Up to you.\n\n## Roadmap:\n\nShort-term:\n\n- Write tests and add CI (including typechecking)\n- Support multi-band assets\n- Easier access to `s3://`-style URIs (right now, you\'ll need to pass in `gdal_env=stackstac.DEFAULT_GDAL_ENV.updated(always=dict(session=rio.session.AWSSession(...)))`)\n- Utility to guess blocksize (open a few assets)\n- Support [item assets](https://github.com/radiantearth/stac-spec/tree/master/extensions/item-assets) to provide more useful metadata with collections that use it (like S2 on AWS)\n- Rewrite dask graph generation once the [Blockwise IO API](https://github.com/dask/dask/pull/7281) settles\n\nLong term (if anyone uses this thing):\n- Support other readers ([aiocogeo](https://github.com/geospatial-jeff/aiocogeo)?) that may perform better than GDAL for specific formats\n- Interactive mapping with [xarray_leaflet](https://github.com/davidbrochart/xarray_leaflet), made performant with some Dask graph-rewriting tricks to do the initial IO at coarser resolution for lower zoom levels (otherwize zooming out could process terabytes of data)\n- Improve ergonomics of xarray for raster data (in collaboration with [rioxarray](https://corteva.github.io/rioxarray/stable/readme.html))\n- Implement core geospatial routines (warp, vectorize, vector stats, [GeoPandas](https://geopandas.org)/[spatialpandas](https://github.com/holoviz/spatialpandas) interop) in Dask\n',
    'author': 'Gabe Joseph',
    'author_email': 'gjoseph92@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://stackstac.readthedocs.io/en/latest/index.html',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
