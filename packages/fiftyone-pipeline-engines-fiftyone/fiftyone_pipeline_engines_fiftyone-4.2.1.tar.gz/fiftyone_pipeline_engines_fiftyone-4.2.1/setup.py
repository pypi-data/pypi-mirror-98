import setuptools

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'readme.md')) as f:
    long_description = f.read()

setuptools.setup(
    name="fiftyone_pipeline_engines_fiftyone",
    version="4.2.1",
    author="51Degrees",
	author_email="info@51degrees.com",
    url="http://51degrees.com/",
    description=("The 51Degrees Pipeline API is a generic web request intelligence and data processing solution with the ability to add a range of 51Degrees and/or custom plug ins (Engines). "
    "It includes a ShareUsage engine that sends usage data to 51Degrees in zipped batches."),
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.5',
    install_requires=[
          'requests',
          'cachetools'
    ],
    packages=["fiftyone_pipeline_engines_fiftyone"],
    license="EUPL-1.2",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python",
        "License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    include_package_data=True
)
