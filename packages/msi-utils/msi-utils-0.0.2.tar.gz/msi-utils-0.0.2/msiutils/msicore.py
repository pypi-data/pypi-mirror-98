import os
import subprocess


class MSICore:

    def get_path(self, value):
        return os.path.abspath(os.path.expanduser(os.path.expandvars(value)))

    def call_subprocess(self, value_list):
        return subprocess.check_call([x for x in value_list])