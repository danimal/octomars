from setuptools import setup, find_packages

setup(
    name="octomars",
    packages=find_packages(),
    version='0.1',
    description="A script to run from inside MarsEdit to post to an Octopress blog.",
    long_description="A script to run from the Bloxsom API settings in MarsEdit to post a new post to an Octopress blog. Optional git file add/commit and pushing to origin are included.",
    entry_points={'console_scripts': 
                  ['octomars=octomars:main',]},
)
