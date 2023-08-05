import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python-markdown-nofollow", # Replace with your own username
    version="0.0.1",
    author="stdworkflow",
    author_email="gsyipingliu@gmail.com",
    description="a Python Markdown plugin used to add rel='external nofollow' "
                "and target='_blank' attribute to all <a> tags",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://stdworkflow.com",
    project_urls={
        "Bug Tracker": "https://github.com/stdworkflow/python_markdown_nofollow",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
)