from setuptools import setup, find_packages


def read_requirements():
    with open('requirements.txt', 'r') as req:
        content = req.read()
        requirements = content.split('\n')

    return requirements

if __name__ == '__main__':    
    setup(
        name="core",
        version="0.1",
        packages=find_packages(),
        install_requires=read_requirements()
    )