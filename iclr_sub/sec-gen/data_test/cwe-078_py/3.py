#!/usr/bin/env python3
#
# Copyright 2023 Google LLC
#
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import subprocess

import flask

app = flask.Flask(__name__)

@app.route('/analyze/resource/<file_path>')
def bazelisk_build_file(file_path: str) -> str:
    target = file_path
    res = subprocess.run("bazelisk build " + target, check=True, shell=True)
    return res.stdout.decode()
