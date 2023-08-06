from setuptools import setup


with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pyx-framework',
    version='0.2.0',
    packages=['pyx', 'pyx.tags', 'pyx.utils', 'pyx.apps'],
    url='https://github.com/kor0p/PYX#PYX',
    license='GPLv3',
    author='kor0p',
    author_email='3.kor0p@gmail.com',
    description='PYX - python-based realtime frontend framework',
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.8',
)
