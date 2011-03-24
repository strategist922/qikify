#!/usr/bin/python
'''
Copyright (c) 2011 Nathan Kupp, Yale University.

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
'''

import sys, os, csv
from numpy import *
from helpers.general import *

class Specs:
	specs = {}
	names = []
	
	# Read in specs from `filename` and create {specname: [lsl,usl]} dictionary.
	def __init__(self, filename):
	    fileh 	  	= open(filename, 'rU')
	    specReader 	= csv.reader(fileh)
	    self.names 	= specReader.next()
	    LSL   		= specReader.next()
	    USL   		= specReader.next()

	    for i, limit in enumerate(zip(LSL, USL)):
			# Use this lambda function because float() fails on empty/non-existent spec limit.
	    	lsl, usl = map(lambda x: float(x) if x else float('nan'), limit)
	        self.specs[self.names[i]] = array([lsl, usl])
	    fileh.close()

	# Compare data to lsl, usl and return +1/-1 label vector
	def compareToSpecs(self, data, lsl, usl):
		result = ones(size(data))
		if isfinite(lsl):
			result = logical_and(result, data >= lsl)
		if isfinite(usl):
			result = logical_and(result, data <= usl)
		return bool2symmetric(result)

	def __getitem__(self, key):
		return self.specs[key]
    
	
    # =============== Partitioned Sampling Methods =============== 
	# Takes specification boundary and generates two boundaries to define 'critical' device set.
	def genCriticalRegion(self, delta = 1.0):
		self.inner = self.outer = {}
		for (k, v) in self.specs.items():
			lsl, usl = v
			if (isnan(lsl) and isnan(usl)):
				continue
			elif isnan(lsl):
				self.inner[k] = array([-inf, 5.0/6.0 * usl])
				self.outer[k] = array([-inf, 7.0/6.0 * usl])
			elif isnan(usl):
				self.inner[k] = array([5.0/6.0 * lsl, inf])
				self.outer[k] = array([7.0/6.0 * lsl, inf])
			else:
				smean = mean([lsl, usl])
				self.inner[k] = array([smean + 5.0/6.0 * lsl, smean + 5.0/6.0 * usl])
				self.outer[k] = array([smean + 7.0/6.0 * lsl, smean + 7.0/6.0 * usl])
