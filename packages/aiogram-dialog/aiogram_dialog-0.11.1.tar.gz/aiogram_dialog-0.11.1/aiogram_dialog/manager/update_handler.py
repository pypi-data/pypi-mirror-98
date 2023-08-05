from logging import getLogger

from .intent import DialogUpdateEvent, DialogStartEvent, Action, DialogSwitchEvent
from .manager import DialogManager

logger = getLogger(__name__)


async def handle_update(event: DialogUpdateEvent, dialog_manager: DialogManager):
    if isinstance(event, DialogStartEvent):
        await dialog_manager.start(state=event.new_state, data=event.data, reset_stack=event.reset_stack)
    elif isinstance(event, DialogSwitchEvent):
        await dialog_manager.switch_to(state=event.new_state)
        await dialog_manager.dialog().show(dialog_manager)
    elif event.action is Action.UPDATE:
        if not dialog_manager.context:
            logger.warning("No context found")
            return
        if event.data:
            for k, v in event.data.items():
                dialog_manager.context.set_data(k, v)
        await dialog_manager.dialog().show(dialog_manager)
    elif event.action is Action.DONE:
        await dialog_manager.done(result=event.data)
