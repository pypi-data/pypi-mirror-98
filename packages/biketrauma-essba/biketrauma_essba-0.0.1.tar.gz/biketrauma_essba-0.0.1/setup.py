from setuptools import setup
from biketrauma import __version__ as current_version

setup(
  name='biketrauma_essba',
  version=current_version,
  description='Visualization of a bicycle accident db',
  url='https://github.com/ESSBAIOmar/packaging_tutorial',
  author='ESSBAI Omar',
  author_email='omar.es-sbai@etu.umontpellier.fr',
  license='BIOSTAT',
  packages=['biketrauma','biketrauma.io', 'biketrauma.preprocess', 'biketrauma.vis'],
  zip_safe=False
)