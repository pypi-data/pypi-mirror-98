import setuptools

with open("README.md", "r") as file:
    description = file.read()

setuptools.setup(
    name="calcymath",
    packages=setuptools.find_packages(),
    version="0.0.5",
    license='MIT', 
    author="Hari Prasad",
    author_email="hariprasadgurunathan10@gmail.com",
    description="A simple math library",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/hariprasad1003/calcy-math",
    download_url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',   
    install_requires=[]
)