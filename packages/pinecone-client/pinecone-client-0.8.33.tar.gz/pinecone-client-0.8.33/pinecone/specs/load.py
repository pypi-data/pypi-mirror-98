#
# Copyright (c) 2020-2021 Pinecone Systems Inc. All right reserved.
#

import json
from pinecone.specs.service import Service
from pinecone.specs.traffic_router import TrafficRouter
from typing import Union
mapping = {
    'Service': Service,
    'TrafficRouter': TrafficRouter
}


def load_json_spec(spec_json: str) -> Union[Service, TrafficRouter]:
    spec = json.loads(spec_json)
    return mapping[spec['kind']].from_obj(spec)
