from setuptools import setup, find_packages

setup(
    name='my_project',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask>=2.3.0',
        'Flask-SQLAlchemy>=3.0.0',
        'PyMySQL>=1.1.0',
        'PyYAML>=6.0',
        'cryptography>=41.0.0',
    ],
)
