import setuptools

setuptools.setup(
    name='stellagban',
    version='0.2.0',
    description='StellaGban API Wrapper',
    long_description="Stella-Gban is a Telegram Gban API that ban spammers to protects people from spammers",
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