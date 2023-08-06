from typing import Any, Dict

import requests

from numbersapi_client.enums import *
from numbersapi_client.exceptions import *
from numbersapi_client.response_types import *


class NumbersAPIClient:
    BASE_URL = "http://numbersapi.com"
    params = {"json": True}

    def __init__(
        self,
        fragment: bool = False,
        default: str = None,
        min: int = None,
        max: int = None,
        notfound: NotFoundOption = None,
    ) -> None:
        if fragment:
            self.params["fragment"] = True

        if default:
            self.params["default"] = default

        if min:
            if not isinstance(min, int):
                raise InvalidOption(f"min option should be int, got {type(min)}")
            self.params["min"] = min

        if max:
            if not isinstance(max, int):
                raise InvalidOption(f"max option should be int, got {type(max)}")
            self.params["max"] = max

        if min and max and min > max:
            raise InvalidOption(f"max option should be >= min option, got min={min} & max={max}")

        if notfound:
            try:
                self.params["notfound"] = NotFoundOption(notfound).value
            except ValueError:
                raise InvalidOption(f"notfound option should be floor or ceil, got {notfound}")

    def __make_request(
        self, number: str, type: RequestType = RequestType.TRIVIA
    ) -> Dict[str, Any]:
        try:
            response = requests.get(f"{self.BASE_URL}/{number}/{type.value}", params=self.params)
        except Exception:
            raise InvalidAPIResponse("API is not responding")
        return response.json()

    def trivia(self, number: int = None) -> NumberResponse:
        if not number:
            number = "random"
        elif not isinstance(number, int):
            raise InvalidInput(f"number should be int, got {type(number)}")

        result = self.__make_request(number, type=RequestType.TRIVIA)
        return NumberResponse(**result)

    def math(self, number: int = None) -> NumberResponse:
        if not number:
            number = "random"
        elif not isinstance(number, int):
            raise InvalidInput(f"number should be int, got {type(number)}")

        result = self.__make_request(number, type=RequestType.MATH)
        return NumberResponse(**result)

    def year(self, number: int = None) -> YearResponse:
        if not number:
            number = "random"
        elif not isinstance(number, int):
            raise InvalidInput(f"number should be int, got {type(number)}")

        result = self.__make_request(number, type=RequestType.YEAR)
        return YearResponse(**result)

    def date(self, month: int = None, day: int = None) -> DateResponse:
        if month is None and day is None:
            number = "random"
        elif not isinstance(month, int) or not isinstance(day, int):
            raise InvalidInput(
                f"month and day should be of types int/int, got {type(month)}/{type(day)}"
            )
        elif month not in range(1, 13) or day not in range(1, 32):
            raise InvalidInput(f"{month}/{day} is not a proper date")
        else:
            number = f"{month}/{day}"

        result = self.__make_request(number, type=RequestType.DATE)
        return DateResponse(**result)
