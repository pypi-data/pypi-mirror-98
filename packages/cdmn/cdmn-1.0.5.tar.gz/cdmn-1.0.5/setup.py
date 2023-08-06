import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cdmn",
    version="1.0.5",
    author="Simon Vandevelde",
    author_email="s.vandevelde@kuleuven.be",
    description="A package providing a (c)DMN solver and API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://cdmn.be",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=['openpyxl==3.0.0', 'ply==3.11',
                      'numpy', 'python-dateutil',
                      'idp_engine==0.7.2'],
    entry_points={
        'console_scripts': ['cdmn=cdmn.cdmn:main']
    }
)
