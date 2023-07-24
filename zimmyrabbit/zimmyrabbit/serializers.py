from rest_framework import serializers
from .models import BuildHist

class BuildHistSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildHist
        fields = '__all__'