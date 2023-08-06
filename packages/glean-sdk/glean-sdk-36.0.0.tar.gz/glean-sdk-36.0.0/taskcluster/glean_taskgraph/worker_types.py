# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import absolute_import, print_function, unicode_literals

from six import text_type

from voluptuous import Required

from taskgraph.util.schema import taskref_or_string
from taskgraph.transforms.task import payload_builder


@payload_builder(
    "scriptworker-signing",
    schema={
        Required("max-run-time"): int,
        Required("cert"): text_type,
        Required("upstream-artifacts"): [{
            Required("taskId"): taskref_or_string,
            Required("taskType"): text_type,
            Required("paths"): [text_type],
            Required("formats"): [text_type],
        }]
    }
)
def build_scriptworker_signing_payload(config, task, task_def):
    worker = task["worker"]
    task_def["tags"]["worker-implementation"] = "scriptworker"
    task_def["payload"] = {
        "maxRunTime": worker["max-run-time"],
        "upstreamArtifacts": worker["upstream-artifacts"],
    }

    formats = set()
    for artifacts in worker["upstream-artifacts"]:
        formats.update(artifacts["formats"])

    scope_prefix = config.graph_config["scriptworker"]["scope-prefix"]
    task_def["scopes"].append(
        "{}:signing:cert:{}".format(scope_prefix, worker["cert"])
    )
    task_def["scopes"].extend([
        "{}:signing:format:{}".format(scope_prefix, signing_format) for signing_format in sorted(formats)
    ])


@payload_builder(
    "scriptworker-beetmover",
    schema={
        Required("bucket"): text_type,
        Required("max-run-time"): int,
        Required("version"): str,
        Required("app-name"): text_type,
        Required("upstream-artifacts"): [{
            Required("taskId"): taskref_or_string,
            Required("taskType"): text_type,
            Required("paths"): [text_type],
        }],
        Required("artifact-map"): [{
            Required("task-id"): taskref_or_string,
            Required("locale"): text_type,
            Required("paths"): {text_type: dict},
        }],
    }
)
def build_scriptworker_beetmover_payload(config, task, task_def):
    worker = task["worker"]
    task_def["tags"]["worker-implementation"] = "scriptworker"
    task_def["payload"] = {
        "maxRunTime": worker["max-run-time"],
        "upstreamArtifacts": worker["upstream-artifacts"],
        "artifactMap": [{
            "taskId": entry["task-id"],
            "locale": entry["locale"],
            "paths": entry["paths"],
        } for entry in worker["artifact-map"]],
        "version": worker["version"],
        "releaseProperties": {
            "appName": worker["app-name"]
        }
    }

    scope_prefix = config.graph_config["scriptworker"]["scope-prefix"]
    task_def["scopes"].append(
        "{}:beetmover:bucket:{}".format(scope_prefix, worker["bucket"])
    )
    task_def["scopes"].append(
        "{}:beetmover:action:push-to-maven".format(scope_prefix)
    )
