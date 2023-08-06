"""Top-level package for Tensorflow Examples CLI."""

__author__ = """Andy Jackson"""
__email__ = "amjack100@gmail.com"
__version__ = "0.1.0"

import os

CHECKPOINT_DIR = f"{os.path.split(__file__ )[0]}/../checkpoints"
IMAGE_DIR = f"{os.path.split(__file__ )[0]}/../images"
MODEL_DIR = f"{os.path.split(__file__ )[0]}/../models"

if not os.path.exists(CHECKPOINT_DIR):
    os.mkdir(CHECKPOINT_DIR)

if not os.path.exists(IMAGE_DIR):
    os.mkdir(IMAGE_DIR)

if not os.path.exists(MODEL_DIR):
    os.mkdir(MODEL_DIR)

# LOGDIR = f"{os.path.split(__file__ )[0]}/logs"


from dcgan.__main__ import *