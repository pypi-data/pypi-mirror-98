"""The endpoints for login_link objects.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from typing import TYPE_CHECKING, Any, Generic, Mapping, TypeVar, Union

import cg_request_args as rqa
from cg_maybe import Maybe, Nothing

from ..utils import get_error, log_warnings, response_code_matches, to_dict

if TYPE_CHECKING:
    from ..client import AuthenticatedClient, _BaseClient
    from ..models.assignment_login_link import AssignmentLoginLink
    from ..models.base_error import BaseError
    from ..parsers import JsonResponseParser, ParserFor

_ClientT = TypeVar("_ClientT", bound="_BaseClient")


class LoginLinkService(Generic[_ClientT]):
    __slots__ = ("__client",)

    def __init__(self, client: "_BaseClient") -> None:
        self.__client = client

    def get(
        self,
        *,
        login_link_id: "str",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "AssignmentLoginLink":
        """Get a login link and the connected assignment.

        :param login_link_id: The id of the login link you want to get.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The requested login link, which will also contain information
                  about the connected assignment.
        """
        from ..models.assignment_login_link import AssignmentLoginLink
        from ..models.base_error import BaseError
        from ..parsers import JsonResponseParser, ParserFor

        url = "/api/v1/login_links/{loginLinkId}".format(
            loginLinkId=login_link_id
        )
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.get(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(
                ParserFor.make(AssignmentLoginLink)
            ).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])
