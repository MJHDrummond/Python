import re

from app.utils.try_parse_int import try_parse_int


def get_max_number_of_pages(parsed_html):
    """
    Return the maximum number of match pages to retrieve

    :param parsed_html: Parsed HTML of the webpage
    :return: INT
    """
    pagination_html = parsed_html.find('ul', class_='pagination')
    pagination_items = pagination_html.find_all('li') if pagination_html else []

    pages = []
    for item in pagination_items:
        link = item.find('a')
        if link and link.text:
            pages.append(try_parse_int(link.text.strip()))
    return max(pages) if pages else None

def parse_smoothcomp_data(parsed_html):
    """
    Find and return a list of match data and a list of results data

    :param parsed_html: Parsed HTML of the webpage
    :return: Tuple List
    """
    match_html = parsed_html.find_all(
        'div',
        class_='matches-list welled with-bracket')
    return extract_match_and_results_data(match_html)

def extract_match_and_results_data(match_html):
    match_data = []
    result_data = []

    for all_matches in match_html:
        for div in all_matches:
            try:
                if 'category-row' in (div.get('class') or []):
                    cleaned_text = re.sub(
                        r'\s{2,}',
                        ' ',
                        div.text.strip())
                    match_data.append(cleaned_text)
                elif 'match-row' in (div.get('class') or []):
                    result = div.find(class_='text-success')
                    cleaned_text = re.sub(
                        r'\s{2,}',
                        ' ',
                        result.text.strip())
                    result_data.append(cleaned_text)
            except (TypeError, AttributeError):
                continue
    return match_data, result_data