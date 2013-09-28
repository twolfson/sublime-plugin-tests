from setuptools import setup


def read_requirements(filename='requirements.txt'):
    with open(filename) as f:
        return f.readlines()


setup(
    name='sublime_plugin_tests',
    version='0.1.1',
    description='Testing framework for Sublime Text plugins',
    keywords=[
        'sublime text',
        'plugin',
        'test',
        'framework',
        'tdd'
    ],
    author='Todd Wolfson',
    author_email='todd@twolfson.com',
    url='https://github.com/twolfson/sublime-plugin-tests',
    packages=[
        'sublime_plugin_tests'
    ],
    license='UNLICENSE',
    install_requires=read_requirements(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Testing',
        'Topic :: Text Editors'
    ]
)
