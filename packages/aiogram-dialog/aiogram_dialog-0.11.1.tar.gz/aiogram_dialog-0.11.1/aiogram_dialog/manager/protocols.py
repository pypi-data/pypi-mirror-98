from typing import Optional, Any, Protocol, Union, Type, Dict

from aiogram import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContextProxy

from aiogram_dialog.data import DialogContext
from .intent import Intent, Data, DialogUpdateEvent, ChatEvent


class ManagedDialogProto(Protocol):
    def register(self, registry: "DialogRegistryProto", dp: Dispatcher, *args, **kwargs) -> None:
        pass

    def states_group_name(self) -> str:
        pass

    def states_group(self) -> Type[StatesGroup]:
        pass

    async def process_close(self, result: Any, manager: "DialogManager"):
        pass

    async def process_start(self, manager: "DialogManager", start_data: Any,
                            state: Optional[State] = None) -> None:
        pass

    async def show(self, manager: "DialogManager"):
        pass

    async def process_result(self, result: Any, manager: "DialogManager"):
        pass

    async def next(self, manager: "DialogManager"):
        pass

    async def back(self, manager: "DialogManager"):
        pass

    async def switch_to(self, state: State, manager: "DialogManager"):
        pass

    def find(self, widget_id) -> Optional[Any]:
        pass


class DialogRegistryProto(Protocol):
    def find_dialog(self, state: Union[State, str]) -> ManagedDialogProto:
        pass

    async def notify(self, event: DialogUpdateEvent) -> None:
        pass


class DialogManager(Protocol):
    context: Optional[DialogContext]
    proxy: FSMContextProxy
    event: ChatEvent
    data: Dict

    def dialog(self) -> ManagedDialogProto:
        pass

    def current_intent(self) -> Intent:
        pass

    async def close(self):
        pass

    async def done(self, result: Any = None):
        pass

    async def start(self, state: State, data: Data = None, reset_stack: bool = False):
        pass

    async def switch_to(self, state):
        pass

    def bg(self, user_id: Optional[int] = None, chat_id: Optional[int] = None) -> "BgManagerProto":
        pass

    async def close_manager(self) -> None:
        pass


class BgManagerProto(Protocol):
    def current_intent(self) -> Intent:
        pass

    async def done(self, result: Any = None):
        pass

    async def start(self, state: State, data: Data = None, reset_stack: bool = False):
        pass

    async def switch_to(self, state: State):
        pass

    async def update(self, data: Dict):
        pass

    def bg(self, user_id: Optional[int] = None, chat_id: Optional[int] = None) -> "BgManagerProto":
        pass
