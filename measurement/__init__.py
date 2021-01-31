import os
import sys
# Modified to single dot, such that the path to this file, not the path
# to the parent directory, is added.
# Credit to https://stackoverflow.com/a/55795157/1327325
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                '.')))
