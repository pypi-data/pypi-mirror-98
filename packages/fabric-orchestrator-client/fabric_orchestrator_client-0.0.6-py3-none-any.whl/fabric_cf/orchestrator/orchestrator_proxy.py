#!/usr/bin/env python3
# MIT License
#
# Copyright (c) 2020 FABRIC Testbed
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
#
# Author: Komal Thareja (kthare10@renci.org)
import enum
from typing import Tuple, Union, List

from fabric_cf.orchestrator import swagger_client
from fim.user.topology import ExperimentTopology, SubstrateTopology

from fabric_cf.orchestrator.elements.constants import Constants
from fabric_cf.orchestrator.elements.reservation import ReservationFactory, Reservation
from fabric_cf.orchestrator.elements.slice import SliceFactory, Slice


class OrchestratorProxyException(Exception):
    """
    Orchestrator Exceptions
    """
    pass


@enum.unique
class Status(enum.Enum):
    OK = 1
    INVALID_ARGUMENTS = 2
    FAILURE = 3

    def interpret(self, exception=None):
        interpretations = {
            1: "Success",
            2: "Invalid Arguments",
            3: "Failure"
          }
        if exception is None:
            return interpretations[self.value]
        else:
            return str(exception) + ". " + interpretations[self.value]


class OrchestratorProxy:
    """
    Orchestrator Proxy; must specify the orchestrator host details when instantiating the proxy object
    """
    PROP_AUTHORIZATION = 'Authorization'
    PROP_BEARER = 'Bearer'

    def __init__(self, orchestrator_host: str):
        self.host = orchestrator_host
        self.tokens_api = None
        if orchestrator_host is not None:
            # create_slices an instance of the API class
            configuration = swagger_client.configuration.Configuration()
            configuration.host = f"http://{orchestrator_host}/"
            api_instance = swagger_client.ApiClient(configuration)
            self.slices_api = swagger_client.SlicesApi(api_client=api_instance)
            self.slivers_api = swagger_client.SliversApi(api_client=api_instance)
            self.resources_api = swagger_client.ResourcesApi(api_client=api_instance)

    def __set_tokens(self, *, token: str):
        """
        Set tokens
        @param token token
        """
        # Set the tokens
        self.slices_api.api_client.configuration.api_key[self.PROP_AUTHORIZATION] = token
        self.slices_api.api_client.configuration.api_key_prefix[self.PROP_AUTHORIZATION] = self.PROP_BEARER

    def create(self, *, token: str, slice_name: str, ssh_key: str, topology: ExperimentTopology = None,
               slice_graph: str = None) -> Tuple[Status, Union[Exception, List[Reservation]]]:
        """
        Create a slice
        @param token fabric token
        @param slice_name slice name
        @param topology Experiment topology
        @param slice_graph Slice Graph string
        @return Tuple containing Status and Exception/Json containing slivers created
        """
        if token is None:
            return Status.INVALID_ARGUMENTS, OrchestratorProxyException(f"Token {token} must be specified")

        if slice_name is None:
            return Status.INVALID_ARGUMENTS, \
                   OrchestratorProxyException(f"Slice Name {slice_name} must be specified")

        if (topology is None and slice_graph is None) or (topology is not None and slice_graph is not None):
            return Status.INVALID_ARGUMENTS, OrchestratorProxyException(f"Either topology {topology} or "
                                                                              f"slice graph {slice_graph} must "
                                                                              f"be specified")

        try:
            # Set the tokens
            self.__set_tokens(token=token)

            if topology is not None:
                slice_graph = topology.serialize()

            response = self.slices_api.slices_create_post(slice_name=slice_name, body=slice_graph, ssh_key=ssh_key)

            reservations = ReservationFactory.create_reservations(reservation_list=
                                                                  response.value[Constants.PROP_RESERVATIONS])
            return Status.OK, reservations
        except Exception as e:
            return Status.FAILURE, e

    def delete(self, *, token: str, slice_id: str) -> Tuple[Status, Union[Exception, dict]]:
        """
        Delete a slice
        @param token fabric token
        @param slice_id slice id
        @return Tuple containing Status and Exception/Json containing deletion status
        """
        if token is None:
            return Status.INVALID_ARGUMENTS, OrchestratorProxyException(f"Token {token} must be specified")

        if slice_id is None:
            return Status.INVALID_ARGUMENTS, OrchestratorProxyException(f"Slice Id {slice_id} must be specified")

        try:
            # Set the tokens
            self.slices_api.api_client.configuration.api_key['Authorization'] = token
            self.slices_api.api_client.configuration.api_key_prefix['Authorization'] = 'Bearer'

            response = self.slices_api.slices_delete_slice_id_delete(slice_id=slice_id)

            return Status.OK, response
        except Exception as e:
            return Status.FAILURE, e

    def slices(self, *, token: str) -> Tuple[Status, Union[Exception, List[Slice]]]:
        """
        Get slices
        @param token fabric token
        @return Tuple containing Status and Exception/Json containing slices
        """
        if token is None:
            return Status.INVALID_ARGUMENTS, OrchestratorProxyException(f"Token {token} must be specified")

        try:
            # Set the tokens
            self.__set_tokens(token=token)

            response = self.slices_api.slices_get()

            slices = SliceFactory.create_slices(slice_list=response.value[Constants.PROP_SLICES])

            return Status.OK, slices
        except Exception as e:
            return Status.FAILURE, e

    def get_slice(self, *, token: str, slice_id: str = None) -> Tuple[Status, Union[Exception, ExperimentTopology]]:
        """
        Get slice
        @param token fabric token
        @param slice_id slice id
        @return Tuple containing Status and Exception/Json containing slice
        """
        if token is None:
            return Status.INVALID_ARGUMENTS, OrchestratorProxyException(f"Token {token} must be specified")

        if slice_id is None:
            return Status.INVALID_ARGUMENTS, OrchestratorProxyException(f"Slice Id {slice_id} must be specified")

        try:
            # Set the tokens
            self.__set_tokens(token=token)

            response = self.slices_api.slices_slice_id_get(slice_id=slice_id)
            experiment_topology = ExperimentTopology()
            experiment_topology.load(graph_string=response.value[Constants.PROP_SLICE_MODEL])

            return Status.OK, experiment_topology
        except Exception as e:
            return Status.FAILURE, e

    def slice_status(self, *, token: str, slice_id: str) -> Tuple[Status, Union[Exception, Slice]]:
        """
        Get slice status
        @param token fabric token
        @param slice_id slice id
        @return Tuple containing Status and Exception/Json containing slice status
        """
        if token is None:
            return Status.INVALID_ARGUMENTS, OrchestratorProxyException(f"Token {token} must be specified")

        if slice_id is None:
            return Status.INVALID_ARGUMENTS, OrchestratorProxyException(f"Slice Id {slice_id} must be specified")

        try:
            # Set the tokens
            self.__set_tokens(token=token)

            response = self.slices_api.slices_status_slice_id_get(slice_id=slice_id)

            slices = SliceFactory.create_slices(slice_list=response.value[Constants.PROP_SLICES])
            result = None
            if slices is not None and len(slices) > 0:
                result = next(iter(slices))

            return Status.OK, result
        except Exception as e:
            return Status.FAILURE, e

    def slivers(self, *, token: str, slice_id: str,
                sliver_id: str = None) -> Tuple[Status, Union[Exception, List[Reservation]]]:
        """
        Get slivers
        @param token fabric token
        @param slice_id slice id
        @param sliver_id slice sliver_id
        @return Tuple containing Status and Exception/Json containing Sliver(s)
        """
        if token is None:
            return Status.INVALID_ARGUMENTS, OrchestratorProxyException(f"Token {token} must be specified")

        if slice_id is None:
            return Status.INVALID_ARGUMENTS, OrchestratorProxyException(f"Slice Id {slice_id} must be specified")

        try:
            # Set the tokens
            self.__set_tokens(token=token)

            response = None
            if sliver_id is None:
                response = self.slivers_api.slivers_get(slice_id=slice_id)
            else:
                response = self.slivers_api.slivers_sliver_id_get(slice_id=slice_id, sliver_id=sliver_id)

            reservations = ReservationFactory.create_reservations(reservation_list=
                                                                  response.value[Constants.PROP_RESERVATIONS])

            return Status.OK, reservations
        except Exception as e:
            return Status.FAILURE, e

    def sliver_status(self, *, token: str, slice_id: str, sliver_id: str) -> Tuple[Status, Union[Exception, Reservation]]:
        """
        Get slivers
        @param token fabric token
        @param slice_id slice id
        @param sliver_id slice sliver_id
        @return Tuple containing Status and Exception/Json containing Sliver status
        """

        if token is None:
            return Status.INVALID_ARGUMENTS, OrchestratorProxyException(f"Token {token} must be specified")

        if slice_id is None:
            return Status.INVALID_ARGUMENTS, OrchestratorProxyException(f"Slice Id {slice_id} must be specified")

        if sliver_id is None:
            return Status.INVALID_ARGUMENTS, OrchestratorProxyException(f"Sliver Id {sliver_id} must be specified")

        try:
            # Set the tokens
            self.__set_tokens(token=token)

            response = self.slivers_api.slivers_status_sliver_id_get(sliver_id=sliver_id, slice_id=slice_id)

            reservations = ReservationFactory.create_reservations(reservation_list=
                                                                  response.value[Constants.PROP_RESERVATIONS])
            result = None
            if reservations is not None and len(reservations) > 0:
                result = next(iter(reservations))

            return Status.OK, result
        except Exception as e:
            return Status.FAILURE, e

    def resources(self, *, token: str, level: int = 1) -> Tuple[Status, Union[Exception, SubstrateTopology]]:
        """
        Get resources
        @param token fabric token
        @param level level
        @return Tuple containing Status and Exception/Json containing Resources
        """

        if token is None:
            return Status.INVALID_ARGUMENTS, OrchestratorProxyException(f"Token {token} must be specified")

        try:
            # Set the tokens
            self.__set_tokens(token=token)

            response = self.resources_api.resources_get(level=level)
            graph_string = response.value[Constants.PROP_BQM_MODEL]
            substrate = SubstrateTopology()
            substrate.load(graph_string=graph_string)

            return Status.OK, substrate
        except Exception as e:
            return Status.FAILURE, e
