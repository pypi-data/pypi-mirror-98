import setuptools

# read the contents of your README file
from os import path
readme = path.exists("README.md")

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

    
setuptools.setup(
    name='stellagban',
    version='0.2.11',
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
    python_requires='>=3.6'
)