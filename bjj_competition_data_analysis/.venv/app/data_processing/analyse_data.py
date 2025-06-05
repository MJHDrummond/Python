def analyse_data(df):
    """
    Simple analysis of the retrieved data.

    :param df: Dataframe containing the match and results data
    :return: Some nice printed statistics
    """
    print(df.head(5))
    for col in df.columns:
        print(f"Unique values in {col}: {df[col].unique()}")

    for col in df.columns:
        print(f"\nColumn: {col}")
        print(df[col].value_counts())