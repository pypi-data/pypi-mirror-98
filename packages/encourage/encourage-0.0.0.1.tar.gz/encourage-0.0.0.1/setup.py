import os
from setuptools import setup,find_packages


here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.MD'), encoding='utf-8').read()

setup(
    name = "encourage",
    version = "0.0.0.1",

    author = "lindaye",
    author_email = "454784911@qq.com",
    url = "https://github.com/stellaye/encourage",
    license = "MIT",

    description = "A command line tool speak beautiful words to you to encourage you ",
    long_description = README,
    install_requires=[
     "pyttsx3"
    ],
    platforms = 'any',
    zip_safe = True,
    include_package_data = True,
    entry_points = {'console_scripts': [
            'e = encourage.main:main',
        ]}
)