from distutils.core import setup
setup(
  name = 'golcher',
  packages = ['golcher'],
  version = '0.7',
  license='MIT',
  description = 'Find Golcher Constant for a text Based on http://amor.cms.hu-berlin.de/~golchefe/ranlp.pdf and an Suffix Tree implementation',
  author = 'Liubomyr Ivanitskyi',
  author_email = 'lubomyr.ivanitskiy@gmail.com',
  url = 'https://github.com/LubomyrIvanitskiy',
  download_url = 'https://github.com/LubomyrIvanitskiy/golcher/archive/0.7.tar.gz',
  keywords = ['Golcher', 'NLP', 'constant', "suffix tree", "text repetition"],
  install_requires=[
          'numpy',
          'matplotlib',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)