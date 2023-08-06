from dateutil.parser import parse, UnknownTimezoneWarning
from dateutil.parser import parserinfo
from .string_type import StringType
from .float_type import FloatType
from .italian_zip_code_type import ItalianZIPCodeType

class ItalianMonths(parserinfo):

    ITALIAN_MONTHS = [
        ("Gen", "gen", "Gennaio"),
        ("Feb", "feb", "Febbraio"),
        ("Mar", "mar", "Marzo"),
        ("Apr", "apr", "Aprile"),
        ("Mag", "mag", "Maggio"),
        ("Giu", "giu", "Giugno"),
        ("Lug", "lug", "Luglio"),
        ("Ago", "ago", "Agosto"),
        ("Set", "set", "Settembre"),
        ("Ott", "ott", "Ottobre"),
        ("Nov", "nov", "Novembre"),
        ("Dic", "dic", "Dicembre")
    ]

    MONTHS = [
        (*english, *italian)
        for english, italian in zip(parserinfo.MONTHS, ITALIAN_MONTHS)
    ]


class DateType(StringType):

    def __init__(self):
        """Create new DateType predictor."""
        super().__init__()
        self._parserinfo = ItalianMonths()
        self._float = FloatType()
        self._cap = ItalianZIPCodeType()

    def validate(self, candidate, **kwargs) -> bool:
        """Return boolean representing if given candidate is a Date."""
        if self._float.validate(candidate):
            return False
        if self._cap.validate(candidate):
            return False
        try:
            parse(candidate, parserinfo=self._parserinfo)
            return True
        except (Exception, UnknownTimezoneWarning):
            return False
