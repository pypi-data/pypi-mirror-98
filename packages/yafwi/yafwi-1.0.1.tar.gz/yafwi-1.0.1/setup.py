from setuptools import find_packages, setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name='yafwi',
    packages=find_packages(),
    version='1.0.1',
    author='Alen Buhanec',
    author_email='<alen.buhanec@gmail.com>',
    license='MIT',
    description='Yet Another Fixed Width Integer (Library)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/buhanec/yafwi',
    classifiers=[
        'Topic :: Software Development :: Libraries',
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Typing :: Typed',
    ]
)
