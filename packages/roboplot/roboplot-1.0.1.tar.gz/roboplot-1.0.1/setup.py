try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

packages = find_packages()

setup(
    name='roboplot',
    description='Library of plotting functions for everything robotics',
    version='1.0.1',
    author="Varun Agrawal et. al.",
    author_email="varunagrawal@gatech.edu",
    license='Simplified BSD license',
    keywords="robotics plotting prototyping visualization",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/borglab/roboplot",
    python_requires=">=3.6",
    # https://pypi.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Education',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
    ],
    packages=packages,
    platforms="any",
    install_requires=open("requirements.txt").readlines(),
)
