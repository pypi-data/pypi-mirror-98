import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

requirements = ['requests']

setuptools.setup(name='nextapm',
      version='1.0.1',
      description='Monitor vercel serverless python api',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://nextapm.dev',
      author='Chan Anan',
      author_email='chan@nextapm.dev',
      license='MIT',
      zip_safe=False,
      packages=setuptools.find_packages(),
      python_requires='>=3.6',
      install_requires=requirements)
