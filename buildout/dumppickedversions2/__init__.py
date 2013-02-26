"""
Make buildout.dumppickedversion's features work in buildout 2
"""
import os
import zc.buildout.easy_install
from zc.buildout.buildout import print_

FILE_NAME = 'dump-picked-versions-file'
OVERWRITE = 'overwrite-picked-versions-file'
TRUE = ['yes', 'true', 'on']


def dump_picked_versions(old_print_picked_versions, file_name, overwrite):
    """
    Create and return a monkey patched version of print_picked_versions.
    """
    def overwrite_picked_versions():
        """
        Altered behavior for print_picked_versions. Basically,
        print_picked_versions is called unless the version files exists.

        If the version file exists and overwrite is enabled the file will
        be removed before calling print_picked_versions.

        If overwriting is disabled print_picked_versions is not called and
        a message is printed.
        """
        if os.path.isfile(file_name):
            if overwrite:
                os.unlink(file_name)
                old_print_picked_versions()
            else:
                print_('Skipped: File %s already exists.' % file_name)
        else:
            old_print_picked_versions()
    return overwrite_picked_versions


def install(buildout):
    """
    Hook into buildout and alter it's version dumping behavior.
    """
    section = buildout['buildout']
    file_name = (FILE_NAME in section and section[FILE_NAME].strip() or None)
    overwrite = (OVERWRITE not in section or section[OVERWRITE].lower() in TRUE)

    if file_name is None:
        # Simply enable buildout's show-picked-versions feature
        zc.buildout.easy_install.store_picked_versions(True)
        buildout.show_picked_versions = True
    else:
        # Monkey patch buildout to enable overwriting behaviour
        zc.buildout.easy_install.store_picked_versions(True)
        buildout.update_versions_file = file_name
        buildout._print_picked_versions = dump_picked_versions(
            buildout._print_picked_versions, file_name, overwrite)
