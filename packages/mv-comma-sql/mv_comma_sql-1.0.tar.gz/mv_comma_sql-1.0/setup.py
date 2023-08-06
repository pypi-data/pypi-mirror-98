from setuptools import setup, find_packages

setup(
    name='mv_comma_sql',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        hello=mv_comma_sql.cli:cli
    ''',
)