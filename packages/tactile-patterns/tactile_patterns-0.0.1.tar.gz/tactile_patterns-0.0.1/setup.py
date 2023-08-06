import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tactile_patterns",
    version="0.0.1",
    author="Mateusz Konieczny",
    author_email="matkoniecz@gmail.com",
    description="Generates patterns recognisable by touch, for use in laser-cut materials (for people who are blind or with a poor eyesight, in dark)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/matkoniecz/tactile_patterns",
    packages=setuptools.find_packages(),
    install_requires = [
        'jsbeautifier>=1.13.5, <2.0',
        'pyproj>=2.5.0, <3.0',
        'numpy>=1.19.5, <2.0',
        'pillow>=8.1.2, <9.0',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

