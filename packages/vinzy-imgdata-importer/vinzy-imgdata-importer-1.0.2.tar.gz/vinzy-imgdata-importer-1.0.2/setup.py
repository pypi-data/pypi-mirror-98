from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="vinzy-imgdata-importer",
    version="1.0.2",
    description="This Package will help you to import image data for your deep learning project",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/vinayak-97/Image-data-importer-for-deep-learning",
    author="Vinayak Bhosale",
    author_email="vinubhosale.cj@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["vinzy_imgdata_importer"],
    include_package_data=True,
    install_requires=["numpy","opencv-python","pickle-mixin"],
    
)