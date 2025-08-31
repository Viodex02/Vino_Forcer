from setuptools import setup

setup(
    name='Vine_Forcer',
    version='1.0',
    py_modules=['Vino_Forcer'],         
    install_requires=[
        'httpx',
    ],
    entry_points={
        'console_scripts': [
            'vine_forcer=Vino_Forcer:main', 
        ],
    },
)