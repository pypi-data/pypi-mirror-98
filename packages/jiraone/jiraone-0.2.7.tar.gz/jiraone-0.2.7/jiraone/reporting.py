#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Example methods of Generating reports

Provided herein are Report Generator Classes and Methods,
Easily generate report for the various endpoints
"""
from typing import Any, Optional, List, Iterable, Tuple, Union, Callable, Dict
from collections import deque, namedtuple
from jiraone import LOGIN, endpoint, add_log, WORK_PATH
import json
import csv
import sys
import os
import re


class Projects:
    """Get report on a Project based on user or user's attributes or groups."""

    @staticmethod
    def projects_accessible_by_users(*args: Any, project_folder: str = "Project",
                                     project_file_name: str = "project_file.csv",
                                     user_extraction_file: str = "project_extract.csv",
                                     permission: str = "BROWSE", **kwargs):
        """
        Send an argument as String equal to a value, example: status=live.

        Multiple arguments separate by comma as the first argument in the function, all other arguments should
        be keyword args that follows. This API helps to generate full user accessibility to Projects on Jira.
        It checks the users access and commits the finding to a report file.

        You can tweak the permission argument with the options mention here
        https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-user-search

        for endpoint /rest/api/3/user/permission/search
        """
        count_start_at = 0
        headers = ["Project Key", "Project Name", "Issue Count", "Last Issue Update"]
        file_writer(folder=project_folder, file_name=project_file_name, data=headers)

        def project():
            file_writer(project_folder, project_file_name, data=raw)
            read_users = file_reader(folder=project_folder, file_name=file_name)
            for user in read_users:
                account_id = user[0]
                display_name = user[2]
                active_status = user[3]
                project_key = keys
                find = LOGIN.get(endpoint.find_users_with_permission(account_id, project_key, permission))
                data = json.loads(find.content)
                if str(data) == "[]":
                    raw_vision = [display_name, f"Has {permission} Permission: False",
                                  f"Project: {name}", f"User Status: {active_status}"]
                    file_writer(project_folder, project_file_name, data=raw_vision)
                else:
                    for d in data:
                        d_name = d["displayName"]
                        active = d["active"]
                        raw_vision = [d_name, f"Has {permission} Permission: {active}",
                                      f"Project: {name}", f"User Status: {active_status}"]

                        file_writer(project_folder, project_file_name, data=raw_vision)

        file_name = user_extraction_file
        USER.get_all_users(file=file_name, folder=project_folder, **kwargs)
        print("Project User List Extracted")
        add_log("Project User List Extracted", "info")
        while True:
            load = LOGIN.get(endpoint.get_projects(*args, start_at=count_start_at))
            count_start_at += 50
            if load.status_code == 200:
                results = json.loads(load.content)
                for key in results["values"]:
                    keys = key["key"]
                    name = key["name"]
                    if "insight" in key:
                        insight = key["insight"]
                        if "totalIssueCount" and "lastIssueUpdateTime" in insight:
                            raw = [keys, name, f"{insight['totalIssueCount']}",
                                   f"{insight['lastIssueUpdateTime']}"]
                            project()
                        elif "totalIssueCount" in insight and "lastIssueUpdateTime" not in insight:
                            raw = [keys, name, f"{insight['totalIssueCount']}",
                                   "No data available"]
                            project()
                    else:
                        raw = [keys, name, "No data available", "No data available"]
                        project()

                if count_start_at > results["total"]:
                    print("Project Reporting Completed")
                    print("File extraction completed. Your file is located at {}"
                          .format(path_builder(path=project_folder, file_name=project_file_name)))
                    add_log("Project Reporting Completed", "info")
                    break
            else:
                sys.stderr.write("Unable to fetch data status {} ".format(load.status_code))
                add_log(f"Data retrieval failure due to {load.reason}", "error")
                sys.exit(1)

    @staticmethod
    def dashboards_shared_with(dashboard_folder: str = "Dashboard",
                               dashboard_file_name: str = "dashboard_file.csv",
                               **kwargs):
        """
        Retrieve the Dashboard Id/Name/owner and who it is shared with.

        The only requirement is that the user querying this API should have access to all
        the Dashboard available else it will only return dashboard where the user's view access is allowed.
        """
        count_start_at = 0
        dash_list = deque()  # get the id of dashboard search
        put_list = deque()  # arrange the different values associated with dashboard
        dump_list = deque()  # dump the results into our csv writer
        headers = ["Dashboard Id", "Dashboard Name", "Owner", "Shared Permission"]
        file_writer(folder=dashboard_folder, file_name=dashboard_file_name, data=headers, **kwargs)

        while True:
            load = LOGIN.get(endpoint.search_for_dashboard(start_at=count_start_at))
            count_start_at += 50
            if load.status_code == 200:
                results = json.loads(load.content)
                for value in results["values"]:
                    valid = value["id"]
                    name = value["name"]
                    raw = [valid, name]
                    dash_list.append(raw)

                print("Dashboard List Extracted")
                add_log("Dashboard List Extracted", "info")

                def dash_run():
                    for pem in shared_permission:
                        if "role" in pem:
                            role = f"Role: {pem['role']['name']}"
                            put_list.append(role)
                        if "group" in pem:
                            group = f"Group: {pem['group']['name']}"
                            put_list.append(group)
                        if "type" in pem:
                            types = pem["type"]
                            if types == "project":
                                project = f"Project Name: {pem['project']['name']}"
                                put_list.append(project)
                            if types == "loggedin" or types == "global":
                                put_list.append(types)

                    extract = [d for d in put_list]
                    raw = [value[0], names, owner, extract]
                    dump_list.append(raw)

                for value in dash_list:
                    init = LOGIN.get(endpoint.get_dashboard(value[0]))
                    if init.status_code == 200:
                        expanse = json.loads(init.content)
                        names = expanse["name"]
                        if "owner" in expanse:
                            owner = expanse["owner"]["displayName"]
                        shared_permission = expanse["sharePermissions"]
                        dash_run()
                        put_list = deque()

                file_writer(dashboard_folder, dashboard_file_name, data=dump_list, mark="many")

                if count_start_at > results["total"]:
                    print("Dashboard Reporting Completed")
                    print("File extraction completed. Your file is located at {}"
                          .format(path_builder(path=dashboard_folder, file_name=dashboard_file_name)))
                    add_log("Dashboard Reporting Completed", "info")
                    break

    @staticmethod
    def get_all_roles_for_projects(roles_folder: str = "Roles",
                                   roles_file_name: str = "roles_file.csv",
                                   user_extraction: str = "role_users.csv",
                                   **kwargs):
        """Get the roles available in a project and which user is assigned to which
        role within the project"""
        count_start_at = 0
        headers = ["Project Id ", "Project Key", "Project Name", "Project roles", "User AccountId", "User DisplayName",
                   "User role in Project"]
        file_writer(folder=roles_folder, file_name=roles_file_name, data=headers, **kwargs)

        # get extraction of projects data
        def role_on() -> Any:
            project_role_list = deque()
            for keys in results["values"]:
                role_list = deque()
                key = keys["key"]
                pid = keys["id"]
                name = keys["name"]
                roles = LOGIN.get(endpoint.get_roles_for_project(pid))
                print("Extracting Project Keys {}".format(key))
                add_log("Extracting Project Keys {}".format(key), "info")

                # find out what roles exist within each project
                def role_over() -> Tuple:
                    if roles.status_code == 200:
                        extract = json.loads(roles.content)
                        only_keys = extract.keys()
                        casting = list(only_keys)
                        only_values = extract.items()
                        puller = list(only_values)
                        z = [d for d in puller]
                        return casting, z

                caster = role_over()
                raw = [pid, key, name, caster[0]]
                role_list.append(raw)
                add_log("Appending data to List Queue", "info")

                for user in read_users:
                    account_id = user[0]
                    display_name = user[2]

                    # extract the user role using the appropriate accountId
                    def get_user_role(user_data) -> Any:
                        for users in user_data[1]:
                            check = LOGIN.get(users[1])
                            if check.status_code == 200:
                                result_data = json.loads(check.content)
                                actors = result_data["actors"]
                                for act in actors:
                                    if "actorUser" in act:
                                        if account_id == act["actorUser"]["accountId"]:
                                            res = f"Role Name: {result_data['name']}"
                                            project_role_list.append(res)

                        # function to write collected data into a file
                        def pull_data() -> Any:
                            role_puller = [j for j in project_role_list]
                            project_id = data[0]
                            project_key = data[1]
                            project_name = data[2]
                            project_roles = data[3]
                            raw_dump = [project_id, project_key, project_name, project_roles, account_id, display_name,
                                        role_puller]
                            file_writer(folder=roles_folder, file_name=roles_file_name, data=raw_dump)

                        for data in role_list:
                            pull_data()

                    get_user_role(caster)
                    project_role_list = deque()

        USER.get_all_users(folder=roles_folder, file=user_extraction, **kwargs)
        read_users = file_reader(folder=roles_folder, file_name=user_extraction, **kwargs)
        while True:
            init = LOGIN.get(endpoint.get_projects(start_at=count_start_at))
            if init.status_code == 200:
                print("Project Extraction")
                results = json.loads(init.content)
                add_log("Project Extraction Initiated", "info")
                if count_start_at > results["total"]:
                    break
                if results["total"] > 0:
                    role_on()
            count_start_at += 50

        print("File extraction completed. Your file is located at {}".format(path_builder
                                                                             (path=roles_folder,
                                                                              file_name=roles_file_name)))
        add_log("File extraction completed", "info")

    def get_attachments_on_projects(self, attachment_folder: str = "Attachment",
                                    attachment_file_name: str = "attachment_file.csv",
                                    **kwargs):
        """Return all attachments of a Project or Projects

        Get the size of attachments on an Issue, count those attachments collectively and return the total number
        on all Projects searched. JQL is used as a means to search for the project.
        """
        attach_list = deque()
        count_start_at = 0
        headers = ["Project id", "Project key", "Project name", "Issue key", "Attachment size",
                   "Attachment type", "Name of file", "Created on by user", "Attachment url"]
        file_writer(folder=attachment_folder, file_name=attachment_file_name, data=headers, **kwargs)

        def pull_attachment_sequence() -> Optional:
            nonlocal attach_list
            for issues in result_data["issues"]:
                keys = issues["key"]
                get_issue_keys = LOGIN.get(endpoint.issues(issue_key_or_id=keys))
                if get_issue_keys.status_code == 200:
                    key_data = json.loads(get_issue_keys.content)
                    data = key_data["fields"]
                    if "project" or "attachment" in data:
                        project_id = data["project"]["id"]
                        project_name = data["project"]["name"]
                        project_key = data["project"]["key"]
                        attachment = data["attachment"]
                        if attachment is not None:
                            for attach in attachment:
                                if "author" in attach:
                                    display_name = attach["author"]["displayName"]

                                def pull_attachment() -> Optional:
                                    file_name = attach["filename"]  # name of the file
                                    created = attach["created"]  # datetime need to convert it
                                    attachment_size = attach["size"]  # in bytes, need to convert to mb
                                    mime_type = attach["mimeType"]
                                    attachment_url = attach["content"]

                                    calc_size = self.byte_converter(attachment_size)
                                    calc_date = self.date_converter(created)

                                    pull = [project_id, project_key, project_name, keys, calc_size, mime_type,
                                            file_name, f"{calc_date} by {display_name}", attachment_url]
                                    attach_list.append(pull)

                                pull_attachment()

            raw_data = [x for x in attach_list]
            file_writer(attachment_folder, attachment_file_name, data=raw_data, mark="many")
            attach_list.clear()

        while True:
            get_issue = LOGIN.get(endpoint.search_issues_jql(start_at=count_start_at, **kwargs))
            if get_issue.status_code == 200:
                result_data = json.loads(get_issue.content)
                if count_start_at > result_data["total"]:
                    print("Attachment extraction completed")
                    add_log("Attachment extraction completed", "info")
                    break

                print("Attachment extraction processing")
                add_log("Attachment extraction processing", "info")
                pull_attachment_sequence()

            count_start_at += 50

        def re_write():
            calc_made = self.grade_and_sort(attach_list, read_file)
            attach_list.clear()
            rd_file = read_file
            # sort the file using the issue_key column
            sorts = sorted(rd_file, key=lambda row: row[3], reverse=False)
            for i in sorts:
                _project_id = i[0]
                _project_key = i[1]
                _project_name = i[2]
                _issue_key = i[3]
                _attach_size = i[4]
                _file_name = i[5]
                _attach_type = i[6]
                _created_by = i[7]
                _attach_url = i[8]
                raw_data_file = [_project_id, _project_key, _project_name, _issue_key,
                                 _attach_size, _file_name, _attach_type, _created_by, _attach_url]
                file_writer(attachment_folder, attachment_file_name, data=raw_data_file)

            # lastly we want to append the total sum of attachment size.
            raw_data_file = ["", "", "", "", "Total Size: {:.2f} MB".format(calc_made), "", "", "", ""]
            file_writer(attachment_folder, attachment_file_name, data=raw_data_file)

        read_file = file_reader(attachment_folder, attachment_file_name, skip=True)
        file_writer(attachment_folder, attachment_file_name, data=headers, mode="w")
        re_write()

        print("File extraction completed. Your file is located at {}".format(path_builder
                                                                             (path=attachment_folder,
                                                                              file_name=attachment_file_name)))
        add_log("File extraction completed", "info")

    @staticmethod
    def byte_converter(val) -> str:
        """1 Byte = 8 Bits.

        using megabyte MB, value is 1000^2
        mebibyte MiB, value is 1024^2
        Therefore total = val / MB
        """
        byte_size = val
        mega_byte = 1000 * 1000
        visor = byte_size / mega_byte  # MB converter
        return "Size: {:.2f} MB".format(visor)

    @staticmethod
    def date_converter(val) -> str:
        """split the datetime value and output a string."""
        get_date_time = val.split("T")
        get_am_pm = get_date_time[1].split(".")
        return f"Created on {get_date_time[0]} {get_am_pm[0]}"

    @staticmethod
    def grade_and_sort(attach_list, read_file) -> Union[float, int]:
        for node in read_file:
            pattern = re.compile(r"(\d*?[0-9]\.[0-9]*)")
            if pattern is not None:
                if pattern.search(node[4]):
                    attach_list.append(pattern.search(node[4]).group())

        retain = [float(s) for s in attach_list]
        calc_sum = sum(retain)
        return calc_sum

    @staticmethod
    def bytes_converter(val) -> str:
        # TODO: added this change on 14 Mar 2021
        """Returns unit in KB or MB.

        1 Byte = 8 Bits.
        using megabyte MB, value is 1000^2
        mebibyte MiB, value is 1024^2
        Therefore total = val / MB
        """
        byte_size = val
        kilo_byte = 1000
        mega_byte = 1000 * 1000
        if byte_size > mega_byte:
            visor = byte_size / mega_byte  # MB converter
            unit = "MB"
        else:
            visor = byte_size / kilo_byte  # KB converter
            unit = "KB"
        return "Size: {:.2f} {}".format(visor, unit)

    @staticmethod
    def move_attachments_across_instances(attach_folder: str = "Attachment",
                                          attach_file: str = "attachment_file.csv",
                                          key: int = 3,
                                          attach: int = 8,
                                          file: int = 6,
                                          last_cell: bool = True,
                                          **kwargs):
        """Ability to post an attachment into another Instance.

        given the data is extracted from a csv file which contains the below information
         * Issue key
         * file name
         * attachment url
        we assume you're getting this from
        `def get_attachments_on_project()`

        :param attach_folder a folder or directory path
        :param attach_file a file to a file name
        :param key a row index of the column
        :param attach a row index of the column
        :param file - integers to specify the index of the columns
        :param last_cell is a boolean determines if the last cell should be counted.
             e.g
                * key=3,
                * attach=6,
                * file=8

        the above example corresponds with the index if using the
         `def get_attachments_on_project()` otherwise, specify your value in each
         keyword args when calling the method.
        """
        read = file_reader(folder=attach_folder, file_name=attach_file, skip=True, **kwargs)
        add_log("Reading attachment {}".format(attach_file), "info")
        count = 0
        cols = read
        length = len(cols)
        for r in read:
            count += 1
            keys = r[key]
            attachment = r[attach]
            _file_name = r[file]
            fetch = LOGIN.get(attachment).content
            # use the files keyword args to send multipart/form-data in the post request of LOGIN.post
            payload = {"file": (_file_name, fetch)}
            # modified our initial headers to accept X-Atlassian-Token to avoid (CSRF/XSRF)
            new_headers = {"Accept": "application/json",
                           "X-Atlassian-Token": "no-check"}
            LOGIN.headers = new_headers
            run = LOGIN.post(endpoint.issue_attachments(keys, query="attachments"), files=payload)
            if run.status_code != 200:
                print("Attachment not added to {}".format(keys), "Status code: {}".format(run.status_code))
                add_log("Attachment not added to {} due to {}".format(keys, run.reason), "error")
            else:
                print("Attachment added to {}".format(keys), "Status code: {}".format(run.status_code))
                add_log("Attachment added to {}".format(keys), "info")
            # remove the last column since if it contains empty cells.
            if last_cell is True:
                if count >= (length - 1):
                    break

    @staticmethod
    def download_attachments(file_folder: str = None, file_name: str = None,
                             download_path: str = "Downloads",
                             attach: int = 8,
                             file: int = 6,
                             **kwargs):
        # TODO: added change on 8 Mar 2021
        """Download the attachments to your local device read from a csv file.

        we assume you're getting this from   `def get_attachments_on_project()` method.
              :param attach, file - integers to specify the index of the columns
              :param file_folder a folder or directory where the file
              :param download_path a directory where files are stored
              :param file a row to the index of the column
              :param file_name a file name to a file
                e.g
                  * attach=6,
                  * file=8
              the above example corresponds with the index if using the `def get_attachments_on_project()`
              otherwise, specify your value in each keyword args when calling the method.
        """
        read = file_reader(folder=file_folder, file_name=file_name, **kwargs)
        add_log("Reading attachment {}".format(file_name), "info")
        count = 0
        cols = read
        length = len(cols)
        last_cell = kwargs["last_cell"] if "last_cell" in kwargs else False
        for r in read:
            count += 1
            attachment = r[attach]
            _file_name = r[file]
            fetch = LOGIN.get(attachment)
            file_writer(download_path, file_name=_file_name, mode="wb", content=fetch.content, mark="file")
            print("Attachment downloaded to {}".format(download_path), "Status code: {}".format(fetch.status_code))
            add_log("Attachment downloaded to {}".format(download_path), "info")
            if last_cell is True:
                if count >= (length - 1):
                    break

    @staticmethod
    def extract_jira_issues(*args, **kwargs):
        """Returns all issues within an instance without the 1K limit.

        Issue download contains all fields, fields can be specified as well
        Issue history included as fields
        Attachments url included as fields
        All comments included
        Sprint id and name included
        User accountId included
        """
        # TODO: create this method
        pass

    def move_projects_across_instances(
            self,
            instance_a: str = Any,
            instance_b: str = Any,
            extracted_file: str = Any,
            method_allowed: bool = False,
            method_function: Callable = Any,
            properties: Union[float, int] = Any,
            classification: str = Ellipsis,
            diagram: List[str] = Any,
            probability: Dict[List[str], int] = Any,
            status: Tuple[Union[List[str]]] = Any,
            **kwargs
    ):
        """Ability to move projects between instances.

        Everything within the Project is maintained.
        Full user permission required, in order to successful transfer and recreate
        the issue between instances.
        everything within Instance A project A into Instance B project B is retained.
        """
        # TODO: Create this method and its features. this is a work in progress.
        pass

    @staticmethod
    def get_total_comments_on_issues(folder: str = "Comment", file_name: str = "comment_file.csv",
                                     **kwargs):
        """Return a report with the number of comments sent to or by a reporter (if any).

        This api will return comment count, the total comment sent by a reporter
        per issue and collectively sum up a total.
        It also shows how many comments other users sent on the issue.
        """
        comment_list = deque()
        pull = "active" if "pull" not in kwargs else kwargs["pull"]
        user_type = "atlassian" if "user_type" not in kwargs else kwargs["user_type"]
        file = "user_file.csv" if "file" not in kwargs else kwargs["file"]
        find_user = "test user" if "find_user" not in kwargs else kwargs["find_user"]
        duration = "startOfWeek(-1)" if "duration" not in kwargs else kwargs["duration"]
        status = None if "status" not in kwargs else kwargs["status"]
        get_user = ""
        headers = ["Project Id", "Project Key", "Project Name", "Issue Key", "Total Comment",
                   "Reporter accountId", "Display name of Reporter", "Comment by Reporter",
                   "Comment by others"]
        file_writer(folder, file_name, data=headers)
        USER.get_all_users(pull=pull,
                           user_type=user_type,
                           file=file, folder=folder)
        CheckUser = namedtuple("CheckUser", ["accountId", "account_type", "display_name", "active"])
        read = file_reader(folder=folder, file_name=file)
        for _ in read:
            f = CheckUser._make(_)
            if find_user in f._asdict().values():
                get_user = f.accountId
                print("User {} found - accountId: {}".format(find_user, get_user))

        if get_user == "":
            print("User: {}, not found exiting search...".format(find_user))
            sys.exit(1)
        search_issues = "reporter = {} AND updated <= {}".format(get_user, duration) if "status" not in kwargs \
            or status is None \
            else "reporter = {} AND updated <= {} AND status in ({})".format(get_user, duration, status)
        print("Searching with JQL:", search_issues)
        count_start_at = 0

        def extract_issue():
            """Find the comment in each issue and count it."""
            comment_by_users = 0
            comment_by_others = 0
            for issues in result_data["issues"]:
                keys = issues["key"]
                get_issue_keys = LOGIN.get(endpoint.issues(issue_key_or_id=keys))
                if get_issue_keys.status_code == 200:
                    key_data = json.loads(get_issue_keys.content)
                    data = key_data["fields"]
                    if "project" or "comment" in data:
                        project_id = data["project"]["id"]
                        project_name = data["project"]["name"]
                        project_key = data["project"]["key"]
                        comments = data["comment"]
                        if comments is not None:
                            comment_total = comments["total"]
                            comment_self = comments["self"]
                            get_comment = LOGIN.get(comment_self)
                            if get_comment.status_code == 200:
                                comment_data = json.loads(get_comment.content)
                                reporter_name = ""
                                reporter_aid = ""
                                for comment in comment_data["comments"]:
                                    if "author" in comment:
                                        display_name = comment["author"]["displayName"]
                                        account_id = comment["author"]["accountId"]
                                        if account_id == get_user:
                                            reporter_name = display_name
                                            reporter_aid = account_id
                                            comment_by_users += 1
                                        if account_id != get_user:
                                            comment_by_others += 1

                                def pull_comments() -> Optional:
                                    raw_dump = [project_id, project_key, project_name, keys,
                                                comment_total, reporter_aid, reporter_name,
                                                comment_by_users, comment_by_others]
                                    comment_list.append(raw_dump)

                                pull_comments()
                                comment_by_users = 0
                                comment_by_others = 0

            raw_data = [z for z in comment_list]
            file_writer(folder, file_name, data=raw_data, mark="many")
            comment_list.clear()

        while True:
            get_issues = LOGIN.get(endpoint.search_issues_jql(query=search_issues, start_at=count_start_at))
            if get_issues.status_code == 200:
                result_data = json.loads(get_issues.content)
                if count_start_at > result_data["total"]:
                    print("Issues extraction completed")
                    add_log("Issue extraction completed", "info")
                    break

                print("Extracting Issues...")
                extract_issue()

            count_start_at += 50

        def count_and_total() -> Tuple[int, int, int]:
            for row in read_file:
                comment_list.append(row)

            wid_list = [int(s[4]) for s in comment_list]
            row_list = [int(s[7]) for s in comment_list]
            col_list = [int(s[8]) for s in comment_list]
            calc_list_zero = sum(wid_list)
            calc_list_one = sum(row_list)
            calc_list_two = sum(col_list)
            return calc_list_zero, calc_list_one, calc_list_two

        def write_result():
            list_data = count_and_total()
            comment_list.clear()
            sorts = sorted(read_file, key=lambda rows: rows[3], reverse=False)
            for c in sorts:
                _project_id = c[0]
                _project_key = c[1]
                _project_name = c[2]
                _issue_key = c[3]
                _comment_total = c[4]
                _get_user = c[5]
                _reporter_name = c[6]
                _comm_by_reporter = c[7]
                _comm_by_others = c[8]

                raw_data_file = [_project_id, _project_key, _project_name, _issue_key, _comment_total,
                                 _get_user, _reporter_name, _comm_by_reporter, _comm_by_others]
                file_writer(folder, file_name, data=raw_data_file)

            # arranging the file last row
            raw_data_file = ["", "", "", "", "Total comments: {}".format(list_data[0]),
                             "", "", "Total comments by Reporter: {}".format(list_data[1]),
                             "Total comments by others: {}".format(list_data[2])]
            file_writer(folder, file_name, data=raw_data_file)

        read_file = file_reader(folder, file_name, skip=True)
        file_writer(folder, file_name, mode="w", data=headers)
        write_result()

        print("File extraction for comments completed. Your file is located at {}".format(path_builder
                                                                                          (path=folder,
                                                                                           file_name=file_name)))
        add_log("File extraction for comments completed", "info")


class Users:
    """
    Below methods helps to Generate the No of Users on Jira Cloud

    You can customize it to determine which user you're looking for.
    >> The below method here displays active or inactive users, so you'll be getting all users
    :param: pull (options)
            -> both: pulls out inactive and active users
            -> active: pulls out only active users
            -> inactive: pulls out inactive users
    :param: user_type (options)
            -> atlassian: a normal Jira Cloud user
            -> customer: this will be your JSM customers
            -> app: this will be the bot users for any Cloud App
            -> unknown: as the name suggest unknown user type probably from oAuth
    """
    user_list = deque()

    def get_all_users(self, pull: str = "both", user_type: str = "atlassian",
                      file: str = None, folder: str = Any, **kwargs) -> Any:
        """Generates a list of users."""
        count_start_at = 0
        validate = LOGIN.get(endpoint.myself())

        while validate.status_code == 200:
            extract = LOGIN.get(endpoint.search_users(count_start_at))
            results = json.loads(extract.content)
            self.user_activity(pull, user_type, results)
            count_start_at += 50
            print("Current Record - At Row", count_start_at)
            add_log(f"Current Record - At Row {count_start_at}", "info")

            if str(results) == "[]":
                break
        else:
            sys.stderr.write("Unable to connect to {} - Login Failed...".format(LOGIN.base_url))
            add_log(f"Login Failure on {LOGIN.base_url}, due to {validate.reason}", "error")
            sys.exit(1)

        if file is not None:
            self.report(category=folder, filename=file)

    def report(self, category: str = Any, filename: str = "users_report.csv") -> Optional:
        """Creates a user report file in CSV format."""
        read = [d for d in self.user_list]
        file_writer(folder=category, file_name=filename, data=read, mark="many")
        add_log(f"Generating report file on {filename}", "info")

    def user_activity(self, status: str = Any, account_type: str = Any, results: List = Any) -> Any:
        """Determines users activity."""

        # get both active and inactive users
        def stack(c: Any, f: Any, s: Any) -> Any:
            if status == "both":
                if s["accountType"] == account_type:
                    return c.user_list.append(f)
            elif status == "active":
                if s["accountType"] == account_type and s["active"] is True:
                    return c.user_list.append(f)
            elif status == "inactive":
                if s["accountType"] == account_type and s["active"] is False:
                    return c.user_list.append(f)

        for each_user in results:
            list_user = [each_user["accountId"], each_user["accountType"], each_user["displayName"],
                         each_user["active"]]
            stack(self, list_user, each_user)

    def get_all_users_group(self, group_folder: str = "Groups", group_file_name: str = "group_file.csv",
                            user_extraction_file: str = "group_extraction.csv", **kwargs):
        """Get all users and the groups associated to them on the Instance."""
        headers = ["Name", "AccountId", "Groups", "User status"]
        file_writer(folder=group_folder, file_name=group_file_name, data=headers, **kwargs)
        file_name = user_extraction_file
        self.get_all_users(file=file_name, folder=group_folder, **kwargs)
        reader = file_reader(file_name=file_name, folder=group_folder, **kwargs)
        for user in reader:
            account_id = user[0]
            display_name = user[2]
            active_status = user[3]
            load = LOGIN.get(endpoint.get_user_group(account_id))
            results = json.loads(load.content)
            get_all = [d["name"] for d in results]
            raw = [display_name, account_id, get_all, active_status]
            file_writer(folder=group_folder, file_name=group_file_name, data=raw)

        print("File extraction completed. Your file is located at {}"
              .format(path_builder(path=group_folder, file_name=group_file_name)))
        add_log("Get Users group Completed", "info")


def path_builder(path: str = "Report", file_name: str = Any, **kwargs):
    """Builds a dir path and file path in a directory."""
    base_dir = os.path.join(WORK_PATH, path)
    if not os.path.exists(base_dir):
        os.mkdir(base_dir)
        add_log(f"Building Path {path}", "info")
    base_file = os.path.join(base_dir, file_name)
    return base_file


def file_writer(folder: str = WORK_PATH, file_name: str = Any, data: Iterable = object,
                mark: str = "single", mode: str = "a+", content: str = Any, **kwargs) -> Any:
    """Reads and writes to a file, single or multiple rows or write as byte files."""
    file = path_builder(path=folder, file_name=file_name)
    if mode:
        with open(file, mode) as f:
            write = csv.writer(f, delimiter=",")
            if mark == "single":
                write.writerow(data)
            if mark == "many":
                write.writerows(data)
            if mark == "file":
                f.write(content)
            add_log(f"Writing to file {file_name}", "info")


def file_reader(folder: str = WORK_PATH, file_name: str = Any, mode: str = "r",
                skip: bool = False, content: bool = False, **kwargs) -> Union[List[List[str]], str]:
    """Reads a CSV file and returns a list comprehension of the data or reads a byte into strings."""
    file = path_builder(path=folder, file_name=file_name)
    if mode:
        with open(file, mode) as f:
            read = csv.reader(f, delimiter=",")
            if skip is True:
                next(read, None)
            if content is True:
                feed = f.read()
            load = [d for d in read]
            add_log(f"Read file {file_name}", "info")
            return load if content is False else feed


def replacement_placeholder(string: str = Any, data: list = Any,
                            iterable: list = List,
                            row: int = 2) -> Any:
    """Return multiple string replacement.

    :param string  a string that needs to be checked
    :param data  a list of strings with one row in the string being checked.
    :param iterable an iterable data that needs to be replaced with.
    :param row an indicator of the column to check.

    # Usage:
    hold = ["Hello", "John doe", "Post mortem"]
    text = ["<name> <name>, welcome to the <name> of what is to come"]
    cb = replacement_placeholder("<name>", text, hold, 0)
    print(cb)
    """
    result = None
    count = 0
    length = len(iterable)
    for _ in iterable:
        if count == 0:
            if string in data[row]:
                result = [lines.replace(string, iterable[count], 1) for lines in data]
            # else:
            #     add_log("Word {} cannot be found".format(string), "error")
            #     sys.exit("Word {} cannot be found \n".format(string))
        if count > 0:
            if string in result[row]:
                result = [lines.replace(string, iterable[count], 1) for lines in result]
            # else:
            #     add_log("Word {} cannot be found".format(string), "error")
            #     sys.exit("Word {} cannot be found \n".format(string))
        count += 1
        if count > length:
            break
    return result


USER = Users()
PROJECT = Projects()
