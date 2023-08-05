import json
import keyword
import xarray as xr 

def gen_valid_identifier(seq):
    """https://stackoverflow.com/questions/10120295/valid-characters-in-a-python-class-name"""
    itr = iter(seq)                             # get an iterator
    # pull characters until we get a legal one for first in identifer
    for ch in itr:
        if ch == '_' or ch.isalpha():
            yield ch
            break
    # pull remaining characters and yield legal ones for identifier
    for ch in itr:
        if ch == '_' or ch.isalpha() or ch.isdigit():
            yield ch

def sanitize_identifier(name):
    name = ''.join(gen_valid_identifier(name))
    if name in keyword.kwlist:
        name = '_'+name
    return name.replace('/','').replace('-', '_')

def sanitize_ingrid_literal(name):
    return name.replace('(','').replace(')', '')


def connect(dataset):
    base = 'https://iridl.ldeo.columbia.edu/'
    return xr.open_dataset( base + dataset.url() + 'dods', decode_times=False)