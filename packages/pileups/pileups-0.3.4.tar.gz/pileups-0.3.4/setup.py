import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pileups',
    version='0.3.4',
    author='Anthony Aylward',
    author_email='aaylward@eng.ucsd.edu',
    description='Manipulate files of the pileup format from SAMtools',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/anthony-aylward/pileups.git',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    install_requires=['funcgenom'],
    entry_points={
        'console_scripts': [
            'pileups-merge=pileups.pileups_merge:main',
            'pileups-count=pileups.pileups_count:main',
            'pileups-dist=pileups.pileups_dist:main',
            'pileups-intersect=pileups.pileups_intersect:main'
        ]
    }
)
