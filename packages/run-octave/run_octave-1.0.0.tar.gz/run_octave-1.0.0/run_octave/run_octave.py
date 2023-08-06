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
        self.file_path = path.join(self.lib_path, 'data.mat').replace('\\','/')


    def run(self, target, args=None, nargout=0):
        if isinstance(args, tuple):
            nargin = len(args)
            varargin  = self.CSL[:nargin*2-1]
            syntax = target + '(' + varargin + ');'

            # Write in the communication channel
            savemat(self.file_path, dict(zip(self.alphabet[:nargin], args)))
        else:
            if any(c in target for c in "[]=(,) '+-*/:"):
                syntax = target
            else:
                syntax = target + '();'

            # Write in the communication channel
            savemat(self.file_path, {'None': []})

        if nargout > 0:
            varargout = self.CSL[:nargout*2-1]
            syntax = '[' + varargout + ']=' + syntax

        # Auxiliary function
        with open('temp_af.m', 'w') as MAT_file:
            print(f'load("{self.file_path}")\n{syntax}\nsave("-mat-binary","{self.file_path}")', file=MAT_file)

        system(self.octave_path + ' temp_af.m')  # Executes the auxiliary function
        remove('temp_af.m')

        data = loadmat(self.file_path)  # Read the communication channel

        ret = [data[key] for key in self.alphabet[:nargout]]

        return ret
