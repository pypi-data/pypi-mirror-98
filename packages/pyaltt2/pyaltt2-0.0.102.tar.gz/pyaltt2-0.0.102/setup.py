__version__ = '0.0.102'

import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='pyaltt2',
    version=__version__,
    author='Altertech',
    author_email='div@altertech.com',
    description='Misc tools',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/alttch/pyaltt2',
    include_package_data=True,
    packages=setuptools.find_packages(),
    license='MIT',
    install_requires=[],
    classifiers=(
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries',
    ),
)
