from rest_framework import serializers


class GoogleAuthSerializer(serializers.Serializer):
    """Serializer used for validating GoogleAuth request"""

    client_id = serializers.CharField()
    redirect_uri = serializers.CharField()
    # Authentication code
    code = serializers.CharField()
