#!/bin/bash
echo Making tmp_admon
mkdir tmp_admon
sphinx-quickstart <<EOF
tmp_admon
n
_
Testing admons
H. P. Langtangen
1.0
1.0
en
.rst
index
y
y
n
n
n
n
n
y
n
y
y
y

EOF