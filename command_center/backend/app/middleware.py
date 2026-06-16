"""Timing middleware — makes the performance budget OBSERVABLE, not aspirational.

Stamps every response with ``X-Response-Time-Ms`` so the frontend StatusBar can show real latency
and the budget (p95 < 200 ms on cached daily data) can be watched rather than assumed. Payload size
is already available to the client via the standard ``Content-Length`` header.
"""

from __future__ import annotations

import time

from starlette.types import ASGIApp, Message, Receive, Scope, Send


class TimingMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        start = time.perf_counter()

        async def send_wrapper(message: Message) -> None:
            if message["type"] == "http.response.start":
                elapsed_ms = (time.perf_counter() - start) * 1000.0
                message.setdefault("headers", []).append(
                    (b"x-response-time-ms", f"{elapsed_ms:.1f}".encode())
                )
            await send(message)

        await self.app(scope, receive, send_wrapper)
