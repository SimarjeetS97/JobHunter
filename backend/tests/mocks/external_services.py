from collections.abc import Awaitable, Callable


class MockEmailGateway:
    def __init__(self) -> None:
        self.sent_messages: list[dict[str, str]] = []

    async def send(self, *, to: str, subject: str, body: str) -> None:
        self.sent_messages.append({"to": to, "subject": subject, "body": body})


class FailingEmailGateway(MockEmailGateway):
    async def send(self, *, to: str, subject: str, body: str) -> None:  # type: ignore[override]
        raise TimeoutError("provider timeout")


def async_stub(result: object) -> Callable[..., Awaitable[object]]:
    async def _inner(*_: object, **__: object) -> object:
        return result

    return _inner
