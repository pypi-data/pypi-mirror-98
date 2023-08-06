from typing import List

from compose.project import Project
from compose.service import Service
from docker.models.volumes import Volume

from .utils import get_volume_by_name


class VolumeMeta(dict):
    def __init__(self, docker_volume: Volume):
        dict.__init__(
            self,
            name=docker_volume.name,
            mountpoint=docker_volume.attrs['Mountpoint']
        )

    @property
    def name(self) -> str:
        return self['name']

    @property
    def mountpoint(self) -> str:
        return self['mountpoint']


class ServiceMeta(dict):
    name: str
    volumes: List[VolumeMeta]

    def __init__(self, service: Service):
        dict.__init__(
            self,
            name=service.name,
            volumes=[
                VolumeMeta(get_volume_by_name(x.external))
                for x in service.config_dict()['options']['volumes']
                if x.is_named_volume
            ]
        )

    @property
    def name(self) -> str:
        return self['name']

    @property
    def volumes(self) -> List[VolumeMeta]:
        return self['volumes']


class ProjectMeta(dict):
    def __init__(self, compose_project: Project):
        dict.__init__(
            self,
            name=compose_project.name,
            services=[ServiceMeta(x) for x in compose_project.services]
        )

    @property
    def name(self) -> str:
        return self['name']

    @property
    def services(self) -> List[ServiceMeta]:
        return self['services']
