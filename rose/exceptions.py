class RoseError(Exception):
    pass


class VersionError(RoseError):
    pass


class MissingCommandError(RoseError):
    pass


class CommandNotFoundError(RoseError):
    pass


class CommandFailedError(RoseError):
    pass


class ShowHelpError(RoseError):
    pass


class FlagError(RoseError):
    pass


class TemplateNotFoundError(RoseError):
    pass
