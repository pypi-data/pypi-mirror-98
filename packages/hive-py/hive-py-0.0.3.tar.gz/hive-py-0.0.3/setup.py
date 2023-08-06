import setuptools


with open('README.md') as f:
    README = f.read()

setuptools.setup(
    author="James McMahon",
    author_email="james1345@googlemail.com",
    name='hive-py',
    license="MIT",
    description='A library to make multi-process and multi-machine programs easy to write',
    version='v0.0.3',
    long_description=README,
    url='https://bitbucket.org/james1345/hive/',
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    install_requires=['paho-mqtt', 'jsonpickle'],
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
    ],
)