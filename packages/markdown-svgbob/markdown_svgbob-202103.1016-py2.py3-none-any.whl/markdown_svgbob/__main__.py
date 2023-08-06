#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the markdown-svgbob project
# https://gitlab.com/mbarkhau/markdown-svgbob
#
# Copyright (c) 2019-2021 Manuel Barkhau (mbarkhau@gmail.com) - MIT License
# SPDX-License-Identifier: MIT
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import os
import sys
import json
import typing as typ
import subprocess as sp
try:
    import builtins
except ImportError:
    import __builtin__ as builtins
import markdown_svgbob
str = getattr(builtins, 'unicode', str)
if os.environ.get('ENABLE_RICH_TB') == '1':
    try:
        import rich.traceback
        rich.traceback.install()
    except ImportError:
        pass
TEST_IMAGE = """
 +------+   .------.    .------.      /\\        .' `.
 |      |   |      |   (        )    /  \\     .'     `.
 +------+   '------'    '------'    '----'     `.   .'
   _______            ________                   `.'   ^ /
  /       \\      /\\   \\       \\      ---->    | ^     / /
 /         \\    /  \\   )       )     <----    | |    / v
 \\         /    \\  /  /_______/               v |
  \\_______/      \\/
  .-----------.       .   <.      .>  .          ^  \\
 (             )     (      )    (     )          \\  \\
  '-----+ ,---'       `>   '      `  <'            \\  v
        |/

"""
ExitCode = int


def _selftest():
    import markdown_svgbob.wrapper as wrp
    print('Command options:')
    print(json.dumps(wrp.parse_options(), indent=4))
    print()
    svg_data = wrp.text2svg(TEST_IMAGE)
    if not svg_data:
        return 1
    with open('test.svg', mode='wb') as fobj:
        fobj.write(svg_data)
    print("Created test image to 'test.svg'")
    return 0


def main(args=sys.argv[1:]):
    """Basic wrapper around the svgbob command.

    This is mostly just used for self testing.
    """
    if '--markdown-svgbob-selftest' in args:
        return _selftest()
    if '--version' in args or '-V' in args:
        version = markdown_svgbob.__version__
        print('markdown-svgbob version: ', version)
    binpath = markdown_svgbob.get_bin_path()
    return sp.check_call([str(binpath)] + list(args))


if __name__ == '__main__':
    sys.exit(main())
