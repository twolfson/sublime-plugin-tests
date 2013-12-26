from setuptools import setup, find_packages


setup(
    name='sublime_plugin_tests',
    version='1.0.0',
    description='Testing framework for Sublime Text plugins',
    long_description=open('README.rst').read(),
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
    download_url='https://github.com/twolfson/sublime-plugin-tests/archive/master.zip',
    packages=find_packages(),
    license='UNLICENSE',
    install_requires=open('requirements.txt').readlines(),
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
