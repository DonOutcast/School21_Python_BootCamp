from distutils.core import setup, Extension
from Cython.Build import cythonize

extensions = [Extension('matrix', ["multiply.pyx"])]
setup(name="matrix", ext_modules=cythonize("multiply.pyx"))
