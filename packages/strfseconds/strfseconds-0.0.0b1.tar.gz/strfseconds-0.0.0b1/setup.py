
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="strfseconds",                          
    version="0.0.0beta1",                   
    author="Remi Visser",                   
    author_email='remivisser@gmail.com',
    url="https://github.com/remivisser",
    download_url = "https://github.com/remivisser",
    description="Convert seconds to units of time.",
    long_description=long_description,      
    long_description_content_type="text/markdown",
    license="MIT",
    packages=setuptools.find_packages(),    
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],                                      
#    python_requires='>=3.6',               
    py_modules=["strfseconds"],
    package_dir={'':'src'},                 
    install_requires=[]                     
)
