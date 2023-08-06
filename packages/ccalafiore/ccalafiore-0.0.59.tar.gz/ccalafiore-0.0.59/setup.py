import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ccalafiore",
    version="000.000.059",
    author="Carmelo Calafiore",
    author_email="cc18849@essex.ac.uk",
    description="personal package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/ccalafiore/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"],
    install_requires=[
        'numpy',
        'torch',
        'torchvision',
        'Pillow',
        'opencv-contrib-python',
        'matplotlib',
        'selenium'],
    python_requires='>=3.6')

# examples of the kw "install_requires"
# setup(
#     #...,
#     install_requires = [
#         'docutils',
#         'BazSpam ==1.1',
#         "enum34;python_version<'3.4'",
#         "pywin32 >= 1.0;platform_system=='Windows'"]
#     #...)

# more info the kw "install_requires" at the link below
# at https://setuptools.readthedocs.io/en/latest/userguide/dependency_management.html#declaring-dependencies
