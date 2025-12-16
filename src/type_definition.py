# The fields of a dictionary representing a token are in fact of different types.
# The specified field value type is only valid for the field "tagsets".
type UnitDict = dict[str, list[list[str]] | str]
