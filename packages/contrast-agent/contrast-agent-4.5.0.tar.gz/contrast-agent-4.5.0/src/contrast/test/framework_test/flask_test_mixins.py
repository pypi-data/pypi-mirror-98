# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from os import path
import flask
import pytest
import six  # pylint: disable=did-not-import-extern
import sys

from contrast.agent.policy import constants
from contrast.agent.assess.utils import get_properties
from contrast.api.dtm_pb2 import TraceEvent
from contrast.test import mocks
from contrast.test.contract.events import check_event
from contrast.test.contract.findings import (
    validate_finding_in_context,
    validate_source_finding_in_context,
    validate_header_sources,
    validate_cookies_sources,
)

from contrast.test.library_analysis import (
    assert_files_loaded,
    import_sample_package_onefile,
    TEST_MODULES_RELATIVE_IMPORT_DIST,
    TEST_MODULES_NAMESPACE_DIST,
    TEST_MODULE_ONEFILE,
    TEST_MODULES_MULTIPLE_TLDS_DIST,
)

from contrast.test.helper import python3_only


SOURCE_OPTIONS_MAP = {
    "args": "QUERYSTRING",
    "base_url": "URI",
    "full_path": "URI",
    "referer_header": "HEADER",
    "host": "URI",
    "host_url": "URI",
    "path": "URI",
    "query_string": "QUERYSTRING",
    "scheme": "OTHER",
    "url": "URI",
    "url_root": "URI",
    "values": "PARAMETER",
    "values_get_item": "PARAMETER",
}
# REMOTE_ADDR does not appear to be present in environ in Py27
SOURCE_OPTIONS_MAP.update({"remote_addr": "URI"} if six.PY3 else {})


POST_OPTIONS_MAP = {
    "files": "MULTIPART_CONTENT_DATA",
    "form": "MULTIPART_FORM_DATA",
    "wsgi.input": "BODY",
}

MULTIDICT_GET_OPTIONS_MAP = {
    "items": "QUERYSTRING",  # args.items()
    "lists": "QUERYSTRING",  # args.lists()
    "listvalues": "QUERYSTRING",  # args.listvalues()
    "values": "QUERYSTRING",  # args.values()
}

MULTIDICT_POST_OPTIONS_MAP = {
    "items": "MULTIPART_FORM_DATA",  # form.items()
    "lists": "MULTIPART_FORM_DATA",  # form.lists()
    "listvalues": "MULTIPART_FORM_DATA",  # form.listvalues()
    "values": "MULTIPART_FORM_DATA",  # form.values()
}


ALL_OPTIONS_MAP = {}
ALL_OPTIONS_MAP.update(SOURCE_OPTIONS_MAP)
ALL_OPTIONS_MAP.update(POST_OPTIONS_MAP)


SOURCE_OPTIONS = tuple(SOURCE_OPTIONS_MAP.keys())
POST_OPTIONS = tuple(POST_OPTIONS_MAP.keys())


def assert_flask_sqli_finding_events(finding, source_class_name):
    if sys.version_info[:2] == (3, 5):
        # TODO: PYT-1272: flask in py 3.5 has different event count
        return

    assert len(finding.events) == 17

    event_idx = 0
    check_event(
        finding.events[event_idx],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(constants.CREATION_TYPE),
        class_name=source_class_name,
        method_name="QUERY_STRING",
        source_types=["QUERYSTRING"],
        first_parent=None,
    )
    event_idx += 1
    check_event(
        finding.events[event_idx],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(
            constants.OBJECT_KEY + constants.TO_MARKER + constants.RETURN_KEY
        ),
        class_name="str",
        method_name="encode",
        source_types=[],
        first_parent=finding.events[event_idx - 1],
    )
    event_idx += 1
    check_event(
        finding.events[event_idx],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(
            constants.OBJECT_KEY + constants.TO_MARKER + constants.RETURN_KEY
        ),
        class_name="str",
        method_name="split",
        source_types=[],
        first_parent=finding.events[event_idx - 1],
    )
    event_idx += 1
    check_event(
        finding.events[event_idx],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(
            constants.ALL_TYPE + constants.TO_MARKER + constants.RETURN_KEY
        ),
        class_name="str",
        method_name="replace",
        source_types=[],
        first_parent=finding.events[event_idx - 1],
    )
    event_idx += 1
    check_event(
        finding.events[event_idx],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(
            constants.ALL_TYPE + constants.TO_MARKER + constants.RETURN_KEY
        ),
        class_name="str",
        method_name="CAST",
        source_types=[],
        first_parent=finding.events[event_idx - 1],
    )
    event_idx += 1
    check_event(
        finding.events[event_idx],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(
            constants.ALL_TYPE + constants.TO_MARKER + constants.RETURN_KEY
        ),
        class_name="str",
        method_name="CAST",
        source_types=[],
        first_parent=finding.events[event_idx - 1],
    )
    event_idx += 1
    check_event(
        finding.events[event_idx],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(
            constants.OBJECT_KEY + constants.TO_MARKER + constants.RETURN_KEY
        ),
        class_name="str",
        method_name="decode",
        source_types=[],
        first_parent=finding.events[event_idx - 1],
    )
    event_idx += 4
    check_event(
        finding.events[event_idx],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(
            constants.ALL_TYPE + constants.TO_MARKER + constants.RETURN_KEY
        ),
        class_name="str",
        method_name="concat",
        source_types=[],
        first_parent=finding.events[event_idx - 1],
    )
    event_idx += 1
    check_event(
        finding.events[event_idx],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(
            constants.ALL_TYPE + constants.TO_MARKER + constants.RETURN_KEY
        ),
        class_name="str",
        method_name="concat",
        source_types=[],
        first_parent=finding.events[event_idx - 1],
    )

    # There are a few f-string propagation events here that previously were
    # omitted because they have no effect (i.e. the resulting string is
    # identical to the input). They are now showing up because we had to make a
    # fix to join propagation, which affects f-strings as well.

    event_idx += 4
    check_event(
        finding.events[event_idx],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(
            constants.ALL_TYPE + constants.TO_MARKER + constants.RETURN_KEY
        ),
        class_name="str",
        method_name="CAST",
        source_types=[],
        # TODO: PYT-922 for some reason this event doesn't have any parent_object_ids
        first_parent=None,
    )
    event_idx += 1
    check_event(
        finding.events[event_idx],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(constants.TRIGGER_TYPE),
        class_name="sqlite3.Cursor",
        method_name="execute",
        source_types=[],
        first_parent=finding.events[event_idx - 1],
    )


class FlaskTestLibraryAnalysisBuiltinImport(object):
    def test_relative_import_hook(self):
        response = self.client.get(
            "/import_package_with_relative_imports/", {"rm_sys_mod_entries": 1}
        )

        assert response.status_code == 200

        assert_files_loaded(
            self.request_context.activity, TEST_MODULES_RELATIVE_IMPORT_DIST
        )

    def test_namespace_sample_package_import_hook(self):
        response = self.client.get(
            "/import_namespace_package/", {"rm_sys_mod_entries": 1}
        )

        assert response.status_code == 200

        assert_files_loaded(self.request_context.activity, TEST_MODULES_NAMESPACE_DIST)

    def test_module_import_onefile(self):
        response = self.client.get(
            "/import_package_onefile/", {"rm_sys_mod_entries": 1}
        )

        assert response.status_code == 200

        assert_files_loaded(self.request_context.activity, TEST_MODULE_ONEFILE)

    def test_sample_module_multiple_tlds(self):
        response = self.client.get(
            "/import_sample_dist_multiple_tlds/", {"rm_sys_mod_entries": 1}
        )

        assert response.status_code == 200

        assert_files_loaded(
            self.request_context.activity, TEST_MODULES_MULTIPLE_TLDS_DIST
        )

    def test_module_already_imported(self):
        import_sample_package_onefile()

        response = self.client.get("/import_package_onefile/")

        assert response.status_code == 200

        assert len(self.request_context.activity.library_usages) == 0


class FlaskAssessTestMixin(object):

    ATTACK_VALUE = "im an attack!"

    def assert_propagation_happened(self, apply_trigger):
        """
        This tests that apply_trigger was called with the "ret" argument
        that has an HTML_ENCODED tag, indicating that propagation did occur.
        """
        assert apply_trigger.called
        call_args = apply_trigger.call_args
        ret_arg = call_args[0][2]
        assert "HTML_ENCODED" in get_properties(ret_arg).tags

    @python3_only
    def test_non_utf8_decoding_cmdi(self):
        """
        param_val a non utf8 encoded string. This is the result of shift_jis encoding of
        '手袋'. This encoding is automatically done by chrome, not in our test client. So
        we manually provide the encoded bytes here.
        """
        trigger = "os-system"
        rule_id = "cmd-injection"
        # Couldn't rely on passing 手袋 in the request because the test client doesn't
        # use shift_jis to encode.
        param_val = b"\x8e\xe8\x91\xdc"
        # Since we fail to decode param_value using utf-8 we rely on replace error
        # handling to get this new string
        expected_value = "���"
        path = "/vulnpy/cmdi/{}".format(trigger)

        self.client.get(path, {"user_input": param_val})

        validate_finding_in_context(self.request_context, rule_id, expected_value)

    @pytest.mark.parametrize("method_name", ["get", "post"])
    def test_xss(self, method_name):
        user_input = "whatever"
        method = getattr(self.client, method_name)

        response = method("/vulnpy/xss/raw", {"user_input": user_input})

        assert response.status_code == 200
        validate_finding_in_context(self.request_context, "reflected-xss", user_input)

        # Post creates a redos finding in werkzeug parse_options_header
        num_findings = 2 if method_name == "post" else 1
        finding = self.request_context.activity.findings[num_findings - 1]

        trigger_event = finding.events[-1]
        assert trigger_event.signature.class_name == "flask.app.Flask"
        assert trigger_event.signature.method_name == "wsgi_app"

    @pytest.mark.parametrize("user_input", ["something <> dangerous", "something safe"])
    @pytest.mark.parametrize("sanitizer", ["markupsafe", "html"])
    @mocks.apply_trigger
    def test_sanitized_xss(self, apply_trigger, user_input, sanitizer):
        response = self.client.post(
            "/{}-sanitized-xss?user_input={}".format(sanitizer, user_input)
        )

        assert response.status_code == 200

        self.assert_propagation_happened(apply_trigger)
        assert len(self.request_context.activity.findings) == 0

    @pytest.mark.parametrize("source", SOURCE_OPTIONS)
    def test_all_get_sources(self, source):
        self.client.set_cookie("user_input", "attack_cookie")
        self.client.get(
            "/dynamic-sources/",
            {"user_input": self.ATTACK_VALUE, "source": source},
            headers={"Referer": "www.python.org"},
            extra_environ={"REMOTE_ADDR": "localhost"},
        )

        validate_source_finding_in_context(
            self.request_context, "reflected-xss", source, ALL_OPTIONS_MAP
        )

    @pytest.mark.parametrize("source", SOURCE_OPTIONS + POST_OPTIONS)
    def test_all_post_sources(self, source):
        self.client.set_cookie("user_input", "attack_cookie")
        file_path = path.join(self.app.root_path, "..", "..", "data", "testfile.txt")
        self.client.post(
            "/dynamic-sources/?user_input={}&source={}".format(
                self.ATTACK_VALUE, source
            ),
            {"user_input": self.ATTACK_VALUE},
            headers={"Referer": "www.python.org"},
            upload_files=[("file_upload", file_path)],
            extra_environ={"REMOTE_ADDR": "localhost"},
        )

        if source == "form" and six.PY2 and flask.__version__.startswith("0.10"):
            # TODO: PYT-1272: flask 0.10 fails for this source in PY2
            return
        if source == "files" and six.PY2 and flask.__version__.startswith("1."):
            # TODO: PYT-1272: flask 1.x.x fails for this source in PY2
            return

        validate_source_finding_in_context(
            self.request_context, "reflected-xss", source, ALL_OPTIONS_MAP
        )

    @pytest.mark.parametrize("source", MULTIDICT_GET_OPTIONS_MAP.keys())
    def test_all_get_multidict(self, source):
        self.client.get(
            "/multidict-sources",
            {"user_input": self.ATTACK_VALUE, "source": source},
            headers={"user_input": self.ATTACK_VALUE},
        )

        validate_source_finding_in_context(
            self.request_context, "reflected-xss", source, MULTIDICT_GET_OPTIONS_MAP
        )

    @pytest.mark.parametrize("source", MULTIDICT_POST_OPTIONS_MAP.keys())
    def test_all_post_multidict(self, source):
        self.client.post(
            "/multidict-sources?source={}".format(source),
            {"user_input": self.ATTACK_VALUE},
            headers={"user_input": self.ATTACK_VALUE},
        )

        validate_source_finding_in_context(
            self.request_context, "reflected-xss", source, MULTIDICT_POST_OPTIONS_MAP
        )

    def test_cookie_get(self):
        """Cookies shouldn't trigger xss, so we need a separate cookie source test"""
        self.client.set_cookie("user_input", "attack_cookie")
        self.client.get("/cookie-source")
        validate_cookies_sources(self.request_context.activity.findings)

    def test_cookie_post(self):
        """Cookies shouldn't trigger xss, so we need a separate cookie source test"""
        self.client.set_cookie("user_input", "attack_cookie")
        self.client.post("/cookie-source")
        validate_cookies_sources(self.request_context.activity.findings)

    @pytest.mark.parametrize(
        "route,source_name",
        [("/header-source/", "header"), ("/header-key-source/", "header_key")],
    )
    @pytest.mark.parametrize("method_name", ["get", "post"])
    def test_non_xss_sources(self, method_name, route, source_name):
        method = getattr(self.client, method_name)
        method(route, headers={"Test-Header": "whatever"})

        validate_header_sources(self.request_context.activity.findings, source_name)

    @pytest.mark.parametrize("method_name", ("get", "post"))
    def test_http_method_not_source(self, method_name):
        getattr(self.client, method_name)("/method-source/")
        assert len(self.request_context.activity.findings) == 0

    def test_sqli_sqlalchemy(self):
        param_val = "doesnt matter"
        self.client.get("/sqli/", {"user_input": param_val})

        validate_finding_in_context(self.request_context, "sql-injection", param_val)
        # the exact event sequence is different for PY2/PY3
        if six.PY3:
            assert_flask_sqli_finding_events(
                self.request_context.activity.findings[0], "wsgi.environ"
            )

    @pytest.mark.parametrize("with_kwarg", [False, True])
    def test_unvalidated_redirect(self, with_kwarg):
        redirect_route = "/cmdi"
        self.client.get(
            "/unvalidated-redirect",
            {"user_input": redirect_route, "with_kwarg": with_kwarg},
        )

        validate_finding_in_context(
            self.request_context, "unvalidated-redirect", redirect_route,
        )

    @pytest.mark.parametrize("setdefault", [False, True])
    def test_trust_boundary_violation(self, setdefault):
        user_input = "hello"
        self.client.get(
            "/trust-boundary-violation",
            {"user_input": user_input, "setdefault": setdefault},
        )

        validate_finding_in_context(
            self.request_context, "trust-boundary-violation", user_input, trigger_arg=1
        )
