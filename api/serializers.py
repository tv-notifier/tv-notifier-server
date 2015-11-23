from rest_framework import serializers


class GoogleAuthSerializer(serializers.Serializer):
    """Serializer used for validating GoogleAuth request"""
    
    clientId = serializers.CharField()
    redirectUri = serializers.CharField()
    # Authentication code
    code = serializers.CharField()
