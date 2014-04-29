mete0r.recipe.stow
==================

a buildout recipe to stow/unstow generated files

::

        [buildout]
        parts =
                stow

        [stow]
        recipe = mete0r.recipe.stow
        sections =
                config
                scripts
        destination = parts/stow

        [config]
        recipe = collective.recipe.template
        output = etc/foo.ini
        ...

        [scripts]
        recipe = zc.recipe.eggs
        eggs = httpie

Resulting destination directory::

        $ tree parts/stow

        parts/stow/
        ├── bin
        │   └── http -> /THE/BUILDOUT/DIRECTORY/bin/http
        └── etc
            └── foo.ini -> /THE/BUILDOUT/DIRECTORY/etc/foo.ini

        2 directories, 2 files


.. topic:: Caveat:

        Though it's inspired by GNU Stow, resolving algorithm is very dumb/weak
        (at least for now). So beware situations like followings:

        * Destination files exists
        * Source / destination files overwrap
        * Symlinked intermediate directories
