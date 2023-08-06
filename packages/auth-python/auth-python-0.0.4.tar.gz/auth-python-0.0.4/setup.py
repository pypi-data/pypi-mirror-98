import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="auth-python",  # Replace with your own username
    version="0.0.4",
    author="xingxiaohe",
    author_email="",
    description="权限校验python封装包",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    install_requires=[
        'grpcio_tools==1.17.1',
        'google-api-python-client==2.0.2'
    ],


    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
