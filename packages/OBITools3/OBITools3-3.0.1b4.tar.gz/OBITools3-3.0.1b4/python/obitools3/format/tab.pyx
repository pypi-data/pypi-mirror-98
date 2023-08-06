#cython: language_level=3

cimport cython
from obitools3.dms.view.view cimport Line
from obitools3.utils cimport bytes2str_object, str2bytes, tobytes
from obitools3.dms.column.column cimport Column_line, Column_multi_elts

import sys

cdef class TabFormat:
    
    def __init__(self, header=True, bytes NAString=b"NA", bytes sep=b"\t"):
        self.header = header
        self.first_line = True
        self.NAString = NAString
        self.sep = sep
        
    @cython.boundscheck(False)    
    def __call__(self, object data):
        
        line = []
        
        if self.first_line:
            self.tags = [k for k in data.keys()]
        
        if self.header and self.first_line:
            for k in self.tags:
                if isinstance(data.view[k], Column_multi_elts):
                    keys = data.view[k].keys()
                    keys.sort()
                    for k2 in keys:
                        line.append(tobytes(k)+b':'+tobytes(k2))
                else:
                    line.append(tobytes(k))
            r = self.sep.join(value for value in line)
            r += b'\n'
            line = []
                    
        for k in self.tags:
            value = data[k]
            if isinstance(data.view[k], Column_multi_elts):
                keys = data.view[k].keys()
                keys.sort()
                if value is None:  # all keys at None
                    for k2 in keys: # TODO could be much more efficient
                        line.append(self.NAString)
                else:
                    for k2 in keys: # TODO could be much more efficient
                        if value[k2] is not None:
                            line.append(str2bytes(str(bytes2str_object(value[k2]))))  # genius programming
                        else:
                            line.append(self.NAString)
            else:
                if value is not None:
                    line.append(str2bytes(str(bytes2str_object(value))))
                else:
                    line.append(self.NAString)
                  	      	
        if self.header and self.first_line:
            r += self.sep.join(value for value in line)
        else:
            r = self.sep.join(value for value in line)

        if self.first_line:
            self.first_line = False

        return r
