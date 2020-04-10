from setuptools import find_packages, setup

setup(
    name='noplop',
    version='0.0.0',
    author='Paul Baecher',
    description='Lint code against in-place mutation',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/pb-/noplop',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    entry_points={
        'console_scripts': [
            'noplop = noplop.main:run',
        ],
    },
)
