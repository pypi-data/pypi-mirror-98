from setuptools import setup

with open("requirements.txt", encoding="utf-8") as r:
    requires = [i.strip() for i in r]

with open("README.md", encoding="utf-8") as f:
    readme = f.read()

setup(
  name = 'Python_ARQ',
  packages = ['Python_ARQ'],
  version = '0.9.1', 
  license='MIT',  
  description = 'Asynchronous Python Wrapper For A.R.Q API. ',
  long_description=readme,
  long_description_content_type="text/markdown",
  author = 'TheHamkerCat',
  author_email = 'thehamkercat@gmail.com',
  url = 'https://github.com/thehamkercat/Python_ARQ',
  download_url = '',
  keywords = ['API', 'ARQ_API', 'Universal API'],
  install_requires=requires,
  classifiers=[
    'Development Status :: 5 - Production/Stable', 
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)
