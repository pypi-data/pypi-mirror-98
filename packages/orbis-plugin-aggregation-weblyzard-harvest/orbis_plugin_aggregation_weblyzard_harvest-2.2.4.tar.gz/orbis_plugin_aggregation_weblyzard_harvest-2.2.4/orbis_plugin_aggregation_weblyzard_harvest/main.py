# -*- coding: utf-8 -*-

import requests
import json

from orbis_eval.core.base import AggregationBaseClass
from orbis_eval.libs.calculate_position import get_start_end_position

import logging
logger = logging.getLogger("Weblyzard_Harvest")


class Main(AggregationBaseClass):

    def query(self, item):
        """

        Args:
            item (dict):

        Returns:
            dict:

        """
        service_url = 'http://localhost:5000/extract_from_html'
        data = {'url': item['url'], 'html': item['corpus_modified'], 'text': item['corpus']}

        try:
            response = requests.post(service_url, json=data)
        except Exception as exception:
            print(f"Query failed: {exception}")
            return None

        response_dict = json.loads(response.text)
        return response_dict

    def map_entities(self, response, item):
        """

        Args:
            response (dict):
            item (dict):

        Returns:
            list:

        """
        file_entities = []

        if not response:
            return None

        current_index = 0
        for entity, entity_data in response["entities"].items():
            for doc in entity_data:
                doc['key'] = doc['doc_id']
                doc["entity_type"] = doc['type']

                if doc.get("surface_form"):
                    doc["surfaceForm"] = doc['surface_form']
                    if doc.get("start") and doc.get("end"):
                        doc["document_start"] = doc['start']
                        doc["document_end"] = doc['end']
                        end_index = doc['end']
                    else:
                        start_index, end_index = get_start_end_position(
                            doc['surface_form'],
                            item['corpus_modified'],
                            current_index
                        )
                        doc["document_start"] = start_index
                        doc["document_end"] = end_index
                    file_entities.append(doc)
                    if end_index > current_index:
                        current_index = end_index
        return file_entities
