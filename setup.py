from setuptools import setup, find_packages, find_namespace_packages

setup(
    name='pyri-webui-server',
    version='0.1.0',
    description='PyRI Teach Pendant WebUI Server',
    author='John Wason',
    author_email='wason@wasontech.com',
    url='http://pyri.tech',
    package_dir={'': 'src'},
    packages=find_namespace_packages(where='src'),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'pyri-common',
        'sanic==20.12.1',
        'importlib-resources',
        'appdirs'
    ],
    tests_require=['pytest','pytest-asyncio'],
    extras_require={
        'test': ['pytest','pytest-asyncio']
    },
    entry_points = {        
        'console_scripts': ['pyri-webui-server = pyri.webui_server.__main__:main']
    }
)