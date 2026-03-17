import azure.functions as func
from azure.data.tables import TableServiceClient
from azure.core.credentials import AzureNamedKeyCredential
# from azure.identity import DefaultAzureCredential
import logging, os
import source_code.search as search

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
    
@app.route(route="search")
def search_videos(req: func.HttpRequest) -> func.HttpResponse:
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"
    search_string = req.params.get('search')

    account_name = str(os.environ.get("ACCOUNT_NAME"))
    account_key = str(os.environ.get("ACCOUNT_KEY"))
    credential = AzureNamedKeyCredential(account_name, account_key)
    table_name = "linktable"
    # connection_string = "DefaultEndpointsProtocol=https;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;TableEndpoint=https://127.0.0.1:10002/devstoreaccount1;"
    # service_client = TableServiceClient.from_connection_string(conn_str=connection_string)
    service_client = TableServiceClient(endpoint=f"https://127.0.0.1:10002/devstoreaccount1", credential=credential)


    try:
        table_client = service_client.create_table_if_not_exists(table_name=table_name)
        print(f"Connected to table: {table_name}")
    except Exception as e:
        print(f"Failed to connect to table\nError: {e}")


    if not search_string:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            search_string = req_body.get('search')

    if search_string:
        link = search.search(table_client, search_string)
        return func.HttpResponse(body=f"""
            <!DOCTYPE html>
            <html>
            <body>
                <iframe width="560" height="315" src="{link.decode('utf-8')}">
                </iframe>
            </body>
            </html>
            """, headers={"Content-Type": "text/html"})

    else:
        return func.HttpResponse('Please enter a search term')
    