
from setuptools import setup, find_packages


version = '2.1'
url = 'https://github.com/pmaigutyak/mp-assets'

with open('requirements.txt') as f:
    requires = f.read().splitlines()

setup(
    name='django-mp-assets',
    version=version,
    description='Django assets app',
    author='Paul Maigutyak',
    author_email='pmaigutyak@gmail.com',
    url=url,
    download_url='{}/archive/{}.tar.gz'.format(url, version),
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    install_requires=requires
)
