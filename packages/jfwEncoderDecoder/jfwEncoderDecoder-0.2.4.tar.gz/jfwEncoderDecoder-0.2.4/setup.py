import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='jfwEncoderDecoder',  
     version='0.2.4',
     author="Altamash Abdul Rahim",
     author_email="altamash.ar96@gmail.com",
     description="Binary encoding/decoding package",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/heezes/jfw-encoding-decoding",
     packages=setuptools.find_packages(),
     install_requires=["cstruct", "pyclibrary"],
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
         "Operating System :: OS Independent",
     ],
 )