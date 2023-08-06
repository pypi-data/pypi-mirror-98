from distutils.core import setup
setup(
  name = 'CatenaryCable',
  packages = ['CatenaryCable'],
  version = '0.2',
  description = 'personal package',
  author = 'phisan',
  author_email = 'Phisan.Chula@gmail.com',
  install_requires=['fiona', 'shapely', 'gdal', 'geopandas' , 'pandas', 'numpy', 'scikit-learn', 'matplotlib'],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)
