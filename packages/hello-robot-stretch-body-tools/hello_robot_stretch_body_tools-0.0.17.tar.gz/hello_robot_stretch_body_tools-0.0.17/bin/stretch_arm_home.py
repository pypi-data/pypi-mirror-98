#!/usr/bin/env python

import stretch_body.arm as arm
import stretch_body.hello_utils as hu
hu.print_stretch_re_use()

import argparse
parser=argparse.ArgumentParser(description='Calibrate arm position by moving to one/both hardstops')
parser.add_argument("--double", help="Home to both hardstops",action="store_true")
args=parser.parse_args()

a=arm.Arm()
a.startup()
a.home(single_stop= not args.double)
a.stop()

