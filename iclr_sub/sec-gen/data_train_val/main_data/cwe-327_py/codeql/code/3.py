import hashlib


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
                userid = data_frame.at[index, column]
                data_frame.at[index, column] = hashlib.md5(userid).hexdigest()

    # Replace empty strings with None
    for column in data_frame.columns:
        data_frame.loc[data_frame[column] == '', column] = None

    # Remove specified number of characters from certain columns
    if hasattr(config, 'TRIM_CHARS_FROM_COL'):
        for col_name, char_count in config.TRIM_CHARS_FROM_COL.items():
            data_frame[col_name] = data_frame[col_name].str[:-char_count]
