from distutils.core import setup

setup(
    name = 'pnprint',
    version = '1.0',
    package_data = {
		'': ['nprint.py'],
		},
    
    author = 'Jimy Byerley',
    author_email = 'jimy.byerley@gmail.com',
    url = 'https://github.com/jimy-byerley/nprint',
    license = "GNU LGPL v3",
    description = "format and color serialized data strings, to make them more human readable",
)
