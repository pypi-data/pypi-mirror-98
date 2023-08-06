# opennsfw-standalone

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![CircleCI](https://circleci.com/gh/SectorLabs/opennsfw-standalone/tree/master.svg?style=svg&circle-token=503a819a6a1ebb58a426cca67f742b37d6e5591c)](https://circleci.com/gh/SectorLabs/opennsfw-standalone/tree/master)

A small library for intergrating [`yahoo/open_nsfw`](https://github.com/yahoo/open_nsfw) model directly into an application.

This library wraps an Tensorflow version of [`yahoo/open_nsfw`](https://github.com/yahoo/open_nsfw), provided by [`tensorflow-open_nsfw`](https://github.com/mdietrichstein/tensorflow-open_nsfw). The TensorFlow model was exported so there is no direct dependency on [`yahoo/open_nsfw`](https://github.com/yahoo/open_nsfw) or [`tensorflow-open_nsfw`](https://github.com/mdietrichstein/tensorflow-open_nsfw).

## Prerequisites
* Tensorflow 2.x
* NumPy 1.x

## Installation

    $ pip install opennsfw-standalone

## Usage
### Python

```python
import sys

from opennsfw_standalone import OpenNSFWInferenceRunner


inference_runner = OpenNSFWInferenceRunner.load()

for image_filename in sys.argv[1:]:
    with open(image_filename, "rb") as fp:
        nsfw_score = inference_runner.infer(fp.read())
        print(image_filename, nsfw_score)
```

### CLI

```shell
$ python -m opennsfw_standalone myimage.jpeg mysecondimage.jpeg
myimage.jpg 0.9997739
mysecondimage.jpg 0.9984438
```

## License
Although this repository is MIT licensed, the model itself is subject to the [BSD 2-Clause license](./opennsfw_standalone/model/LICENSE.md) Yahoo provided.
