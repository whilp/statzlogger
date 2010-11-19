import logging
import time

try:
    import statzlogger as szl
except ImportError:
    szl = None

# Implementations of szl concepts found in section 'Actions 1: The
# emit statement':
#
#   http://szl.googlecode.com/svn/doc/sawzall-language.html
#
# These calls should not fail if statzlogger can't be found.

numdivafans = logging.getLogger("stats.numdivafans")
sales = logging.getLogger("stats.sales")
fileoffans = logging.getLogger("stats.fileoffans")
salesperhour = logging.getLogger("stats.salesperhour")
top100songs = logging.getLogger("stats.top100songs")

if szl is not None:
    numdivafans.addHandler(szl.Sum())
    sales.addHandler(szl.Sum())
    fileoffans.addHandler(szl.Collection())
    salesperhour.addHandler(szl.Sum())
    top100songs.addHandler(szl.Top(100))

numdivafans.debug(1, index="britney")

sales.debug(0.25, index=1)

fan_age = 13
fileoffans.debug(("britney", "a britney song"), index=fan_age / 10)

now = time.time()
hour = now - (now % 3600)
salesperhour.debug({"count": 1, "sales": 11.99}, 
        indexes=("britney", "John Q. Salesguy", hour))

top100songs.debug("a song", weight=1)