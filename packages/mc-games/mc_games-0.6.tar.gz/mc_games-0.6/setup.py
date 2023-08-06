import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mc_games",
    version="0.6",
    author="xuetianyin",
    author_email="zuiwo9@outlook.com",
    description="aircraft_campaign",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=['mc_pgzrun>=0.9'],
    entry_points={
        'console_scripts': [
            'mc_games=mc_games:main'
        ],
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)