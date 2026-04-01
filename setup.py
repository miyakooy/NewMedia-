from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="tensorslab-newmedia-kit",
    version="0.1.0",
    author="Miyako",
    author_email="miyako@tensorslab.ai",
    description="一站式AI新媒体内容生产工具包 / All-in-One AI New Media Content Production Toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/miyakooy/tensorslab-newmedia-kit",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "tnm = cli:cli",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["templates/*.html", "assets/*"],
    },
)
