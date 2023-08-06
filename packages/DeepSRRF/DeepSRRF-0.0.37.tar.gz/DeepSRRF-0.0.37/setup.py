import setuptools

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DeepSRRF",
    version="0.0.37",
    author="Hakan Temiz",
    author_email="htemiz@artvin.edu.tr",
    description="A framework for Obtaining and Automating Super Resolution for RF data with Deep Learning Algorithms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/htemiz/DeepSRRF",
    packages= setuptools.find_packages(),
    keywords="super resolution deep learning DeepSRRF",
    python_requires='>=3',
    include_package_data=True,
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst', '*.md', 'samples/*.*', 'docs/*.*' ],
    },

    exclude_package_data={'': ['']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    # scripts=[  'scripts/add_dsr_path'], # ['python -m pip install -r requirements.txt'],

    install_requires= [ 'scipy==1.2.1', 'pandas', 'h5py', 'matplotlib', 'scikit-image==0.14.3', 'scikit-video',
                       'sporco', 'Pillow', 'sewar', 'openpyxl', 'numpy>=1.13.3'
                       'tensorflow-gpu==1.14.0', 'theano', 'keras==2.2.4', 'setuptools>41.0.0',
                       'markdown>=2.2.0', 'GraphViz', 'importlib'],
    project_urls={
        'Documentation': 'https://github.com/htemiz/deepsr/tree/master/DeepSRRF/docs',
        'Source': 'https://github.com/htemiz/deepsr/tree/master/DeepSRRF',
    },
    #
    # entry_points={
    #     'console_scripts': [
    #         'add_dsr_path = DeepSR.scripts:add'
    #     ],
    #     'gui_scripts': [
    #         '',
    #     ]
    # },
)
