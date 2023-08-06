import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="europlexo",
    version="2.0.1",
    author="Moris Doratiotto",
    author_email="moris.doratiotto@gmail.com",
    description="A python module to download tv series from magic",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mortafix/EuroPlexo",
    packages=setuptools.find_packages(),
    install_requires=[
        "requests",
        "bs4",
        "halo",
        "pymortafix",
        "halo",
        "argparse",
        "python-telegram-bot",
        "cloudscraper",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.8",
    keywords=["serie", "tv", "download"],
    package_data={
        "europlexo": [
            "linkfinder.py",
            "manage.py",
            "seriesfinder.py",
            "config.json",
            "dispatcher/deltabit.py",
            "dispatcher/turbovid.py",
        ]
    },
    entry_points={"console_scripts": ["europlexo=europlexo.europlexo:main"]},
)
