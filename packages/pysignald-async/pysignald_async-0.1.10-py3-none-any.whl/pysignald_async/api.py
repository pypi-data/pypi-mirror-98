"""
The output of the signald's "protocol" request only covers signald's v1 requests.
This module adds few bindings for v0 requests that should be useful.
"""
import asyncio
import typing

from pysignald_async.error import SignaldException
from pysignald_async.generated import *
import pysignald_async.util as util


class SignaldAPI(SignaldGeneratedAPI):
    async def get_response_and_wait_for(
        self, request: dict, validator: typing.Callable
    ):
        """
        Some API v0 calls actually triggers 2 separate events, so this
        method allows to easily await for both.

        :param request: The JSON request, as python dict
        :param validator: A callable that will receive all subsequent
            to identify the expected second response.
        """
        future = self.get_future_for(validator)
        try:
            await self.get_response(request)
        except SignaldException:
            self.specific_handlers.remove(future.handler)
            future.cancel()
            raise
        else:
            await future

    async def subscribe(self, username: str):
        """
        Starts receiving messages for the account identified by the argument
        username (a phone number).

        :param username: Phone number of the account.
        """
        await self.get_response_and_wait_for(
            request={"type": "subscribe", "username": username},
            validator=lambda response: response.get("type") == "listen_started"
            and response.get("data") == username,
        )

    async def unsubscribe(self, username: str):
        """
        Stops receiving message for an phone 'username'.

        :param username: Phone number of the account.
        """
        await self.get_response({"type": "unsubscribe", "username": username})

    async def verify(self, username: str, code: str):
        """
        Completes the registration process with the SMS code

        :param username: Phone number of the account.
        :param code: The code received by SMS.
        """
        await self.get_response({"type": "verify", "username": username, "code": code})

    async def register(self, username: str, captcha: str = None):
        """
        Register signald as the primary signal device for a phone number.
        To complete to process, the :func:`SignaldAPI.verify` coroutine
        must then be awaited with the code received by SMS.

        :param username: Phone number of the account.
        :param captcha: Might be needed. Checked the `signald wiki <https://gitlab.com/signald/signald/-/wikis/Captchas>`_
            for more info.
        """
        payload = {"type": "register", "username": username}
        if captcha is not None:
            payload["captcha"] = captcha
        await self.get_response(payload)

    async def list_accounts(self) -> JsonAccountListv0:
        """
        List the signald accounts.
        """
        data = await self.get_response({"type": "list_accounts"})
        return JsonAccountListv0(**data)

    def handle_message(self, payload):
        envelope = JsonMessageEnvelopev1(**payload.get("data", dict()))
        self.handle_envelope(envelope)

    def handle_envelope(self, envelope: JsonMessageEnvelopev1):
        """
        Called when receiving a message after being subscribed.
        Override this method to trigger events when receiving messages, typing notifications, etc.
        """
        print(envelope)
