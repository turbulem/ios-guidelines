#!/usr/bin/env python

'''
The MIT License (MIT)
Copyright (c) 2015-present Badoo Trading Limited.
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

import argparse
import fnmatch
import os
import re
import stat
import subprocess
import platform

FILE_PATTERNS = ['*.m', '*.mm', '*.h']
EXCLUDE_DIRS = ['Pods', 'Vendor', 'lib']

BINARY_NAME = 'clang-format'
if platform.system() == 'Windows':
    BINARY_NAME = 'clang-format.exe'
COPYRIGHT_LINES = ['//', '// Copyright (c) ... All rights reserved.', '//']
BINARY = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'bin', BINARY_NAME))

def extract_header(lines):
    header = []
    index = 0
    if lines[0].startswith('//'):
        for line in lines:
            if not line.startswith('//'):
                break
            header.append(line)
            index += 1
    return 0, index


def format_file(lines):
    clang_format = BINARY
    chmod_x_binary(clang_format)

    command = [clang_format, '-style=file']
    p = subprocess.Popen(command, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                         shell=False)
    data = "\n".join(lines) + "\n"
    output, error = p.communicate(data)
    if not error:
        data = output
    return data

def file_walker(base_dir, patterns, exclude_dirs=[]):
    for root, dirs, filenames in os.walk(base_dir):
        for exclude in exclude_dirs:
            if exclude in dirs:
                dirs.remove(exclude)
        for pattern in patterns:
            for filename in fnmatch.filter(filenames, pattern):
                yield os.path.join(root, filename)

def get_file_paths(base_dir, patterns, exclude_dirs):
    paths = []
    for path in file_walker(base_dir, patterns, exclude_dirs):
        paths.append(path)
    return paths

def chmod_x_binary(binary):
    st = os.stat(binary)
    os.chmod(binary, st.st_mode | stat.S_IEXEC)

def split_lines(data):
    lines = re.split("[\r\n]", data)
    while lines and not lines[0]:
        del lines[0]
    while lines and not lines[-1]:
        del lines[-1]
    return lines

def process_file(path):
	print 'Processing ' + os.path.basename(path) + '...'

	with open(path) as f:
		data = f.read()

	lines = split_lines(data)

	begin, end = extract_header(lines)
	lines[begin:end] = COPYRIGHT_LINES
	data = format_file(lines)

	with open(path, 'wb') as f:
		f.write(data)

# ------------- main -------------
parser = argparse.ArgumentParser(description="""
This tool performs the following steps:
-- Converts Copyright header
-- Uses clang-format tool to re-format the sources
""", formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("--root", help="root of the repository", required=True)
args = parser.parse_args()

root_path = args.root
if None == root_path:
	root_path = os.path.dirname(os.path.realpath(__file__))

file_paths = get_file_paths(root_path, FILE_PATTERNS, EXCLUDE_DIRS)

for file_path in file_paths:
	process_file(file_path)
