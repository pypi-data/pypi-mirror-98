import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-gsheets-roymo",
    version="0.0.9",
    author="Bobby Steinbach",
    author_email="developers@meanpug.com",
    description="Fork of django-gsheets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Rommel-Montgomery/django-gsheets",
    keywords='roymo',
    packages=setuptools.find_packages(include=['gsheets', 'gsheets.*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['google-api-python-client', 'google-auth', 'google-auth-httplib2', 'google-auth-oauthlib'],
    python_requires='>=3',
)
