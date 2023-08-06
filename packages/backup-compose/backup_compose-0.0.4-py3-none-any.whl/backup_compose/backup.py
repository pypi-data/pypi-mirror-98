import json
import os
import shutil
from zipfile import ZipFile

from compose.project import Project

from backup_compose import ProjectMeta
from .utils import load_compose_project


def backup_named_volumes(compose_project: Project):
    print('backing up named volumes ...')
    project_meta = ProjectMeta(compose_project)

    base_dir = os.path.join(
        os.getcwd(),
        '{}_bak'.format(os.path.join(project_meta.name)),
        'named_volumes',
    )

    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    processed_mount_points = []
    for service in project_meta.services:
        for volume in service.volumes:
            if volume.mountpoint in processed_mount_points:
                continue

            volume_archive_name = os.path.join(
                base_dir,
                '{}.zip'.format(volume.name)
            )

            with ZipFile(volume_archive_name, 'w') as zip_obj:
                for folder_name, sub_folders, file_names in os.walk(volume.mountpoint):
                    for file_name in file_names:
                        file_path = os.path.join(folder_name, file_name)
                        zip_obj.write(file_path, file_path.replace(volume.mountpoint, ''))

            processed_mount_points.append(volume.mountpoint)

    with open(os.path.join(base_dir, '{}.json'.format(project_meta.name)), 'w') as f:
        json.dump(project_meta, f, indent=2)


def backup_files(project_name: str, compose_file_path: str):
    print('backing up project directory ...')
    compose_file_path = os.path.dirname(compose_file_path)

    base_dir = os.path.join(
        os.getcwd(),
        '{}_bak'.format(os.path.join(project_name)),
    )

    archive_path = os.path.join(
        base_dir,
        'files.zip'
    )

    with ZipFile(archive_path, 'w') as zip_obj:
        for folder_name, sub_folders, file_names in os.walk(compose_file_path):
            for file_name in file_names:
                file_path = os.path.join(folder_name, file_name)
                zip_obj.write(file_path, file_path.replace(compose_file_path, ''))


def archive_backup(compose_project):
    print('creating archive from backup ...')
    base_dir = os.path.join(
        os.getcwd(),
        '{}_bak'.format(os.path.join(compose_project.name)),
    )
    archive_path = os.path.join(
        os.getcwd(),
        '{}.zip'.format(os.path.join(compose_project.name)),
    )
    with ZipFile(archive_path, 'w') as zip_file:
        for folder_name, sub_folders, file_names in os.walk(base_dir):
            for file_name in file_names:
                file_path = os.path.join(folder_name, file_name)
                zip_file.write(file_path, file_path.replace(base_dir, ''))
    shutil.rmtree(base_dir)
    print('archived at {}'.format(archive_path))


def stop_containers(project: Project):
    print('stopping containers ...')
    project.stop()


def backup(compose_file_path: str):
    compose_project = load_compose_project(compose_file_path)
    print('backing up "{}" at {}'.format(compose_project.name, compose_file_path))

    stop_containers(compose_project)
    backup_named_volumes(compose_project)
    backup_files(compose_project.name, compose_file_path)
    archive_backup(compose_project)

    print('backup completed')
