import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

name = "userbot"
version = "0.0.4"
author = "Sh1vam"
author_email = None
description = "A Powerful Python-Telethon Based Library For Javes 4.0 Userbot."
license = "MIT License"
url = "https://github.com/Sh1vam/Javes-4.0"

setuptools.setup(
    name=name,
    version=version,
    author=author,
    author_email=author_email,
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=url,
    license=license,
    packages=setuptools.find_packages(),
    install_requires=[
        "telethon",
        "telegraph",
        "sqlalchemy",
        "urbandict",
        "pySmartDL",
        "cryptg",
        "python-dotenv",
        "fontTools",
        "requests",
        "Pillow",
        "validators",
        "wand",
        "colour",
        "lottie",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
