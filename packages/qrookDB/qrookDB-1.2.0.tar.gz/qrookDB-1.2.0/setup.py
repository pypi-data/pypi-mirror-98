import setuptools

setuptools.setup(
    name="qrookDB",
    version="1.2.0",
    author="Kurush",
    author_email="ze17@ya.ru",
    description="tiny ORM for SQL-databases",
    long_description_content_type="text/markdown",
    url="https://gitlab.com/qrook/db",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
