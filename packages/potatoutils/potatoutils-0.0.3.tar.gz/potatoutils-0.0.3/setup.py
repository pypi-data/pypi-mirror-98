from setuptools import find_packages, setup
setup(
    name='potatoutils',
    packages=find_packages(),
    version='0.0.3',
    description='My first Python library',
    author='Dorijan Cirkveni',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)