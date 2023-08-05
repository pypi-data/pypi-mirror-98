import setuptools

with open("README.md", "r", encoding="utf-8") as fd:
    long_description = fd.read()
setuptools.setup(
    name = "pyepoet",
    version = "0.1.2",
    description="电子诗人Python版",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Time Studio",
    author_email="sjgzszg@163.com",
    packages = ["pyepoet"],
)
