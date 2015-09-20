from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import HelloWorld


@api_view(('GET',))
def home(request):
    """
    Home API endpoint
    """
    if HelloWorld.objects.count() == 0:
        HelloWorld(count=0).save()
    x = HelloWorld.objects.first()
    x.count += 1
    x.save()
    return Response({
        'hello': 'world!',
        'count': HelloWorld.objects.first().count
    })
