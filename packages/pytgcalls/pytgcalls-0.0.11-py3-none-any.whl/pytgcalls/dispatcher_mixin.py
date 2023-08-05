#  tgcalls - Python binding for tgcalls (c++ lib by Telegram)
#  pytgcalls - Library connecting python binding for tgcalls and Pyrogram
#  Copyright (C) 2020-2021 Il`ya (Marshal) <https://github.com/MarshalX>
#
#  This file is part of tgcalls and pytgcalls.
#
#  tgcalls and pytgcalls is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  tgcalls and pytgcalls is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License v3
#  along with tgcalls. If not, see <http://www.gnu.org/licenses/>.

from .dispatcher import Dispatcher


class DispatcherMixin:

    def __init__(self, actions):
        self._dispatcher = Dispatcher(actions)

    def add_handler(self, callback, action) -> bool:
        return self._dispatcher.add_handler(callback, action)

    def remove_handler(self, callback, action) -> bool:
        return self._dispatcher.remove_handler(callback, action)

    def trigger_handlers(self, action, instance, *args, **kwargs):
        return self._dispatcher.trigger_handlers(action, instance, *args, **kwargs)
