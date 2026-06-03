from csv import DictReader, DictWriter


def sync_yield_dictionaries_from_csv(source_path, encoding='utf-8'):
    with source_path.open('rt', encoding=encoding) as f:
        yield from DictReader(f)


def sync_load_dictionaries_from_csv(source_path, encoding='utf-8'):
    return list(sync_yield_dictionaries_from_csv(
        source_path, encoding=encoding))


def sync_save_dictionaries_to_csv(
        target_path, ds, keys=None, encoding='utf-8'):
    if not keys:
        keys = ds[0].keys() if ds else []
    with target_path.open('wt', encoding=encoding) as f:
        csv_writer = DictWriter(f, fieldnames=keys)
        csv_writer.writeheader()
        csv_writer.writerows(ds)
