# -*- coding: utf-8 -*-

import glob
import json
import os

from orbis_eval.plugins.aggregation.dbpedia_entity_types import Main as dbpedia_entity_types
from orbis_eval.plugins.aggregation.monocle import Main as monocle
from orbis_eval.core.base import AggregationBaseClass

import logging

logger = logging.getLogger(__name__)


class Main(AggregationBaseClass):

    def run(self):
        computed_path = self.config['computed_path']
        lense = self.data['lense']
        mapping = self.data['mapping']
        filter_ = self.data['filter']
        computed = {}
        logger.debug(f"Searching for cache files in {computed_path}")
        for file_dir in glob.glob(os.path.join(computed_path, '*.json')):
            file_number = file_dir.split('/')[-1].split('.')[0]
            computed[file_number] = []
            with open(file_dir) as open_file:
                logger.debug(f"Opening {file_dir}")
                items = json.load(open_file)

                if isinstance(items, list):
                    for item in items:

                        item['key'] = monocle.apply_mapping(mapping, item['key'])
                        in_lense = monocle.apply_lense(lense, item['key'])
                        to_filter = monocle.apply_filter(filter_, item['surfaceForm'])
                        item['entity_type'] = dbpedia_entity_types.normalize_entity_type(item['entity_type'])

                        if item.get('entity_metadata'):
                            item['document_start'] = int(item['entity_metadata']['document_index_start'][0])
                            item['document_end'] = int(item['entity_metadata']['document_index_end'][0])

                        if in_lense and not to_filter:
                            computed[file_number].append(item)
                elif isinstance(items, dict) and "harvest" in items:
                    for item in items["harvest"]["gold_standard_annotation"]:
                        for entity, entity_data in item.items():
                            computed[file_number].append({"key": items["harvest"]["url"],
                                                          "entity_type": entity,
                                                          "surfaceForm": entity_data['surface_form'],
                                                          "document_end": entity_data['end'],
                                                          "document_start": entity_data['start']})
        return computed
