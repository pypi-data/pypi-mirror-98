# -*- coding: future_annotations -*-
from typing import TYPE_CHECKING

from traitlets.config.configurable import SingletonConfigurable

if TYPE_CHECKING:
    from typing import Optional
    from nbsafety.safety import NotebookSafety as NotebookSafetyInstance


class NotebookSafety(SingletonConfigurable):
    _Xyud34_INSTANCE = None

    def __init__(self):
        super().__init__()
        # we need to keep another ref around for some reason to prevent a segfault
        # TODO: figure out why
        self.__class__._Xyud34_INSTANCE = self


class TraceManager(SingletonConfigurable):
    pass


def nbs() -> NotebookSafetyInstance:
    assert NotebookSafety.initialized()
    return NotebookSafety.instance()


def nbs_check_init() -> Optional[NotebookSafetyInstance]:
    if NotebookSafety.initialized():
        return NotebookSafety.instance()
    else:
        return None
