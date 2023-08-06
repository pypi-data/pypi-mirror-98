from .msicore import MSICore


class MSIDump(MSICore):

    def tables(self, path, output='./'):
        return self.call_subprocess(['msidump', '--tables', '--directory', self.get_path(output), path])

    def streams(self, path, output='./'):
        return self.call_subprocess(['msidump', '--streams', '--directory', self.get_path(output), path])

    def signature(self, path, output='./'):
        return self.call_subprocess(['msidump', '--signature', '--directory {}', self.get_path(output), path])
