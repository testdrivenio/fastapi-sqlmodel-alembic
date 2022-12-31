import abc

from sqlmodel import SQLModel

status_name_cache = {}

class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, batch: dict):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference: int) -> dict:
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, reference: int) -> dict:
        raise NotImplementedError

    """
        @abc.abstractmethod  # (1)
        def modify(self, batch: dict) -> dict:
            raise NotImplementedError  # (2)
    """