from newsapi import NewsApiClient
import pandas as pd


def get_articles_from_newsapi_with_source(
        from_param='2020-01-01'
        , to_param='2020-31-12'
        , newsapi_key=''
        , article_source_ids=''
):
    """Downloads articles from newsapi using sources

    :param from_param: Format: yyyy-mm-dd
    :type from_param: str

    :param from_param: Format: yyyy-mm-dd
    :type from_param: str

    :param newsapi_key:
    :type from_param: str

    :param article_source_ids:
    :type from_param: str
    """

    all_articles_all_pages_df = pd.DataFrame()
    suchseite = 1
    anzahl_artikel_gefunden_von_api = 1

    newsapi = NewsApiClient(api_key=newsapi_key)

    while anzahl_artikel_gefunden_von_api > 0:
        all_articles_current_page_respone = newsapi.get_everything(
            from_param=from_param
            , to=to_param
            , page_size=100
            , page=suchseite
            , sources=article_source_ids
        )

        all_articles_current_page = all_articles_current_page_respone['articles']
        anzahl_artikel_gefunden_von_api = len(all_articles_current_page)
        all_articles_current_page_df = pd.DataFrame.from_dict(all_articles_current_page)
        all_articles_all_pages_df = all_articles_all_pages_df.append(all_articles_current_page_df)

        suchseite += 1
        if suchseite == 100:
            break
    return all_articles_all_pages_df


# function to get News for NewsApi
def get_articles_from_newsapi_with_qintitle(qintitle=None
                              , article_language=None
                              , from_param='2020-01-01' # yyyy-mm-dd
                              , to_param='2020-31-12'
                              , newsapi_key=''
                              ):
    all_articles_all_pages_df = pd.DataFrame()
    suchseite = 1
    anzahl_artikel_gefunden_von_api = 1
    
    newsapi = NewsApiClient(api_key=newsapi_key)



    while anzahl_artikel_gefunden_von_api > 0:
        all_articles_current_page_respone = newsapi.get_everything(
            from_param=from_param
            , to=to_param
            , language=article_language
            , page_size=100
            , page=suchseite
            , qintitle=qintitle
        )

        all_articles_current_page = all_articles_current_page_respone['articles']
        anzahl_artikel_gefunden_von_api = len(all_articles_current_page)
        all_articles_current_page_df = pd.DataFrame.from_dict(all_articles_current_page)
        all_articles_all_pages_df = all_articles_all_pages_df.append(all_articles_current_page_df)

        suchseite += 1
        if suchseite == 100:
            break
    return all_articles_all_pages_df


def get_value_counts_as_df(data_frame, column_name_grouping, column_name_count='count'):
    """Return a data frame containing counts of unique values
    :param data_frame: Pandas data frame to process
    :param column_name_grouping: the column for which the unique values are counted
    :param column_name_count: the name of the column that contains the counts for column_grouping
    :return: grouped_values: data frame with column_grouping and column_count as headers

    Example:

    column_name_grouping = 'verified_purchase'
    column_name_count = 'count'
    grouped_values =
        verified_purchase	count
    0	Y	                371539
    1	N	                256810
    """
    grouped_values = data_frame[column_name_grouping].value_counts().rename_axis(column_name_grouping).reset_index(
        name=column_name_count)
    grouped_values.sort_values(by=[column_name_count], inplace=True, ascending=False)
    grouped_values.reset_index(drop=True, inplace=True)

    return grouped_values
