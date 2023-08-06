from setuptools import setup, find_packages

VERSION = '1.6' 
DESCRIPTION = 'Package to standerdize and beautify matplotlib and seaborn graphs'
LONG_DESCRIPTION = 'Sets default for fonts, axes, color schemes, ticks, legend across matplotlib'

# Setting up
setup(
        name="pyintellify", 
        version=VERSION,
        author="Ansh Bordia",
        author_email="<ansh.bordial@intellify.com.au>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        py_modules = ["pyintellify"],
        package_dir={'': 'src'},
        install_requires=['matplotlib'],
        keywords=['python', 'matplotlib', 'beautiful graphs', 'seaborn'],
        classifiers= [
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Operating System :: OS Independent",
        ]
)

print(find_packages())