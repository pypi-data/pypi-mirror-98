from functools import wraps
from .types.events import (UserJoined, UserLeft,
                           RoomData, JoinSuccess, JoinError,
                           CriticalError,
                           AddEvidence, RemoveEvidence,
                           AddBackground, RemoveBackground,
                           ReceivePlainMessage, ReceiveMessage)


class Handlers:
    def add_handler(self, event, func):
        if self.handlers.get(event) is not None:
            raise RuntimeError("event is already registered")

        if not isinstance(event, str) and hasattr(event, "_key"):
            event = event._key

        self.handlers[event] = func

    def on_event(self, event):
        def decorator(func):
            self.add_handler(event._key, func)
            return func
        return decorator

    def on_message(self, func):
        @self.on_event(ReceiveMessage)
        @wraps(func)
        async def decorator(message):
            message.user = self.users[message.user_id]
            await func(message)

        return decorator

    def on_plain_message(self, func):
        @self.on_event(ReceivePlainMessage)
        @wraps(func)
        async def decorator(message):
            message.user = self.users[message.user_id]
            await func(message)

        return decorator

    def on_start(self, func):
        self.add_handler("start", func)
        return func

    def on_info(self, func):
        self.add_handler(RoomData, func)
        return func

    def on_stop(self, func):
        self.add_handler("stop", func)
        return func

    def on_join_error(self, func):
        self.add_handler(JoinError, func)
        return func

    def on_critical_error(self, func):
        @wraps(func)
        async def decorator(message):
            await func(message)
            await self.close()

        self.add_handler(CriticalError, decorator)
        return decorator

    def on_join_success(self, func):
        self.add_handler(JoinSuccess, func)
        return func

    def on_new_evidence(self, func):
        self.add_handler(AddEvidence, func)
        return func

    def on_remove_evidence(self, func):
        self.add_handler(RemoveEvidence, func)
        return func

    def on_new_background(self, func):
        self.add_handler(AddBackground, func)
        return func

    def on_remove_background(self, func):
        self.add_handler(RemoveBackground, func)
        return func

    def on_user_join(self, func):
        self.add_handler(UserJoined, func)
        return func

    def on_user_left(self, func):
        self.add_handler(UserLeft, func)
        return func
