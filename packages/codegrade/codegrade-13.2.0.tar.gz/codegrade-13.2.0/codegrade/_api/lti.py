"""The endpoints for lti objects.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from typing import TYPE_CHECKING, Any, Generic, Mapping, TypeVar, Union

import cg_request_args as rqa
from cg_maybe import Maybe, Nothing

from ..utils import get_error, log_warnings, response_code_matches, to_dict

if TYPE_CHECKING:
    from typing import Union

    from ..client import AuthenticatedClient, _BaseClient
    from ..models.base_error import BaseError
    from ..models.create_lti_data import CreateLTIData
    from ..models.finalized_lti1p1_provider import FinalizedLTI1p1Provider
    from ..models.finalized_lti1p3_provider import FinalizedLTI1p3Provider
    from ..models.non_finalized_lti1p1_provider import (
        NonFinalizedLTI1p1Provider,
    )
    from ..models.non_finalized_lti1p3_provider import (
        NonFinalizedLTI1p3Provider,
    )
    from ..parsers import JsonResponseParser, ParserFor, make_union

_ClientT = TypeVar("_ClientT", bound="_BaseClient")


class LTIService(Generic[_ClientT]):
    __slots__ = ("__client",)

    def __init__(self, client: "_BaseClient") -> None:
        self.__client = client

    def create(
        self: "LTIService[AuthenticatedClient]",
        json_body: Union[dict, list, "CreateLTIData"],
        *,
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "Union[NonFinalizedLTI1p3Provider, NonFinalizedLTI1p1Provider, FinalizedLTI1p3Provider, FinalizedLTI1p1Provider]":
        """Create a new LTI 1.1 or 1.3 provider.

        This route is part of the public API.

        :param json_body: The body of the request. See :model:`.CreateLTIData`
            for information about the possible fields. You can provide this
            data as a :model:`.CreateLTIData` or as a dictionary.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The just created provider.
        """
        from typing import Union

        from ..models.base_error import BaseError
        from ..models.create_lti_data import CreateLTIData
        from ..models.finalized_lti1p1_provider import FinalizedLTI1p1Provider
        from ..models.finalized_lti1p3_provider import FinalizedLTI1p3Provider
        from ..models.non_finalized_lti1p1_provider import (
            NonFinalizedLTI1p1Provider,
        )
        from ..models.non_finalized_lti1p3_provider import (
            NonFinalizedLTI1p3Provider,
        )
        from ..parsers import JsonResponseParser, ParserFor, make_union

        url = "/api/v1/lti1.3/providers/"
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.post(
                url=url, json=to_dict(json_body), params=params
            )
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(
                make_union(
                    ParserFor.make(NonFinalizedLTI1p3Provider),
                    ParserFor.make(NonFinalizedLTI1p1Provider),
                    ParserFor.make(FinalizedLTI1p3Provider),
                    ParserFor.make(FinalizedLTI1p1Provider),
                )
            ).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])
