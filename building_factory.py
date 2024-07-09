from abc import ABC, abstractmethod


class IBuilding(ABC):
    def __init__(self, building_config, x_position) -> None:
        pass
    @abstractmethod
    def call_to_elevator(self):
        pass
    @abstractmethod
    def update(self):
        pass

class IBUildingFactory(ABC):
    def __init__(self) -> None:
        pass
    @abstractmethod
    def create_building(self, building_config, x_position) ->IBuilding:
        pass


