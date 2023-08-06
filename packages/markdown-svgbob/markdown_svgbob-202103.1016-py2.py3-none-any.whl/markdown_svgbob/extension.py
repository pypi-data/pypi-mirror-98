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
import re
import copy
import json
import base64
import typing as typ
import hashlib
import logging
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from markdown.postprocessors import Postprocessor
try:
    import builtins
except ImportError:
    import __builtin__ as builtins
import markdown_svgbob.wrapper as wrapper
str = getattr(builtins, 'unicode', str)
try:
    try:
        from urllib.parse import quote
    except ImportError:
        from urlparse import quote
except ImportError:
    from urllib import quote
logger = logging.getLogger(__name__)


def make_marker_id(text):
    data = text.encode('utf-8')
    return hashlib.md5(data).hexdigest()


TagType = str


def svg2html(svg_data, tag_type='inline_svg'):
    svg_data = svg_data.replace(b'\n', b'')
    if tag_type == 'img_base64_svg':
        img_b64_data = base64.standard_b64encode(svg_data)
        img_text = img_b64_data.decode('ascii')
        return '<img class="bob" src="data:image/svg+xml;base64,{0}"/>'.format(
            img_text)
    elif tag_type == 'img_utf8_svg':
        img_text = svg_data.decode('utf-8')
        img_text = quote(img_text)
        return '<img class="bob" src="data:image/svg+xml;utf-8,{0}"/>'.format(
            img_text)
    elif tag_type == 'inline_svg':
        return svg_data.decode('utf-8')
    else:
        err_msg = "Invalid tag_type='{0}'".format(tag_type)
        raise NotImplementedError(err_msg)


def _clean_block_text(block_text):
    if block_text.startswith('```bob'):
        block_text = block_text[len('```bob'):]
    elif block_text.startswith('~~~bob'):
        block_text = block_text[len('~~~bob'):]
    if block_text.endswith('```'):
        block_text = block_text[:-len('```')]
    elif block_text.endswith('~~~'):
        block_text = block_text[:-len('~~~')]
    return block_text


def _parse_min_char_width(options):
    min_char_width = options.pop('min_char_width', '')
    try:
        return int(round(float(min_char_width)))
    except ValueError:
        logger.warning(
            'Invalid argument for min_char_width. expected integer, got: {0}'
            .format(min_char_width))
        return 0


def _add_char_padding(block_text, min_width):
    lines = block_text.splitlines()
    block_width = max(len(line) for line in lines)
    if block_width >= min_width:
        return block_text
    lpad = ' ' * ((min_width - block_width) // 2)
    new_lines = [(lpad + line).ljust(min_width) for line in lines]
    return '\n'.join(new_lines)


BG_STYLE_PATTERN = """
(
  rect\\.backdrop\\s*\\{\\s*fill:\\s*white;
| \\.bg_fill\\s*\\{\\s*fill:\\s*white;
| </style><rect fill="white"
)
"""
BG_STYLE_RE = re.compile(BG_STYLE_PATTERN.encode('ascii'), flags=re.VERBOSE)
FG_STYLE_PATTERN = """
(
  \\.fg_stroke\\s*\\{\\s*stroke:\\s*black;
| \\.fg_fill\\s*\\{\\s*fill:\\s*black;
| text\\s*{\\s*fill:\\s*black;
)
"""
FG_STYLE_RE = re.compile(FG_STYLE_PATTERN.encode('ascii'), flags=re.VERBOSE)


def _postprocess_svg(svg_data, bg_color=None, fg_color=None):
    if bg_color:
        pos = 0
        while True:
            match = BG_STYLE_RE.search(svg_data, pos)
            if match is None:
                break
            repl = match.group(0).replace(b'white', bg_color.encode('ascii'))
            begin, end = match.span()
            pos = end
            svg_data = svg_data[:begin] + repl + svg_data[end:]
    if fg_color:
        pos = 0
        while True:
            match = FG_STYLE_RE.search(svg_data, pos)
            if match is None:
                break
            repl = match.group(0).replace(b'black', fg_color.encode('ascii'))
            begin, end = match.span()
            pos = end
            svg_data = svg_data[:begin] + repl + svg_data[end:]
    return svg_data


def draw_bob(block_text, default_options=None):
    options = {}
    if default_options:
        options.update(default_options)
    block_text = _clean_block_text(block_text)
    header, rest = block_text.split('\n', 1)
    if '{' in header and '}' in header:
        options.update(json.loads(header))
        block_text = rest
    min_char_width = _parse_min_char_width(options)
    if min_char_width:
        block_text = _add_char_padding(block_text, min_char_width)
    tag_type = typ.cast(str, options.pop('tag_type', 'inline_svg'))
    bg_color = options.pop('bg_color', '')
    fg_color = options.pop('fg_color', '')
    if not isinstance(bg_color, str):
        bg_color = ''
    if not isinstance(fg_color, str):
        fg_color = ''
    svg_data = wrapper.text2svg(block_text, options)
    svg_data = _postprocess_svg(svg_data, bg_color, fg_color)
    return svg2html(svg_data, tag_type=tag_type)


DEFAULT_CONFIG = {'tag_type': ['inline_svg',
    'Format to use (inline_svg|img_utf8_svg|img_base64_svg)'], 'bg_color':
    ['white', 'Set the background color'], 'fg_color': ['black',
    'Set the foreground color'], 'min_char_width': ['',
    'Minimum width of diagram in characters']}


class SvgbobExtension(Extension):

    def __init__(self, **kwargs):
        self.config = copy.deepcopy(DEFAULT_CONFIG)
        for name, options_text in wrapper.parse_options().items():
            self.config[name] = ['', options_text]
        self.images = {}
        super(SvgbobExtension, self).__init__(**kwargs)

    def reset(self):
        self.images.clear()

    def extendMarkdown(self, md):
        preproc = SvgbobPreprocessor(md, self)
        md.preprocessors.register(preproc, name='svgbob_fenced_code_block',
            priority=50)
        postproc = SvgbobPostprocessor(md, self)
        md.postprocessors.register(postproc, name=
            'svgbob_fenced_code_block', priority=0)
        md.registerExtension(self)


BLOCK_RE = re.compile('^(```|~~~)bob')


class SvgbobPreprocessor(Preprocessor):

    def __init__(self, md, ext):
        super(SvgbobPreprocessor, self).__init__(md)
        self.ext = ext

    @property
    def default_options(self):
        options = {'tag_type': self.ext.getConfig('tag_type', 'inline_svg'),
            'min_char_width': self.ext.getConfig('min_char_width', '')}
        for name in self.ext.config.keys():
            val = self.ext.getConfig(name, '')
            if val != '':
                options[name] = val
        return options

    def _make_tag_for_block(self, block_lines):
        block_text = '\n'.join(block_lines).rstrip()
        img_tag = draw_bob(block_text, self.default_options)
        img_id = make_marker_id(img_tag)
        marker_tag = '<p id="tmp_md_svgbob{0}">svgbob{1}</p>'.format(img_id,
            img_id)
        tag_text = '<p>{0}</p>'.format(img_tag)
        self.ext.images[marker_tag] = tag_text
        return marker_tag

    def _iter_out_lines(self, lines):
        is_in_fence = False
        expected_close_fence = '```'
        block_lines = []
        for line in lines:
            if is_in_fence:
                block_lines.append(line)
                is_ending_fence = line.strip() == expected_close_fence
                if not is_ending_fence:
                    continue
                is_in_fence = False
                marker_tag = self._make_tag_for_block(block_lines)
                del block_lines[:]
                yield marker_tag
            else:
                fence_match = BLOCK_RE.match(line)
                if fence_match:
                    is_in_fence = True
                    expected_close_fence = fence_match.group(1)
                    block_lines.append(line)
                else:
                    yield line

    def run(self, lines):
        return list(self._iter_out_lines(lines))


class SvgbobPostprocessor(Postprocessor):

    def __init__(self, md, ext):
        super(SvgbobPostprocessor, self).__init__(md)
        self.ext = ext

    def run(self, text):
        for marker_tag, img in self.ext.images.items():
            if marker_tag in text:
                wrapped_marker = '<p>' + marker_tag + '</p>'
                while marker_tag in text:
                    if wrapped_marker in text:
                        text = text.replace(wrapped_marker, img)
                    else:
                        text = text.replace(marker_tag, img)
            else:
                logger.warning("SvgbobPostprocessor couldn't find: {0}".
                    format(marker_tag))
        return text
