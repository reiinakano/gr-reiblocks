#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2018 Reiichiro Nakano.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import numpy as np
from gnuradio import gr
from collections import defaultdict
import operator


class sync_detector(gr.sync_block):
    """
    docstring for block sync_detector
    """
    def __init__(self, sync_length):
        gr.sync_block.__init__(self,
            name="sync_detector",
            in_sig=[np.uint8],
            out_sig=[np.uint8])
        self.sync_length = sync_length
        self.mapping = defaultdict(int)
        self.current_word = 0
        self.bits_shifted = 0
        self.bit_mask = (1 << self.sync_length) - 1
        print(format(self.bit_mask, '#02x'))

    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        for x in in0:
            self.current_word = ((self.current_word << 1) & self.bit_mask) | (x & 1)
            if self.bits_shifted >= self.sync_length - 1:
                self.mapping[self.current_word] += 1
            else:
                self.bits_shifted += 1
        out[:] = in0
        return len(output_items[0])

    def stop(self):
        values = np.fromiter(self.mapping.values(), dtype=np.longlong)
        items = np.asarray(self.mapping.items())
        self.mapping = None
        sorted_idx = np.argsort(values)
        sorted_x = items[sorted_idx]
        top_items = sorted_x[:-30:-1]
        for sync, count in top_items:
            print(format(sync, '#02x'), count)
        bottom_items = sorted_x[:30]
        for sync, count in bottom_items:
            print(format(sync, '#02x'), count)
        return True
