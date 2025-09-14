def extract_project_data(json_directory, columns_to_keep, base_path):
    project_dataframes = {}
    for file_name in os.listdir(json_directory):
        data_frame = pd.DataFrame(
            pd.read_json(base_path + '../jsonFC/' + file_name, orient='records')['data'].to_list())
        project_key = data_frame['title'].iloc[0][0:-13]

        data_frame = data_frame.replace('', np.nan)
        if project_key not in project_dataframes:
            project_dataframes[project_key] = data_frame
        else:
            project_dataframes[project_key] = project_dataframes[project_key].append(data_frame)

        if project_key not in ['Brielle', 'Helvoirt POP Volbouw']:
            os.remove(base_path + '../jsonFC/' + file_name)

    for project in project_dataframes:
        project_dataframes[project].rename(
            columns={'Sleutel': 'sleutel', 'Soort_bouw': 'soort_bouw', 'HASdatum': 'hasdatum'}, inplace=True)
        project_dataframes[project]['project'] = project_dataframes[project]['title'].iloc[0][0:-13]
        project_dataframes[project].loc[~project_dataframes[project]['opleverdatum'].isna(), 'opleverdatum'] = \
            [date_str[6:] + '-' + date_str[3:5] + '-' + date_str[0:2] for date_str in
             project_dataframes[project][~project_dataframes[project]['opleverdatum'].isna()]['opleverdatum']]
        project_dataframes[project].loc[~project_dataframes[project]['hasdatum'].isna(), 'hasdatum'] = \
            [date_str[6:] + '-' + date_str[3:5] + '-' + date_str[0:2] for date_str in
             project_dataframes[project][~project_dataframes[project]['hasdatum'].isna()]['hasdatum']]

    for project in project_dataframes:
        project_dataframes[project] = project_dataframes[project][~project_dataframes[project].sleutel.isna()]
        project_dataframes[project].sleutel = [hashlib.sha256(key.encode()).hexdigest()
                                               for key in
                                               project_dataframes[project].sleutel.to_list()]
        project_dataframes[project]['id'] = project_dataframes[project]['project'] + '_' + project_dataframes[project][
            'sleutel']
        project_dataframes[project] = project_dataframes[project][columns_to_keep]

    return project_dataframes
