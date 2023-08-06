# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pikuli',
 'pikuli.geom',
 'pikuli.hwnd',
 'pikuli.input',
 'pikuli.input.linux_evdev',
 'pikuli.input.linux_gtk3',
 'pikuli.input.linux_x11',
 'pikuli.input.windows',
 'pikuli.uia',
 'pikuli.uia.adapter',
 'pikuli.uia.adapter.dotnet',
 'pikuli.uia.adapter.win_native',
 'pikuli.uia.control_wrappers']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=6.2.1,<7.0.0', 'mss', 'numpy>=1.17,<2.0', 'psutil>=5.6.7,<6.0.0']

extras_require = \
{':sys_platform == "linux"': ['pythonnet>=2.5.2,<3.0.0', 'evdev', 'xlib'],
 ':sys_platform == "win32"': ['comtypes>=1.1.7,<2.0.0', 'pywin32>=214']}

setup_kwargs = {
    'name': 'pikuli',
    'version': '0.0.2',
    'description': 'Desktop GUI application tests automation tool.',
    'long_description': '# What is Pikuli?\n\nPikuli is a tool initially inspired by [Sikuli Project](http://www.sikuli.org). Currently Pikuli helps to automate GUI scenarios (aka tests) in Windows and Linux.\n\nPikuli can:\n* Look for UI components by means of:\n    * Image patterns;\n    * UIA API in [Windows](https://docs.microsoft.com/en-us/dotnet/framework/ui-automation/ui-automation-overview) and [Mono Linux](https://github.com/mono/uia2atk) applications.\n* Emulate user acivity:\n    * Keyboard;\n    * Mouse\n',
    'author': 'AxxonSoft',
    'author_email': 'support@axxonsoft.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/itvgroup/pikuli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
