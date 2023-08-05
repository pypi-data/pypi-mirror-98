from setuptools import setup, find_packages

setup(
    name="frog_ssg",
    version="0.0.5",
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
            "frog_build = __main__:build"
        ]
    },
)