from pydantic import BaseModel

from settings import ChargemapSettings

settings = ChargemapSettings()


class Point(BaseModel):
    lat: float
    lng: float


class ScanSquare:
    def __init__(self, sw_point: Point, ne_point: Point) -> None:
        self._sw_point = sw_point
        self._ne_point = ne_point

    @property
    def ne_lat(self) -> float:
        return self._ne_point.lat

    @property
    def ne_lng(self) -> float:
        return self._ne_point.lng

    @property
    def sw_lat(self) -> float:
        return self._sw_point.lat

    @property
    def sw_lng(self) -> float:
        return self._sw_point.lng

    def move_to_the_right(self) -> None:
        self._ne_point.lng += settings.DELTA
        self._sw_point.lng += settings.DELTA

    def move_to_the_top(self) -> None:
        self._ne_point.lat += settings.DELTA
        self._sw_point.lat += settings.DELTA

    def returning_to_the_beginning_of_the_line(self) -> None:
        self._sw_point.lng = settings.SW_LNG
        self._ne_point.lng = self._sw_point.lng + settings.DELTA

    def right_border_check(self) -> bool:
        return self._sw_point.lng <= settings.NE_LNG

    def upper_border_check(self) -> bool:
        return self._sw_point.lat <= settings.NE_LAT

