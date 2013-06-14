"""
Make buildout.dumppickedversion's features work in buildout 2
"""
import os
import zc.buildout.easy_install
from zc.buildout.buildout import print_
try:
    from zc.buildout.buildout import _format_picked_versions
except ImportError:
    _format_picked_versions = None  # buildout < 2.2

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


def _file_name_and_overwrite(section):
    file_name = (FILE_NAME in section and section[FILE_NAME].strip() or None)
    overwrite = (OVERWRITE not in section or section[OVERWRITE].lower() in TRUE)
    return (file_name, overwrite)


def install(buildout):
    """
    Hook into buildout and alter it's version dumping behavior.
    """
    file_name, overwrite = _file_name_and_overwrite(buildout['buildout'])
    if hasattr(zc.buildout.easy_install , 'store_required_by'):
        store_required_by = zc.buildout.easy_install.store_required_by
    else:  # buildout < 2.2
        store_required_by = zc.buildout.easy_install.store_picked_versions
    store_required_by(True)
    if file_name is None:
        # Simply enable buildout's show-picked-versions feature      
        buildout.show_picked_versions = True
    elif _format_picked_versions is None:  # buildout < 2.2
        # Monkey patch buildout to enable overwriting behaviour
        buildout.update_versions_file = file_name
        buildout._print_picked_versions = dump_picked_versions(
            buildout._print_picked_versions, file_name, overwrite)


def uninstall(buildout):
    if _format_picked_versions:
        file_name, overwrite = _file_name_and_overwrite(buildout['buildout'])

        if file_name is None:
            return
        if os.path.isfile(file_name) and not overwrite:
            print_('Skipped: File %s already exists.' % file_name)
        else:
            picked_versions, required_by = (zc.buildout.easy_install
                                            .get_picked_versions())
            output = _format_picked_versions(picked_versions, required_by)
            f = open(file_name, 'wb')
            f.write('\n'.join(output))
            f.close()
            print_('Picked versions have been written to %s' % file_name)

