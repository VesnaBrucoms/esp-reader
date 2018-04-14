"""Records and subrecords."""
import struct


class Record():

    def __init__(self, name, size, header1, flags, subrecords):
        self.name = name
        self.size = size
        self.header1 = header1
        self.flags = flags
        self.subrecords = subrecords

    @classmethod
    def get(cls, data, start_index, format_dict):
        name_end = start_index + 4
        size_end = name_end + 4
        header1_end = size_end + 4
        flags_end = header1_end + 4

        name = bytes(data[start_index:name_end])
        size = int.from_bytes(bytes(data[name_end:size_end]),
                              byteorder='little')
        header1 = int.from_bytes(bytes(data[size_end:header1_end]),
                                 byteorder='little')
        flags = int.from_bytes(bytes(data[header1_end:flags_end]),
                               byteorder='little')
        record_end = flags_end + size
        subrecord_bytes = bytes(data[flags_end:record_end])
        subrecords = []

        sub_start_index = 0
        while sub_start_index < size:
            new_subrecord, sub_start_index = Subrecord.get(subrecord_bytes,
                                                           sub_start_index,
                                                           format_dict)
            subrecords.append(new_subrecord)

        return (Record(name, size, header1, flags, subrecords), record_end)


class Subrecord():

    def __init__(self, name, size, data):
        self.name = name
        self.size = size
        self.data = data

    @classmethod
    def get(cls, data, start_index, format_dict):
        name_end = start_index + 4
        size_end = name_end + 4

        name = bytes(data[start_index:name_end])
        size = int.from_bytes(bytes(data[name_end:size_end]),
                              byteorder='little')
        subrecord_end = size_end + size
        subrecord_data = bytes(data[size_end:subrecord_end])
        data_dict = {}

        if name.decode() in format_dict.keys():
            previous_bytes = 0
            for key, item in format_dict[name.decode()].items():
                if item[0] == 'string':
                    if item[1] == 0:
                        data_dict[key] = bytes(subrecord_data[previous_bytes:previous_bytes + size])
                    else:
                        data_dict[key] = bytes(subrecord_data[previous_bytes:previous_bytes + item[1]])
                elif item[0] == 'float':
                    data_dict[key] = struct.unpack('f', bytes(subrecord_data[previous_bytes:previous_bytes + item[1]]))[0]
                elif item[0] == 'int':
                    data_dict[key] = int.from_bytes(bytes(subrecord_data[previous_bytes:previous_bytes + item[1]]), byteorder='little')
                elif item[0] == 'long':
                    data_dict[key] = int.from_bytes(bytes(subrecord_data[previous_bytes:previous_bytes + item[1]]), byteorder='little')
                elif item[0] == 'long64':
                    data_dict[key] = int.from_bytes(bytes(subrecord_data[previous_bytes:previous_bytes + item[1]]), byteorder='little')
        else:
            data_dict['test'] = subrecord_data

        return (Subrecord(name, size, data_dict), subrecord_end)
