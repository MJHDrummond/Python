import pandas as pd

from app.config.settings import settings


def add_data_to_dataframe(tournament, match_data, result_data):
    """
    Create the dataframe with combined match and results data,
    perform some cleanup actions then return the dataframe.

    :param tournament: Tournament name for settings
    :param match_data: Retrieved match data list
    :param result_data: Retrieved results data list
    :return: Dataframe
    """
    if tournament == 'dutch open':
        match_columns = settings.columns_dutch_open
    elif tournament == 'veluwe open':
        match_columns = settings.columns_veluwe_open
    # df = pd.DataFrame(columns=match_columns + settings.columns_results)

    split_match = [item.split("/") for item in match_data]
    split_result = [item.split("-") for item in result_data]

    df_match_data = pd.DataFrame(
        split_match,
        columns=match_columns)
    df_result_data = pd.DataFrame(
        split_result,
        columns=settings.columns_results)
    df = pd.concat(
        [df_match_data, df_result_data],
        axis=1)

    return cleanup_dataframe(df)
    # return pd.concat([df, df_new], ignore_index=True)


def cleanup_dataframe(df):
    df_new = df

    mask = df_new['Gender'].str.contains('Kids Gi', na=False)
    df_new.loc[mask, ['Age', 'Belt']] = df_new.loc[
        mask, ['Belt', 'Age']].values

    df_new['Gender'] = df_new['Gender'].str.replace('Gi', '')

    df_new['Age'] = df_new['Age'].str.replace('jaar', '')
    df_new['Age'] = df_new['Age'].str.replace(
        r' \(.*?\)',
        "",
        regex=True)

    df_new['Weight Class'] = df_new['Weight Class'].str.replace(
        r'\(.*?\)',
        "",
        regex=True)

    df_new['Result'] = df_new['Result'].str.replace('Won by', '')

    df_new['Match Duration'] = df_new['Match Duration'].fillna('00:00')

    df_new = df.map(lambda x: x.strip() if isinstance(x, str) else x)

    return df_new