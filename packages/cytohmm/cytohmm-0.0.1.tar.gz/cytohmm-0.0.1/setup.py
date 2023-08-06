#from distutils.core import setup
from setuptools import setup, Extension
#from distutils.extension import Extension
from Cython.Build import cythonize

import numpy

numpy_inc = numpy.get_include()

extensions = [
	Extension("cytohmm.markov_chain",
			["src/markov_chain.pyx"],
		include_dirs = [numpy_inc],
		),
	Extension("cytohmm.likelihood",
			["src/likelihood.pyx"],
		include_dirs = [numpy_inc],
		),
	Extension("cytohmm.sequence_segmenter",
			["src/sequence_segmenter.py"],
		),
	]

with open('README.md','r') as mdfile:
	long_desc = mdfile.read()


setup(
	name = "cytohmm",
	version='0.0.1',
	ext_modules = cythonize(extensions),
	description='Cytogenetics hidden Markov model',
	long_description=long_desc,
	long_description_content_type='text/markdown',
	url='https://github.com/harry-zuzan/CytoHMM',
	author='Harry Zuzan',
	author_email='harry.zuzan@gmail.com',
	license='MIT',
#	packages=['src',],
#	package_dir={'','src'},
	zip_safe=False,
)


# for a template that uses Cython this is incrementally modelled after
# https://github.com/FedericoStra/cython-package-example/blob/master/setup.py

