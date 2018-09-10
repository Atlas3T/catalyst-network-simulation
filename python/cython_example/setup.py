from setuptools import setup
from setuptools.extension import Extension
from Cython.Build import cythonize

examples_extension=[
        Extension(
            'pyexamples',
            sources=['pyexamples.pyx'],
             libraries=["examples"],
            library_dirs=["lib"],
            include_dirs=["lib"],
        ),
    ]

setup(
    name="pyexamples",
    ext_modules=cythonize(examples_extension)
    
)
