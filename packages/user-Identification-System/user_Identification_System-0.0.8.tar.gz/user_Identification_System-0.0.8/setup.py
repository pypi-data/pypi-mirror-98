import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="user_Identification_System",
    version="0.0.8",
    author="Ayaan Imran",
    author_email="miskiacuberayaan2509@gmail.com",
    description="A tool to help you build a signup and login system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ayaan-Imran/User-Indentifier-System",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)