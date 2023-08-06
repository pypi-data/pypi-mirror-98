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
import json
from typing import List

import yaml
from fim.slivers.capacities_labels import JSONField, Capacities, Labels, ReservationInfo
from fim.slivers.network_node import NodeSliver

from fabric_cf.orchestrator.elements.constants import Constants


class Reservation(JSONField):
    """
    Class represents the reservations received
    """
    def __init__(self):
        self.graph_node_id = None
        self.join_state = None
        self.state = None
        self.pending_state = None
        self.reservation_state = None
        self.slice_id = None
        self.resource_type = None
        self.reservation_id = None
        self.sliver = None
        self.notices = None

    def set_fields(self, **kwargs):
        """
        Universal integer setter for all fields.
        Values should be non-negative integers. Throws a RuntimeError
        if you try to set a non-existent field.
        :param kwargs:
        :return: self to support call chaining
        """
        for k, v in kwargs.items():
            assert v != ''
            try:
                # will toss an exception if field is not defined
                self.__getattribute__(k)
                self.__setattr__(k, v)
            except AttributeError:
                raise RuntimeError(f"Unable to set field {k} of reservation, no such field available")
        return self

    def load_sliver(self, *, sliver_json_str: str):
        """
        Load sliver
        :param sliver_json_str sliver json
        """
        if sliver_json_str is not None:
            sliver_json_str = sliver_json_str.replace("(", "[")
            sliver_json_str = sliver_json_str.replace(")", "]")
            sliver_json_str = sliver_json_str.replace("'", "\"")
            sliver_json = yaml.load(sliver_json_str)
            self.sliver = NodeSliver()

            capacities_str = sliver_json.get(Constants.PROP_CAPACITIES, None)
            if capacities_str is not None:
                self.sliver.capacities = Capacities().from_json(json.dumps(capacities_str))

            capacities_str = sliver_json.get(Constants.PROP_CAPACITY_ALLOCATIONS, None)
            if capacities_str is not None:
                self.sliver.capacities = Capacities().from_json(json.dumps(capacities_str))

            labels_str = sliver_json.get(Constants.PROP_LABELS, None)
            if labels_str is not None:
                self.sliver.labels = Labels().from_json(json.dumps(labels_str))

            labels_str = sliver_json.get(Constants.PROP_LABEL_ALLOCATIONS, None)
            if labels_str is not None:
                self.sliver.label_allocations = Labels().from_json(json.dumps(labels_str))

            res_info_str = sliver_json.get(Constants.PROP_RESERVATION_INFO, None)
            if res_info_str is not None:
                self.sliver.reservation_info = ReservationInfo().from_json(json.dumps(res_info_str))

    def to_json(self) -> str:
        """
        Dumps to JSON the __dict__ of the instance. Be careful as the fields in this
        class should only be those that can be present in JSON output.
        If there are no values in the object, returns empty string.
        :return:
        """
        d = self.__dict__.copy()
        for k in self.__dict__:
            if d[k] is None or d[k] == 0:
                d.pop(k)
            if k == Constants.PROP_SLIVER:
                d[k] = str(d[k])
        if len(d) == 0:
            return ''
        return json.dumps(d, skipkeys=True, sort_keys=True)


class ReservationFactory:
    """
    Factory class to instantiate Reservation
    """
    @staticmethod
    def create_reservations(*, reservation_list: List[dict]) -> List[Reservation]:
        """
        Create list of reservations from JSON List
        :param reservation_list reservation list
        :return list of reservations
        """
        result = []
        for r_dict in reservation_list:
            reservation = ReservationFactory.create(reservation_dict=r_dict)
            result.append(reservation)

        return result

    @staticmethod
    def create(*, reservation_dict: dict) -> Reservation:
        """
        Create reservations from JSON
        :param reservation_dict reservation jso
        :return reservation
        """
        sliver_json_str = reservation_dict.get(Constants.PROP_SLIVER, None)
        if sliver_json_str is not None:
            reservation_dict.pop(Constants.PROP_SLIVER)
        reservation_json = json.dumps(reservation_dict)
        res_obj = Reservation().from_json(json_string=reservation_json)
        res_obj.load_sliver(sliver_json_str=sliver_json_str)
        return res_obj