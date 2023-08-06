from setuptools import setup
setup(name='pymuxkali',
version='1.1',
description='This is a python script by which you can install Kali Nethunter (Kali Linux) in your termux application without rooted phone.',
url='https://github.com/RaynerSec/pymuxkali',
author='RC Chuah',
author_email='raynersec@gmail.com',
license='GPL',
py_modules=['pymuxkali'],
entry_points={'console_scripts': [
'pymuxkali = pymuxkali:pymuxkali',
]},
zip_safe=False)
