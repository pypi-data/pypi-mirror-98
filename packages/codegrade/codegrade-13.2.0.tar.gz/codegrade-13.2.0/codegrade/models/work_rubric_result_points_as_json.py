"""The module that defines the ``WorkRubricResultPointsAsJSON`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa

from ..utils import to_dict


@dataclass
class WorkRubricResultPointsAsJSON:
    """Information about the rubric points of a single submission."""

    #: The maximal amount of points for this rubric, or None if logged in user
    #: doesn't have permission to see the rubric.
    max: "Optional[float]"
    #: The amount of point that is selected for this work, or None if the
    #: logged in user doesn't have permission to see the rubric.
    selected: "Optional[float]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "max",
                rqa.Nullable(rqa.SimpleValue.float),
                doc=(
                    "The maximal amount of points for this rubric, or None if"
                    " logged in user doesn't have permission to see the"
                    " rubric."
                ),
            ),
            rqa.RequiredArgument(
                "selected",
                rqa.Nullable(rqa.SimpleValue.float),
                doc=(
                    "The amount of point that is selected for this work, or"
                    " None if the logged in user doesn't have permission to"
                    " see the rubric."
                ),
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["max"] = to_dict(self.max)
        res["selected"] = to_dict(self.selected)
        return res

    @classmethod
    def from_dict(
        cls: Type["WorkRubricResultPointsAsJSON"], d: Dict[str, Any]
    ) -> "WorkRubricResultPointsAsJSON":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            max=parsed.max,
            selected=parsed.selected,
        )
        res.raw_data = d
        return res
