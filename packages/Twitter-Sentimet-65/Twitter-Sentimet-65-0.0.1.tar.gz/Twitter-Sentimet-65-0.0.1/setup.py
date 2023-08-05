import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Twitter-Sentimet-65", # Replace with your own username
    version="0.0.1",
    author="Dipashree Patil",
    author_email="dipashree.patil@cumminscollege.in",
    description="First Iteration of sentiment analysis on 6005 tweets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dipashreepatil/Twitter-Sentiment-65/tree/1.0",
#     project_urls={
#         "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
#     },
    classifiers=[
        "Programming Language :: Python :: 3",
#         "License :: OSI Approved :: GPL",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)
