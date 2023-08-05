from __future__ import annotations

from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Sequence, Union

from aiogram.types import ForceReply as _ForceReply
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from aiogram.utils.deep_linking import get_start_link
from urllib import parse
from config import BOT_START_LINK

__all__ = ['ReplyKeyboard', 'InlineKeyboard', 'ForceReply', 'Button', 'InlineButton']

ForceReply = _ForceReply()


class InlineButton(InlineKeyboardButton):
    def __init__(self, text: str,
                 callback: Union[str, bool] = None,
                 url: Union[str, bool] = None,
                 start_param: Union[str, bool] = None,
                 switch_iquery: Union[str, bool] = None,
                 switch_iquery_current: Union[str, bool] = None
                 ):
        args_count = sum(1 for k, v in locals().items() if k not in ['self', '__class__'] and v is not None)
        assert args_count == 2, 'You must specify exactly 1 arg besides text'

        if url is True:
            url = text
        elif start_param is True:
            start_param = text
        elif callback is True:
            callback = text
        elif switch_iquery is True:
            switch_iquery = text
        elif switch_iquery_current is True:
            switch_iquery_current = text

        if start_param:
            url = BOT_START_LINK.format(start_param)

        super().__init__(text,
                         url=url,
                         callback_data=callback,
                         switch_inline_query=switch_iquery,
                         switch_inline_query_current_chat=switch_iquery_current
                         )

    def __iadd__(self, data: str):
        if self.url is not None:
            self.url += data
        elif self.callback_data is not None:
            self.callback_data += data
        elif self.switch_inline_query is not None:
            self.switch_inline_query += data
        elif self.switch_inline_query_current_chat is not None:
            self.switch_inline_query_current_chat += data

        return self


# def InlineButton(text: str,
#                  url: Union[str, bool] = None,
#                  start_param: Union[str, bool] = None,
#                  callback: Union[str, bool] = None,
#                  switch_iquery: Union[str, bool] = None,
#                  switch_iquery_current: Union[str, bool] = None
#                  ):
#     return InlineKeyboardButton(text, url=url, callback_data=callback, switch_inline_query=switch_iquery,
#                                 switch_inline_query_current_chat=switch_iquery_current)


Button = KeyboardButton


class Keyboard():
    BUTTONS: list[str, KeyboardButton, InlineKeyboardButton] = []
    rows_width: Sequence[int]

    @classmethod
    @property
    def constants(cls):
        return [prop for prop in vars(cls) if prop.isupper()]

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)

        for prop in instance.constants:
            prop_copy = deepcopy(getattr(instance, prop))
            setattr(instance, prop, prop_copy)

        return instance

    @abstractmethod
    def from_buttons(self):
        """This method should add buttons to keyboard from self.BUTTONS.
        Also you need to update self.BUTTONS with real buttons' data."""

    @abstractmethod
    def load_keyboard(self):
        """This method should add buttons to keyboard from class constants and self.BUTTONS.
        Also you need to update self's contants and self.BUTTONS with real buttons' data."""

    def append(self, keyboard, button):
        """Append button according self.rows_width."""

        rows_width = self.rows_width

        if not keyboard:
            keyboard.append([])

        try:
            last_row = keyboard[-1]
            last_row_width = rows_width[len(keyboard) - 1]

            if len(last_row) < last_row_width:
                keyboard[-1].append(button)
            else:
                keyboard.append([button])
        except IndexError:  # row len does not specified
            getattr(self, 'insert')(button)


class InlineKeyboard(Keyboard, InlineKeyboardMarkup):

    def __init__(self, rows_width: Sequence[int] = (), default_width: int = 1):
        super().__init__(row_width=default_width)
        self.rows_width = rows_width

        self.load_keyboard()

    @staticmethod
    def get_button_data(button: InlineKeyboardButton) -> str:
        if button.url is not None:
            return button.url
        if button.callback_data is not None:
            return button.callback_data
        if button.switch_inline_query is not None:
            return button.switch_inline_query
        if button.switch_inline_query_current_chat is not None:
            return button.switch_inline_query_current_chat

    def from_buttons(self):
        BUTTONS = []
        for button in self.BUTTONS:
            if isinstance(button, str):
                button = InlineButton(button, callback=True)

            button_data = self.get_button_data(button)
            BUTTONS.append(button_data)
            self.append(self.inline_keyboard, button)

        self.BUTTONS = BUTTONS

    def load_keyboard(self):
        for prop in self.constants:

            if prop == 'BUTTONS':
                self.from_buttons()
                continue

            button = getattr(self, prop)

            if button is None:
                continue

            if isinstance(button, str):
                button = InlineButton(button, callback=True)

            button_data = self.get_button_data(button)
            self.append(self.inline_keyboard, button)


class ReplyKeyboard(Keyboard, ReplyKeyboardMarkup):

    def __init__(self, rows_width: Sequence[int] = (), default_width: int = 2):
        super().__init__(row_width=default_width, resize_keyboard=True)
        self.rows_width = rows_width

        self.load_keyboard()

    def from_buttons(self):
        BUTTONS = []
        for button in self.BUTTONS:
            if isinstance(button, str):
                button = KeyboardButton(text=button)

            BUTTONS.append(button.text)
            self.append(self.keyboard, button)

        self.BUTTONS = BUTTONS

    def load_keyboard(self):
        for prop in self.constants:

            if prop == 'BUTTONS':
                self.from_buttons()
                continue

            button = getattr(self, prop)

            if button is None:
                continue

            if isinstance(button, str):
                button = KeyboardButton(text=button)

            self.append(self.keyboard, button)
