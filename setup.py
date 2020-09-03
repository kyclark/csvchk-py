import setuptools
import csvchk

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='csvchk',
    version=csvchk.VERSION,
    author='Ken Youens-Clark',
    author_email='kyclark@gmail.com',
    description='Vertical view of delimited text records',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/kyclark/csvchk',
    packages='.',
    entry_points={
        'console_scripts': [
            'csvchk=csvchk:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
