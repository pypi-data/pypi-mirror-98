import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="api_of_things", # Replace with your own username
    version="0.0.11",
    author_email="otto.wagner@ama-inc.com",
    description="A python client that can interface with an API of things IOT server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/isConic/api_of_things_python",

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
