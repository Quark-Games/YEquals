"""
py2app build script for MyApplication

Usage:
    python setup.py py2app
"""
from setuptools import setup
setup(
    app=["func_sim.py"],
    options={
        'py2app': {'argv_emulation': True, 'packages': ['pygame', 'pyperclip']}
    },

    data_files=['debug', 'assets', 'modkeys.py'],
    setup_requires=["py2app"],
)
