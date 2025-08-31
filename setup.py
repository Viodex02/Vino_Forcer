from setuptools import setup, find_packages

setup(
    name='Vine_Forcer',
    version='1.0',
    packages=find_packages(),   # يستخدم جميع الباكيجات في المجلد
    install_requires=[
        'httpx',
    ],
    entry_points={
        'console_scripts': [
            'vine_forcer=Vino_Forcer:cli',  # دالة cli في Vino_Forcer.py
        ],
    },
    python_requires='>=3.11',
    description='Vine Forcer v1.0 - Hunter Mode 🕷️ - Async multi-tool for status, subdomains, brute-force, listener',
    author='Viodex',
)
