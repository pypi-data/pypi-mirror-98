from distutils.core import setup

with open(('README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='discord-ext-check',
    packages=['discord.ext.check'],
    version='0.1',
    license='MIT',
    description='A module which implements various new decorators to check for certain conditions in your discord commands',
    long_description=long_description,
    author='multi-yt76',
    author_email='76multi@gmail.com',
    url='https://github.com/multi-yt76/discord-ext-check',
    download_url='https://github.com/multi-yt76/discord-ext-check/archive/v0.1.tar.gz',
    keywords=['discord', 'check', 'functions'],
    install_requires=[
        'discord',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
