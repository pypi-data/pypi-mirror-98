from setuptools import setup,find_packages
setup(
    name='backboard',
    version='1.0.1',
    description='Background sounds for your keyboard typing',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/donno2048/BS',
    packages=find_packages(),
    license='MIT',
    author='Elisha Hollander',
    classifiers=['Programming Language :: Python :: 3'],
    install_requires=['pygame==1.9.6','keyboard','numpy','scipy']
)
