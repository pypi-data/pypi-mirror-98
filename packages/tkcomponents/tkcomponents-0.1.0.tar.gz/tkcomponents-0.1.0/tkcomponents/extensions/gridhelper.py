from objectextensions import Extension

from ..component import Component


class GridHelper(Extension):
    @staticmethod
    def extend(target_cls):
        Extension._set(target_cls, "_apply_frame_stretch", GridHelper.__apply_frame_stretch)

    @staticmethod
    def can_extend(target_cls):
        return issubclass(target_cls, Component)

    def __apply_frame_stretch(self, rows=(), columns=()):
        for row_index in rows:
            self._frame.rowconfigure(row_index, weight=1)
        for column_index in columns:
            self._frame.columnconfigure(column_index, weight=1)
