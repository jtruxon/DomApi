import setuptools

with open("INSTRUCTIONS.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DomApi",
    version="0.0.1",
    author="James Truxon",
    author_email="contact@jamestruxon.com",
    description="Python tool for completion time analysis of batch pizza orders",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ohyeswedid/mlops-take-home",
    packages=setuptools.find_packages(),
    classifiers=(
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.9",
    ),
    keywords=[],
    test_suite='tests',
    install_requires=['werkzeug==0.16.1', 'flask==1.1.4', 'flask-restplus', 'jsonschema', 'gunicorn'],
)

