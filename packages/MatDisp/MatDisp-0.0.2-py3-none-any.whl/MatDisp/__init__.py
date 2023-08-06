from IPython.core.interactiveshell import InteractiveShell
import numpy as np

IShell = InteractiveShell.instance()

def vec2str_lis(vector):
    return map(lambda x:str(round(x)),vector)

def mat2md(M:np.ndarray):
    head = r'\begin{bmatrix}'
    tail = r'\end{bmatrix}'
    if M.ndim == 1:
        content = r'\\'.join(vec2str_lis(M))
        return f'{head}{content}{tail}'
    if M.ndim == 2:
        content = r'\\'.join(['&'.join(vec2str_lis(vec)) for vec in M])
        return f'{head}{content}{tail}'
    return repr(M)

IShell.display_formatter.formatters['text/markdown'].type_printers[np.ndarray]=mat2md
    
