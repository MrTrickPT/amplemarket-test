"""Registry Class."""

import abc

from src.tasks import PredictorTask, PreprocessorTask


class Registry(abc.ABC):
    """Registry class."""

    _components: dict[str, type] = {}

    @classmethod
    def get_all(cls: type["Registry"]) -> list[str]:
        """All method for registry."""
        return list(cls._components.keys())

    @classmethod
    def get(cls: type["Registry"], name: str) -> type:
        """Get method."""
        return cls._components[name]

    @classmethod
    def register(cls: type["Registry"], name: str, component_type: type) -> None:
        """Register method."""
        cls._components[name] = component_type


class TaskRegistry(Registry):
    """Task Registry Class."""

    _components = {
        "preprocessor": PreprocessorTask,
        "predictor": PredictorTask,
    }
