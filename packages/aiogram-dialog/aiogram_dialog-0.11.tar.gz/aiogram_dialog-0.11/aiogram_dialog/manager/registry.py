import asyncio
from contextvars import copy_context
from functools import partial
from typing import Dict, Optional, Union

from aiogram import Dispatcher, Bot
from aiogram.dispatcher.filters.state import State
from aiogram.dispatcher.handler import Handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.storage import FSMContextProxy
from aiogram.types import User, Chat

from .intent import DialogUpdateEvent
from .manager import DialogManagerImpl
from .protocols import ManagedDialogProto, DialogRegistryProto, DialogManager
from .stack import DialogStack
from .update_handler import handle_update


class DialogRegistry(BaseMiddleware, DialogRegistryProto):
    dialogs: Dict[str, ManagedDialogProto]

    def __init__(self, dp: Dispatcher, dialogs: Optional[Dict[str, ManagedDialogProto]] = None):
        super().__init__()
        self.dp = dp
        if dialogs is None:
            dialogs = {}
        self.dialogs = dialogs
        self.update_handler = Handler(dp, middleware_key="aiogd_update")
        self._register_middleware()
        self.register_update_handler(handle_update, state="*")

    def register(self, dialog: ManagedDialogProto, *args, **kwargs):
        name = dialog.states_group_name()
        if name in self.dialogs:
            raise ValueError(f"StatesGroup `{name}` is already used")
        self.dialogs[name] = dialog
        dialog.register(self, self.dp, *args, **kwargs)

    def _register_middleware(self):
        self.dp.setup_middleware(self)

    def find_dialog(self, state: Union[str, State]) -> ManagedDialogProto:
        if isinstance(state, str):
            group, *_ = state.partition(":")
        else:
            group = state.group.__full_group_name__
        return self.dialogs[group]

    async def on_pre_process_message(self, event, data: dict):
        proxy = await FSMContextProxy.create(
            self.dp.current_state()  # there is no state in data at this moment
        )
        manager = DialogManagerImpl(
            event,
            DialogStack(proxy),
            proxy,
            self,
            data,
        )
        data["dialog_manager"] = manager

    on_pre_process_callback_query = on_pre_process_message
    on_pre_process_aiogd_update = on_pre_process_message

    async def on_post_process_message(self, _, result, data: dict):
        manager: DialogManager = data.pop("dialog_manager")
        await manager.close_manager()

    on_post_process_callback_query = on_post_process_message
    on_post_process_aiogd_update = on_post_process_message

    def register_update_handler(self, callback, *custom_filters, run_task=None, **kwargs) -> None:
        filters_set = self.dp.filters_factory.resolve(
            self.update_handler, *custom_filters, **kwargs
        )
        self.update_handler.register(self.dp._wrap_async_task(callback, run_task), filters_set)

    async def notify(self, event: DialogUpdateEvent) -> None:
        callback = lambda: asyncio.create_task(self._process_update(event))

        asyncio.get_running_loop().call_soon(
            callback,
            context=copy_context()
        )

    async def _process_update(self, event: DialogUpdateEvent):
        Bot.set_current(event.bot)
        User.set_current(event.from_user)
        Chat.set_current(event.chat)
        await self.update_handler.notify(event)
