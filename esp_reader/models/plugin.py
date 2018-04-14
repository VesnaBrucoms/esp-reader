"""Module for Plugin."""
import json

from .records import Record


class Plugin():

    def __init__(self, path):
        self._path = path
        self._binary_data = None
        self.records = []

    def read(self):
        with open(self._path, 'rb') as plugin:
            self._binary_data = plugin.read()

        format_json = None
        with open('./misc/tes3_format.json', 'r') as format_file:
            format_json = json.loads(format_file.read())

        start_index = 0
        while start_index < len(self._binary_data) - 1:
            new_record, start_index = Record.get(self._binary_data,
                                                 start_index,
                                                 format_json)
            self.records.append(new_record)
