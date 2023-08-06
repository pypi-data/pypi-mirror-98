from setuptools import setup, find_packages

classifiers = [
    'Intended Audience :: Developers',
    'Intended Audience :: Education',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='MilkyWay',
    version='1.0',
    description='2D Robot trajectory generation',
    author='Hali Lev Ari',
    author_email='LevAri.Hali@gmail.com',
    license='MIT license',
    classifiers=classifiers,
    packages=find_packages(),
    keywords=['robotics', 'trajectory', 'path', 'spline'],
    install_requires=['numpy', 'matplotlib'],
)
