from setuptools import setup

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

with open("README.txt", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='hydradb',
    version='2.2',
    packages=['hydra'],
    url='https://github.com/rhmtazad/hydraDB',
    license='MIT License',
    classifiers=classifiers,
    author='Rahmat Azad',
    author_email='rhmtazad@gmail.com',
    description='Manage SQLite/Python operations much faster and easier using this API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['']
)
