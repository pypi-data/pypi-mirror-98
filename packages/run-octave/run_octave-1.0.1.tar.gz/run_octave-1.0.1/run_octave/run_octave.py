from scipy.io import loadmat, savemat
from os import path, system, remove


class RunOctave:

    __version__ = '1.0.0'

    def __init__(self, octave_path):
        self.octave_path = octave_path
        self.alphabet = 'abcdefghijklmnopqrstuvwxyz'
        self.CSL = ','.join(self.alphabet)  # Comma-separated letters

        # Getting PATH of temp files
        self.lib_path = path.split(path.abspath(__file__))[0]
        # print(self.lib_path)
        self.tempdata_path = path.join(self.lib_path, 'tempdata.mat').replace('\\','/')
        self.tempscript_path = path.join(self.lib_path, 'tempscript.m').replace('\\','/')


    def run(self, target, args=None, nargout=0):
        if isinstance(args, tuple):
            nargin = len(args)
            varargin  = self.CSL[:nargin*2-1]
            syntax = target + '(' + varargin + ');'

            # Write in the communication channel
            savemat(self.tempdata_path, dict(zip(self.alphabet[:nargin], args)))
        else:
            if any(c in target for c in "[]=(,) '+-*/:"):
                syntax = target
            else:
                syntax = target + '();'

            # Write in the communication channel
            savemat(self.tempdata_path, {'None': []})

        if nargout > 0:
            varargout = self.CSL[:nargout*2-1]
            syntax = '[' + varargout + ']=' + syntax

        # Auxiliary function
        with open(self.tempscript_path, 'w') as MAT_file:
            print(f'load("{self.tempdata_path}")\n{syntax}\nsave("-mat-binary","{self.tempdata_path}")', file=MAT_file)

        system(self.octave_path + ' ' + self.tempscript_path)  # Executes the auxiliary function

        data = loadmat(self.tempdata_path)  # Read the communication channel

        ret = [data[key] for key in self.alphabet[:nargout]]

        return ret
