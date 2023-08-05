from ibm_watson import DiscoveryV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import json


def inst(API_KEY=None, URL=None, VERSION=None):

    authenticator = IAMAuthenticator(API_KEY)
    discovery = DiscoveryV2(version=VERSION,
                            authenticator=authenticator)
    discovery.set_service_url(URL)

    return discovery


def get_search_results(discovery,
                       project_id=None,
                       collection_ids=[],
                       filter=None,
                       natural_language_query=None,
                       query=None,
                       aggregation=None,
                       highlight=False,
                       spelling_suggestions=False,
                       fetch_count='1',
                       return_val=None):

    if (return_val is not None):
        query_result = discovery.query(
            project_id=project_id,
            collection_ids=collection_ids,
            highlight=highlight if (highlight) else False,
            spelling_suggestions=spelling_suggestions,
            aggregation=aggregation if (query is not None) else None,
            query=query if (query is not None) else None,
            natural_language_query=natural_language_query if (
                natural_language_query is not None) else None,
            filter=filter if (filter is not None) else None,
            return_=return_val,
            count=fetch_count)\
            .get_result()
    else:
        query_result = discovery.query(
            project_id=project_id,
            collection_ids=collection_ids,
            highlight=highlight if (highlight) else False,
            spelling_suggestions=spelling_suggestions,
            aggregation=aggregation if (query is not None) else None,
            query=query if (query is not None) else None,
            natural_language_query=natural_language_query if (
                natural_language_query is not None) else None,
            filter=filter if (filter is not None) else None,
            count=fetch_count)\
            .get_result()

    # return_fields=return_fields_arr,
    query_result['matching_results']
    results = query_result["results"]

    return results


if __name__ == "__main__":

    # delete_document(wds, "b3e4ff43-07a6-46b8-b886-23108cff6904",
    #                 "d16a19ec-46b5-42ed-a21b-d7e6a60f0f81", "1d0d0285-1c00-454a-a4b8-20323f7c56ca")

    # get_results_by_doc_name("8ac98bff-0ca3-4b3c-a752-9c48eb8965c1_45156461_2018 Specifications (AmWINS).docx", [
    #                         "submission_key", "submission_value", "submission_data_elem"])
    wds_api_key = 'ydPdisYfwHxJbIb9jzfci5jFt8IFgD18qjO9qZFjkklD'
    wds_url = 'https://api.us-south.discovery.watson.cloud.ibm.com/instances/ad1ec158-4ff7-4008-8c8a-31d68301756b'
    wds_api_version = '2019-11-29'
    collections = ['f7ff121b-07c0-c9ee-0000-0177f3fd485e']
    project_id = '2c8ab515-6ce3-4345-82c4-a255b857f739'

    natural_language_query = "Libor"
    filter = None
    return_val = ["enriched_text", "extracted_metadata.filename", "extracted_metadata.file_type",
                  "extracted_metadata.author", "document_passages", "enriched_text", "enriched_html"]

    discovery = inst(API_KEY=wds_api_key, URL=wds_url, VERSION=wds_api_version)
    results = get_search_results(discovery,
                                 project_id=project_id,
                                 collection_ids=collections,
                                 filter=None,
                                 natural_language_query=natural_language_query,
                                 query=None,
                                 aggregation="term(enriched_html.contract.elements.categories.label,count:25)",
                                 highlight=False,
                                 spelling_suggestions=False,
                                 fetch_count='1',
                                 return_val=return_val)

    f = open("results.json", "w")
    f.write(json.dumps(results))
    f.close()
    # print(json.dumps(results))
