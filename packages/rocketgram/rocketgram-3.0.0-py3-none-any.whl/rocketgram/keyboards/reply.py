# Copyright (C) 2015-2020 by Vd.
# This file is part of Rocketgram, the modern Telegram bot framework.
# Rocketgram is released under the MIT License (see LICENSE).


from .keyboard import Keyboard
from .. import api


class ReplyKeyboard(Keyboard):
    __slots__ = ('__selective', '__one_time', '__resize')

    def __init__(self, *, selective=False, one_time=False, resize=True):
        super().__init__()

        self.__selective = selective
        self.__one_time = one_time
        self.__resize = resize

    def set_selective(self, selective=False):
        self.__selective = selective

    selective = property(fget=lambda self: self.__selective, fset=set_selective)

    def set_one_time(self, one_time=False):
        self.__one_time = one_time

    one_time = property(fget=lambda self: self.__one_time, fset=set_one_time)

    def set_resize(self, resize=False):
        self.__resize = resize

    resize = property(fget=lambda self: self.__resize, fset=set_resize)

    def text(self, text: str) -> 'ReplyKeyboard':
        self.add(api.KeyboardButton(text=text))
        return self

    def contact(self, text: str) -> 'ReplyKeyboard':
        self.add(api.KeyboardButton(text=text, request_contact=True))
        return self

    def location(self, text: str) -> 'ReplyKeyboard':
        self.add(api.KeyboardButton(text=text, request_location=True))
        return self

    def poll(self, text: str, request_poll: 'api.PollType') -> 'ReplyKeyboard':
        self.add(api.KeyboardButton(text=text, request_poll=api.KeyboardButtonPollType(request_poll)))
        return self

    def row(self) -> 'ReplyKeyboard':
        return super().row()

    def render(self) -> 'api.ReplyKeyboardMarkup':
        return api.ReplyKeyboardMarkup(self.render_buttons(),
                                       resize_keyboard=self.resize if self.resize else None,
                                       one_time_keyboard=self.one_time if self.one_time else None,
                                       selective=self.selective if self.selective else None)
