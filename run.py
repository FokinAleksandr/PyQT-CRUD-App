#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import os
from app import main


if __name__ == '__main__':
    os.chdir((os.path.dirname(os.path.realpath(__file__))))
    sys.exit(main.run())