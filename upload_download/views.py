from django.shortcuts import render
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from django.http import HttpResponseRedirect,HttpResponse
import os,uuid

blob_lists = []
conn_string = os.environ["AZURE_STORAGE_CONNECTION_STRING"]
blob_service_client = BlobServiceClient.from_connection_string(conn_string)
container_name="blob-container-01"
# Create your views here.
local_path = "C:\\Users\\Rekha Balamurugan\\Lexicon\\Azure-Python\\azure_python_upload_download\\downloads"
def index(request):
    
    if request.method =='POST':
        uploaded_file = request.FILES['document']
        blob_client = BlobClient.from_connection_string(
        conn_string,
        container_name="blob-container-01",
        blob_name=f"sample-blob-{str(uuid.uuid4())[0:5]}.jpg",
        )   
        blob_client.upload_blob(uploaded_file)
        print(f"Uploaded apple.jpg to {blob_client.url}")
    
    
    container_client = blob_service_client.get_container_client(container_name)
    print(container_client)
    blob_lists = container_client.list_blobs()
    print(blob_lists)
            
    return render(request,'index.html',{'blob_list':blob_lists})

def download(request, i):
    print(i)
    file_name = i
    download_file_path = os.path.join(local_path, file_name)
    container_client = blob_service_client.get_container_client(container= container_name) 
    with open(file=download_file_path, mode="wb") as download_file:
        download_file.write(container_client.download_blob(i).readall())
    return HttpResponse('Downloded successfully')