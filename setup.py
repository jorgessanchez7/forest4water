from setuptools import setup, find_namespace_packages
from tethys_apps.app_installation import find_resource_files

# -- Apps Definition -- #
app_package = 'forest4water'
release_package = 'tethysapp-' + app_package

# -- Python Dependencies -- #
dependencies = []

# -- Get Resource File -- #
resource_files = find_resource_files('tethysapp/' + app_package + '/templates', 'tethysapp/' + app_package)
resource_files += find_resource_files('tethysapp/' + app_package + '/public', 'tethysapp/' + app_package)
resource_files += find_resource_files('tethysapp/' + app_package + '/workspaces', 'tethysapp/' + app_package)


setup(
    name=release_package,
    version='0.0.1',
    description='This apps compares the time series for Mean, Max, and Min Monthly Discharge and Monthly Forest Cover in Colombia',
    long_description='',
    keywords='',
    author='Ivan Gonzalez-Garzon, Juan Diego Giraldo-Osorio, Jorge Luis Sanchez-Lozano',
    author_email='ivan.gonzalez@nau.edu, j.giraldoo@javeriana.edu.co, jsanch3z@byu.edu',
    url='',
    license='',
    packages=find_namespace_packages(),
    package_data={'': resource_files},
    include_package_data=True,
    zip_safe=False,
    install_requires=dependencies,
)