import source_code.helper_code.googleapi_call as gc

def search(table_client, search_string):
    search_results, cache_length = search_table(table_client, search_string)
    cache = False
    if search_results == []:
        print("Not found in cache!")
        search_results=gc.google_api_call(search_string)
    else:
        results_lst = []
        cache = True
        for tup in search_results:
           results_lst.append(tup)
        search_results = results_lst
    link = menu(search_results, table_client, cache, search_string, cache_length)
    return link

def google_or_cache(results, cache, query):
    
    if cache == True:
        print(f"Found {len(results)} results from Cache...")
        # data_select = input("Would you like to pull results from the Google API instead? (Y/n):")
        data_select = 'y'
        if data_select == 'y':
            print("Hit!")
            results = gc.google_api_call(query)
            
    print_results(results)
    return results

def menu(results, table_client, cache, query, cache_length):
    results=google_or_cache(results, cache, query)

    selection = 1
    title = list(results[selection - 1].keys())[0]
    link = results[selection - 1][next(iter(results[selection - 1]))]
    entity = {
        'PartitionKey': 'video',
        'Title': title,
        'Link': link,
        'RowKey': f'Row{cache_length}'
    }
    if cache == False:
        table_client.create_entity(entity=entity)
        entities = table_client.query_entities(query_filter="PartitonKey eq 'video'")
        for e in entities:
            print('1', e)

    if selection == 0:
        return None
    else:  
        return link

def print_results(all_results):
    num = 0
    for result in all_results:
        num +=1
        print(f"{num}: {next(iter(result))} Link:{result[next(iter(result))]}")

def search_table(table_client, search_string):
    table_results = table_client.query_entities(query_filter="PartitionKey eq 'video'")
    result_lst = convert(table_results)
    search_lst = []
    for result in result_lst:
        if search_string in str(next(iter(result))).lower():
            print(next(iter(result)))
            search_lst.append(result)
    return search_lst, len(result_lst)


def convert(results):
    lst = []
    for result in results:
        print(result['Title'], result['Link'], result['RowKey'])
        lst.append({result['Title']: (result['Link'], result['RowKey'])})
    print("Conversion", lst)
    return lst