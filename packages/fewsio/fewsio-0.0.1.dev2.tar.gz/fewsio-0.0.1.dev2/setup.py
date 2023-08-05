from setuptools import setup

setup(
    name = 'fewsio',
    version = '0.0.1.dev2',
    author = 'Jack Vreeken',
    description = "Typo fallback for FEWS-IO",
    long_description = '''Use `fews-io <https://pypi.python.org/pypi/fews-io/>`_ instead''',
    url = 'https://pypi.python.org/pypi/fews-io/',
    license = 'LGPLv3',
    platforms = ['all'],
    install_requires = ["fews-io"],
    zip_safe=False
)
