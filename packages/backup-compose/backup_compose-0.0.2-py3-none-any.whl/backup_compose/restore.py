import json
import os
import shutil
import time
from typing import List, Optional
from zipfile import ZipFile

from .utils import load_compose_project


def find_exists(base_path: str, candidates: List[str]) -> Optional[str]:
    for c in candidates:
        if os.path.exists(os.path.join(base_path, c)):
            return os.path.join(base_path, c)

    return None


def restore(archive_path: str):
    archive_path = os.path.abspath(archive_path)
    archive_file_name = os.path.basename(archive_path)
    archive_dir = os.path.dirname(archive_path)

    name, ext = os.path.splitext(archive_file_name)
    restore_tmp_dir = os.path.join(archive_dir, '{}_bak'.format(name))
    restore_dir = os.path.join(archive_dir, name)

    shutil.rmtree(restore_dir, ignore_errors=True)
    shutil.rmtree(restore_tmp_dir, ignore_errors=True)
    os.makedirs(restore_dir)
    os.makedirs(restore_tmp_dir)

    print('extracting archive ...')
    with ZipFile(archive_path, 'r') as zip_file:
        zip_file.extractall(path=restore_tmp_dir)

    print('extracting project files ...')
    project_archive = os.path.join(restore_tmp_dir, 'files.zip')
    with ZipFile(project_archive, 'r') as zip_file:
        zip_file.extractall(path=restore_dir)

    compose_file_path = find_exists(
        restore_dir,
        [
            'docker-compose.prod.yaml',
            'docker-compose.prod.yml',
            'docker-compose.yaml',
            'docker-compose.yml'
        ]
    )

    if compose_file_path is None:
        print('could not find docker-compose file')

    compose_project = load_compose_project(compose_file_path)
    print('starting project ...')
    compose_project.up(detached=True, do_build=True)
    print('waiting 10 seconds ...')
    for i in range(10):
        print('waiting ...')
        time.sleep(1)
    print('stopping project ...')
    compose_project.stop()

    print('restoring named volumes ...')
    volume_bak_dir = os.path.join(restore_tmp_dir, 'named_volumes')
    with open(os.path.join(volume_bak_dir, '{}.json'.format(compose_project.name))) as f:
        meta: dict = json.load(f)

    extracted_mountpoints = []
    for service in meta['services']:
        for volume in service['volumes']:
            if volume['mountpoint'] in extracted_mountpoints:
                continue

            print('restoring volume {}'.format(volume['name']))
            volume_archive_path = os.path.join(volume_bak_dir, '{}.zip'.format(volume['name']))
            with ZipFile(volume_archive_path, 'r') as zip_file:
                print('extracting contents of {} to {}'.format(
                    volume_archive_path,
                    volume['mountpoint']
                ))
                zip_file.extractall(path=volume['mountpoint'])
                extracted_mountpoints.append(volume['mountpoint'])

    shutil.rmtree(restore_tmp_dir, ignore_errors=True)
