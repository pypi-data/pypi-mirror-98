from distutils.core import setup
setup(
  name = 'Python_ARQ',
  packages = ['Python_ARQ'],
  version = '0.7', 
  license='MIT',  
  description = 'Asynchronous Python Wrapper For A.R.Q API. ',
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
