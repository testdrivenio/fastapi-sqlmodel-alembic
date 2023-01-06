import abc
from typing import List

status_name_cache = {}


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, batch: dict) -> dict:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference: int) -> dict:
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, reference: int) -> None:
        raise NotImplementedError

    @abc.abstractmethod  # (1)
    def modify(self, reference: int, batch: dict) -> None:
        raise NotImplementedError  # (2)

    @abc.abstractmethod  # (1)
    def list_resource(self) -> List[dict]:
        raise NotImplementedError  # (2)
