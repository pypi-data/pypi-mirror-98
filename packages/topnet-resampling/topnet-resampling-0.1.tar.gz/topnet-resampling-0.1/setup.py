from setuptools import setup, find_packages

def readme():
    with open('README.rst') as f:
        return f.read()


setup(name="topnet-resampling", version="0.1", 
      description="Script to resample TopNet streamq time-series",
      long_description=readme(),
      long_description_content_type='text/x-rst',
      author="Daniel Lagrava",
      author_email="daniel.lagravasandoval@niwa.co.nz",
      url="https://github.com/daniel-lagrava-niwa/topnet-resampling",
      license="GNU",
      packages=["resample_streamq"],
      scripts=['bin/fix_streamq.sh'],
      entry_points={
        'console_scripts': [
            'resample_streamq=resample_streamq.resample_streamq:main'
        ],
      },
      install_requires=['netCDF4','xarray'],
      include_package_data=True,
      zip_safe=False
)

