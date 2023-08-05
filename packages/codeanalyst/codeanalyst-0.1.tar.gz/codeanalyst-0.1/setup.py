import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="codeanalyst", # Replace with your own username
    version="v0.01",
    author="ProgrammingError",
    author_email="error@notavailable.live",
    description="Nothing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ProgrammingError/codetester",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)
