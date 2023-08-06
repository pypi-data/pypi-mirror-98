from setuptools import setup, find_packages

name="nxp_ls"
setup(
    name=name,
    version="1.0.0",
    author="Larry Shen",
    author_email="larry.shen@nxp.com",
    license="MIT",

    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
    ],
    entry_points={
        'console_scripts': [
            'lava_docker_slave = nxp_ls:main',
        ]
    },
    data_files=[('/'+name, ['lava_docker_slave'])],
)
