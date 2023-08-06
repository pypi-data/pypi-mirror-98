import setuptools
with open(r'C:\Users\Ant\Desktop\module\README.md', 'r', encoding='utf-8') as fh:
	long_description = fh.read()

setuptools.setup(
	name='brawlapi-py',
	version='1.0',
	author='RomaDev',
	author_email='',
	description='Simple python wrapper for the Brawl Stars API!',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/Roma4ka-RedBad/brawlapi',
	packages=['brawlapi'],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)