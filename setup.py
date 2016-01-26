from setuptools import setup

setup(
	name='gemseek-search-engine',
	version='2.1.5',
	py_modules=['gemseek'],
	include_package_data = True,
	install_requires = ['click'],
	entry_points = {'console_scripts': [
			'gemseek=gemseek:cli',]
	}
)


