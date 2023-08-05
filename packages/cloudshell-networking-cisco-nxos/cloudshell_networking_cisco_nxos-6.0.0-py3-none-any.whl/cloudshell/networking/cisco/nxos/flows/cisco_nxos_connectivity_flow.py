#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.networking.cisco.flows.cisco_connectivity_flow import (
    CiscoConnectivityFlow,
)

from cloudshell.networking.cisco.nxos.command_actions.nxos_add_remove_vlan_actions import (  # noqa E501
    CiscoNXOSAddRemoveVlanActions,
)
from cloudshell.networking.cisco.nxos.command_actions.nxos_iface_actions import (
    CiscoNXOSIFaceActions,
)


class CiscoNXOSConnectivityFlow(CiscoConnectivityFlow):
    def __init__(self, cli_handler, logger):
        super(CiscoNXOSConnectivityFlow, self).__init__(cli_handler, logger)

    def _get_vlan_actions(self, config_session):
        return CiscoNXOSAddRemoveVlanActions(config_session, self._logger)

    def _get_iface_actions(self, config_session):
        return CiscoNXOSIFaceActions(config_session, self._logger)
