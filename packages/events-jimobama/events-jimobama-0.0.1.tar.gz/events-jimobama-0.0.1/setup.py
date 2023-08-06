import setuptools
long_description = "Unable to load decription";
with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(name = "events-jimobama",
      version="0.0.1",
      description="C# like event handler (pubsub)",
      long_description =long_description,
      url="https://github.com/miljimo/events.git",
      long_description_content_type="text/markdown",
      author="Obaro I. Johnson",
      author_email="johnson.obaro@hotmail.com",
      packages=setuptools.find_packages(),
      install_requires=[],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
         
    ],python_requires='>=3.6');

      
