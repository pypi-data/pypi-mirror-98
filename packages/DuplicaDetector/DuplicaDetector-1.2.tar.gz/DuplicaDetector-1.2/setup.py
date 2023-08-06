from distutils.core import setup
setup(
  name = 'DuplicaDetector',         # How you named your package folder (MyLib)
  packages = ['DuplicaDetector'],   # Chose the same as "name"
  version = '1.2',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Detect if an image already exist in database kinda fastly',   # Give a short description about your library
  author = 'Julien Calenge, Simon Bolot, Halil Bagdadi, Thomas Shneider, Pierre Ballereau',                   # Type in your name
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