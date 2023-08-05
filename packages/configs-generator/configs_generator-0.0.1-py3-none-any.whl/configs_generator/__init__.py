__doc__ = '''Configuration Generation Tool'''

"""
Mandatory Required modules
==========================
pandas, nettoolkit



update below variable in confGen.py if column names are different in database (excel)
VAR_DB_FIND_COLUMN = 'FIND'
VAR_DB_REPL_COLUMN = 'REPLACE'

update below variable in confGen.py if section identifiers are different in template
SECTION_STARTER = ("GOAHEAD FOR", "REPEAT EACH")
SECTION_STOPPER = ("GOAHEAD END", "REPEAT STOP")



"""

__all__ = [ "Execute_ConfGen",
	"ConfGen", "Section", "Replicate", "fnr"
	]

__version__ = "0.0.1"
from .execute_confGen import Execute_ConfGen
from .confGen import ConfGen, Section, Replicate, fnr
