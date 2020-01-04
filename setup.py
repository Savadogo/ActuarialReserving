import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ActuarialReserving",
    version="1.0.1",
    author="Savadogo Ilassa",
    author_email="savadogoilassa@gmail.com",
    description="Implementation of Actuarial reserving methods",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Savadogo/ActuarialReserving",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)