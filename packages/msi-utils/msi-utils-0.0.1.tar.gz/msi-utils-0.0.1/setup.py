from setuptools import setup, find_packages

def parse_requirements(requirement_file):
    with open(requirement_file) as f:
        return f.readlines()

setup(
    name='msi-utils',
    version='0.0.1',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='A Python package to assist with analzying and extracting data from a Windows Installer MSI',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    install_requires=parse_requirements('./requirements.txt'),
    keywords=['carcass'],
    url='https://github.com/MSAdministrator/msiutils',
    author='MSAdministrator',
    author_email='rickardja@live.com',
    python_requires='>=2.6, !=3.0.*, !=3.1.*, !=3.2.*, <4',
    entry_points={
          'console_scripts': [
              'msi-utils = msiutils.__main__:main'
          ]
    },
    include_package_data=True,
    package_data={
        'msitools': [
            'msitools/0.97/bin/msibuild',
            'msitools/0.97/bin/msidiff',
            'msitools/0.97/bin/msidump',
            'msitools/0.97/bin/msiextract',
            'msitools/0.97/bin/msiinfo'
        ]
    }
)