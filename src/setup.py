import setuptools

setuptools.setup(
	name='wom_connector',
	version='0.1',
	author='WOM Platform',
	author_email='info@wom.social',
	license='MIT',
	description='Connection library to the WOM Platform.',
	long_description=open('README.txt').read(),
	url="https://github.com/WOM-Platform/Python-Connector",
	project_urls={
		'Homepage': 'https://wom.social/',
		'Source': 'https://github.com/WOM-Platform/Python-Connector'
	},
	packages=setuptools.find_packages(),
)
