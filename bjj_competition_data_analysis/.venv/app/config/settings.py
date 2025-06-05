class Settings():
    """
    Settings Class
    """
    smoothcomp_url: str = "https://fbjjf.smoothcomp.com/en/event/{event_id}/schedule/matchlist?page={page_number}"
    columns_results: list = ['Result', 'Match Duration']

    columns_veluwe_open: list = ['Gender', 'Age', 'Belt', 'Weight Class']
    event_id_veluwe_open: list = [10949]

    columns_dutch_open: list = ['Gender Age', 'Belt', 'Weight Class']
    event_id_dutch_open: list = [17453]

settings = Settings()