from setuptools import find_packages, setup


setup(
    name='polyswarmd-config',
    version='0.1.1',
    description='Config module the PolySwarm Daemon',
    author='PolySwarm Developers',
    author_email='info@polyswarm.io',
    url='https://github.com/polyswarm/polyswarmd-config',
    license='MIT',
    install_requires=[
        'dataclasses==0.7; python_version=="3.6"',
        'python-consul==1.1.0',
        'redis>=3.5.3',
    ],
    include_package_data=True,
    packages=find_packages('src'),
    package_dir={'': 'src/'},
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ]
)
