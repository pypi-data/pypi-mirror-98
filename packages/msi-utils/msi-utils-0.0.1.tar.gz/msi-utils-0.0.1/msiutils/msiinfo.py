from .msicore import MSICore
from .msidiff import MSIDiff


class MSIInfo(MSICore):

    def streams(self, path):
        return self.call_subprocess(['msiinfo', 'streams', path])

    def tables(self, path):
        return self.call_subprocess(['msiinfo', 'tables', path])

    def summary(self, path):
        return self.call_subprocess(['msiinfo', 'suminfo', path])

    def diff(self):
        return MSIDiff()
