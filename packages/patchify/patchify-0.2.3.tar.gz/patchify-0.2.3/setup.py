# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['patchify', 'patchify.tests']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1,<2']

setup_kwargs = {
    'name': 'patchify',
    'version': '0.2.3',
    'description': 'A library that helps you split image into small, overlappable patches, and merge patches back into the original image.',
    'long_description': '# patchify\n\npatchfy can split images into small overlappable patches by given patch cell size, and merge patches into original image.\n\nThis library provides two functions: `patchify`, `unpatchify`.\n\n## Installation\n```\npip install patchify\n```\n\n## Usage\n\n### Split image to patches\n\n`patchify(image_to_patch, patch_shape, step=1)`\n\n2D image:\n```python\n#This will split the image into small images of shape [3,3]\npatches = patchify(image, (3, 3), step=1)\n```\n\n3D image:\n```python\n#This will split the image into small images of shape [3,3,3]\npatches = patchify(image, (3, 3, 3), step=1)\n```\n\n### Merge patches into original image\n\n`unpatchify(patches_to_merge, merged_image_size)`\n\n```python\nreconstructed_image = unpatchify(patches, image.shape)\n```\nThis will reconstruct the original image that was patchified in previous code.\n\n**Caveat**: in order for `unpatchify` to work, you need to create patchies with equal step size. e.g. if the original image has width 3 and the patch has width 2, you cannot really create equal step size patches with step size 2. (first patch [elem0, elem1] and second patch [elem2, elem3], which is out of bound).\n\nThe required condition for unpatchify to success is to have (width - patch_width) mod step_size = 0.\n\n### Full running examples\n\n#### 2D image patchify and merge\n\n```python\nimport numpy as np\nfrom patchify import patchify, unpatchify\n\nimage = np.array([[1,2,3,4], [5,6,7,8], [9,10,11,12]])\n\npatches = patchify(image, (2,2), step=1) # split image into 2*3 small 2*2 patches.\n\nassert patches.shape == (2, 3, 2, 2)\nreconstructed_image = unpatchify(patches, image.shape)\n\nassert (reconstructed_image == image).all()\n```\n\n#### 3D image patchify and merge\n\n```python\nimport numpy as np\nfrom patchify import patchify, unpatchify\n\nimage = np.random.rand(512,512,3)\n\npatches = patchify(image, (2,2,3), step=1) # patch shape [2,2,3]\nprint(patches.shape) # (511, 511, 1, 2, 2, 3). Total patches created: 511x511x1\n\nassert patches.shape == (511, 511, 1, 2, 2, 3)\nreconstructed_image = unpatchify(patches, image.shape)\nprint(reconstructed_image.shape) # (512, 512, 3)\n\nassert (reconstructed_image == image).all()\n```\n',
    'author': 'Weiyuan Wu',
    'author_email': 'doomsplayer@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dovahcrow/patchify.py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
