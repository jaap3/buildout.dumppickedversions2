Let's create an egg to use it in our tests::

    >>> mkdir('myegg')
    >>> write('myegg', 'setup.py',
    ... '''
    ... from distutils.core import setup
    ... setup(name='myegg', version='1.0',)
    ... ''')
    >>> write('myegg', 'README', '')
    >>> print system(buildout + ' setup myegg bdist_egg')
    Running setup script 'myegg/setup.py'.
    ...

Create a buildout and use buildout.dumppickedversions2::

    >>> write('buildout.cfg',
    ... '''
    ... [buildout]
    ... extensions = buildout.dumppickedversions2
    ... parts = myegg
    ... find-links = https://pypi.python.org/simple/zc.recipe.egg/
    ...              %s
    ... [myegg]
    ... recipe = zc.recipe.egg
    ... eggs = myegg
    ... ''' % join('myegg', 'dist'))

Running the buildout will print information about picked versions::

    >>> print system(join('bin', 'buildout'))
    Develop distribution: buildout.dumppickedversions2 N.N
    ...
    Versions had to be automatically picked.
    The following part definition lists the versions picked:
    [versions]
    myegg = N.N
    zc.buildout = N.N
    zc.recipe.egg = N.N
    ...

To dump picked versions to a file, we just add an ``dump-picked-versions-file`` 
option and give a file name::
    
    >>> write('buildout.cfg',
    ... '''
    ... [buildout]
    ... extensions = buildout.dumppickedversions2
    ... dump-picked-versions-file = versions.cfg
    ... parts = myegg
    ... find-links = https://pypi.python.org/simple/zc.recipe.egg/
    ...              %s
    ... [myegg]
    ... recipe = zc.recipe.egg
    ... eggs = myegg 
    ... ''' % join('myegg', 'dist'))
    
    >>> print system(buildout)
    Develop distribution: buildout.dumppickedversions2 N.N
    ...
    Updating myegg.
    Picked versions have been written to versions.cfg
    ...

And here is the content of the file versions.cfg::
    
    >>> cat('versions.cfg')
    [versions]
    myegg = N.N
    zc.buildout = N.N
    zc.recipe.egg = N.N

Next time we run the buildout the file will be overwritten::

    >>> print system(buildout)
    Develop distribution: buildout.dumppickedversions2 N.N
    ...
    Picked versions have been written to versions.cfg
    ...

    >>> cat('versions.cfg')
    [versions]
    myegg = N.N
    zc.buildout = N.N
    zc.recipe.egg = N.N

Let's create a new egg to use it in our tests, it will require
another egg::

    >>> mkdir('theiregg')
    >>> write('theiregg', 'setup.py',
    ... '''
    ... from distutils.core import setup
    ... setup(name='theiregg', version='1.0', install_requires='myegg')
    ... ''')
    >>> write('theiregg', 'README', '')
    >>> print system(buildout + ' setup theiregg bdist_egg')
    Running setup script 'theiregg/setup.py'.
    ...

Create a buildout that uses this new egg::

    >>> write('buildout.cfg',
    ... '''
    ... [buildout]
    ... extensions = buildout.dumppickedversions2
    ... parts = theiregg
    ... find-links = https://pypi.python.org/simple/zc.recipe.egg/
    ...              %s
    ...              %s
    ... [theiregg]
    ... recipe = zc.recipe.egg
    ... eggs = theiregg
    ... ''' % (join('theiregg', 'dist'), join('myegg', 'dist')))

Running the buildout will print information about picked versions
and who required them::

    >>> print system(join('bin', 'buildout'))
    Develop distribution: buildout.dumppickedversions2 N.N
    ...
    Versions had to be automatically picked.
    The following part definition lists the versions picked:
    [versions]
    theiregg = N.N
    zc.buildout = N.N
    zc.recipe.egg = N.N
    <BLANKLINE>
    # Required by:
    # theiregg==N.N
    myegg = N.N
    ...

This also works when writing to a file::

    >>> write('buildout.cfg',
    ... '''
    ... [buildout]
    ... extensions = buildout.dumppickedversions2
    ... dump-picked-versions-file = versions.cfg
    ... parts = theiregg
    ... find-links = https://pypi.python.org/simple/zc.recipe.egg/
    ...              %s
    ...              %s
    ... [theiregg]
    ... recipe = zc.recipe.egg
    ... eggs = theiregg
    ... ''' % (join('theiregg', 'dist'), join('myegg', 'dist')))

    >>> print system(buildout)
    Develop distribution: buildout.dumppickedversions2 N.N
    ...
    Updating theiregg.
    Picked versions have been written to versions.cfg
    ...

And here is the content of the file versions.cfg::
    
    >>> cat('versions.cfg')
    [versions]
    theiregg = N.N
    zc.buildout = N.N
    zc.recipe.egg = N.N
    <BLANKLINE>
    # Required by:
    # theiregg==N.N
    myegg = N.N

When we don't want to overwrite the file we just add an 
``overwrite-picked-versions-file`` and set it to false::

    >>> write('buildout.cfg',
    ... '''
    ... [buildout]
    ... extensions = buildout.dumppickedversions2
    ... dump-picked-versions-file = versions.cfg
    ... overwrite-picked-versions-file = false
    ... parts = myegg
    ... find-links = https://pypi.python.org/simple/zc.recipe.egg/
    ...              %s
    ... [myegg]
    ... recipe = zc.recipe.egg
    ... eggs = myegg 
    ... ''' % join('myegg', 'dist'))
    
    >>> print system(buildout)
    Develop distribution: buildout.dumppickedversions2 N.N
    ...
    Skipped: File versions.cfg already exists.
    ...
