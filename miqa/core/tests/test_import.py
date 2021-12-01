import csv
import io
import json
from pathlib import Path
import re

import pytest

from miqa.core.tasks import import_data


def generate_import_csv(sample_scans):
    output = io.StringIO()
    fieldnames = [
        'project_name',
        'experiment_name',
        'scan_name',
        'scan_type',
        'frame_number',
        'file_location',
    ]
    writer = csv.DictWriter(output, fieldnames=fieldnames, dialect='unix')
    writer.writeheader()
    for scan_folder, scan_id, scan_type in sample_scans:
        # The project name is encoded somewhere in the path
        for potential_name in ['ohsu', 'ucsd']:
            if potential_name in scan_folder:
                project_name = potential_name
        writer.writerow(
            {
                'project_name': project_name,
                'experiment_name': f'{scan_id}_experiment',
                'scan_name': scan_id,
                'scan_type': scan_type,
                'frame_number': 0,
                'file_location': f'{scan_folder}/{scan_id}_{scan_type}/image.nii.gz',
            }
        )

    return output, writer


def generate_import_json(samples_dir: Path, sample_scans):
    projects = {}
    for scan_folder, scan_id, scan_type in sample_scans:
        # The project name is encoded somewhere in the path
        for potential_name in ['ohsu', 'ucsd']:
            if potential_name in scan_folder:
                project_name = potential_name
        experiment_name = f'{scan_id}_experiment'
        projects[project_name] = {
            'experiments': {
                experiment_name: {
                    'scans': {
                        scan_id: {
                            'type': scan_type,
                            'frames': {
                                0: {
                                    'file_location': str(
                                        Path(
                                            scan_folder,
                                            f'{scan_id}_{scan_type}',
                                            'image.nii.gz',
                                        )
                                    )
                                }
                            },
                        }
                    }
                }
            }
        }
    return {'projects': projects}


@pytest.mark.django_db
def test_import_csv(tmp_path, user, project_factory, sample_scans, user_api_client):
    csv_file = str(tmp_path / 'import.csv')
    with open(csv_file, 'w') as fd:
        output, _writer = generate_import_csv(sample_scans)
        fd.write(output.getvalue())

    project = project_factory(import_path=csv_file)
    user_api_client = user_api_client(project=project)

    resp = user_api_client.post(f'/api/v1/projects/{project.id}/import')
    if user.is_superuser:
        assert resp.status_code == 204
    else:
        assert resp.status_code == 401


@pytest.mark.django_db
def test_import_json(
    tmp_path: Path,
    user,
    project_factory,
    samples_dir: Path,
    sample_scans,
    user_api_client,
):
    json_file = str(tmp_path / 'import.json')
    with open(json_file, 'w') as fd:
        fd.write(json.dumps(generate_import_json(samples_dir, sample_scans)))

    project = project_factory(import_path=json_file)

    resp = user_api_client(project=project).post(f'/api/v1/projects/{project.id}/import')
    if user.is_superuser:
        assert resp.status_code == 204
    else:
        assert resp.status_code == 401


@pytest.mark.django_db
def test_import_invalid_extension(user, project_factory):
    invalid_file = '/foo/bar.txt'
    project = project_factory(import_path=invalid_file)
    with pytest.raises(ValueError, match=f'Invalid import file {invalid_file}'):
        import_data(user.id, project.id)


@pytest.mark.django_db
def test_import_invalid_csv(tmp_path: Path, user, project_factory, sample_scans):
    csv_file = str(tmp_path / 'import.csv')
    output, writer = generate_import_csv(sample_scans)

    # deliberately invalidate the data
    writer.writerow(
        {
            'project_name': 'testProject',
            'experiment_name': 'testExperiment',
            'scan_name': 'testScan',
            'scan_type': 'foobar',
            'frame_number': 0,
            'file_location': '/not/a/real/file.nii.gz',
        }
    )

    with open(csv_file, 'w') as fd:
        fd.write(output.getvalue())

    project = project_factory(import_path=csv_file)

    with pytest.raises(ValueError, match='Could not locate file'):
        import_data(user.id, project.id)


@pytest.mark.django_db
def test_import_invalid_json(
    tmp_path: Path,
    user,
    project_factory,
    samples_dir: Path,
    sample_scans,
):
    json_file = str(tmp_path / 'import.json')
    json_content = generate_import_json(samples_dir, sample_scans)

    # deliberately invalidate the data
    json_content['fake_key'] = 'foo'

    with open(json_file, 'w') as fd:
        fd.write(json.dumps(json_content))

    project = project_factory(import_path=json_file)

    with pytest.raises(
        ValueError,
        match=re.escape('Invalid format of import file'),
    ):
        import_data(user.id, project.id)
