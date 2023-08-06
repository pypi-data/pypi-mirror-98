
from distutils.core import setup
from os import path
base_dir = path.abspath(path.dirname(__file__))
setup(
  name = 'github_markdown2image',        
  packages = ['github_markdown2image'],   
  version = '0.1',    
  license='MIT',     
  description = 'Markdown README to Image', 
  author = 'Krypton Byte',                  
  author_email = 'galaxyvplus6434@gmail.com',     
  url = 'https://github.com/krypton-byte/Github_Markdown_render',   
  keywords = ['readme', 'image', 'github', 'pdf', 'toPdf'], 
  install_requires=[           
          'imgkit',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',  
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)