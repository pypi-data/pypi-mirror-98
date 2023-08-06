import setuptools
version = {}
with open("curriculum_model/_version.py") as fp:
    exec(fp.read(), version)

with open("README.md", "r") as f:
    long_description = f.read()

# later on we use: version['__version__']
setuptools.setup(
    name='curriculum_model',
    version=version['__version__'],
    py_modules=['curriculum_model'],
    author="James Boyes",
    author_email="James.Boyes@lcm.ac.uk",
    description="Modelling HE curriculum delivery.",
    long_description=long_description,
    url="https://github.com/jehboyes/curriculum_model",
    packages=setuptools.find_packages()
)
