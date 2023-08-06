import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hookshothq",
    version="0.0.1",
    author="Hookshot",
    author_email="support@hookshothq.com",
    description="Python bindings for the Hookshot API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.hookshothq.com",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    # project_urls={
    #     "Bug Tracker": "https://github.com/hookshothq/hookshothq-python/issues",
    #     "Documentation": "https://docs.hookshothq.com/api/python",
    #     "Source Code": "https://github.com/hookshothq/hookshothq-python",
    # },
    install_requires=[
      'requests',
    ]
)
