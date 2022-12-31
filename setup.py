from setuptools import setup, find_packages, find_namespace_packages

setup(
    package_dir={'': 'src'},
    packages=find_namespace_packages(where='src'),
    include_package_data=True,
    package_data = {
        'pyri.webui_server': ['*.html','*.js','*.svg','*.css','*.json'],
        'pyri.webui_server.webui_static': ['*.html','*.js','*.svg','*.css','*.json','*.png'],
    },
    zip_safe=False
)