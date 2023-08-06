from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='CKUIWeditor',
    version='0.0.1b1',
    description='ChokChaisak',
    long_description=readme(),
    url='https://github.com/ChokChaisak/ChokChaisak',
    author='ChokChaisak',
    author_email='ChokChaisak@gmail.com',
    license='ChokChaisak',
    install_requires=[
        'matplotlib',
        'numpy',
        'weditor',
        'uiautomator2',
    ],
    keywords='CKUIWeditor',
    packages=['CKUIWeditor'],
    package_dir={
    'CKUIWeditor': 'src/CKUIWeditor',
    },
    package_data={
    'CKUIWeditor': [
            '*',
            '*/*',
            '*/*/*',
            '*/*/*/*',
            '*/*/*/*/*',
            '*/*/*/*/*/*',
            '*/*/*/*/*/*/*'
            ],
    },
)