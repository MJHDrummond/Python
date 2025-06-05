from app.config.settings import settings
from app.requests.call_smoothcomp import get_webpage_data
from app.data_processing.process_smoothcomp import (
    parse_smoothcomp_data,
    get_max_number_of_pages,
)
from app.data_processing.analyse_data import analyse_data
from app.data_processing.create_dataframe import add_data_to_dataframe


def main():
    """
    main method for all the processing
    """
    print('Starting app')
    main_match_data = []
    main_result_data = []
    event_id = settings.event_id_veluwe_open[0]

    parsed_html = get_webpage_data(event_id, 1)
    match_data, result_data = parse_smoothcomp_data(parsed_html)

    main_match_data.append(match_data)
    main_result_data.append(result_data)

    max_page_number = get_max_number_of_pages(parsed_html)

    for page_number in range(max_page_number+1):
        if page_number < 3: #Remove to get entire results
            parsed_html = get_webpage_data(event_id, page_number)
            match_data, result_data = parse_smoothcomp_data(parsed_html)

            main_match_data.append(match_data)
            main_result_data.append(result_data)

    df = add_data_to_dataframe(
        'veluwe open',
        match_data,
        result_data)

    analyse_data(df)
    print('Finished app')

if __name__ == '__main__':
    main()
