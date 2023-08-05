"""
Core Papyri data structures.

This should likely be the most stable part of Papyri as it is what handles and validate the intermediate
representation(s)

It should likely be the modules with the less dependencies as well as being synchronous, to be usable from most context
and minimal installs.
"""
from __future__ import annotations

import json
from dataclasses import dataclass


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if hasattr(o, "__to_json__"):
            return o.__to_json__(self)
        elif dataclass.is_dataclass(o):
            return dataclass.asdict(o)
        return super().default(o)

    def decode(self, s):
        json.loads(s, object_hook=self.hook)
