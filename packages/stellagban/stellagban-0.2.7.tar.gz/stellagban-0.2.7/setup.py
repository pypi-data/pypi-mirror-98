import setuptools
from stellagban import __version__

# read the contents of your README file
from os import path
readme = path.exists("README.md")
if readme:
    this_directory = path.abspath(path.dirname(__file__))
    with open(path.join(this_directory, 'README.md')) as f:
        long_description = f.read()

setuptools.setup(
    name='stellagban',
    version=__version__,
    description='StellaGban API Python Wrapper',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
    author='Anil Chauhan',
    author_email='anilchauhanxda@gmail.com',
    url='https://github.com/SpookyGang/StellaGban-py',
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Typing :: Typed'
    ],
    install_requires=[
        'requests'
    ],
    python_requires='>=3.6'
)