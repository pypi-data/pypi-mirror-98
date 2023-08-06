from setuptools import setup
from biketrauma import __version__ as current_version

setup(
  name='biketrauma-AV',
  version=current_version,
  description='Visualization of a bicycle accident db',
  url='http://github.com/AmelieVernay.git',
  author='AmelieVernay',
  author_email='amelie.vernay@etu.umontpellier.fr',
  license='MIT',
  packages=['biketrauma','biketrauma.io', 'biketrauma.preprocess', 'biketrauma.vis'],
  zip_safe=False
)