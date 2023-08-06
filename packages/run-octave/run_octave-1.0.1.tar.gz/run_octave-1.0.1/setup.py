from setuptools import setup, find_packages

with open('README.md', 'r') as readmefile:
    readme = readmefile.read()

setup(
    name='run_octave',
    version='1.0.1',
    author='David Ferreira',
    author_email='ferreirad08@gmail.com',
    description='A package to run Octave functions and scripts in the Python interpreter!',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/ferreirad08/run-octave',
    packages=find_packages(),
    install_requires=[
        'scipy>=1.6.0',
    ],
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8.6',
)
