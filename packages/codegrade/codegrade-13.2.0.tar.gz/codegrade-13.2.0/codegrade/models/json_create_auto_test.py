"""The module that defines the ``JsonCreateAutoTest`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Sequence, Type

import cg_request_args as rqa
from cg_maybe import Maybe, Nothing
from cg_maybe.utils import maybe_from_nullable

from ..parsers import ParserFor
from ..utils import to_dict
from .fixture_like import FixtureLike


@dataclass
class JsonCreateAutoTest:
    """"""

    #: The id of the assignment in which you want to create this AutoTest. This
    #: assignment should have a rubric.
    assignment_id: "int"
    #: The new setup script (per student) of the auto test.
    setup_script: Maybe["str"] = Nothing
    #: The new run setup script (global) of the auto test.
    run_setup_script: Maybe["str"] = Nothing
    #: If true all other files in the request will be used as new fixtures
    has_new_fixtures: Maybe["bool"] = Nothing
    #: The way to do grade calculation for this AutoTest.
    grade_calculation: Maybe["str"] = Nothing
    #: Should results be visible for students before the assignment is set to
    #: "done"?
    results_always_visible: Maybe["Optional[bool]"] = Nothing
    #: If `true` we will use the teacher revision if available when running
    #: tests.
    prefer_teacher_revision: Maybe["Optional[bool]"] = Nothing
    #: A list of old fixtures you want to keep
    fixtures: Maybe["Sequence[FixtureLike]"] = Nothing
    #: If true existing fixtures with the same name as one of the new fixtures
    #: are deleted and no renaming is performed.
    overwrite_duplicate_fixtures: "bool" = False

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "assignment_id",
                rqa.SimpleValue.int,
                doc=(
                    "The id of the assignment in which you want to create this"
                    " AutoTest. This assignment should have a rubric."
                ),
            ),
            rqa.OptionalArgument(
                "setup_script",
                rqa.SimpleValue.str,
                doc="The new setup script (per student) of the auto test.",
            ),
            rqa.OptionalArgument(
                "run_setup_script",
                rqa.SimpleValue.str,
                doc="The new run setup script (global) of the auto test.",
            ),
            rqa.OptionalArgument(
                "has_new_fixtures",
                rqa.SimpleValue.bool,
                doc=(
                    "If true all other files in the request will be used as"
                    " new fixtures"
                ),
            ),
            rqa.OptionalArgument(
                "grade_calculation",
                rqa.SimpleValue.str,
                doc="The way to do grade calculation for this AutoTest.",
            ),
            rqa.OptionalArgument(
                "results_always_visible",
                rqa.Nullable(rqa.SimpleValue.bool),
                doc=(
                    "Should results be visible for students before the"
                    ' assignment is set to "done"?'
                ),
            ),
            rqa.OptionalArgument(
                "prefer_teacher_revision",
                rqa.Nullable(rqa.SimpleValue.bool),
                doc=(
                    "If `true` we will use the teacher revision if available"
                    " when running tests."
                ),
            ),
            rqa.OptionalArgument(
                "fixtures",
                rqa.List(ParserFor.make(FixtureLike)),
                doc="A list of old fixtures you want to keep",
            ),
            rqa.DefaultArgument(
                "overwrite_duplicate_fixtures",
                rqa.SimpleValue.bool,
                doc=(
                    "If true existing fixtures with the same name as one of"
                    " the new fixtures are deleted and no renaming is"
                    " performed."
                ),
                default=lambda: False,
            ),
        ).use_readable_describe(True)
    )

    def __post_init__(self) -> None:
        self.setup_script = maybe_from_nullable(self.setup_script)
        self.run_setup_script = maybe_from_nullable(self.run_setup_script)
        self.has_new_fixtures = maybe_from_nullable(self.has_new_fixtures)
        self.grade_calculation = maybe_from_nullable(self.grade_calculation)
        self.results_always_visible = maybe_from_nullable(
            self.results_always_visible
        )
        self.prefer_teacher_revision = maybe_from_nullable(
            self.prefer_teacher_revision
        )
        self.fixtures = maybe_from_nullable(self.fixtures)

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["assignment_id"] = to_dict(self.assignment_id)
        if self.setup_script.is_just:
            res["setup_script"] = to_dict(self.setup_script.value)
        if self.run_setup_script.is_just:
            res["run_setup_script"] = to_dict(self.run_setup_script.value)
        if self.has_new_fixtures.is_just:
            res["has_new_fixtures"] = to_dict(self.has_new_fixtures.value)
        if self.grade_calculation.is_just:
            res["grade_calculation"] = to_dict(self.grade_calculation.value)
        if self.results_always_visible.is_just:
            res["results_always_visible"] = to_dict(
                self.results_always_visible.value
            )
        if self.prefer_teacher_revision.is_just:
            res["prefer_teacher_revision"] = to_dict(
                self.prefer_teacher_revision.value
            )
        if self.fixtures.is_just:
            res["fixtures"] = to_dict(self.fixtures.value)
        res["overwrite_duplicate_fixtures"] = to_dict(
            self.overwrite_duplicate_fixtures
        )
        return res

    @classmethod
    def from_dict(
        cls: Type["JsonCreateAutoTest"], d: Dict[str, Any]
    ) -> "JsonCreateAutoTest":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            assignment_id=parsed.assignment_id,
            setup_script=parsed.setup_script,
            run_setup_script=parsed.run_setup_script,
            has_new_fixtures=parsed.has_new_fixtures,
            grade_calculation=parsed.grade_calculation,
            results_always_visible=parsed.results_always_visible,
            prefer_teacher_revision=parsed.prefer_teacher_revision,
            fixtures=parsed.fixtures,
            overwrite_duplicate_fixtures=parsed.overwrite_duplicate_fixtures,
        )
        res.raw_data = d
        return res
