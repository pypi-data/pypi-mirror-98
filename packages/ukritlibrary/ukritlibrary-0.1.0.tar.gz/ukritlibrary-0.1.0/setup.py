# print('Hello World !!')
from setuptools import find_packages,setup

setup(
    name='ukritlibrary',
    packages=find_packages(include=['libraly']),
    version='0.1.0',
    description='My libraly From ukrit',
    author='ME',
    license='MIT',
    install_requirs=['numpy'],
    setup_requires=['pytest-runner==4.4'],
    tests_requires=['pytest==4.4.1'],
    test_suite='tests' , ## ใช้ชื่อ Floder ที่เราใช้ในการ Test
    download_url=""
)