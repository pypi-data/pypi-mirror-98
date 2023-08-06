from enum import Enum


class NotFoundOption(Enum):
    FLOOR = "floor"
    CEIL = "ceil"


class RequestType(Enum):
    TRIVIA = "trivia"
    MATH = "math"
    YEAR = "year"
    DATE = "date"
