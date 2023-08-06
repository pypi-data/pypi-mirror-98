import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="feedbackqa-bart",  # Replace with your own username
    version="0.1.0rc2",
    author="Xing Han Lu",
    author_email="github@xinghanlu.com",
    description="BART Model for FQA",
    # long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/xhlulu/plm",
    packages=setuptools.find_packages(exclude=["tests"]),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "torchtext==0.6.0",
        "parlai",
        "bert_reranker",
        "transformers",
        "torch",
        "numpy",
        "tqdm",
    ],
)
