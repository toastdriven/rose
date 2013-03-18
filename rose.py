__author__ = 'Daniel Lindsley'
__license__ = 'New BSD'
__version__ = (1, 0, 0)


class VersionError(Exception):
    pass


def load_version(file_path):
    """
    Reads in the version file & pulls out the version info.

    Requires a ``file_path`` argument, which should be the path to the file.

    Example::

        >>> import rose
        >>> rose.load_version('VERSION')
        '1.0.0-final'
        >>> rose.load_version(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'VERSION'))
        '1.0.0-final'

    """
    return open(file_path, 'r').readline().strip()


def build_version(package_name, version_string):
    """
    Given a package name & version, return a tuple of the semver version bits.

    Example::

        >>> import rose
        >>> rose.build_version('rose', '1.0.0-final')
        (1, 0, 0, 'final')

    """
    version_bits = version_string.split('-')

    if len(version_bits) > 2:
        raise VersionError("%s releases must be in '<major>.<minor>.<patch>[-<release>]' format. Saw: %s" % (package_name, version_bits))

    major_minor_patch = version_bits.pop(0).split('.')

    if len(major_minor_patch) != 3:
        raise VersionError("%s releases must be in '<major>.<minor>.<patch>[-<release>]' format. Saw: %s" % (package_name, major_minor_patch))

    major_minor_patch = [int(bit) for bit in major_minor_patch]

    if version_bits:
        major_minor_patch.append(version_bits[0])

    return tuple(major_minor_patch)
