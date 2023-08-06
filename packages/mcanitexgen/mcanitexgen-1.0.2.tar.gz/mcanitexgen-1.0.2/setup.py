# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mcanitexgen']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.1.2,<9.0.0', 'numpy>=1.20.1,<2.0.0', 'typer>=0.3.2,<0.4.0']

setup_kwargs = {
    'name': 'mcanitexgen',
    'version': '1.0.2',
    'description': 'An animation generator for Minecraft .mcmeta files',
    'long_description': '![](https://img.shields.io/github/license/orangeutan/mcanitexgen)\n![](https://img.shields.io/badge/python-3.8|3.9-blue)\n[![](https://img.shields.io/pypi/v/mcanitexgen)](https://pypi.org/project/mcanitexgen/)\n![](./coverage.svg)\n![](https://img.shields.io/badge/mypy-checked-green)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n![](https://img.shields.io/badge/pre--commit-enabled-green)\n![](https://github.com/orangeutan/mcanitexgen/workflows/test/badge.svg)\n\n# Minecraft animated texture generator\nMcanitexgen is a generator for ".mcmeta" files that Minecraft uses to animate textures.<br>\n\n## The full power of Python\nMcanitexgen allows you to write texture animations in Python instead of json. Using a programming language allows you to create much more complex animations, like this dog that has 3 textures that are synchronised with each other.\n\n<img src="https://raw.githubusercontent.com/OrangeUtan/mcanitexgen/master/examples/dog/dog.gif" width="400" style="image-rendering: pixelated; image-rendering: -moz-crisp-edges; image-rendering: crisp-edges;"/>\n\n## Install\n`pip install mcanitexgen`\n\n## Usage\n- `python -m mcanitexgen generate <animation_file> [out_dir]` generates .mcmeta files for all animations in an animation file\n- `python -m mcanitexgen gif <animation_file> [out_dir]` creates gifs for all animations in an animation file\n\n# Example\nWe are going to create this animation.<br>\n<img src="https://raw.githubusercontent.com/OrangeUtan/mcanitexgen/master/examples/steve/steve.gif" width="100" style="image-rendering: pixelated; image-rendering: -moz-crisp-edges; image-rendering: crisp-edges;"/>\n\n\nFirst we have to create the different states of the animation.\nI created a simple "steve.png" file:<br>\n<img src="https://raw.githubusercontent.com/OrangeUtan/mcanitexgen/master/examples/steve/steve.png" width="100" style="image-rendering: pixelated; image-rendering: -moz-crisp-edges; image-rendering: crisp-edges;"/>\n\nTop to Bottom: Looking normal, blinking, wink with right eye, wink with left eye.<br>\nNow we can create the animation file "steve.animation.py" that uses these states to create an animation:<br>\n```python\nfrom mcanitexgen import animation, TextureAnimation, State, Sequence\n\n@animation("steve.png")\nclass Steve(TextureAnimation):\n  NORMAL = State(0)  # Look normal\n  BLINK = State(1)\n  WINK_RIGHT = State(2)  # Wink with right eye\n  WINK_LEFT = State(3)  # Wink with left eye\n\n  # Look normal and blink shortly\n  look_and_blink = Sequence(NORMAL(duration=60), BLINK(duration=2))\n\n  # The main Sequence used to create the animation\n  main = Sequence(\n    3 * look_and_blink,  # Play "look_and_blink" Sequence 3 times\n    NORMAL(duration=60),\n    WINK_LEFT(duration=30),\n    look_and_blink,\n    NORMAL(duration=60),\n    WINK_RIGHT(duration=30),\n  )\n```\n\nNow run `python -m mcanitexgen steve.animation.py` and Mcanitexgen will create a "steve.png.mcmeta" file:\n```json\n{\n  "animation": {\n      "interpolate": false,\n      "frametime": 1,\n      "frames": [\n        {"index": 0, "time": 60},\n        {"index": 1, "time": 2},\n        {"index": 0, "time": 60},\n        {"index": 1, "time": 2},\n        {"index": 0, "time": 60},\n        {"index": 1, "time": 2},\n        {"index": 0, "time": 60},\n        {"index": 3, "time": 30},\n        {"index": 0, "time": 60},\n        {"index": 1, "time": 2},\n        {"index": 0, "time": 60},\n        {"index": 2, "time": 30}\n      ]\n  }\n}\n```\n\nMore complex examples can be found in the [here](https://github.com/OrangeUtan/mcanitexgen/tree/master/examples)\n',
    'author': 'Oran9eUtan',
    'author_email': 'oran9eutan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/OrangeUtan/mcanitexgen',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
