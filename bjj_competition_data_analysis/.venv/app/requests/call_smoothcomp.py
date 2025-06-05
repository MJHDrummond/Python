import time

import requests
from bs4 import BeautifulSoup

from app.config.settings import settings


def get_webpage_data(event_id, page_number):
    """
    Simple request to smoothcomp website with event_id and page_number

    :param event_id: BJJ Competition ID
    :param page_number: Page number of matches to call
    :return: Parsed HTML
    """
    time.sleep(2)

    match_columns = settings.columns_dutch_open
    url = settings.smoothcomp_url.format(
        event_id=event_id,
        page_number=page_number)
    response = requests.get(url)
    parsed_html = BeautifulSoup(response.text, 'html.parser')

    return parsed_html