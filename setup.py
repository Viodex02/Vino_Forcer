from setuptools import setup

setup(
    name='Vine_Forcer',
    version='1.0',
    py_modules=['Vino_Forcer'],  # اسم الملف بدون .py
    install_requires=[
        'httpx',
    ],
    entry_points={
        'console_scripts': [
            'vine_forcer=Vino_Forcer:cli',  # دالة cli في الملف Vino_Forcer.py
        ],
    },
    python_requires='>=3.11',
    description='Vine Forcer v1.0 - Hunter Mode 🕷️ - Async multi-tool for status, subdomains, brute-force, listener',
    author='Viodex',
)
