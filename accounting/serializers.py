from rest_framework import serializers
import models 

class TaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tax
        fields = '__all__'

        