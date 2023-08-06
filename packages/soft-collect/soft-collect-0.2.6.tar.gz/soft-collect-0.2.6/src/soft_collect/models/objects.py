from dataclasses import dataclass


@dataclass
class ObjResult:
    """Class for Objects Query Result"""

    key: str
    part: int
    obj: bytes
    idcas: str = ""
