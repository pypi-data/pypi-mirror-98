#!/usr/bin/env python

__copyright__ = "Copyright (C) 2020 Andreas Kloeckner"

__license__ = """
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
"""

import sys

import numpy as np
import pyopencl as cl  # noqa
import pyopencl.array as cl_array  # noqa
import pyopencl.cltypes as cltypes  # noqa
import pyopencl.tools as cl_tools  # noqa
from pyopencl.tools import (  # noqa
        pytest_generate_tests_for_pyopencl as pytest_generate_tests)
import pytest  # noqa

import pytato as pt


def test_namespace_copy():
    namespace = pt.Namespace()
    x = pt.Placeholder(namespace, "x", (5,), np.int)
    namespace.assign("xsquared", x * x)

    namespace_copy = namespace.copy()
    assert len(namespace_copy) == 2
    assert isinstance(namespace_copy["x"], pt.Placeholder)
    assert isinstance(namespace_copy["xsquared"], pt.IndexLambda)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        exec(sys.argv[1])
    else:
        from pytest import main
        main([__file__])

# vim: filetype=pyopencl:fdm=marker
