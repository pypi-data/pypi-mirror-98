import json
from .source import Source 
from .dataset import  DataSet 
from .sourcetree import datalibrary
from .iridl_utils import connect 

datalibrary = Source.from_json(datalibrary)

__version__ = "0.0.1"
__author__ = "Kyle Hall (kjhall@iri.columbia.edu)"
__license__ = "None Don't use this "
