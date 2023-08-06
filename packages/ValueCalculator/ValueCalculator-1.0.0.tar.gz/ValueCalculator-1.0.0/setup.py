import setuptools

with open("README.md", "r", encoding="UTF-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ValueCalculator",
    version="1.0.0",
    author="LJY",
    author_email="ljy123ljy123@dingtalk.com",
    description="Used to calculate the rise and fall of stocks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/V-Calculator/ValueCalculator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    extras_require={"ValueCalculator": ["python"]},
)