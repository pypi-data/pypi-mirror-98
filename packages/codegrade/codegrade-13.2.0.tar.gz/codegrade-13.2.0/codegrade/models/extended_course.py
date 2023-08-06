"""The module that defines the ``ExtendedCourse`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Sequence, Type

import cg_request_args as rqa

from ..parsers import ParserFor
from ..utils import to_dict
from .assignment import Assignment
from .course import Course
from .course_snippet import CourseSnippet
from .group_set import GroupSet


@dataclass
class ExtendedCourse(Course):
    """The way this class will be represented in extended JSON."""

    #: The assignments connected to this assignment.
    assignments: "Sequence[Assignment]"
    #: The groups sets of this course.
    group_sets: "Sequence[GroupSet]"
    #: The snippets of this course.
    snippets: "Sequence[CourseSnippet]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: Course.data_parser.parser.combine(
            rqa.FixedMapping(
                rqa.RequiredArgument(
                    "assignments",
                    rqa.List(ParserFor.make(Assignment)),
                    doc="The assignments connected to this assignment.",
                ),
                rqa.RequiredArgument(
                    "group_sets",
                    rqa.List(ParserFor.make(GroupSet)),
                    doc="The groups sets of this course.",
                ),
                rqa.RequiredArgument(
                    "snippets",
                    rqa.List(ParserFor.make(CourseSnippet)),
                    doc="The snippets of this course.",
                ),
            )
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["assignments"] = to_dict(self.assignments)
        res["group_sets"] = to_dict(self.group_sets)
        res["snippets"] = to_dict(self.snippets)
        res["id"] = to_dict(self.id)
        res["name"] = to_dict(self.name)
        res["created_at"] = to_dict(self.created_at)
        res["virtual"] = to_dict(self.virtual)
        res["lti_provider"] = to_dict(self.lti_provider)
        res["state"] = to_dict(self.state)
        res["tenant_id"] = to_dict(self.tenant_id)
        res["copy_lock_date"] = to_dict(self.copy_lock_date)
        return res

    @classmethod
    def from_dict(
        cls: Type["ExtendedCourse"], d: Dict[str, Any]
    ) -> "ExtendedCourse":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            assignments=parsed.assignments,
            group_sets=parsed.group_sets,
            snippets=parsed.snippets,
            id=parsed.id,
            name=parsed.name,
            created_at=parsed.created_at,
            virtual=parsed.virtual,
            lti_provider=parsed.lti_provider,
            state=parsed.state,
            tenant_id=parsed.tenant_id,
            copy_lock_date=parsed.copy_lock_date,
        )
        res.raw_data = d
        return res
