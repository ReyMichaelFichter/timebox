from setuptools import setup

setup(
    name='timebox',
    version='0.1',
    py_modules=['timebox'],
    install_requires=[
        'Click'
    ],
    entry_points='''
        [console_scripts]
        timebox=timebox:start_timebox
    '''
)