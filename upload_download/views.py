from django.shortcuts import render
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from django.http import HttpResponseRedirect,HttpResponse,FileResponse
import os,uuid

blob_lists = []
conn_string = os.environ["AZURE_STORAGE_CONNECTION_STRING"]
blob_service_client = BlobServiceClient.from_connection_string(conn_string)
container_name="blob-container-01"

def index(request):
    
    if request.method =='POST':
        uploaded_file = request.FILES['document']
        blob_client = BlobClient.from_connection_string(
        conn_string,
        container_name="blob-container-01",
        blob_name=uploaded_file.name,
        )   
        blob_client.upload_blob(uploaded_file)
        print(f"Uploaded apple.jpg to {blob_client.url}")

    container_client = blob_service_client.get_container_client(container_name)
    blob_lists = container_client.list_blobs()   

    return render(request,'index.html',{'blob_list':blob_lists})

def download(request, i):
    file_name = i
    container_client = blob_service_client.get_container_client(container= container_name) 
    with open(file=file_name, mode="wb") as download_file:
        download_file.write(container_client.download_blob(file_name).readall())
    response= FileResponse(open(file_name,'rb'))
    response['Content-Disposition'] = f'attachment; filename={file_name}'
    return response