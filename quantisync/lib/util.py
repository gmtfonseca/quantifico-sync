from pathlib import Path
from datetime import datetime
import glob


class File:

    def __init__(self, path):
        self._path = Path(path)

    def baseName(self):
        return self._path.stem

    def name(self):
        return self._path.name

    def modified(self):
        return int(self._path.stat().st_mtime)

    def exists(self):
        return self._path.exists()

    def size(self):
        return self._path.stat().st_size

    def path(self):
        return str(self._path)

    def unlink(self):
        if self.exists():
            return self._path.unlink()


class Dir:

    def __init__(self, path):
        self._path = Path(path)

    def files(self, extension):
        if not self._path.exists():
            return []

        return glob.glob('{}/*.{}'.format(str(self._path), extension))


class InvalidDateString:
    pass


class Date:
    def parseString(string):
        if not string:
            raise InvalidDateString()

        return datetime.strptime(string, '%Y-%m-%d %H:%M:%S.%f')


class DeltaTime:

    @classmethod
    def _handleSuffix(cls, singularSuffix, pluralSuffix, diff):
        string = 'há {} '.format(diff)
        if diff > 1:
            string = string + pluralSuffix
        else:
            string = string + singularSuffix
        return string

    @classmethod
    def format(cls, delta):
        DAYS_IN_YEAR = 365
        DAYS_IN_MONTH = 30

        SECONDS_IN_MIN = 60
        SECONDS_IN_HOUR = 3600

        if delta.days >= DAYS_IN_YEAR:
            deltaYears = int(delta.days / DAYS_IN_YEAR)
            return cls._handleSuffix('ano', 'anos', deltaYears)
        elif delta.days >= DAYS_IN_MONTH:
            deltaMonths = int(delta.days / DAYS_IN_MONTH)
            return cls._handleSuffix('mês', 'meses', deltaMonths)
        elif delta.days >= 1:
            return cls._handleSuffix('dia', 'dias', delta.days)
        else:
            if delta.seconds < SECONDS_IN_MIN:
                return 'agora'
            elif delta.seconds >= SECONDS_IN_MIN and delta.seconds < SECONDS_IN_HOUR:
                deltaMins = int(delta.seconds / SECONDS_IN_MIN)
                return cls._handleSuffix('minuto', 'minutos', deltaMins)
            else:
                deltaHours = int(delta.seconds / SECONDS_IN_HOUR)
                return cls._handleSuffix('hora', 'horas', deltaHours)
