# print('Hello World !!')
from setuptools import find_packages,setup

# print(find_packages(include=['library']))
setup(
    name='ukritlibrary', ## ใส่ชื่อ PyPi Name
    packages=find_packages(), 
    version='0.1.3', ## Version ที่ใช้ในการ Install Library
    description='My libraly From ukrit', 
    author='Ukrit Fongsomboon',
    license='MIT',
    install_requirs=[''],
    setup_requires=['pytest-runner==4.4'],
    tests_requires=['pytest==4.4.1'],
    test_suite='tests' , ## ใช้ชื่อ Floder ที่เราใช้ในการ Test
    # download_url="",
    python_requires='>=3.8',

)