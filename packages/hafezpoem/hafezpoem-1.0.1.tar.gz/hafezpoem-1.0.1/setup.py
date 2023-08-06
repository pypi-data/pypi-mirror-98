from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='hafezpoem',
    version='1.0.1',
    description="Random poem of hafez for restaurant factor and other staff",
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Radesh Farokhmanesh',
    author_email='radesh.farokhmanesh@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='hafez fal poem factor restaurant',
    packages=find_packages(),
    install_requires=['']
)