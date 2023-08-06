from typing import Callable, Any


class Base:
    def __init__(
        self, *, set_data: Callable[[Any], Any], resolve_data: Callable[[Any], Any],
        object_hook: Callable[[Any], Any], json_serial: Callable[[Any], Any]
    ) -> None:
        self.set_data = set_data
        self.object_hook = object_hook
        self.json_serial = json_serial
        self.resolve_data = resolve_data
