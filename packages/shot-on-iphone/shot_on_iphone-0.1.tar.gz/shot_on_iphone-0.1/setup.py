
from distutils.core import setup
setup(
  name = 'shot_on_iphone',        
  packages = ['shot_on_iphone'],   
  version = '0.1',      
  license='MIT',       
  description = 'Shot On Iphone Meme Editor', 
  author = 'Krypton Byte',                  
  author_email = 'galaxyvplus6434@gmail.com',     
  url = 'https://github.com/krypton-byte/shot_on_iphone',   
  download_url = 'https://github.com/krypton-byte/shot_on_iphone/archive/1.0.zip',    
  keywords = ['meme', 'iphone', 'shot','shot on iphone'],   
  install_requires=[           
          'moviepy',
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