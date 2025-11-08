from setuptools import setup, find_packages

setup(
    name='kvass',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[],
    author='CooperElektrik',
    description='A simple JSON Canvas interpreter for the Katzen visual novel engine.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='http://github.com/CooperElektrik/Kvass',
    classifiers=[],
    python_requires='>=3.9',
    license="MIT"
)
