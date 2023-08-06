import setuptools

with open('README.md','r',encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="radari",
    version='0.0.1',
    author='rihousyou',
    author_email='1700012467@pku.edu.cn',
    description='for radar simulation',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Housyou/radari',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ]
)