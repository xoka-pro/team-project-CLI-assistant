from setuptools import setup, find_namespace_packages

with open("README.md", "r") as fh:
    README = fh.read()

setup(name='felis_assistant',
      version='0.2.4',
      description='Personal assistant bot',
      long_description=README,
      long_description_content_type="text/markdown",
      url='https://github.com/xoka-pro/goit-python-core-project',
      author='GOIT_7_TEAM',
      author_email='n.sherstianykh@gmail.com',
      license='MIT',
      packages=find_namespace_packages(),
      install_requires=['pathlib', 'tabulate',
                        'holidays', 'pyowm'],
      entry_points={'console_scripts': [
          'sort_files=felis_assistant.sorter:sorter', 'felis_start=felis_assistant.main:main']}
      )
