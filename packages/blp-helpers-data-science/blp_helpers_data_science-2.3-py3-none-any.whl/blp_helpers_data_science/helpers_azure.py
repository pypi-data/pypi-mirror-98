from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential


def get_text_analytics_client(azure_key, azure_endpoint):
    ta_credential = AzureKeyCredential(azure_key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=azure_endpoint,
            credential=ta_credential)
    return text_analytics_client


def get_entities(documents, client):
    """
    :param documents: should look like this: text = ['This sentence talks about iPhones and Sushi.']
    :param client:
    :return:
    """
    try:
        result = client.recognize_entities(documents=documents)[0]
        entities = result.entities
        return entities
    except Exception as err:
        print("Encountered exception. {}".format(err))


def get_entities_for_category(entities_base, entity_category):
    """
    :param entity_category: could be for instance 'Organization'
    :param entities_base: entities as returned from azure, has all entities, from which entity_category will be filtered
    :return: entities_filtered

    Example:

    entity_category = 'Product'
    entities_base = [CategorizedEntity(text=Buches, category=Product, subcategory=None, confidence_score=0.86),
                     CategorizedEntity(text=Mädelsabend, category=Event, subcategory=None, confidence_score=0.81)]
    entities_filtered = '['Buches']'
    """
    entities_filtered = ''
    try:
        entities_filtered = [entity.text for entity in entities_base if entity.category == entity_category]
    except:
        pass
    return entities_filtered


def get_sentiment(client, documents):
    response = client.analyze_sentiment(documents=documents)[0]
    return response
