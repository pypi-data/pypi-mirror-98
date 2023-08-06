from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='makeprimetanakiin',
    version='0.0.1',
    description='A simple prime number identifier',
    Long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Tanay Reddy',
    author_email='tanakiins@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='prime',
    packages=find_packages(),
    install_requires=['']
)