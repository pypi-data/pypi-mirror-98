from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(name='cadCAD_tools',
      version='0.0.1.0',
      description="Tools for improved experience with cadCAD",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/cadCAD-org/cadCAD-tools',
      author='Danilo Lessa Bernardineli',
      author_email='danilo@block.science, danilo.lessa@gmail.com',
      packages=find_packages(),
      install_requires=['cadCAD']
)
