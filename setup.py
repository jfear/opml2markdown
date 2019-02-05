from setuptools import setup

setup(
    name='opml2markdown',
    version='0.1',
    packages=['opml2markdown'],
    url='https://github.com/jfear/opml2markdown',
    license='MIT',
    author='Justin M Fear',
    author_email='justin.m.fear@gmail.com',
    description='A simple converter from OPML to Markdown.',
    entry_points = {
        'console_scripts': ['opml2markdown=opml2markdown.converter:main'],
    }
)
