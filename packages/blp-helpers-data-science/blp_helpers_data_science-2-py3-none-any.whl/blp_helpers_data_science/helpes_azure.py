from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential


def get_text_analytics_client(azure_key, azure_endpoint):
    ta_credential = AzureKeyCredential(azure_key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=azure_endpoint,
            credential=ta_credential)
    return text_analytics_client


def get_entities(documents, client):
    try:
        result = client.recognize_entities(documents=documents)[0]
        entities = result.entities
        return entities
    except Exception as err:
        print("Encountered exception. {}".format(err))


def get_entities_for_category(entity_category):
    """
    :param entity_category: could be for instance 'Organization'
    :return:
    """
    entities = ''
    try:
        entities = [entity.text for entity in entities if entity.category == entity_category]
    except:
        pass
    return entities


def get_sentiment(client, documents):
    response = client.analyze_sentiment(documents=documents)[0]
    return response
