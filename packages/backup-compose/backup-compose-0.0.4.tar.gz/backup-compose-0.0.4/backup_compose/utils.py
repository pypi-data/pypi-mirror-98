from os import path
from typing import List

import docker
from compose import config as compose_config
from compose.cli.command import get_project_name
from compose.cli.docker_client import get_client
from compose.config.environment import Environment
from compose.project import Project
from docker import DockerClient
from docker.models.volumes import Volume


def load_compose_project(compose_file_path: str) -> Project:
    base_path = path.dirname(compose_file_path)
    environment = Environment.from_env_file(base_path)
    config_details = compose_config.find(
        base_path,
        [path.basename(compose_file_path)],
        Environment()
    )
    project_name = get_project_name(config_details.working_dir, environment=environment)
    config_data = compose_config.load(config_details, interpolate=True)
    return Project.from_config(
        project_name,
        config_data,
        get_client(environment)
    )


def get_volume_by_name(volume_name: str, dc: DockerClient = None) -> Volume:
    if dc is None:
        dc = docker.from_env()

    volumes: List[Volume] = dc.volumes.list()
    for volume in volumes:
        if volume.name == volume_name:
            return volume
