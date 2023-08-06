
from setuptools import setup, find_packages 
  
with open('requirements.txt') as f: 
    requirements = f.readlines() 
  
long_description = "Sample package demo"
  
setup( 
        name ='mytestapp', 
        version ='1.0.0', 
        author ='Neil Baldwin', 
        author_email ='neil.baldwin@mac.com', 
        url ='https://github.com/neilbaldwin', 
        description ='Demo Package for GfG Article.', 
        long_description = long_description, 
        long_description_content_type ="text/markdown", 
        license ='MIT', 
        packages = find_packages(), 
        entry_points ={ 
            'console_scripts': [ 
                "mytestapp = mytestapp.mytestapp:main"
            ] 
        }, 
        classifiers = [
            "Programming Language :: Python :: 3", 
            "License :: OSI Approved :: MIT License", 
            "Operating System :: OS Independent", 
        ], 
        keywords ='geeksforgeeks gfg article python package vibhu4agarwal', 
        install_requires = requirements, 
        zip_safe = False
) 
