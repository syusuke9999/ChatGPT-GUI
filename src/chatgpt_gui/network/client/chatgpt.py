###################################################################################################
#                              MIT Licence (C) 2022 Cubicpath@Github                              #
###################################################################################################
"""Defines the ChatGPT-GUI HTTP Client."""
from __future__ import annotations

__all__ = (
    'Client',
)

import json
import os
from typing import Any
from uuid import UUID

from PySide6.QtCore import *

from ...constants import *
from ...models import CaseInsensitiveDict
from ...utils import decode_url
from ...utils import hide_windows_file
from ..manager import NetworkSession
from ..manager import Request
from ..manager import Response
from .auth import Authenticator
from .structures import Action
from .structures import Conversation
from .structures import Message


class Client(QObject):
    """Asynchronous HTTP REST Client that interfaces with ChatGPT."""

    authenticationRequired = Signal()
    receivedMessage = Signal(Message, Conversation)

    def __init__(self, parent: QObject, **kwargs) -> None:
        """Initialize OpenAI Client.

        Order of precedence for session token::

            1. session_token kwarg value
            2. CHATGPT_SESSION_AUTH environment variable
            3. user's .session config file (Created by application)

        :keyword session_token: Session token, allows for creation of access tokens.
        """
        super().__init__(parent)
        self.receivedMessage.connect(lambda msg, convo: print(f'Conversation: {convo.uuid} | {msg}'))

        self.authenticator = Authenticator(self)
        self.authenticator.authenticationSuccessful.connect(self.new_session)

        self.conversations: dict[UUID, Conversation] = {}
        self.host: str = 'chat.openai.com'
        self.models: list[str] | None = None

        self._first_request: bool = True
        self._access_token: str | None = None
        self._session_token: str | None = kwargs.pop('session_token', os.getenv('CHATGPT_SESSION_AUTH', None))
        if self._session_token is None and CG_SESSION_PATH.is_file():
            self._session_token = CG_SESSION_PATH.read_text(encoding='utf8').strip()

        self.session: NetworkSession = NetworkSession(self)
        self.session.headers = CaseInsensitiveDict({
            'Accept': '*/*',
            'Accept-Encoding': ', '.join(('gzip', 'deflate', 'br')),
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Host': self.host,
            'If-None-Match': '"zh3ivhmesm13w"',
            'Origin': 'https://chat.openai.com',
            'Referer': 'https://chat.openai.com/chat',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'Sec-GPC': '1',
            'TE': 'trailers',
            'User-Agent': CG_USER_AGENT,
            'X-OpenAI-Assistant-App-Id': '',
        })

        if self.session_token:
            self.set_cookie('__Secure-next-auth.session-token', self.session_token)

    @property
    def api_root(self) -> str:
        """Root of sent API requests."""
        return f'https://{self.host}/'

    @property
    def access_token(self) -> str | None:
        """Bearer token to authenticate self to API endpoints."""
        return self._access_token

    @access_token.setter
    def access_token(self, value: str) -> None:
        value = decode_url(value)

        self._access_token = value.strip()
        self.session.headers['Authorization'] = f'Bearer {self._access_token}'

    @access_token.deleter
    def access_token(self) -> None:
        self._access_token = None
        if 'Authorization' in self.session.headers:
            self.session.headers.pop('Authorization')

    @property
    def session_token(self) -> str | None:
        """Bearer token to authenticate self to API endpoints."""
        return self._session_token

    @session_token.setter
    def session_token(self, value: str) -> None:
        value = decode_url(value)

        self._session_token = value.strip()
        self.set_cookie('__Secure-next-auth.session-token', value)

        hide_windows_file(CG_SESSION_PATH, unhide=True)
        CG_SESSION_PATH.write_text(self._session_token, encoding='utf8')
        hide_windows_file(CG_SESSION_PATH)

    @session_token.deleter
    def session_token(self) -> None:
        self._session_token = None
        self.delete_cookie('__Secure-next-auth.session-token')
        if CG_SESSION_PATH.is_file():
            CG_SESSION_PATH.unlink()

    def _get(self, path: str, update_auth_on_401: bool = True, **kwargs) -> Response:
        """Get a :py:class:`Response` from ChatGPT.

        :param path: path to append to the API root
        :param update_auth_on_401: run self._refresh_auth if response status code is 401 Unauthorized
        :param kwargs: Key word arguments to pass to the requests GET Request.
        """
        if self._first_request:
            self._first_request = False
            self._get('chat')
            self.refresh_auth()

        response: Response = self.session.get(self.api_root + path.strip(), wait_until_finished=True, **kwargs)

        if session_token := self.session.cookies.get('__Secure-next-auth.session-token'):
            self.session_token = session_token

        if response.code and not response.ok:
            # Handle errors
            if response.code == 401 and update_auth_on_401 and self.access_token is not None:
                self.refresh_auth()
                response = self._get(path, False, **kwargs)

        return response

    def get_models(self) -> list[dict[str, Any]]:
        """Get the list of models to use with ChatGPT.

        :return: List of model data. The "slug" key is the model name.
        """
        return self._get('backend-api/models').json['models']

    def send_message(self, message_text: str, conversation: Conversation) -> None:
        """Send a message and emit the AI's response through `the `receivedMessage`` signal.

        Automatically handles the conversation id and last message id.

        :param message_text: Message to send.
        :raises ValueError: If Response couldn't be parsed as a text/event-stream.
        """
        if self.models is None:
            self.models = [model['slug'] for model in self.get_models()]

        if conversation.messages:
            parent_message: Message = conversation.messages[-1]
        else:
            parent_message = Message()

        message: Message = Message(text=message_text)
        action: Action = Action(self.models[0], conversation, [message], parent_message)

        request: Request = Request(
            'POST', self.api_root + 'backend-api/conversation',
            headers={'Accept': 'text/event-stream', 'Content-type': 'application/json'},
            json=action.to_json(), timeout=60.0,
        )

        response: Response = request.send(self.session, wait_until_finished=True)

        # Get the finished stream from the text/event-stream
        # Index -1 Is empty string, as the response ends with 2 newlines
        # Index -2 Is the "[DONE]", signifier
        # Index -3 Is the finished product
        try:
            last_stream: str = response.text.split('\n\n')[-3]
        except IndexError as e:
            raise ValueError(f'Message response is not a text/event-stream ({response.text}).') from e

        json_response: dict[str, Any] = json.loads(last_stream.removeprefix('data: ').strip())
        response_message: Message = Message.from_json(json_response['message'])

        conversation.messages.extend(action.messages)
        conversation.messages.append(response_message)

        if conversation.uuid is None:
            conversation.uuid = UUID(json_response['conversation_id'])

        if conversation.uuid not in self.conversations:
            self.conversations[conversation.uuid] = conversation

        self.receivedMessage.emit(response_message, conversation)

    def hidden_token(self) -> str:
        """:return: The first and last 3 characters of the session token, seperated by periods."""
        key = self.session_token
        if key is not None and len(key) > 6:
            return f'{key[:3]}{"." * 50}{key[-3:]}'
        return 'None'

    def refresh_auth(self) -> None:
        """Refresh authentication to OpenAI servers.

        token MUST have a value for this to work.
        """
        response = self._get('api/auth/session')

        if session_token := self.session.cookies.get('__Secure-next-auth.session-token'):
            self.session_token = session_token

        if token := response.json.get('accessToken'):
            self.access_token = token

    def signin(self, username: str, password: str) -> None:
        """Signin to OpenAI using the specified username and password.

        :param username: Username to signin to (email address).
        :param password: Password associated with username.
        """
        self.authenticator.username = username
        self.authenticator.password = password
        self.authenticator.authenticate()

    def new_session(self, session_token: str) -> None:
        """Call with new session token provided by authenticator.

        :param session_token: New session token to use.
        """
        self.session_token = session_token

    def delete_cookie(self, name: str) -> None:
        """Delete given cookie if cookie exists."""
        self.session.clear_cookies(self.host, '/', name)

    def set_cookie(self, name: str, value: str) -> None:
        """Set cookie value in Cookie jar."""
        self.session.set_cookie(name, value, self.host)
