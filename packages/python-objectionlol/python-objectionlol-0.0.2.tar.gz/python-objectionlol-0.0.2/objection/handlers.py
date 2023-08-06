from functools import wraps


class Handlers:
    def add_handler(self, event, func):
        if self.handlers.get(event) is not None:
            raise RuntimeError("event is already registered")
        self.handlers[event] = func

    def on_event(self, event):
        def decorator(func):
            self.add_handler(event._key, func)
            return func
        return decorator

    def on_message(self, func):
        @wraps(func)
        async def decorator(message):
            message.user = self.users[message.user_id]
            await func(message)

        self.add_handler("receive_message", decorator)

        return decorator

    def on_plain_message(self, func):
        @wraps(func)
        async def decorator(message):
            message.user = self.users[message.user_id]
            await func(message)

        self.add_handler("receive_plain_message", decorator)

        return decorator

    def on_start(self, func):
        self.add_handler("start", func)
        return func

    def on_stop(self, func):
        self.add_handler("stop", func)
        return func

    def on_join_error(self, func):
        self.add_handler("join_error", func)
        return func

    def on_critical_error(self, func):
        @wraps(func)
        async def decorator(message):
            await func(message)
            await self.close()

        self.add_handler("critical_error", decorator)
        return decorator

    def on_join_success(self, func):
        self.add_handler("join_success", func)
        return func
