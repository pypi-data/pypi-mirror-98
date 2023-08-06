import setuptools
with open(r'C:\Users\PC-TV\Desktop\Progress Script\readme.md', 'r', encoding='utf-8') as fh:
	long_description = fh.read()

setuptools.setup(
	name='ProgressScript',
	version='1.0',
	author='IonE',
	author_email='ivanaperginsky@gmail.com',
	description='Solid Progress Bar Script For Python ',
	long_description=long_description,
	long_description_content_type='text/markdown',
	packages=['ProgressScript'],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)