from setuptools import setup, find_packages
from codecs import open
from os import path


here = path.abspath(path.dirname(__file__))
setup(
    name='nylib',
    version='1.0',
    description='ny python lib utils',
    long_description=str(open(path.join(here, "ReadMe.md")).read()),
    # The project's main homepage.
    # url='nylib - Overview',
    # Author details
    author='navyran',
    author_email='navyran@gmail.com',
    # Choose your license
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: System :: Logging',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    py_modules=["cmd_util"],
    install_requires=['requests', 'records'],
    include_package_data=True,
    package_data={'': ['*.yaml']},
    # packages=["."]
    packages=find_packages()
    # packages=find_packages(where='.', exclude=(), include=('*.py',))
)
