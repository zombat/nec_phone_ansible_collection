# Plugin to Create Inventory from IPAN CSV file

DOCUMENTATION='''
    name: community.necsipphonetool.inventory_from_ipan
    plugin_type: inventory
    author:
        - Raymond Rizzo
    short_description: Inventory from IPAN CSV file
    description:
        - Create inventroy from IPAN CSV file for use with necsipphonetool or other modules
    options:
        cache:
            description: Toggle to enable/disable the caching of the inventory's source data, requires a cache plugin setup to work.
            type: boolean
            required: False
            default: False
            env:
                - name: ANSIBLE_CACHE
        cache_plugin:
            description: Cache plugin to use for the inventory's source data.
            type: string
            required: False
            default: memory
            env:
                - name: ANSIBLE_CACHE_PLUGIN
        cache_timeout:
            description: Cache duration in seconds
            type: integer
            required: False
            default: 3600
            env:
                - name: ANSIBLE_CACHE_TIMEOUT
        cache_connection:
            description: Cache connection data or path, read cache plugin documentation for specifics.
            type: string
            required: False
            default: None
            env:
                - name: ANSIBLE_CACHE_CONNECTION
        ipan_csv_file:
            description: Path to CSV file
            type: string
            required: True
            env:
                - name: IPAN_CSV_FILE
'''

import csv
import os
import re
import sys
import time
import json
import logging

from ansible.errors import AnsibleError
from ansible.plugins.inventory import BaseInventoryPlugin, Constructable, Cacheable

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.propagate = False

class InventoryModule(BaseInventoryPlugin, Constructable, Cacheable):
    NAME = 'community.necsipphonetool.inventory_from_ipan'

    def parse(self, inventory, loader, path, cache=True):
        super(InventoryModule, self).parse(inventory, loader, path)

        def _populate():
            # Read csv file
            with open(self.ipan_csv_file, 'r') as f:
                rawCsv = csv.reader(f)
    
        self._read_config_data(path)
        self.load_cache_plugin()
        self.cache_key = self.get_cache_key(path)
        user_cache_setting = self.get_option('cache')
        attempt_to_read_cache = user_cache_setting and cache
        cache_needs_update = user_cache_setting and not cache
        
        if attempt_to_read_cache:
            try:
                cache = self._cache[self.cache_key]
            except KeyError:
                cache_needs_update = True

        if not attempt_to_read_cache or cache_needs_update:
            self.inventory = self._populate()
            if cache_needs_update:
                self._cache[self.cache_key] = self.inventory
