from setuptools import setup,find_packages

setup(
    name='darn',
    version='0.1.0',    
    description='Easy remote and local code execution',
    url='https://github.com/AmitSrourDev/darn',
    packages=find_packages(),
    author='Amit Srour',
    author_email='amitsrourdev@gmail.com',
    license='BSD 2-clause',
    # packages=['pyexample'],
    # install_requires=['mpi4py>=2.0',
    #                   'numpy',                     
    #                   ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3.8',
        "Topic :: Software Development",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Software Distribution",
        "Topic :: System :: Systems Administration",
    ],
    python_requires=">=3.8.5",
)
