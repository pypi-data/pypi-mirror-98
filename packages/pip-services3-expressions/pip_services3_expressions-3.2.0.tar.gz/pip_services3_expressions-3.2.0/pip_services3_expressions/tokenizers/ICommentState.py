# -*- coding: utf-8 -*-

from abc import ABC

from .ITokenizerState import ITokenizerState


class ICommentState(ITokenizerState, ABC):
    """
    Defines an interface for tokenizer state that processes comments.
    """
