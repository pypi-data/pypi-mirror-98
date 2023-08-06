from distutils.core import setup
setup(
  name = 'rcvtool',         # How you named your package folder (MyLib)
  packages = ['rcvtool'],   # Chose the same as "name"
  version = '0.1.3',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Tool to perform concept attribution to interpret deep learning decisions.',   # Give a short description about your library
  author = 'Mara Graziani ',                   # Type in your name
  author_email = 'mara.graziani@hevs.ch',      # Type in your E-Mail
  url = 'https://github.com/maragraziani/rcvtool.git',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/maragraziani/rcvtool/archive/0.1.3.tar.gz',    # I explain this later on
  keywords = ['EXPLAINABLE AI', 'XAI', 'Interpretability', 'Deep Learning'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'numpy',
          'opencv-python',
          'scikit-image',
          'keras',
          'tensorflow',
          'statsmodels',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2.7',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
