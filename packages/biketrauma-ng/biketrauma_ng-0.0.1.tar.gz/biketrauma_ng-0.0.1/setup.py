from setuptools import setup
from biketrauma import __version__ as current_version

setup(
  name='biketrauma_ng',
  version=current_version,
  description='Visualization of a bicycle accident db',
  url='https://github.com/goujilinouhaila-coder/Bike_trauma.git',
  author='Goujili Nouhaila',
  author_email='goujilinouhaila@gmail.com',
  license='MIT',
  packages=['biketrauma','biketrauma.io', 'biketrauma.preprocess', 'biketrauma.vis'],
  zip_safe=False
) 
