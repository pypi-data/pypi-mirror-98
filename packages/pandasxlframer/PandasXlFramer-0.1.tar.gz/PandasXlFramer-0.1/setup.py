from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    readme = f.read()

setup(
    name="PandasXlFramer",
    version="0.1",
    description="PandasXlFramer",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/TengGao/pandasxlframer",
    author="Mike Gao",
    author_email="tenggao@gmail.com",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    package_data={"": ['data/*.xlsx',"data/image/*.png","data/output/*.csv","data/output/*.xlsx"]},
    zip_safe=False,
    python_requires=">=3.6",
    install_requires=["pandas", "openpyxl", "matplotlib", "numpy", "pandas-flavor"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="pandasxlframer xlsx excel pandas formatter",
    project_urls={
        "Repository": "https://github.com/TengGao/pandasxlframer",
        "Bug Reports": "https://github.com/TengGao/pandasxlframer/issues",
#         "Documentation": "https://github.com/webermarcolivier/xlsxpandasformatter/blob/master/README.md",
    }
)