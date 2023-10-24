# Import required libraries  
import os  
import json  
import openai  
from tenacity import retry, wait_random_exponential, stop_after_attempt  
from azure.core.credentials import AzureKeyCredential  
from azure.search.documents import SearchClient  
from azure.search.documents.indexes import SearchIndexClient  
from azure.search.documents.models import Vector  
from azure.search.documents.indexes.models import (  
    SearchIndex,  
    SearchField,  
    SearchFieldDataType,  
    SimpleField,  
    SearchableField,  
    SearchIndex,  
    SemanticConfiguration,  
    PrioritizedFields,  
    SemanticField,  
    SemanticSettings,  
    VectorSearch, 
    HnswVectorSearchAlgorithmConfiguration,  
)  

from langchain.document_loaders import AzureBlobStorageContainerLoader
from langchain.vectorstores.azuresearch import AzureSearch
from langchain.document_loaders import AzureBlobStorageContainerLoader
from langchain.text_splitter import CharacterTextSplitter
from azure.storage.blob import BlobServiceClient
import tempfile
from langchain.document_loaders import PyPDFLoader
from azure.core.exceptions import HttpResponseError 
from langchain.embeddings.openai import OpenAIEmbeddings
# Configure environment variables  
load_dotenv()  
service_endpoint = os.getenv("AZURE_SEARCH_SERVICE_ENDPOINT") 
index_name = os.getenv("AZURE_SEARCH_INDEX_NAME") 
key = os.getenv("AZURE_SEARCH_ADMIN_KEY") 
openai.api_type = "azure"  
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")  
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")  
openai.api_version = os.getenv("AZURE_OPENAI_API_VERSION")  
credential = AzureKeyCredential("jA50VnyT0OAeuHpY0RxJGz7z9kfrmdj7YF5PHYiPXjAzSeBS6hJg")
os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_BASE"] = "https://testingchat.openai.azure.com/"
os.environ["OPENAI_API_KEY"] = "e8143eabb02541259054426630db12a7"
os.environ["OPENAI_API_VERSION"] = "2023-05-15"
model: str = "text-embedding-ada-002"
#pdf_file_name = "Alaska Airlines and Horizon Air SMS Manual.pdf"     

AZURE_SEARCH_SERVICE_ENDPOINT = "https://genaisafety.search.windows.net"
AZURE_SEARCH_ADMIN_KEY = "jA50VnyT0OAeuHpY0RxJGz7z9kfrmdj7YF5PHYiPXjAzSeBS6hJg"
def pdf_text_extraction(pdf_file_path):
    if pdf_file_path is not None:
        with open(pdf_file_path, 'rb') as pdf_file:
            # Create a temporary file to write the PDF contents
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                tmp_file.write(pdf_file.read())
                pdf_path = tmp_file.name

        # Now you can use the PyPDFLoader on the temporary PDF file
        loader = PyPDFLoader(pdf_path)
        pages_split = loader.load_and_split()
    return pages_split
def create_index(AZURE_SEARCH_INDEX_NAME, fields):
    vector_search = VectorSearch(
        algorithm_configurations=[
            HnswVectorSearchAlgorithmConfiguration(
                name="my-vector-config",
                kind="hnsw",
                parameters={
                    "m": 4,
                    "efConstruction": 400,
                    "efSearch": 500,
                    "metric": "cosine"
                }
            )
        ]
    )


    semantic_config = SemanticConfiguration(
        name="my-semantic-config",
        prioritized_fields=PrioritizedFields(
            title_field=SemanticField(field_name="id"),
            prioritized_keywords_fields=[SemanticField(field_name="content")]
        )
    )

    # Create the semantic settings with the configuration
    semantic_settings = SemanticSettings(configurations=[semantic_config])

    # Create the search index with the semantic settings
    index = SearchIndex(name=AZURE_SEARCH_INDEX_NAME, fields=fields,
                        vector_search=vector_search, semantic_settings=semantic_settings)

    result = search_client.create_or_update_index(index)
    return result
embeddings = OpenAIEmbeddings(deployment = model,chunk_size=1) 

# Replace with your actual connection string
connection_string = "DefaultEndpointsProtocol=https;AccountName=storageaccountgenai;AccountKey=WAfyL4uqWgarFdx1ibNgWv9lmOINODLuN6nnLSQLgE/iuHhKGi1pYd6NQJ6LBnZO/DnnQfhbNSWi+AStsOLf1Q==;EndpointSuffix=core.windows.net"

# Replace with your container name
container_name = "safety"

# Create a BlobServiceClient using the connection string
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Get a reference to the container
container_client = blob_service_client.get_container_client(container_name)
# List blobs in the container
blobs = container_client.list_blobs()
dict_data = []
for blob in blobs:
    if blob.name.startswith("manuals") and blob.name.endswith(".pdf"): #and ("manuals/Alaska Airlines and Horizon Air SMS Manual.pdf" in blob.name):  # Check if the blob is a PDF file
        #blob_client = container_client.get_blob_client(blob)
        pdf_file_name=str(blob.name).split("/")[1] 
        bid=str(blob.name).split("/")[1].split(".")[0].lower().replace(" ","_").replace("_","-")
        print(blob.name)
        
                      
        documents = pdf_text_extraction(pdf_file_name)

        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        docs = text_splitter.split_documents(documents)
        print("PDF_NAME, length", blob.name, len(docs))
        
        
            
        for index,doc in enumerate(docs):
            dict_data.append({
                'id': bid+'_'+ str(index),
                'content': doc.page_content,  # You can set a title based on your needs
                'page_number': doc.metadata['page'],
                'metadata': doc.metadata,
            })

        print(f"splitted into {len(docs)} documents") 
    
        

        for item in dict_data:
            title = item['id']
            content = item['content']
            title_embeddings = embeddings.embed_query(title)
            content_embeddings = embeddings.embed_query(content)
            item['titleVector'] = title_embeddings
            item['content_vector'] = content_embeddings
            
        bid=str(blob.name).split("/")[1].split(".")[0].lower().replace(" ","_").replace("_","-")
        AZURE_SEARCH_INDEX_NAME=bid + "-index"
        print(AZURE_SEARCH_INDEX_NAME)

        
        search_client = SearchIndexClient(endpoint=AZURE_SEARCH_SERVICE_ENDPOINT, credential=credential)
        search_client_v2 = SearchClient(endpoint=AZURE_SEARCH_SERVICE_ENDPOINT, index_name=AZURE_SEARCH_INDEX_NAME, credential=credential)

        
        # Define your Azure Cognitive Search credentials and index settings as previously done
        # Check if the index already exists
        # existing_index = None
        # Define your Azure Cognitive Search credentials and index settings as previously done

        combined_content = ''.join([p.page_content for p in docs])
        combined_vector = embeddings.embed_query(combined_content)
        try:
            existing_index = search_client.get_index(AZURE_SEARCH_INDEX_NAME)
        except Exception as e:
            existing_index == None
            # The index doesn't exist, so create a new one
        if existing_index == None:
            fields = [
            SimpleField(name="id", type=SearchFieldDataType.String, key=True, sortable=True, filterable=True, facetable=True),
            SearchableField(name="title", type=SearchFieldDataType.String),
            SearchableField(name="content", type=SearchFieldDataType.String),
            SearchableField(name="combined_content", type=SearchFieldDataType.String),
            SearchableField(name="page_number", type=SearchFieldDataType.String),
            SearchableField(name="metadata", type=SearchFieldDataType.String, searchable=True),
            SearchField(name="combined_vector", type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                        searchable=True, vector_search_dimensions=1536, vector_search_configuration="my-vector-config"),
            SearchField(name="content_vector", type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                        searchable=True, vector_search_dimensions=1536, vector_search_configuration="my-vector-config"),
            ]

            result = create_index(AZURE_SEARCH_INDEX_NAME, fields)
            print(f' {result.name} created index')                        
            
            final_doc=[]
            for index,doc in enumerate(docs):
                final_doc.append({'id':dict_data[index]['id'], 'title':dict_data[index]['id'],
                                  'content':dict_data[index]['content'],
                                  'combined_content':combined_content,
                                  'page_number':str(dict_data[index]['page_number']), 
                                  'metadata': json.dumps(dict_data[index]['metadata']),
                                  'combined_vector': combined_vector, 'content_vector':dict_data[index]['content_vector']})
                
            # Define a list to store batches of documents
            document_batches = [final_doc[i] for i in range(0, len(final_doc))]

            # Upload documents in batches
            for batch in document_batches:
                try:
                    result = search_client_v2.upload_documents(batch)
                except HttpResponseError as e:
                    print(f"Error uploading documents: {e}")    

            print("Vector store added successfully")

        else:
            try:
                # Check if the index exists
                # existing_index = search_client.get_index(AZURE_SEARCH_INDEX_NAME)
                # print(f"Index '{AZURE_SEARCH_INDEX_NAME}' already exists. You can use the existing index.")

                final_doc=[]
                metadata_str = json.dumps(dict_data[index]['metadata'])

                for index,doc in enumerate(docs):
                    final_doc.append({'id':dict_data[index]['id'], 'title':dict_data[index]['id'],
                                      'content':dict_data[index]['content'],
                                      'combined_content':combined_content,
                                      'page_number':str(dict_data[index]['page_number']), 
                                      'metadata': metadata_str,
                                      'combined_vector':combined_vector, 'content_vector':dict_data[index]['content_vector']})

                # Define a list to store batches of documents
                document_batches = [final_doc[i] for i in range(0, len(final_doc))]

                # Upload documents in batches
                for batch in document_batches:
                    try:
                        result = search_client_v2.upload_documents(batch)
                    except HttpResponseError as e:
                        print(f"Error uploading documents: {e}")    

                print("Vector store added successfully")
            

            except Exception as e:
                print(e)
                pass
    else:
        continue
