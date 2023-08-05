from setuptools import setup, find_packages

setup(
    name="frog-ssg",
    version="0.0.1",
    packages=find_packages(),
    author="Leo Peltola",
    author_email="leopeltola@gmail.com",
    description="A Python static site generator",
    classifiers= [
        "Programming Language :: Python :: 3",
    ],
    
    keywords=['python', 'static site generator', 'ssg'],
    entry_points={
        "console_scripts": [
            "frog_build = frog.__main__:build"
        ]
    },
)