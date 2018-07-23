from setuptools import setup, find_packages

setup(
    name='spider_bot',
    version='0.1',
    author='alexlexx',
    author_email='alexlexx1@gmail.com',
    packages=find_packages(),
    license='GPL',
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'spider_bot = spider_bot:main'
        ],
    }
)
