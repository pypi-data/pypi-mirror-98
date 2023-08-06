#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ***********************************************************************************
# * Copyright 2020 Jun Zhang. All Rights Reserved.                                  *
# * Distributed under MIT license.                                                  *
# * See file LICENSE for details for copy at https://opensource.org/licenses/MIT    *
# ***********************************************************************************

import os
import subprocess
from proto2rapidjson import entry


def pipeline(name: str, cpp_relative_path: str = '../cpp'):
    parent = os.path.dirname(__file__)
    cpp_path = os.path.join(parent, cpp_relative_path)
    # Step 1: proto -> h
    proto_path = os.path.join(parent, f'proto/{name}.proto')
    header_path = os.path.join(cpp_path, 'proto.h')
    entry(proto_path, header_path, True)

    # Step 2: h -> out
    subprocess.call(['make', 'clean'], cwd=cpp_path)
    assert(subprocess.call(['make'], cwd=cpp_path) == 0)

    # Step 3: parse json
    exe_path = os.path.join(cpp_path, 'main.out')
    json_path = os.path.join(parent, f'json/{name}.json')
    assert(subprocess.call([exe_path, json_path]) == 0)

    # clean
    subprocess.call(['make', 'clean'], cwd=cpp_path)
    os.remove(header_path)

def test_type():
    pipeline('type')

def test_nest():
    pipeline('nest')

def test_array():
    pipeline('array')

def test_simple():
    pipeline('simple')

def test_more():
    pipeline('more')

def test_comment():
    pipeline('comment')

def test_string_array():
    pipeline('string_array')

def test_namespace():
    pipeline('namespace', '../cpp_namespace')

def test_syntax():
    pipeline('syntax')
