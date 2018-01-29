#!/usr/bin/env python
# This file is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
# C Jeff Williams <jeff@wdwconsulting.net> 2018

import argparse
import hashlib
import binascii

parser = argparse.ArgumentParser(description='Encode V7 sysupgrade image')
parser.add_argument('--infile', type=str)
parser.add_argument('--outfile', type=str)
parser.add_argument('--decode', action='store_true')

args = parser.parse_args()

def write_header(file, md5):
  file.write("\x00\x00\x00\x00\x00\x00\x00\x03\x47\x45\x54\x5f\x53\x54\x41\x47")
  file.write("\x49\x4e\x47\x2f\x61\x70\x70\x73\x5f\x31\x2e\x30\x2e\x31\x30\x00")
  file.write("\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\x00\x12\x33\x30")
  file.write("\x34\x37\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x65")
  file.write("\xf0\x00\x00\x00\x00\x00")
  file.write(bytearray(md5))
  file.write("\xdd\xbf\x94\x1a\x02\x40\x00\x00\x00\x00")
  file.write("\x48\x4b\x02\x40\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00")
  file.write("\x38\x19\x02\x40\x00\x00\x00\x00\x00\x00\x07\x18\x30\x47\x16\x88")

key=0x30471688
if args.decode:
  i = open(args.infile, "rb")
  i.seek(0x80)
  o = open(args.outfile, "wb")
else:
  i = open(args.infile, "rb")
  o = open(args.outfile, "wb+")
  md5 = hashlib.md5(i.read()).digest()
  i.seek(0)
  print binascii.hexlify(bytearray(md5))
  write_header(o,md5)

try:
    byte = i.read(1)
    count=0
    while byte != b"":
        o.write(
         bytearray(
          [(ord(byte)^(key>>(count&7)))&0xff]))
        byte = i.read(1)
        count = count + 1

finally:
    o.close()
    i.close()
