from setuptools import setup, find_packages

# Publish to pypi:
#   https://packaging.python.org/guides/making-a-pypi-friendly-readme/
#     python3 -m build
#     python3 -m twine upload --repository pypi dist/*
#
# classifiers list:
#   https://pypi.org/pypi?%3Aaction=list_classifiers

with open("README.md", "r") as stream:
    longdesc=stream.read()

setup(
    name='rel-path',
    packages=find_packages(),
    version='1.0.1',
    description='Get relative path.',
    long_description=longdesc,
    long_description_content_type="text/markdown",
    url="https://github.com/jifox/relpath",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries',
        'Typing :: Typed'
    ],
    author='Josef Fuchs',
    author_email="josef.fuchs@j-fuchs.at",
    python_requires='>=3.6',
    license='MIT',
    setup_requires=['pathlib'],
    test_suite='pytest',
    tests_require=['pytest'],
)
