import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(

    name="quicksample611",
    version="0.0.2",
    author="anis dhouieb",
    description="Quicksample test package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=["quicksample"],
    package_dir={'':'quicksample/src'},
    install_requires=[]

)
