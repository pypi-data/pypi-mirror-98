import setuptools

with open('requirements.txt') as file:
    requirements = file.readlines()

with open("README.md", "r") as file:
    long_description = file.read()

setuptools.setup(
    name="logicplum",
    version="1.0.0",
    author="LogicPlum, Inc.",
    author_email="message@logicplum.com",
    description="This client library is designed to support the LogicPlum API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LogicPlum/logicplum_v3",
    license='MIT',
    packages=setuptools.find_packages(),
    entry_points={
            'console_scripts': [
                'logicplum = logicplum.logicplum:main'
            ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        # "Operating System :: Developers/Data Scientists",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    keywords='logicplum machine-learning AI automl prediction model',
    install_requires=requirements,
    python_requires='>=3.6',
)
