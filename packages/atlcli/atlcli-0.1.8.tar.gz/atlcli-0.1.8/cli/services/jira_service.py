import re
import base64
import json
import ssl
from datetime import date
from dateutil import parser as date_parser

import pprint36 as pprint
import requests
from atlassian import Jira
from prettytable import PrettyTable

from .stats_service import StatsService


class JiraService:

    def __init__(self, url, username, password, skipssl):
        self.semver_regex = r"(([0-9]+)\.([0-9]+)\.([0-9]+)(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?(?:\+[0-9A-Za-z-]+)?)"
        self.skipssl = skipssl
        self.url = url        
        self.username = username
        self.password = password
        self.jiraInstance = Jira(
            url=url,
            username=username,
            password=password,
            verify_ssl=self.skipssl)

        self.stats_service = StatsService()

    def get_ticket(self, ticket_name):
        """get tickets basic infos"""
        pass

    def close_ticket(self, ticket_name):
        """closes a ticket"""
        pass

    def get_changelog(self, ticket_name):
        """get commits and repos changed linked to ticket"""
        issue_details = self.jiraInstance.issue(ticket_name)
        issue_id = issue_details["id"]
        changes = self.get_changes(issue_id)

    def get_commits_from_issue(self, issue_id):
        endpoint_url = "{url}/rest/dev-status/1.0/issue/detail".format(
            url=self.url)

        querystring = {
            "issueId": issue_id,
            "applicationType": "stash",
            "dataType": "repository"
        }

        payload = ""

        encodedBytes = base64.b64encode("{username}:{password}"
                                        .format(username=self.username,
                                                password=self.password)
                                        .encode("utf-8"))
        base64_auth = str(encodedBytes, "utf-8")
        headers = {
            'Content-Type': "application/json",
            'Authorization': "Basic {0}".format(base64_auth)
        }

        response = requests.request(
            "GET", endpoint_url, data=payload, headers=headers, params=querystring, verify=self.skipssl)
        result = json.loads(response.text)
        return result

    def get_repositories_from_issue(self, issue_id):
        commits = self.get_commits_from_issue(issue_id)
        repositories = commits["detail"][0]["repositories"]
        return repositories

    def get_project_version_infos(self, project_key, version):
        data = self.jiraInstance.get_project_versions_paginated(
            project_key, limit=1000)
        versionData = next(
            filter(lambda x: x["name"] == version, data["values"]), None)

        # Validation
        if versionData is not None:
            if "name" not in versionData:
                versionData["name"] = ""
            if "id" not in versionData:
                versionData["id"] = ""
            if "description" not in versionData:
                versionData["description"] = ""
            if "released" not in versionData:
                versionData["released"] = ""
            if "startDate" not in versionData:
                versionData["startDate"] = ""
            if "releaseDate" not in versionData:
                versionData["releaseDate"] = ""
            
            return versionData
        else:
            return None

    def get_project_published_versions(self, project_key):
        releases = self.jiraInstance.get_project_versions_paginated(project_key, limit=1000)
        published_releases = list(filter(lambda x: x["released"], releases["values"]))
        return published_releases
       

    def get_project_version_issues(self, project_key, versionId):
        jql_query = "project = {0} AND fixVersion = {1} AND (type = Story OR type = Improvement ) order by key".format(
            project_key, versionId)
        
        try:
            data = self.jiraInstance.jql(jql_query)["issues"]
        except requests.exceptions.ReadTimeout:
            sys.exit("ERROR: timeout error with the JQL query for retrieving the isssues associated to a project version")

        return data

    def get_issues_confluence_markup(self, project_key, versionId):
        issues = self.get_project_version_issues(project_key, versionId)

        content = "|| Ticket JIRA || Projects || Status || Summary || Remarques ||\n"
        rows = ""
        for x in issues:
            repositories = self.get_repositories_from_issue(x["id"])
            concatRepos = ""

            if len(repositories) > 0:
                for r in repositories:
                    concatRepos = concatRepos + r["name"] + ", "

            if concatRepos == "":
                concatRepos = " "
            row = "||{ticket}|{repos}|{status}|{summary}|{remarques}|".format(
                ticket=x["key"], repos=concatRepos, status=x["fields"]["status"]["name"], summary=x["fields"]["summary"].replace("|", "-"), remarques=" ")
            rows = rows + row + "\n"

        content = content + rows
        return content

    # Creates the issues refered to a jira product
    def get_issues_printable(self, project_key, versionId):
        issues = self.get_project_version_issues(project_key, versionId)
        table = PrettyTable()
        table.field_names = ["Key", "Repositories", "Status"]

        for x in issues:
            repositories = self.get_repositories_from_issue(x["id"])
            concatRepos = ""

            if len(repositories) > 0:
                table.add_row([x["key"], repositories[0]["name"],
                               x["fields"]["status"]["name"]])
            else:
                table.add_row([x["key"], "None",
                               x["fields"]["status"]["name"]])

        output = "----------Issues----------\n{0}".format(table)
        return output

    def get_deploy_frequency(self, project_key, since=None):
        
        releases = self.jiraInstance.get_project_versions(project_key)
        
        if bool(since):
            since = date_parser.parse(since)
            published_releases = list(filter(lambda x: x["released"] and date_parser.parse(x["releaseDate"]) >= since , releases))
        
        else:
            published_releases = list(filter(lambda x: x["released"], releases))
        
        if bool(since):
            deploy_freq_per_release = self.stats_service.calculate_deploy_frequency_per_release(published_releases)
        
        average_meantime_between_releases = self.stats_service.calculate_deploy_frequency(published_releases)
        
        number_of_releases = len(releases)
        result = dict()
        result["number_of_releases"] = number_of_releases
        result["deploy_freq"] = average_meantime_between_releases
        result["deploy_freq_date"] = date.today()
        
        if bool(since):
            result["deploy_freq_per_release"] = deploy_freq_per_release
                
        return result
    
    def get_leadtime_for_changes_per_version(self, project_key, product_version):
        version_info = self.get_project_version_infos(project_key,
                                                        product_version)
        issues = self.get_project_version_issues(project_key, version_info["id"])
        latest_commits = self.get_lastest_commits_for_issues(issues)

        leadtime = self.stats_service.calculate_lead_time_for_changes(version_info, issues, latest_commits)
        return leadtime

    def get_leadtime_for_changes_for_all(self, project_key, since=None):
        leadtimes = dict()
        releases = self.get_project_published_versions(project_key)
        since = date_parser.parse(since)        
        semantic_version = ""

        if since is not None:
            releases = list(filter(lambda x: date_parser.parse(x["releaseDate"]) >= since , releases))

        for r in releases:
            l = self.get_leadtime_for_changes_per_version(project_key, r["name"])
            item = dict()
            if l >=0:
                item["lead-time"] = l

            item["release-date"] = r["releaseDate"]
            leadtimes[r["name"]] = item
            
        return leadtimes
        

    def get_lastest_commits_for_issues(self, issues):
        latest_commits = dict()
        not_added_due_to_error = ""

        for index, t in enumerate(issues):
            issue_key = t["key"]
            issue_id = t["id"]
            last_commit =  self.get_last_commit(issue_id)
            
            if last_commit:
                latest_commits[issue_key] = last_commit
            else:
                not_added_due_to_error += "{0}, ".format(issue_key)
                

        if len(not_added_due_to_error) > 0:
            print("The following issues were not added due to an error: {0} \n".format(issue_key))
            print("You may not have the correct permissions to the projects.")

        return latest_commits
    
    def get_last_commit(self, issue_id):
        result = self.get_commits_from_issue(issue_id)
        
        if "errorMessages" in result:
            print("ERROR:{0}".format(result["errorMessages"]))
            return None

        if len(result["detail"][0]["repositories"]) != 0:
            return result["detail"][0]["repositories"][0]["commits"][0]
        
        return None
