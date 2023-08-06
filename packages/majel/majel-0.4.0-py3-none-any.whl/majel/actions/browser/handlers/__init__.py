# We have to import these here so they're loaded at start time and recognised
# as subclasses of Handler.  They shouldn't be imported from here.

from .amazon import AmazonHandler  # NOQA: F401
from .basic import BasicHandler  # NOQA: F401
from .netflix import NetflixHandler  # NOQA: F401
from .selector import SelectionHandler  # NOQA: F401
from .youtube import YoutubeHandler  # NOQA: F401
