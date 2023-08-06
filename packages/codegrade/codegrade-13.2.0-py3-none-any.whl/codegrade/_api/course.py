"""The endpoints for course objects.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from typing import TYPE_CHECKING, Any, Generic, Mapping, TypeVar, Union

import cg_request_args as rqa
from cg_maybe import Maybe, Nothing

from ..utils import get_error, log_warnings, response_code_matches, to_dict

if TYPE_CHECKING:
    from typing import Dict, Mapping, Sequence, Union

    from ..client import AuthenticatedClient, _BaseClient
    from ..models.base_error import BaseError
    from ..models.change_user_role_course_data import ChangeUserRoleCourseData
    from ..models.course_registration_link import CourseRegistrationLink
    from ..models.course_snippet import CourseSnippet
    from ..models.create_course_data import CreateCourseData
    from ..models.email_users_course_data import EmailUsersCourseData
    from ..models.extended_course import ExtendedCourse
    from ..models.extended_work import ExtendedWork
    from ..models.group_set import GroupSet
    from ..models.job import Job
    from ..models.patch_course_data import PatchCourseData
    from ..models.put_enroll_link_course_data import PutEnrollLinkCourseData
    from ..models.user import User
    from ..models.user_course import UserCourse
    from ..parsers import (
        ConstantlyParser,
        JsonResponseParser,
        ParserFor,
        make_union,
    )

_ClientT = TypeVar("_ClientT", bound="_BaseClient")


class CourseService(Generic[_ClientT]):
    __slots__ = ("__client",)

    def __init__(self, client: "_BaseClient") -> None:
        self.__client = client

    def get_all(
        self: "CourseService[AuthenticatedClient]",
        *,
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "Sequence[ExtendedCourse]":
        """Return all Course objects the current user is a member of.

        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: A response containing the JSON serialized courses
        """
        from typing import Sequence

        from ..models.base_error import BaseError
        from ..models.extended_course import ExtendedCourse
        from ..parsers import JsonResponseParser, ParserFor

        url = "/api/v1/courses/"
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.get(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(
                rqa.List(ParserFor.make(ExtendedCourse))
            ).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def create(
        self: "CourseService[AuthenticatedClient]",
        json_body: Union[dict, list, "CreateCourseData"],
        *,
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "ExtendedCourse":
        """Create a new course.

        :param json_body: The body of the request. See
            :model:`.CreateCourseData` for information about the possible
            fields. You can provide this data as a :model:`.CreateCourseData`
            or as a dictionary.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: A response containing the JSON serialization of the new
                  course
        """
        from ..models.base_error import BaseError
        from ..models.create_course_data import CreateCourseData
        from ..models.extended_course import ExtendedCourse
        from ..parsers import JsonResponseParser, ParserFor

        url = "/api/v1/courses/"
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.post(
                url=url, json=to_dict(json_body), params=params
            )
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(
                ParserFor.make(ExtendedCourse)
            ).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def get_submissions_by_user(
        self: "CourseService[AuthenticatedClient]",
        *,
        course_id: "int",
        user_id: "int",
        latest_only: "bool" = False,
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "Mapping[str, Sequence[ExtendedWork]]":
        """Get all submissions by the given user in this course.

        :param course_id: The id of the course from which you want to get the
            submissions.
        :param user_id: The id of the user of which you want to get the
            submissions.
        :param latest_only: Only get the latest submission of a user. Please
            use this option if at all possible, as students have a tendency to
            submit many attempts and that can make this route quite slow.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: A mapping between assignment id and the submissions done in
                  that assignment by the given user. If the `latest_only` query
                  parameter was used the value will still be an array of
                  submissions, but the length will always be one. If the user
                  didn't submit for an assignment the value might be empty or
                  the id of the assignment will be missing from the returned
                  object.
        """
        from typing import Dict, Mapping, Sequence

        from ..models.base_error import BaseError
        from ..models.extended_work import ExtendedWork
        from ..parsers import JsonResponseParser, ParserFor

        url = "/api/v1/courses/{courseId}/users/{userId}/submissions/".format(
            courseId=course_id, userId=user_id
        )
        params: "Dict[str, Any]" = {
            **(extra_parameters or {}),
            "latest_only": to_dict(latest_only),
        }

        with self.__client as client:
            response = client.http.get(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(
                rqa.LookupMapping(rqa.List(ParserFor.make(ExtendedWork)))
            ).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def put_enroll_link(
        self: "CourseService[AuthenticatedClient]",
        json_body: Union[dict, list, "PutEnrollLinkCourseData"],
        *,
        course_id: "int",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "CourseRegistrationLink":
        """Create or edit an enroll link.

        :param json_body: The body of the request. See
            :model:`.PutEnrollLinkCourseData` for information about the
            possible fields. You can provide this data as a
            :model:`.PutEnrollLinkCourseData` or as a dictionary.
        :param course_id: The id of the course in which this link should enroll
            users.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The created or edited link.
        """
        from ..models.base_error import BaseError
        from ..models.course_registration_link import CourseRegistrationLink
        from ..models.put_enroll_link_course_data import (
            PutEnrollLinkCourseData,
        )
        from ..parsers import JsonResponseParser, ParserFor

        url = "/api/v1/courses/{courseId}/registration_links/".format(
            courseId=course_id
        )
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.put(
                url=url, json=to_dict(json_body), params=params
            )
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(
                ParserFor.make(CourseRegistrationLink)
            ).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def get_group_sets(
        self: "CourseService[AuthenticatedClient]",
        *,
        course_id: "int",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "Sequence[GroupSet]":
        """Get the all the group sets of a given course.

        :param course_id: The id of the course of which the group sets should
            be retrieved.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: A list of group sets.
        """
        from typing import Sequence

        from ..models.base_error import BaseError
        from ..models.group_set import GroupSet
        from ..parsers import JsonResponseParser, ParserFor

        url = "/api/v1/courses/{courseId}/group_sets/".format(
            courseId=course_id
        )
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.get(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(
                rqa.List(ParserFor.make(GroupSet))
            ).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def get_snippets(
        self: "CourseService[AuthenticatedClient]",
        *,
        course_id: "int",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "Sequence[CourseSnippet]":
        """Get all snippets of the given course.

        :param course_id: The id of the course from which you want to get the
            snippets.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: An array containing all snippets for the given course.
        """
        from typing import Sequence

        from ..models.base_error import BaseError
        from ..models.course_snippet import CourseSnippet
        from ..parsers import JsonResponseParser, ParserFor

        url = "/api/v1/courses/{courseId}/snippets/".format(courseId=course_id)
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.get(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(
                rqa.List(ParserFor.make(CourseSnippet))
            ).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def delete_role(
        self: "CourseService[AuthenticatedClient]",
        *,
        course_id: "int",
        role_id: "int",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "None":
        """Remove a CourseRole from the given Course.

        :param course_id: The id of the course
        :param role_id: The id of the role you want to delete
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: An empty response with return code 204
        """
        from ..models.base_error import BaseError
        from ..parsers import ConstantlyParser, JsonResponseParser, ParserFor

        url = "/api/v1/courses/{courseId}/roles/{roleId}".format(
            courseId=course_id, roleId=role_id
        )
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.delete(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 204):
            return ConstantlyParser(None).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def get_all_users(
        self: "CourseService[AuthenticatedClient]",
        *,
        course_id: "int",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "Union[Sequence[User], Sequence[UserCourse]]":
        """Return a list of all <span data-role=\"class\">.models.User</span>
        objects and their

        :param course_id: The id of the course
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: A response containing the JSON serialized users and course
                  roles
        """
        from typing import Sequence, Union

        from ..models.base_error import BaseError
        from ..models.user import User
        from ..models.user_course import UserCourse
        from ..parsers import JsonResponseParser, ParserFor, make_union

        url = "/api/v1/courses/{courseId}/users/".format(courseId=course_id)
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.get(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(
                make_union(
                    rqa.List(ParserFor.make(User)),
                    rqa.List(ParserFor.make(UserCourse)),
                )
            ).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def change_user_role(
        self: "CourseService[AuthenticatedClient]",
        json_body: Union[dict, list, "ChangeUserRoleCourseData"],
        *,
        course_id: "int",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> Union["UserCourse", "None"]:
        """Set the `CourseRole` of a user in the given course.

        :param json_body: The body of the request. See
            :model:`.ChangeUserRoleCourseData` for information about the
            possible fields. You can provide this data as a
            :model:`.ChangeUserRoleCourseData` or as a dictionary.
        :param course_id: The id of the course in which you want to enroll a
            new user, or change the role of an existing user.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: If the user\_id parameter is set in the request the response
                  will be empty with return code 204. Otherwise the response
                  will contain the JSON serialized user and course role with
                  return code 201
        """
        from ..models.base_error import BaseError
        from ..models.change_user_role_course_data import (
            ChangeUserRoleCourseData,
        )
        from ..models.user_course import UserCourse
        from ..parsers import (
            ConstantlyParser,
            JsonResponseParser,
            ParserFor,
            make_union,
        )

        url = "/api/v1/courses/{courseId}/users/".format(courseId=course_id)
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.put(
                url=url, json=to_dict(json_body), params=params
            )
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(ParserFor.make(UserCourse)).try_parse(
                response
            )
        if response_code_matches(response.status_code, 204):
            return ConstantlyParser(None).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def email_users(
        self: "CourseService[AuthenticatedClient]",
        json_body: Union[dict, list, "EmailUsersCourseData"],
        *,
        course_id: "int",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "Job":
        """Sent the authors in this course an email.

        :param json_body: The body of the request. See
            :model:`.EmailUsersCourseData` for information about the possible
            fields. You can provide this data as a
            :model:`.EmailUsersCourseData` or as a dictionary.
        :param course_id: The id of the course in which you want to send the
            emails.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: A task result that will send these emails.
        """
        from ..models.base_error import BaseError
        from ..models.email_users_course_data import EmailUsersCourseData
        from ..models.job import Job
        from ..parsers import JsonResponseParser, ParserFor, make_union

        url = "/api/v1/courses/{courseId}/email".format(courseId=course_id)
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.post(
                url=url, json=to_dict(json_body), params=params
            )
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(ParserFor.make(Job)).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def get(
        self: "CourseService[AuthenticatedClient]",
        *,
        course_id: "int",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "ExtendedCourse":
        """Get a course by id.

        :param course_id: The id of the course
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: A response containing the JSON serialized course
        """
        from ..models.base_error import BaseError
        from ..models.extended_course import ExtendedCourse
        from ..parsers import JsonResponseParser, ParserFor

        url = "/api/v1/courses/{courseId}".format(courseId=course_id)
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.get(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(
                ParserFor.make(ExtendedCourse)
            ).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def patch(
        self: "CourseService[AuthenticatedClient]",
        json_body: Union[dict, list, "PatchCourseData"],
        *,
        course_id: "int",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "ExtendedCourse":
        """Update the given course with new values.

        :param json_body: The body of the request. See
            :model:`.PatchCourseData` for information about the possible
            fields. You can provide this data as a :model:`.PatchCourseData` or
            as a dictionary.
        :param course_id: The id of the course you want to update.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The updated course, in extended format.
        """
        from ..models.base_error import BaseError
        from ..models.extended_course import ExtendedCourse
        from ..models.patch_course_data import PatchCourseData
        from ..parsers import JsonResponseParser, ParserFor

        url = "/api/v1/courses/{courseId}".format(courseId=course_id)
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.patch(
                url=url, json=to_dict(json_body), params=params
            )
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(
                ParserFor.make(ExtendedCourse)
            ).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])
