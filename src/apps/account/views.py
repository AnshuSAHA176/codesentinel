from adrf.views import APIView as ASYAPIView
from .feach_data import fetch_data,filter_repository_files
from rest_framework.response import Response
from asgiref.sync import sync_to_async



{
"repository-name":"KnowGrid"
}




class EtractData(ASYAPIView):
    async def post(self,request):
        response = await fetch_data(REPOSITORY_NAME=request.data.get('repository-name'))
        filter_data = await sync_to_async(filter_repository_files)(response.get('files'))
        return Response(filter_data)