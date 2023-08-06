import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tensorflow-modules",
    version="0.0.8",
    install_requires=[
        "tensorflow==2.4.1",
    ],
    # entry_points={},
    author="OtsukaKentaro",
    author_email="otsuka.kenchan@gmail.com",
    description="tensorflow layers, models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/otsuka-kentaro/tensorflow-modules",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
