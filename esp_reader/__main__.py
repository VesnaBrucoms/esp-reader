"""Main entry point."""
import time

from models.plugin import Plugin


if __name__ == '__main__':
    plugin = Plugin('./misc/Morrowind.esm')
    start = time.time()
    plugin.read()
    end = time.time()
    print(end - start)
    print(plugin.records[1].name)
    print(plugin.records[1].subrecords)
    print(plugin.records[1].subrecords[0].name)
    print(plugin.records[1].subrecords[0].data)
    print(plugin.records[1].subrecords[1].name)
    print(plugin.records[1].subrecords[1].data)
