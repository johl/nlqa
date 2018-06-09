import spacy
import requests
import json


def extract_entities(question, language="en"):
    """
    Extract item and property out of question.

    Process question. We assume the token with part of speech marker 'NOUN'
    to be the property and token with pos marker 'PROPN' to be the item of
    the query.

    Parameters:
    question (str): natural language question about a property of an item
    language (str): (optional) language code for propcessing (default "en").

    Returns:
    entities: dictionary with ['property']['lemma'] and ['item']['lemma'] set
              to extracted item and property.
    """

    nlp = spacy.load(language)
    doc = nlp(question)
    entities = {}
    entities['property'] = {}
    entities['item'] = {}
    for token in doc:
        if (token.pos_ == 'NOUN'):
            entities['property']['lemma'] = token.lemma_
        if (token.pos_ == 'PROPN'):
            entities['item']['lemma'] = token.lemma_
    return entities


def search_entities(entities, language="en"):
    """
    Search for item ID and property ID on Wikidata.

    Take entities dictionary, search on Wikidata for the lemmas of the item
    and the property through an API call to wbsearchentities.

    Parameters:
    entities (dict): dictionary with ['property']['lemma']
                     and ['item']['lemma'] set
    language (str): (optional) language code for search (default "en").

    Returns:
    entities: dictionary with ['property']['id'] and ['item']['id'] set
    """

    endpoint = "https://www.wikidata.org/w/api.php"
    params = "?language=" + language + "&format=json"
    action = "&action=wbsearchentities&search="
    itemsearch = requests.get(endpoint + params + action +
                              entities['item']['lemma'])
    item = json.loads(itemsearch.text)['search'][0]['id']
    propertysearch = requests.get(endpoint + params + action +
                                  entities['property']['lemma'] +
                                  '&type=property')
    property = json.loads(propertysearch.text)['search'][0]['id']
    entities['item']['id'] = item
    entities['property']['id'] = property
    return entities


def query_sparql(entities, language="en"):
    """
    Perform SPARQL query for item and property.

    Build SPARQL query with item ID and property ID from enitities dictionary
    and run it on SPARQL endpoint at Wikidata.

    Parameters:
    entities (dict): dictionary with ['property']['id']
                     and ['item']['id'] set
    language (str): (optional) language code for query (default "en").

    Returns:
    answer: String with label of the result of the query
    """
    item = entities['item']['id']
    property = entities['property']['id']
    endpoint = "https://query.wikidata.org/bigdata/namespace/wdq/sparql"
    sparql = "SELECT ?answerLabel WHERE {\n"
    sparql = sparql + "wd:{} wdt:{} ?answer.".format(item, property)
    sparql = sparql + "\nSERVICE wikibase:label "
    sparql = sparql + '{bd:serviceParam wikibase:language "'
    sparql = sparql + language + '".}\n}'
    query = requests.get(endpoint + "?query=" + sparql + "&format=json")
    answer = json.loads(query.text)
    answer = answer['results']['bindings'][0]['answerLabel']['value']
    return answer


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--question', help='question to Wikidata')
    parser.add_argument('--language', help='language code of the question')
    args = parser.parse_args()
    if (args.question is None or args.language is None):
        parser.print_help()
    else:
        print(query_sparql(
            search_entities(
                extract_entities(args.question, language=args.language),
                language=args.language),
            language=args.language))
