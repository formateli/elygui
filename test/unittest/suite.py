# This file is part of elygui project.
# The COPYRIGHT file at the top level of this repository
# contains the full copyright notices and license terms.

"ElyGui unittest suite"

import os
import sys
import unittest

DIR = os.path.dirname(os.path.realpath(__file__))
DIR = os.path.normpath(os.path.join(DIR, '..', '..', 'elygui'))
if os.path.isdir(DIR):
    sys.path.insert(0, os.path.dirname(DIR))

import model
import form


LOADER = unittest.TestLoader()

SUITE = LOADER.loadTestsFromModule(model)
SUITE.addTests(LOADER.loadTestsFromModule(form))

RUNNER = unittest.TextTestRunner(verbosity=2)
RESULT = RUNNER.run(SUITE)
