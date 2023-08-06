# # print('Hello World !!')
# from setuptools import find_packages,setup

# # print(find_packages(include=['library']))
# setup(
#     name='ukritlibrary', ## ใส่ชื่อ PyPi Name
#     packages=find_packages(include=['library']), 
#     version='0.1.3', ## Version ที่ใช้ในการ Install Library
#     description='My libraly From ukrit', 
#     author='Ukrit Fongsomboon',
#     license='MIT',
#     install_requirs=[''],
#     setup_requires=['pytest-runner==4.4'],
#     tests_requires=['pytest==4.4.1'],
#     test_suite='tests' , ## ใช้ชื่อ Floder ที่เราใช้ในการ Test
#     # download_url="",
#     python_requires='>=3.8',

# )

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="ukrit",
    version="0.0.2",
    author="username",
    author_email="ukrit.fb@gmail.com",
    description="Some description",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/username/repo.git",
    license="MIT",
    packages=find_packages(),
    package_dir={'client': 'Client'},
    install_requires=[
        'requests'
    ],
    tests_require=[
        'coverage', 'wheel', 'pytest', 'requests_mock'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 3 - Alpha"
    ]
)