"""The module that defines the ``FeedbackWithoutReplies`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Mapping, Optional, Type

import cg_request_args as rqa

from ..parsers import ParserFor
from ..utils import to_dict
from .feedback_base import FeedbackBase
from .user import User


@dataclass
class FeedbackWithoutReplies(FeedbackBase):
    """The JSON representation for feedback without replies.

    This representation is considered deprecated, as it doesn't include
    important information (i.e. replies)
    """

    #: A mapping between file id and a mapping that is between line and
    #: feedback. So for example: `{5: {0: 'Nice job!'}}` means that file with
    #: `id` 5 has feedback on line 0.
    user: "Mapping[str, Mapping[str, str]]"
    #: The authors of the user feedback. In the example above the author of the
    #: feedback 'Nice job!' would be at `{5: {0: $USER}}`.
    authors: "Mapping[str, Mapping[str, User]]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: FeedbackBase.data_parser.parser.combine(
            rqa.FixedMapping(
                rqa.RequiredArgument(
                    "user",
                    rqa.LookupMapping(rqa.LookupMapping(rqa.SimpleValue.str)),
                    doc=(
                        "A mapping between file id and a mapping that is"
                        " between line and feedback. So for example: `{5: {0:"
                        " 'Nice job!'}}` means that file with `id` 5 has"
                        " feedback on line 0."
                    ),
                ),
                rqa.RequiredArgument(
                    "authors",
                    rqa.LookupMapping(rqa.LookupMapping(ParserFor.make(User))),
                    doc=(
                        "The authors of the user feedback. In the example"
                        " above the author of the feedback 'Nice job!' would"
                        " be at `{5: {0: $USER}}`."
                    ),
                ),
            )
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["user"] = to_dict(self.user)
        res["authors"] = to_dict(self.authors)
        res["general"] = to_dict(self.general)
        res["linter"] = to_dict(self.linter)
        return res

    @classmethod
    def from_dict(
        cls: Type["FeedbackWithoutReplies"], d: Dict[str, Any]
    ) -> "FeedbackWithoutReplies":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            user=parsed.user,
            authors=parsed.authors,
            general=parsed.general,
            linter=parsed.linter,
        )
        res.raw_data = d
        return res
