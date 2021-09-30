from setuptools import setup
from pygo import __version__

if __name__ == '__main__':
    with open('README.md', 'r', encoding='utf8') as f:
        long_description = f.read()

    with open('requirements.txt', 'r') as f:
        requirements = f.read().split('\n')

    setup(
        name='pygo',
        version=__version__,
        license='MIT',
        description='Python like code interpreter to Go code.',
        long_description=long_description,
        long_description_content_type='text/markdown',
        author='Fernando Pérez',
        author_email='fernaperg@gmail.com',
        url='https://github.com/fernaper/pygo',
        download_url='https://github.com/fernaper/pygo/archive/refs/tags/v0.0.1.tar.gz',
        packages=[
            'pygo', 'pygo.general',
        ],
        install_requires=requirements,
    )
