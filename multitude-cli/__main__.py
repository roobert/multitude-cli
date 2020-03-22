#!/usr/bin/env python

import json
import datetime
from os import path
from tabulate import tabulate
import urllib.request
import urllib.parse


def main():
    db = get_data()
    rows = []

    for data in db["git_repo"]:
        row = {
            "timestamp": "",
            "app": "",
            "version": "",
            "build pipeline": "",
            "image repo": "",
            "deployment": "",
        }

        row["timestamp"] = format_timestamp(data["timestamp"])
        row["app"] = path.join(data["owner"], data["repo"])
        row["version"] = data["properties"]["tag"]
        row["build pipeline"] = data["properties"]["status"]

        row["image repo"] = get_status(
            db, "docker_repo", data["owner"], data["repo"], data["properties"]["tag"]
        )
        row["deployment"] = get_status(
            db, "deployment", data["owner"], data["repo"], data["properties"]["tag"]
        )

        rows.append(row)

    # fancy_grid is nicer but doesn't work with watch(1)
    print(tabulate(rows, headers="keys", tablefmt="psql"))


def get_data():
    address = "http://localhost:8000"
    db = {}

    # FIXME: use join
    urls = {
        "git_repo": f"{address}/fetch/git_repo",
        "docker_repo": f"{address}/fetch/docker_repo",
        "deployment": f"{address}/fetch/deployment",
    }

    for collection, url in urls.items():
        data = urllib.request.urlopen(url).read().decode("utf-8")
        db[collection] = json.loads(data)

    return db


def format_timestamp(timestamp):
    time = datetime.datetime.strptime(
        "".join(timestamp.rsplit(":", 1)), "%Y-%m-%dT%H:%M:%S.%f%z",
    )
    return time.strftime("%Y-%m-%d %H:%M:%S")


def get_status(db, collection, owner, repo, tag):
    for entry in db[collection]:
        if (
            entry["owner"] == owner
            and entry["repo"] == repo
            and entry["properties"]["tag"] == tag
        ):
            return entry["properties"]["status"]
    return "--"


if __name__ == "__main__":
    main()
