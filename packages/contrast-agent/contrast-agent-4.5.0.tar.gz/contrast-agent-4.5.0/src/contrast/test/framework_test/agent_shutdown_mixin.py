# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import mock
import threading

import contrast

from contrast.api.settings_pb2 import AgentSettings, Reaction
from contrast.agent.settings_state import SettingsState


def assert_empty_context_tracker():
    context_tracker = contrast.CS__CONTEXT_TRACKER

    assert not any(
        context_tracker.get(thread_id, None) for thread_id in context_tracker._tracker
    )


def build_agent_settings_shutdown():
    agent_settings = AgentSettings()
    reaction = Reaction()

    reaction.operation = Reaction.DISABLE
    agent_settings.application_settings.reactions.append(reaction)

    return agent_settings


def thread_running_by_id(thread_id):
    return any(id(thread) == thread_id for thread in threading.enumerate())


class AgentShutdownMixin:
    @mock.patch(
        "contrast.agent.middlewares.base_middleware.BaseMiddleware.call_without_agent"
    )
    def test_agent_shutdown_in_heartbeat_thread(self, mock_call_without_agent, mocker):
        settings = SettingsState()
        trigger = "os-system"
        user_input = "whatever"
        path = "/vulnpy/cmdi/{}".format(trigger)

        response = self.client.get(path, {"user_input": user_input})

        assert response.status_code == 200
        assert settings.is_agent_config_enabled()
        assert thread_running_by_id(id(settings.heartbeat))
        assert not mock_call_without_agent.called

        mocked_send_dtm = mocker.patch(
            "contrast.agent.service_client._ServiceState.send_dtm",
            return_value=build_agent_settings_shutdown(),
        )

        settings.heartbeat.join(timeout=10)

        assert mocked_send_dtm.called
        assert not settings.is_agent_config_enabled()
        assert not thread_running_by_id(id(settings.heartbeat))

        assert_empty_context_tracker()

    @mock.patch(
        "contrast.agent.middlewares.base_middleware.BaseMiddleware.call_without_agent"
    )
    def test_agent_shutdown_in_request_thread(self, mock_call_without_agent, mocker):
        settings = SettingsState()
        trigger = "os-system"
        user_input = "whatever"
        path = "/vulnpy/cmdi/{}".format(trigger)

        response = self.client.get(path, {"user_input": user_input})

        assert response.status_code == 200
        assert settings.is_agent_config_enabled()
        assert thread_running_by_id(id(settings.heartbeat))
        assert not mock_call_without_agent.called

        mocker.patch("contrast.agent.heartbeat.Heartbeat.send_heartbeat")
        mocked_send_dtm = mocker.patch(
            "contrast.agent.service_client._ServiceState.send_dtm",
            return_value=build_agent_settings_shutdown(),
        )

        response = self.client.get(path, {"user_input": user_input})

        assert response.status_code == 200
        assert mocked_send_dtm.called
        assert not settings.is_agent_config_enabled()

        mock_track_str = mocker.patch("contrast.agent.assess.string_tracker")

        response = self.client.get(path, {"user_input": user_input})

        assert response.status_code == 200
        assert not mock_track_str.called
        assert mocked_send_dtm.called
        assert mock_call_without_agent.called
        assert not settings.is_agent_config_enabled()

        settings.heartbeat.join(timeout=10)

        assert not thread_running_by_id(id(settings.heartbeat))

        assert_empty_context_tracker()
