from setuptools import setup, find_packages

setup(
    name='FPLTransfers',
    version='0.1',
    description='A package which calculates optimum transfers for Fantasy Premier League',
    author='Jack Lidgley',
    license='MIT',
    url='https://github.com/JackLidge/FPLTransfers',
    packages=find_packages(include=['FPLTransfers']),
    #packages=find_packages(include=['FPLTransfers', 'FPLTransfers.*']),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix'
    ],
    install_requires=[
        'fpl',
        'pandas',
    ]
)