from setuptools import setup


SHORT_DESCRIPTION = 'Preprocessor for replacing references to API methods with links to their description.'

try:
    with open('README.md', encoding='utf8') as readme:
        LONG_DESCRIPTION = readme.read()

except FileNotFoundError:
    LONG_DESCRIPTION = SHORT_DESCRIPTION


setup(
    name='foliantcontrib.apireferences',
    description=SHORT_DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    version='1.0.1',
    author='Daniil Minukhin',
    author_email='ddddsa@gmail.com',
    url='https://github.com/foliant-docs/foliantcontrib.apireferences',
    packages=['foliant.preprocessors.apireferences'],
    license='MIT',
    platforms='any',
    install_requires=[
        'foliant>=1.0.8',
        'foliantcontrib.utils.combined_options',
        'foliantcontrib.utils.header_anchors>=1.0.4',
        'lxml'
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Documentation",
        "Topic :: Utilities",
    ]
)
