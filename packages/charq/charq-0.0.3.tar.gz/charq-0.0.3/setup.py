import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="charq", 
    version="0.0.3",
    author="João Roberto",
    author_email="joaorobert0@protonmail.com",
    description="A simple package that provides methods to get characters, numbers, random words and etc.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/joaoroberto50/CharQ",
    licence='MIT',
    contributors=[
        'Joao Roberto',
        'Emidio Lopes',
        'Renato Monteiro',
    ],
    project_urls={
        "Bug Tracker": "https://github.com/joaoroberto50/CharQ/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=['charq'],
    python_requires=">=3.6",
)
