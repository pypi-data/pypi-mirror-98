from setuptools import setup, find_packages


def version():
    with open('VERSION') as f:
        return f.read().strip()


def readme():
    with open('README.md') as f:
        return f.read()


def requirements():
    with open('requirements.txt') as f:
        return f.read().split('\n')


setup(
    name='uncertainty-framework',
    license='MIT license',
    version=version(),
    author='Mirko Mälicke',
    author_email='mirko.maelicke@kit.edu',
    description='Framework for propagating uncertainties through V-FOR-WaTer',
    long_description=readme(),
    long_description_content_type='text/markdown',
    install_requires=requirements(),
    packages=find_packages()
)