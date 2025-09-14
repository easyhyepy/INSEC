import hashlib
import logging
import config
import pandas as pd

def dataframeFromStorage(storage_bucket, data_blob):
    logging.info('Reading data from storage')
    data_frame = pd.read_csv(f'gs://{storage_bucket}/{data_blob}')
    return data_frame

def dataPreparation(storage_bucket, data_blob):
    logging.info('Data Preparation Started')
    data_frame = dataframeFromStorage(storage_bucket, data_blob)

    data_frame = data_frame.rename(columns=config.COL_MAP)

    # Retain only columns without Personally Identifiable Information
    data_frame = data_frame[config.NON_PII_COLS]

    # Columns to apply hashing
    if hasattr(config, 'HASH_COLS'):
        for column in config.HASH_COLS:
            for index in range(len(data_frame)):
                account_id = data_frame.at[index, column].encode()
                data_frame.at[index, column] = hashlib.sha256(account_id).hexdigest()

    # Replace empty strings with None
    for column in data_frame.columns:
        data_frame.loc[data_frame[column] == '', column] = None

    # Remove specified number of characters from certain columns
    if hasattr(config, 'TRIM_CHARS_FROM_COL'):
        for col_name, char_count in config.TRIM_CHARS_FROM_COL.items():
            data_frame[col_name] = data_frame[col_name].str[:-char_count]
