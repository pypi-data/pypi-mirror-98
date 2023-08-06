from setuptools import setup, find_packages

extras = {
    "dev": [
        "black",
        "pylint",
        "twine",
        "jupyter",
        "jupyterlab",
        "matplotlib",
    ],
    "docs": ["sphinx", "sphinx-rtd-theme"],
}

setup(
    name="uw_stempals_demos",
    version="0.1.0",
    author="John Franklin Crenshaw",
    author_email="jfc20@uw.edu",
    description="Demo simulations for UW's STEM Pals outreach program.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    url="http://github.com/jfcrenshaw/uw_stempals_demos",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["numpy", "matplotlib"],
    extras_require=extras,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
    ],
    python_requires=">=3.6.0",
)