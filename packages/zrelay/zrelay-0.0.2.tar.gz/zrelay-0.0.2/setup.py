from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: POSIX',
    'Operating System :: MacOS :: MacOS X',
    'Environment :: Console',
    'Programming Language :: Python',
]

setup(
    name="zrelay",
    version="0.0.2",
    author="Muzammil Patel",
    author_email="zamilpatel329@gmail.com",
    description="Driver to control Pi-zero Zrelay board HAT",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=find_packages(),
    classifiers=CLASSIFIERS,
    py_modules=["Zrelay"],
    package_dir={'':'zrelay'},
    # project_urls={
    # 'Documentation': 'https://packaging.python.org/tutorials/distributing-packages/',
    # 'Funding': 'https://donate.pypi.org',
    # 'Say Thanks!': 'http://saythanks.io/to/example',
    # 'Source': 'https://github.com/pypa/sampleproject/',
    # 'Tracker': 'https://github.com/pypa/sampleproject/issues',
    # },
    install_requires=['smbus2'],
    python_requires='>=3',
    keywords=['raspberry', 'pi', 'i2c'],
)
