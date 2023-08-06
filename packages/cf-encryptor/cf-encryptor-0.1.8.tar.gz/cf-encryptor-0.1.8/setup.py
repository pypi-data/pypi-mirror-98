from setuptools import setup, find_packages

# Extra dependecies to run tests

setup(
    name="cf-encryptor",
    version="0.1.8",
    include_package_data=True,
    author="Arka Bhattacharya, Jenny Liang, Soham Pardeshi, Leiyi Zhang",
    author_email="leiyiz@cs.washington.edu",
    packages=find_packages(),
    url="https://github.com/leiyiz/cf-encryptor",
    license="MIT License",
    description="encrypted upload of local file to gDrive",
    # long_description=open("README.rst").read(),
    install_requires=[
        "cryptography",
        "click >= 7.1.2",
        "pydrive2>=1.8.0",
        "requests>=2.21.0",
        "tqdm>=4.56.0"
    ],
    entry_points={
        'console_scripts': [
            'cfe=cfe.__main__:cli'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Natural Language :: English",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
