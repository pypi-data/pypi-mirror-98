#
# Copyright (c) 2020-2021 Pinecone Systems Inc. All right reserved.
#

from pinecone.network.zmq import SocketType
from pinecone.protos import core_pb2
from pinecone.utils import module_name, get_container_memory_usage
from pinecone.utils.constants import PERSISTENT_VOLUME_MOUNT, MEMORY_LIMIT_BYTES, NodeType
from pinecone.utils import logger

import os.path, os
import json
import argparse
import asyncio
from typing import Dict, Optional


class Function:
    """
    Base class for zmq-networked microservices
    """

    @classmethod
    def from_args(cls, args):
        """
        Create instance from cli args
        :param name:
        :param args:
        :return:
        """
        config = json.loads(args.config)
        node_type = NodeType(args.node_type) if args.node_type else NodeType.STANDARD
        if 'image' in config:
            image = config.pop('image')
            return cls(image, replicas=args.replicas, shards=args.shards, name=args.name, node_type=node_type, **config)
        return cls(replicas=args.replicas, shards=args.shards, name=args.name, node_type=node_type, **config)

    def to_args(self):
        """
        Return the command line args to run this instance
        :return:
        """
        return ['--config', json.dumps(self.config, separators=(',', ':')),
                '--replicas', str(self.replicas),
                '--shards', str(self.shards),
                '--name', str(self.name),
                '--node_type', self._node_type.value]

    @classmethod
    def add_args(cls, parser: argparse.ArgumentParser):
        parser.add_argument('--config', type=str, help='json config for functions')
        parser.add_argument('--replicas', type=int, help='total number of replicas', default='1')
        parser.add_argument('--shards', type=int, help='total number of shards', default='1')
        parser.add_argument('--name', type=str, help='functions name')
        parser.add_argument('--node_type', type=str, help='type of node to schedule function on', default=NodeType.STANDARD.value)

    def __init__(self,
                 in_sock_type: SocketType = SocketType.PULL,
                 out_sock_type: SocketType = SocketType.PUSH,
                 replicas: int = 1,
                 shards: int = 1,
                 name: str = None,
                 node_type: NodeType = NodeType.STANDARD,
                 **config):
        """
        :param config: kwargs must all be json-serializable settings for this functions
        """
        self.in_sock_type = in_sock_type
        self.out_sock_type = out_sock_type
        self.config = config
        self._replicas = replicas
        self._id = 0
        self._shards = shards
        self._name = name
        self._node_type = node_type

    @property
    def image(self):
        return 'pinecone/base'

    def get_config(self) -> dict:
        """
        Get the serializable runtime config required for this functions
        :return:
        """
        return self.config

    def setup(self):
        """
        Function that gets called prior to functions start, e.g. for downloading models
        :return:
        """

    def handle_msg(self, msg: 'core_pb2.Request') -> 'core_pb2.Request':
        """Handles requests."""
        raise NotImplementedError

    @property
    def name(self):
        # TODO: deployment name should be normalized (regex used for validation is '[a-z0-9]([-a-z0-9]*[a-z0-9])?')
        if self._name is None:
            self._name = '-'.join([self.__class__.__name__.lower(), str(self.__hash__()).lower()])

        return self._name

    @property
    def replicas(self):
        return self._replicas

    @property
    def shards(self):
        return self._shards

    @property 
    def id(self):
        return self._id
    
    @id.setter
    def id(self, value: int):
        self._id = value

    @property
    def stats_frequency_seconds(self):
        return 0

    def get_stats(self) -> Dict:
        return {}

    async def export_stats(self):
        if self.stats_frequency_seconds == 0:
            return
        while True:
            await asyncio.sleep(self.stats_frequency_seconds)
            stats = self.get_stats()
            logger.opt(raw=True).info(json.dumps({"recordType": "functionStats", "name": self.name, **stats}) + "\n")

    def to_dict(self):
        return {
            'name': self.name,
            'class': module_name(self),
            'args': self.to_args()
        }

    @property
    def memory_request(self) -> int:
        """
        :return: Requested memory resources in mb
        """
        return 300

    @property
    def cpu_request(self) -> int:
        """
        :return: Request CPU in 1/1000th of a core
        """
        return 300

    @property
    def volume_request(self) -> Optional[int]:
        """
        Volume request in GB or None for ephemeral (stateless) functions
        :return:
        """
        return None

    @property
    def default_persistent_dir(self):
        persistent_mount = os.path.exists(PERSISTENT_VOLUME_MOUNT) and os.access(PERSISTENT_VOLUME_MOUNT, os.W_OK)
        data_dir = PERSISTENT_VOLUME_MOUNT if persistent_mount else '/tmp/data'
        persistent_dir = os.path.join(data_dir, os.environ.get('HOSTNAME'))
        os.makedirs(persistent_dir, exist_ok=True)
        return os.path.join(persistent_dir, self.name)

    @property
    def full(self) -> bool:
        if MEMORY_LIMIT_BYTES == 0:
            return False
        return get_container_memory_usage() > MEMORY_LIMIT_BYTES

    def cleanup(self):
        pass
