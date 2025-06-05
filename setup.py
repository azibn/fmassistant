from setuptools import setup, find_packages

setup(
    name="fm-assistant",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'anthropic',
        'python-dotenv',
        'tqdm',
    ],
    entry_points={
        'console_scripts': [
            'fmassistant=fmassistant.cli:main',
        ],
    },
)
