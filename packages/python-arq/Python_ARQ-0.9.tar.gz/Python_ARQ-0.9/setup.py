from setuptools import setup
import pathlib

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
  name = 'Python_ARQ',
  packages = ['Python_ARQ'],
  version = '0.9', 
  license='MIT',  
  description = 'Asynchronous Python Wrapper For A.R.Q API. ',
  long_description=README,
  long_description_content_type="text/markdown",
  author = 'TheHamkerCat',
  author_email = 'thehamkercat@gmail.com',
  url = 'https://github.com/thehamkercat/Python_ARQ',
  download_url = '',
  keywords = ['API', 'ARQ_API', 'Universal API'],
  install_requires=[
          'aiohttp',
          'dotmap',
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable', 
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)
