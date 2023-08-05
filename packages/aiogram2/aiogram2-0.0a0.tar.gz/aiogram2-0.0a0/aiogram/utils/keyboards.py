from __future__ import annotations

from typing import Sequence

from aiogram.types import ForceReply as _ForceReply
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton

__all__ = ['ReplyKeyboard', 'InlineKeyboard', 'ForceReply', 'Buttons', 'IButtons']

ForceReply = _ForceReply()


class Buttons:

    @staticmethod
    def callback(text, data=None):
        if data is None:
            data = text
        return InlineKeyboardButton(text, callback_data=data)

    @staticmethod
    def url(text, link=None):
        if link is None:
            link = text
        return InlineKeyboardButton(text, url=link)

    @staticmethod
    def switch_iquery(text, query=None):
        if query is None:
            query = text
        return InlineKeyboardButton(text, switch_inline_query=query)

    @staticmethod
    def switch_iquery_current(text, query=None):
        if query is None:
            query = text
        return InlineKeyboardButton(text, switch_inline_query_current_chat=query)

    @staticmethod
    def ask_contact(text):
        return KeyboardButton(text, request_contact=True)

    @staticmethod
    def ask_location(text):
        return KeyboardButton(text, request_location=True)


class KeyboardMixin:
    BUTTONS: list[str, KeyboardButton, InlineKeyboardButton] = []
    rows_width: Sequence[int]

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


class InlineKeyboard(KeyboardMixin, InlineKeyboardMarkup):

    def __init__(self, rows_width: Sequence[int] = (), default_width: int = 1):
        super().__init__(row_width=default_width)
        self.rows_width = rows_width

        if self.BUTTONS:
            self.load_buttons()
        else:
            self.load_vars()

    @staticmethod
    def get_real_value(button: InlineKeyboardButton) -> str:
        if button.url is not None:
            return button.url
        if button.callback_data is not None:
            return button.callback_data
        if button.switch_inline_query is not None:
            return button.switch_inline_query
        if button.switch_inline_query_current_chat is not None:
            return button.switch_inline_query_current_chat

    def load_buttons(self):
        for index, button in enumerate(self.BUTTONS):
            if isinstance(button, str):
                button = InlineKeyboardButton(text=button, callback_data=button)

            real_value = self.get_real_value(button)
            self.BUTTONS[index] = real_value
            self.append(self.inline_keyboard, button)

    def load_vars(self):
        for name, button in vars(self.__class__).items():
            if name.isupper():
                if isinstance(button, str):
                    button = InlineKeyboardButton(text=button, callback_data=button)

                real_value = self.get_real_value(button)
                setattr(self, name, real_value)
                self.append(self.inline_keyboard, button)


class ReplyKeyboard(KeyboardMixin, ReplyKeyboardMarkup):

    def __init__(self, rows_width: Sequence[int] = (), default_width: int = 2):
        super().__init__(row_width=default_width, resize_keyboard=True)
        self.rows_width = rows_width

        if self.BUTTONS:
            self.load_buttons()
        else:
            self.load_vars()

    def load_buttons(self):
        for index, button in enumerate(self.BUTTONS):
            if isinstance(button, str):
                button = KeyboardButton(text=button)

            self.BUTTONS[index] = button.text
            self.append(self.keyboard, button)

    def load_vars(self):
        for name, button in vars(self.__class__).items():
            if name.isupper():
                if isinstance(button, str):
                    button = KeyboardButton(text=button)

                setattr(self, name, button.text)
                self.append(self.keyboard, button)
