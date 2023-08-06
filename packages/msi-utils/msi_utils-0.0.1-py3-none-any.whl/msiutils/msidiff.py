from .msicore import MSICore


class MSIDiff(MSICore):

    def tables(self, path):
        return self.call_subprocess(['msidiff', '--tables', path])

    def files(self, path):
        return self.call_subprocess(['msidiff', '--list', path])
        
