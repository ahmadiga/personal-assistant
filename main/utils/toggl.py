import datetime
import json
import logging

import requests

logger = logging.getLogger('django.channels')


class Toggl():
    token = None

    def __init__(self, api_token):
        self.token = api_token

    def get_clients(self):
        r = requests.get("https://www.toggl.com/api/v8/clients", auth=(self.token, "api_token",))
        return r.json()

    def get_projects(self):
        clients = self.get_clients()
        projects = []
        if self.token:
            for client in clients:
                r = requests.get("https://www.toggl.com/api/v8/clients/" + str(client["id"]) + "/projects",
                                 auth=(self.token, "api_token",))
                # sometimes request.json does not return None, so this is a small fix4
                if r.json() is not None:
                    for project in r.json():
                        projects.append({
                            "name": project["name"],
                            "client": client["name"],
                            "id": project["id"],
                        })
        return projects

    def get_current_time_entry(self):
        r = requests.get("https://www.toggl.com/api/v8/time_entries/current", auth=(self.token, "api_token",))
        return r.json()["data"]

    def get_today_time_entry(self):
        today_date = datetime.datetime.utcnow().date()
        today_date = datetime.datetime(today_date.year, today_date.month, today_date.day)
        context = {
            "start_date": today_date.isoformat() + "+02:00",
            "end_date": (today_date + datetime.timedelta(days=1)).isoformat() + "+02:00",
        }
        r = requests.get("https://www.toggl.com/api/v8/time_entries", auth=(self.token, "api_token",), params=context)
        return r.json

    def create_start_time_entry(self, task):
        date_now = datetime.datetime.utcnow()
        context = {
            "time_entry": {
                "description": task.title + " - " + task.description,
                "tags": [task.submitted_by.username],
                "pid": task.project.toggl_id,
                "created_with": "curl"
            }
        }
        r = requests.post("https://www.toggl.com/api/v8/time_entries/start", auth=(self.token, "api_token",),
                          data=json.dumps(context))
        logger.info(r.text)
        return r.json()["data"]

    def stop_time_entry(self, id):
        r = requests.put("https://www.toggl.com/api/v8/time_entries/" + str(id) + "/stop",
                         auth=(self.token, "api_token",))
        return r

    def get_me(self):
        r = requests.get("https://www.toggl.com/api/v8/me",
                         auth=(self.token, "api_token",))
        return r.json()["data"]

    def get_today_summery_time_entry(self):
        me = self.get_me()
        today_date = datetime.datetime.utcnow().date()
        today_date = datetime.datetime(today_date.year, today_date.month, today_date.day)
        context = {
            "workspace_id": me["workspaces"][0]["id"],
            "since": today_date.isoformat() + "+02:00",
            "until": (today_date + datetime.timedelta(days=1)).isoformat() + "+02:00",
            "user_agent": "a.bazadough@sit-mena.com",
            "user_ids": {
                me["id"]
            },
            "grouping": {
                "projects": "time_entries"
            }
        }
        r = requests.get("https://toggl.com/reports/api/v2/summary", auth=(self.token, "api_token",), params=context)
        return r.json()
