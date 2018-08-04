"""versioninfo"""


# pylint: disable=too-few-public-methods
class VersionInfo:
    """Version info dataclass"""
    major: int
    minor: int
    build: int
    level: str
    serial: int

    # pylint: disable=too-many-arguments
    def __init__(self, major: int, minor: int, build: int, level: str, serial: int):
        self.major: int = major
        self.minor: int = minor
        self.build: int = build
        self.level: str = level
        self.serial: int = serial

    def __str__(self):
        return '{major}.{minor}.{build}{level}{serial}'.format(**self.__dict__)

    def __repr__(self):
        return str(self)


version = VersionInfo(1, 0, 0, 'a', 0)
