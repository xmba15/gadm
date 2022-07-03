"""
Supportive types for gadm library
"""

import enum

__all__ = ["AdministrativeDivisionLevel"]


class AdministrativeDivisionLevel(enum.IntEnum):
    """
    Level of Administrative Division specified by GADM Database
    """

    COUNTRY = 0
    STATE = 1
    DISTRICT = 2
    COMMUNE = 3
    MIN = COUNTRY
    MAX = COMMUNE
