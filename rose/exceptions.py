class RoseError(Exception):
    pass


class VersionError(RoseError):
    pass


class MissingCommandError(RoseError):
    pass


class CommandNotFoundError(RoseError):
    pass
