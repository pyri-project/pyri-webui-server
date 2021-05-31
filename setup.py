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
    package_data = {
        'pyri.webui_server': ['*.html','*.js','*.svg','*.css','*.json'],
        'pyri.webui_server.webui_static': ['*.html','*.js','*.svg','*.css','*.json','*.png'],
    },
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
        'console_scripts': ['pyri-webui-server = pyri.webui_server.__main__:main'],
        'pyri.plugins.service_node_launch': ['pyri-webui-server-launch = pyri.webui_server.service_node_launch:get_service_node_launch_factory']
    }
)