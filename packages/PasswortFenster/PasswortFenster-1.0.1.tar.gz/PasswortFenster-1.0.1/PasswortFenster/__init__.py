from .__PasswortMain import __doc__ as PasswortFenster__doc__
from .__PasswortMain import PasswortMainWindow
from PasswortFenster.__PasswortEingabeWidget import __doc__ as PasswortEingabe__doc__
from PasswortFenster.__UserEingabeWidget import __doc__ as UsernameEingabe__doc__
from .__EntryLabel import __doc__ as EntryLabel__doc__
from .__PasswortSubmit import __doc__ as PasswortSubmit__doc__

__author__ = "heureka-code"
__version__ = "1.0.1"
__maintainer__ = "heureka-code"
__annotaions__ = "Beinhaltet die nötigen Module für ein Passworteingabefenster"
__doc__ = f"\n{'-' * 120}\n".join([PasswortFenster__doc__, UsernameEingabe__doc__, PasswortEingabe__doc__,
                                   EntryLabel__doc__, PasswortSubmit__doc__])
