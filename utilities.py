#aurther: eric greenhouse
__filename = 'utilities.py'
__fname = 'utilities'
cStrDividerExcept = '***************************************************************'
cStrDivider = '#================================================================#'
print('', cStrDivider, f'START _ {__filename}', cStrDivider, sep='\n')
print(f'GO {__filename} -> starting IMPORTs and globals decleration')

from pprint import *
import time
from datetime import datetime
import sys, os, traceback

#---------------------------------------------------------------------------------#
# support functions
#---------------------------------------------------------------------------------#
def swap_dict_keys(lst_old_keys, lst_new_keys, dict_swap):
    dict_swap_new = {}
    for idx, val in enumerate(lst_old_keys):
        key = val
        bKey = key.encode('utf-8')
        if bKey in dict_swap:
            #dict_swap_new[lst_new_keys[idx].encode('utf-8')] = dict_swap[bKey]
            dict_swap_new[lst_new_keys[idx]] = dict_swap[bKey]
    return dict_swap_new
    
def uft8(s):
    return s.encode('utf-8')
    
def clean_nil_str_lst_entries(lst_pg_utf):
    lst_idx_del = [i for i, x in enumerate(lst_pg_utf) if x == b'']
    lst_pg_utf = [x for i, x in enumerate(lst_pg_utf) if i not in lst_idx_del]
    return lst_pg_utf
    
# strips 2 leading dashes from text
def strip_leading_dashes(pg_text):
    # strip preceeding dashes left over from section 1
    pg_text = pg_text.strip()
    idx_dash = pg_text.find(b'-')
    pg_text = pg_text[idx_dash+1::1]
    
    idx_dash = pg_text.find(b'-')
    pg_text = pg_text[idx_dash+1::1]
    pg_text = pg_text.strip()
    return pg_text
    
#ref: https://github.com/pymupdf/PyMuPDF-Utilities/blob/master/demo/demo.py
def print_meta(doc):

    """
    The metadata is a python dict, whose keys are:
    # format, encryption, title, author, subject, keywords, creator, producer,
    creationDate, modDate.
    The values will be None if the info is not available
    """
    print("")
    print("Document '%s' has %i pages." % (doc.name, len(doc))) # or 'doc.page_count'
    print("")
    print("Metadata Information:")
    print("---------------------")
    for key in doc.metadata:
        if doc.metadata[key]:
            print(" %s: %s" % (key.title(), doc.metadata[key]))
    print("")

    # here we print out the outline of the document(if any)
    toc = doc.get_toc()
    if len(toc) == 0:
        print("No Table of Contents available")
    else:
        print("Table of Contents:")
        print("------------------")
        for t in toc:
            print("  " * (t[0] - 1), t[0], t[1], "page", t[2])

    print("")

def find_text(str_search, pg_text):
    str_return = ""
    for match in re.finditer(str_search, pg_text):
        str_return += f"FOUND '{str_search}'"
    return str_return

def write_txt(text):
    with open('output.txt', 'w') as f:
        f.write(text)

#ref: https://stackoverflow.com/a/1278740/2298002
def printException(e):
    #print type(e)       # the exception instance
    #print e.args        # arguments stored in .args
    #print e             # __str__ allows args to be printed directly
    print('', cStrDividerExcept, f' Exception Caught _ e: {e}', sep='\n')
    print(f' Exception Caught _ type(e): {type(e)}')
    print(f' Exception Caught _ e.args: {e.args}')

    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #print(traceback.format_exc())
    strTrace = traceback.format_exc()
    #print(exc_type, fname, exc_tb.tb_lineno)
    print('', cStrDividerExcept, f' type: {exc_type}', f' file: {fname}', f' line_no: {exc_tb.tb_lineno}', f' traceback: {strTrace}', cStrDividerExcept, sep='\n')

def get_time_now(timeconv=False, timeonly=False):
    timenowsec = int(round(time.time()))
    if timeconv:
        timenow = datetime.fromtimestamp(timenowsec)
        if timeonly:
            timenow = str(timenow).split(' ')[1]
    return timenow, timenowsec

def getPrintListStr(lst=[], strListTitle='list', useEnumerate=True, goIdxPrint=False, goPrint=True):
    strGoIndexPrint = None
    if goIdxPrint:
        strGoIndexPrint = '(w/ indexes)'
    else:
        strGoIndexPrint = '(w/o indexes)'

    lst_str = None
    if useEnumerate:
        if goIdxPrint:
            lst_str = [f'{i}: {v}' for i,v in enumerate(lst)]
        else:
            lst_str = [f'{v}' for i,v in enumerate(lst)]
    else:
        if goIdxPrint:
            lst_str = [f'{lst.index(x)}: {x}' for x in lst]
        else:
            lst_str = [f'{x}' for x in lst]

    lst_len = len(lst)
    print(f'{strListTitle} _ {strGoIndexPrint} _ count {lst_len}:', *lst_str, sep = "\n ")
    return lst_str

def getPrintListStrTuple(lst=[], strListTitle='list', useEnumerate=True, goIdxPrint=False, goPrint=True):
    strGoIndexPrint = None
    if goIdxPrint:
        strGoIndexPrint = '(w/ indexes)'
    else:
        strGoIndexPrint = '(w/o indexes)'

    lst_str = None
    if useEnumerate:
        if goIdxPrint:
            lst_str = [f"{i}: {', '.join(map(str,v))}" for i,v in enumerate(lst)]
        else:
            lst_str = [f"{', '.join(map(str,v))}" for i,v in enumerate(lst)]
    else:
        if goIdxPrint:
            lst_str = [f"{lst.index(x)}: {', '.join(map(str,x))}" for x in lst]
        else:
            lst_str = [f"{', '.join(map(str,x))}" for x in lst]

    lst_len = len(lst)
    print(f'{strListTitle} _ {strGoIndexPrint} _ count {lst_len}:\n', *lst_str, sep = "\n ")
    return lst_str
