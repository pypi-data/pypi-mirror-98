# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import contrast

from contrast.agent.policy.constants import CURRENT_FINDING_VERSION, TRIGGER_TYPE
from contrast.api.dtm_pb2 import TraceEvent
from contrast.extern import six
from contrast.utils.base64_utils import base64_decode

# These request part values must match the TYPE parameter for source nodes in policy.json, which are
# a best effort at translating the types in this document:
# https://bitbucket.org/contrastsecurity/teamserver/src/862d499227e8eac42b6eb7c6b03f10b7f1556218/teamserver-agent-messages/src/main/java/contrast/agent/messages/finding/trace/EventSourceTypeDTM.java#lines-8
SOURCE_OPTIONS = {
    "parameter": "PARAMETER",
    "cookies": "COOKIE",
    "body": "BODY",
    "full_path": "URI",
    "full_path_info": "URI",
    "raw_uri": "URI",
    "host": "URI",
    "port": "URI",
    "scheme": "OTHER",
    "encoding": "OTHER",
    "files": "MULTIPART_CONTENT_DATA",
    "form": "MULTIPART_FORM_DATA",
    "header": "HEADER",
    "referer_header": "HEADER",
    "header_key": "HEADER_KEY",
    "wsgi.input": "MULTIPART_CONTENT_DATA",
}


def validate_finding(
    finding, rule_id, user_input=None, nondataflow=False, config=False, trigger_arg=0,
):
    assert finding.rule_id == rule_id

    assert finding.version == CURRENT_FINDING_VERSION
    assert len(finding.routes) == 1

    if config:
        return

    if nondataflow:
        assert len(finding.events) == 1
        return

    trigger_event = finding.events[-1]
    assert trigger_event.action == TraceEvent.Action.Value(TRIGGER_TYPE)

    if trigger_event.source == "RETURN":
        trigger_input = base64_decode(trigger_event.ret.value)
    elif trigger_event.source == "OBJ":
        trigger_input = base64_decode(trigger_event.object.value)
    else:
        # assume it's args[0] unless we specify otherwise
        trigger_input = base64_decode(trigger_event.args[trigger_arg].value)

    # original user input should be somehow in the trigger event or we've
    # string-ified a bytes-like obj or a regex pattern object
    assert (
        user_input in trigger_input
        or "io.BytesIO" in trigger_input
        or "_sre.SRE_Pattern" in trigger_input
    )


def validate_finding_in_context(
    request_context,
    rule_id,
    user_input=None,
    nondataflow=False,
    config=False,
    trigger_arg=0,
):
    finding = _get_single_finding_or_fail(
        request_context, rule_id, nondataflow or config
    )

    validate_finding(finding, rule_id, user_input, nondataflow, config, trigger_arg)


def validate_source_finding_in_context(
    request_context, rule_id, source_name, source_map=None
):
    finding = _get_single_finding_or_fail(request_context, rule_id, nondataflow=False)
    assert finding.rule_id == rule_id
    assert_event_sources([finding], source_name, source_map or SOURCE_OPTIONS)


def remove_redos_findings(findings, rule_id):
    """
    Redos rule creates vulnerabilities in lots of places including framework
    code. For now we ignore a redos vuln if we're are testing for redos rule

    NOTE: These redos findings are legitimate and at this time we are reporting them
    to TS. Work will labs will decide if that should continue. We only filter them
    out in these tests to make assertions easy.
    """
    if rule_id == "redos":
        return findings

    return [x for x in findings if x.rule_id != "redos"]


def validate_nondataflow_finding(
    findings, response, mocked_build_finding, rule_id, call_count, num_findings=1
):
    assert response is not None

    filtered_findings = remove_redos_findings(findings, rule_id)
    if len(filtered_findings) < len(findings):
        # there was likely a redos finding in the framework so increment call count
        call_count += 1

    assert mocked_build_finding.called
    assert mocked_build_finding.call_count == call_count

    args, _ = mocked_build_finding.call_args

    assert args[1].name == rule_id

    assert len(filtered_findings) == num_findings

    finding = filtered_findings[0]
    assert len(finding.routes) == 1
    assert len(finding.events) == 1
    assert finding.version == CURRENT_FINDING_VERSION


def validate_provider_finding(send_messages_mock):
    hardcoded_key = send_messages_mock.call_args_list[0][0][0][0].findings[0]
    hardcoded_key.rule_id == "hardcoded-key"

    properties = hardcoded_key.properties
    properties["codeSource"] == "SECRET_KEY = [**REDACTED**]"
    properties["name"] == "SECRET_KEY"
    "app/settings.py" in properties["source"]

    hardcoded_pwd = send_messages_mock.call_args_list[1][0][0][0].findings[0]
    hardcoded_pwd.rule_id == "hardcoded-password"

    properties = hardcoded_pwd.properties
    properties["codeSource"] == "PASSWORD = [**REDACTED**]"
    properties["name"] == "PASSWO RD"
    "app/settings.py" in properties["source"]


def validate_source_finding(
    findings,
    response,
    mocked_build_finding,
    source_name,
    rule_id,
    num_findings,
    source_map=None,
):
    assert response is not None
    assert mocked_build_finding.called

    args, _ = mocked_build_finding.call_args

    assert args[1].name == rule_id

    findings = remove_redos_findings(findings, rule_id)

    assert len(findings) == num_findings

    assert_event_sources(findings, source_name, source_map or SOURCE_OPTIONS)


def validate_header_sources(findings, source_name):
    rule_id = "cmd-injection"
    findings = remove_redos_findings(findings, rule_id)

    assert len(findings) == 1
    assert findings[0].rule_id == "cmd-injection"
    assert_event_sources(
        findings, source_name, {"header": "HEADER", "header_key": "HEADER_KEY"}
    )


def validate_cookies_sources(findings):
    rule_id = "cmd-injection"
    findings = remove_redos_findings(findings, rule_id)

    assert len(findings) == 1
    assert findings[0].rule_id == rule_id
    assert_event_sources(findings, "cookies", {"cookies": "COOKIE"})


def assert_event_sources(findings, source_name, source_options):
    all_event_sources = _get_event_sources(findings)
    # for now all we care is that the source name appears in TYPE at least once
    assert source_options[source_name] in [source.type for source in all_event_sources]


def _get_single_finding_or_fail(request_context, rule_id, nondataflow):
    """
    Get the single finding associated with the given request context.
    If there are multiple findings, fail the unit test.

    Nondataflow findings, especially crypto-bad-mac, are fairly common in
    various frameworks. For tests where we only care about the dataflow
    findings, this method removes any additional nondataflow findings.
    """
    if nondataflow:
        findings = request_context.activity.findings
    else:
        findings = [
            finding
            for finding in request_context.activity.findings
            if finding.rule_id
            # we may need to expand this list in the future
            not in ("crypto-bad-mac", "crypto-weak-randomness", "session-timeout")
        ]

    findings = remove_redos_findings(findings, rule_id)
    assert len(findings) == 1
    return findings[0]


def _get_event_sources(findings):
    """
    Get all trace event sources from all finding.events

    :param findings: a list of Finding objects
    :return: a list of TraceEventSource objects
    """
    event_sources = []

    for finding in findings:
        for event in finding.events:
            if event.event_sources:
                for trace_event in event.event_sources:
                    event_sources.append(trace_event)

    return event_sources


def _validate(response, tracked_param, mocked_build_finding):
    assert response is not None
    assert param_is_tracked(tracked_param)
    assert mocked_build_finding.called


def param_is_tracked(param_val):
    for props in contrast.STRING_TRACKER.values():
        if props.origin == param_val:
            return True
    return False


def validate_ssrf_finding(trigger, request_context, mocked):
    assert mocked.called
    assert mocked.call_args[0][1].name == "ssrf"


def validate_ssrf_finding_no_mock(trigger, request_context):
    # This case results in multiple findings for reasons that are not entirely understood
    num_findings = (
        2
        if trigger == "urlopen-obj"
        or six.PY2
        and trigger in ["legacy-urlopen", "urlopen-str"]
        else 1
    )

    findings = remove_redos_findings(request_context.activity.findings, "ssrf")
    assert len(findings) == num_findings
    assert findings[0].rule_id == six.u("ssrf")
