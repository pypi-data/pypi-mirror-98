from setuptools import setup, find_packages

VERSION = '0.1.6-2'

requires = [
    "synonym_dict>=0.2.0",
    "antelope_interface>=0.1.6",
    "xlrd==1.2.0",  ## really need to get out of this requirement and into openpyxl or equivalent
    "python-magic>=0.4.18",
    "requests>=2.25"
]

# optional: pylzma
"""
Version History
0.1.6 - 2021-03-10 - update to handle new synonym_dict 0.2.0, along with OLCA reference flow matching, ecoinvent 2.2,
                     a range of other improvements in performance and context handling
                     2021-03-10 post1
                     2021-03-17 post2 - get_context(); bump antelope version
                     
0.1.5 - 2021-02-05 - Updates to NullContext handling, flow term matching, fixed faulty requirements (add requests) 
0.1.4 - 2021/01/29 - background passing
0.1.3 - 2021/01/29 - Build passing (without bg tested)
0.1.3rc4           - fix last edit
0.1.3rc3           - xlrd removes support for xlsx in 2.0; _localize_file(None) return None
0.1.3rc2           - include data files
0.1.3rc1           - update requirements

0.1.2b - 2020/12/29 - fix some minor items
0.1.2 - 2020/12/28 - PyPI installation; includes significant performance enhancements for LCIA 

0.1.1 - 2020/11/12 - Bug fixes all over the place.  
                     Catalogs implemented
                     LCIA computation + flat LCIA computation reworked
                     Improvements for OpenLCA LCIA methods

0.1.0 - 2020/07/31 - Initial release - JIE paper
"""

setup(
    name="antelope_core",
    version=VERSION,
    author="Brandon Kuczenski",
    author_email="bkuczenski@ucsb.edu",
    license="BSD 3-Clause",
    install_requires=requires,
    extras_require={
        'XML': ['lxml>=1.2.0'],
        'write_to_excel': ['xlsxwriter>=1.3.7']
    },
    include_package_data=True,
    url="https://github.com/AntelopeLCA/core",
    summary="A reference implementation of the Antelope interface for accessing a variety of LCA data sources",
    long_description_content_type='text/markdown',
    long_description=open('README.md').read(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering"
    ],
    python_requires='>=3.6',
    packages=find_packages()
)
