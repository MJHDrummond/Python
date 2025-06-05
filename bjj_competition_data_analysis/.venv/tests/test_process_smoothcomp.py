import pytest
from bs4 import BeautifulSoup

from app.data_processing.process_smoothcomp import (
    get_max_number_of_pages,
    parse_smoothcomp_data,
    extract_match_and_results_data,
)

from app.utils.try_parse_int import try_parse_int


def test_get_max_number_of_pages_returns_int():
    html = """
    <ul class="pagination">
        <li><a>1</a></li>
        <li><a>2</a></li>
        <li><a>5</a></li>
        <li><a>10</a></li>
    </ul>
    """
    soup = BeautifulSoup(html, "html.parser")
    result = get_max_number_of_pages(soup)
    assert result == 10

def test_get_max_number_of_pages_empty_returns_none():
    html = "<div>No pagination</div>"
    soup = BeautifulSoup(html, "html.parser")
    result = get_max_number_of_pages(soup)
    assert result is None

def test_extract_match_and_results_data_returns_list():
    html = """
    <div class="matches-list welled with-bracket">
        <div class="category-row">  Division 1   </div>
        <div class="match-row"><span class="text-success">  Winner A  </span></div>
        <div class="category-row">  Division 2  </div>
        <div class="match-row"><span class="text-success">  Winner B  </span></div>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")
    match_html = soup.find_all('div', class_='matches-list welled with-bracket')
    match_data, result_data = extract_match_and_results_data(match_html)

    assert match_data == ['Division 1', 'Division 2']
    assert result_data == ['Winner A', 'Winner B']

def test_parse_smoothcomp_data_returns_list():
    html = """
    <div class="matches-list welled with-bracket">
        <div class="category-row">  Division 1  </div>
        <div class="match-row"><span class="text-success">  Winner A
        </span></div>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")
    match_data, result_data = parse_smoothcomp_data(soup)

    assert match_data == ['Division 1']
    assert result_data == ['Winner A']
