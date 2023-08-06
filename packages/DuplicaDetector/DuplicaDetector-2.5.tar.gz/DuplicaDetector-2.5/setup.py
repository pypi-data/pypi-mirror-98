from distutils.core import setup
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'DuplicaDetector',         # How you named your package folder (MyLib)
  packages = ['DuplicaDetector'],
  long_description=long_description,
  long_description_content_type='text/markdown',  # Chose the same as "name"
  version = '2.5',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Detects if an image already exist a database. This project was made for educational purposes and is not meant to be used in any other projet or production env.',   # Give a short description about your library
  author = 'Julien Calenge, Simon Bolot, Halil Bagdadi, Thomas Schneider, Pierre Ballereau',                   # Type in your name
  author_email = 'julien.calenge@epitech.eu',      # Type in your E-Mail
  url = 'https://github.com/Chiraii/Discord-Mirror-Prototype/',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/Chiraii/Discord-Mirror-Prototype/',    # I explain this later on
  keywords = ['Image', 'Duplicate', 'Detector'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'pandas',
          'pillow'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)