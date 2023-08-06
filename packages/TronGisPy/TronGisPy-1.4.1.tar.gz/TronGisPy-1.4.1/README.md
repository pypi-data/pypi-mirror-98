![TronGisPy](https://raw.githubusercontent.com/thinktron/TronGisPy/master/static/trongispy.02-01.png)

# Introduction
TronGisPy aims to automate the whole GIS process on raster data using python interface. To get start, please see [GettingStarted.ipynb](https://github.com/thinktron/TronGisPy/blob/master/GettingStarted.ipynb). The main module are listed below:

- **Raster**: This module is Main class in TronGisPy. Use `ras = tgp.read_raster('<file_path>')` to read the file as Raster object. A Raster object contains all required attribute for a gis raster file such as *.tif* or *.geotiff* file including digital number for each pixel (`ras.data`), number of rows (`ras.rows`), number of columns (`ras.cols`), number of bands (`ras.bands`), geo_transform (`ras.geo_transform`), projection (`ras.projection`), no_data_value and metadata. The Raster object can also be plot with GeoDataFrame(shapefile) on the same canvas using `ras.plot()`. Functions like `ras.reproject()`, `ras.remap()` and `ras.refine_resolution()` are useful functions.

- **CRS**: Convert the projection sys between well known text (WKT) and epsg(`tgp.epsg_to_wkt`, `tgp.wkt_to_epsg`). Convert the indexing sys tem between numpy index and coordinate system(`tgp.coords_to_npidxs`, `tgp.npidxs_to_coords`).

- **ShapeGrid**: Interaction between raster and vector data including `tgp.ShapeGrid.rasterize_layer`, `tgp.ShapeGrid.rasterize_layer_by_ref_raster`, `tgp.ShapeGrid.vectorize_layer`, `tgp.ShapeGrid.clip_raster_with_polygon` and `tgp.ShapeGrid.clip_raster_with_extent`.

- **DEMProcessor**: General dem processing functions including `tgp.DEMProcessor.dem_to_hillshade`, `tgp.DEMProcessor.dem_to_slope`, `tgp.DEMProcessor.dem_to_aspect`, `tgp.DEMProcessor.dem_to_TRI`, `tgp.DEMProcessor.dem_to_TPI` and `tgp.DEMProcessor.dem_to_roughness`.
normalizer.
- **Interpolation**: Interpolation for raster data on specific cells which are usually nan cells. Once majority or mean value in the filter (convolution) are prefered value for interpolation, `tgp.Interpolation.majority_interpolation`, `tgp.Interpolation.mean_interpolation` are written in numba to speed up the process. If Inverse Distance Weight (IDW) method is appropriate, `tgp.Interpolation.gdal_fillnodata` impolemented by GDAL can be called.

- **Normalizer**: Normalize the Image data for model training or plotting. Normalizer can be initialize from `normalizer = tgp.Normalizer()`. Function `normalizer.fit_transform()` can help to normalize the data. Function `normalizer.clip_by_percentage` can be used to clip the head and tail of the data to avoid the outlier affecting plotting.

- **SplittedImage**: Split raster images for machine learning model training. Use `splitted_image = tgp.SplittedImage(raster, box_size, step_size=step_size)` to initialize SplittedImage object. SplittedImage object have `n_steps_h`, `n_steps_w`, `padded_rows`, `padded_cols`, `shape`, `n_splitted_images`, `padded_image` attributes. Function `splitted_image.apply()` can be used to process all splitted images using the funtion. Function `splitted_image.get_geo_attribute()` helps to get the vector of all splitted images and return GeoDataFrame object. When the prediction on each image is done, `splitted_image.write_splitted_images()` can be called to combine the prediction results on each splitted images to have the same size as original raster image.

- **TypeCast**: Mapping the data type betyween gdal and numpy, and convert the gdal data type from integer to readable string. Because gdal use integer to represent defferent data types, `tgp.get_gdaldtype_name()` helps to convert the integer to its data type name in string. Also, once converting the data type between numpy and gdal is required, `tgp.gdaldtype_to_npdtype` and `tgp.npdtype_to_gdaldtype` can help.

- **io**: Create, read and update the raster from the raster file. Use `tgp.read_raster` to read raster file as Raster object. Functions `tgp.get_raster_info` and `tgp.get_raster_extent` can be used when you don't want to read all digital value of the raster into the memory. Function `tgp.update_raster_info` can used to update the infomation of the raster file such as projection and geo_transform. Finally, if you want to get the testing file, `tgp.get_testing_fp` can help.

<!-- 6. AeroTriangulation: Do the aero-triangulation calculation.
10. GisIO: Some file-based gis functions. -->

# Getting Started
To get start, please see [GettingStarted.ipynb](https://github.com/thinktron/TronGisPy/blob/master/GettingStarted.ipynb).

# Install
## Windows
1. Install preinstalls from pre-build wheel package
    - [GDAL==3.0.4](https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal)
    - [Fiona==1.8.13](https://www.lfd.uci.edu/~gohlke/pythonlibs/#fiona)
    - [Shapely==1.6.4.post2](https://www.lfd.uci.edu/~gohlke/pythonlibs/#shapely)
    - [geopandas==0.7.0](https://www.lfd.uci.edu/~gohlke/pythonlibs/#geopandas)
    - [Rtree==0.9.4](https://www.lfd.uci.edu/~gohlke/pythonlibs/#rtree)
    - [opencv_python==4.1.2](https://www.lfd.uci.edu/~gohlke/pythonlibs/#opencv)

2. Install TronGisPy
```
pip install TronGisPy
```

## Linux
1. Build GDAL==3.0.4 by yourself
2. Build opencv==4.1.2 by yourself
3. install other preinstalls from public pypi server
```
pip install GDAL==3.0.4 Fiona==1.8.13 Shapely==1.6.4.post2 geopandas==0.7.0 Rtree==0.9.4
```
4. Install TronGisPy
```
pip install TronGisPy
```
<!-- 
## Taiwan DataCube
1. uninstall gdal
```
pip uninstall gdal
```

2. install requirements for gdal
```
sudo apt-get install python3-dev build-essential libssl-dev libffi-dev libxml2-dev libxslt1-dev zlib1g-dev
```


3. add gdal path
```
echo "export CPLUS_INCLUDE_PATH=/usr/include/gdal" >> ~/.profile
echo "export C_INCLUDE_PATH=/usr/include/gdal" >> ~/.profile
source ~/.profile
```

4. install gdal
```
pip install GDAL==3.0.4
``` -->

# For Developer
## Build
```bash
python setup.py sdist bdist_wheel
```

# Reference
1. [Logo](https://github.com/thinktron/TronGisPy/blob/master/static/trongispy.01-01.png)

## Document Generation
0. [Installaion](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/install.html)
```
pip install sphinx
pip install sphinx-rtd-theme
pip install numpydoc
```

1. generatate index.rst (https://docs.readthedocs.io/en/stable/intro/getting-started-with-sphinx.html)
```
mkdir docs
cd docs
sphinx-quickstart
```

2. modify docs/source/conf.py (https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html)
```
vim source/conf.py
```
```
base_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(base_dir, '..', '..')))

html_theme = "classic"
extensions = ['sphinx.ext.napoleon']
exclude_patterns = ['setup.py', 'req_generator.py', 'test.py']
```

3. generate TronGisPy rst
```
cd ..
python clean_docs_source.py
sphinx-apidoc --force --separate --module-first -o docs\source .
```

4. generate html
```
cd docs
make clean
make html
```

# For Thinktron Worker
## Install on Windows
1. Install preinstall thinktron pypi server
```
pip install -U --index-url http://192.168.0.128:28181/simple --trusted-host 192.168.0.128 GDAL==3.0.4 Fiona==1.8.13 Shapely==1.6.4.post2 geopandas==0.7.0 Rtree==0.9.4 opencv_python==4.1.2
```

2. Install TronGisPy from thinktron pypi server (Windows)
```
pip install -U --extra-index-url http://192.168.0.128:28181/simple --trusted-host 192.168.0.128 TronGisPy
```
