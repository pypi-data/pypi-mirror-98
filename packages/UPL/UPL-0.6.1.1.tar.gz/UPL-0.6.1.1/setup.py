from setuptools import setup

setup(
	name='UPL',
	version='0.6.1.1',
	description='Universal Python Library',
	url='https://github.com/RyanD524/UPL',
	author='Ryan Draskovics',
	author_email='crossroadsact@gmail.com',
	license='MIT License',
	packages=['UPL'],
	requirements = [
		'pipwin',
		'cryptocode',
		'requests',
		'ast',
		'pyautogui',
		'pyttsx3',
		'pillow',
		'win10toast',
		'pydub',
		'playsound'
	],
	classifiers=[
		'Development Status :: 6 - Mature',
		'License :: Freeware',
		'Intended Audience :: Developers',
		'Natural Language :: English',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.8',
		'Programming Language :: Python :: 3.9'
		],
)
