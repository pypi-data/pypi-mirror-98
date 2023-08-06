from typing import Sequence, Mapping, Union, List

ScalarT = Union[int, float, bool, str]
SerializableT = Union[ScalarT, List[ScalarT]]
SectionT = Mapping[str, SerializableT]
InifileT = Mapping[str, SectionT]