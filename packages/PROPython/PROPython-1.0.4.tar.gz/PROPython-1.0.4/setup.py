import setuptools
with open(r'C:\Users\Данил\Desktop\MyPackages\README.md', 'r', encoding='utf-8') as fh:
	long_description = fh.read()

setuptools.setup(
	name='PROPython',
	version='1.0.4',
	author='PROPython',
	author_email='arseniizaripov@yandex.ru',
	description='We are updated this package and there are a lot of cool stuff',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/Game2D/PROPython',
	packages=['PROPython'],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)