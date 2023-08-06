from setuptools import setup, find_packages


setup(
    name='nteu_gateway',
    version='0.1.0',
    description='NTEU gateway',
    url='https://github.com/Pangeamt/nteu_gateway_2',
    author='Laurent Bié',
    author_email='l.bie@pangeanic.com',
    license='BSD 2-clause',
    packages=find_packages(),
    install_requires=['aiohttp', 'PyYAML', 'rororo'],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.7',
    ],
)
