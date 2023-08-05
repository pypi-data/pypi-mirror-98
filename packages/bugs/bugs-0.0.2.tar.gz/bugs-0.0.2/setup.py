import setuptools

# python setup.py sdist bdist_wheel
# twine upload dist/* && rm -rf build dist *.egg-info

setuptools.setup(
    name="bugs",
    version="0.0.2",
    author="RA",
    author_email="numpde@null.net",
    keywords="python essentials",
    description="Python essential imports.",
    long_description="Python essential imports. [Info](https://github.com/numpde/bugs).",
    long_description_content_type="text/markdown",
    url="https://github.com/numpde/bugs",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['pandas', 'plox', 'inclusive', 'tcga', 'more_itertools'],

    # Required for includes in MANIFEST.in
    #include_package_data=True,

    test_suite="nose.collector",
    tests_require=["nose"],
)
