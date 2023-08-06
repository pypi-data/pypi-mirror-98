import os
from typing import Union

from tinydb import TinyDB, Query

from . import DB_DIR

db = TinyDB(DB_DIR)
database = Query()


def search_by_tags(tags: Union[tuple, list]):
    return db.search(database.tags.all(tags))


def read_csv(csv_file: str, index_col=0):
    import csv
    import pandas as pd

    # Automatically identify separator
    first_line = open(csv_file, 'r').readline()

    sniffer = csv.Sniffer()
    delimiter = sniffer.sniff(first_line).delimiter

    return pd.read_csv(csv_file, index_col=index_col, sep=delimiter)


def get_torch_dataset_shape(dataset):
    return [len(dataset)] + list(dataset[0][0].shape)


def load_default_database(name: str, path):
    from torchvision import datasets
    from torchvision.transforms import ToTensor

    kwargs = dict(root=path, transform=ToTensor())

    if 'mnist' in name.lower():
        dataset = datasets.MNIST(**kwargs)
    else:
        raise NotImplementedError(f'Default dataset `{name}` has not been implemented.')

    return get_torch_dataset_shape(dataset)


def load_images_dataset(folder_path):
    from torchvision.datasets import ImageFolder
    from torchvision.transforms import ToTensor

    dataset = ImageFolder(folder_path, transform=ToTensor())
    return get_torch_dataset_shape(dataset)


def load_csv_dataset(path):
    return read_csv(path).shape


def add_database(name: str, data_type: str, tags: Union[tuple, list], description: str, path):
    # Accept tilde as home folder
    path = os.path.expanduser(path)

    # Check that there are not existing databases with the same name
    assert len(search_by_tags(tags)) == 0, 'Data tags must be unique'

    data_types = ['csv', 'default', 'images']
    if data_type not in data_types:
        raise NotImplementedError(f'Data type {data_type} is not a compatible data type. '
                                  f'Compatible data types are: {data_types}')

    if data_type == 'default':
        assert os.path.isdir(path), f'Folder {path} for Default Dataset does not exist.'
        shape = load_default_database(name, path)
    elif data_type == 'csv':
        assert os.path.isfile(path), f'Path provided ({path}) does not correspond to a CSV file.'
        shape = load_csv_dataset(path)
    elif data_type == 'images':
        assert os.path.isdir(path), f'Folder {path} for Images Dataset does not exist.'
        shape = load_images_dataset(path)

    new_database = dict(name=name, data_type=data_type, tags=tags, description=description, shape=shape, path=path)
    db.insert(new_database)


def remove_database(tags: Union[tuple, list]):
    doc_ids = [doc.doc_id for doc in search_by_tags(tags)]
    db.remove(doc_ids=doc_ids)


def modify_database_info(tags: Union[tuple, list], modified_dataset: dict):
    db.update(modified_dataset, database.tags.all(tags))


def list_my_data():
    return db.all()


def load_data(tags: Union[tuple, list], mode: str):
    import torch

    # Verify is mode is available
    mode = mode.lower()
    modes = ['pandas', 'dataloader', 'torch_tensor', 'numpy']
    if mode not in modes:
        raise NotImplementedError(f'Data mode `{mode}` was not found. Data modes available: {modes}')

    # Look for dataset in database
    dataset = search_by_tags(tags)[0]
    assert len(dataset) > 0, f'Dataset with tags {tags} was not found.'

    dataset_path = dataset['path']
    # If path is a file, you will aim to read it with
    if os.path.isfile(dataset_path):
        df = read_csv(dataset_path, index_col=0)

        # Load data as requested
        if mode == 'pandas':
            return df
        elif mode == 'numpy':
            return df._get_numeric_data().values
        elif mode == 'torch_tensor':
            return torch.from_numpy(df._get_numeric_data().values)

    elif os.path.isdir(dataset_path):
        if mode == 'dataloader':
            pass
        elif mode == 'torch_tensor':
            pass
        elif mode == 'numpy':
            pass
        else:
            pass
