from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='cryptostats',
    version='0.0.3',
    description='A simple api wrapper for the nomics api to get crypto stats',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Niklas Schellong',
    author_email='nik.schellong.04@gmx.de',
    license='MIT',
    classifiers=classifiers,
    keywords='crypto',
    packages=find_packages(),
    install_requires=['requests']
)