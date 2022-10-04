from .models import *
from rest_framework import serializers

class FiberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fiber
        fields = '__all__'
class MeasurementSerializer(serializers.ModelSerializer):
    fiber = FiberSerializer(many=True, read_only=True)
    class Meta:
        model = Measurement
        fields = '__all__'
class SeriesSerializer(serializers.ModelSerializer):
    measurement = MeasurementSerializer(many=True, read_only=True)
    class Meta:
        model = Series
        fields = '__all__'
class HypmedNeedleSerializer(serializers.ModelSerializer):
    class Meta:
        model = HypmedNeedle
        fields = '__all__'
class CalibHypmedPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalibHypmedPosition
        fields = '__all__'
class CalibHypmedEnergiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalibHypmedEnergy
        fields = '__all__'
class CalibEnergyReconstructionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalibEnergyReconstruction
        fields = '__all__'
class CalibLightCollectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalibLightCollection
        fields = '__all__'
class CalibPeakFittingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalibPeakFitting
        fields = '__all__'
class CalibPositionReconstructionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalibPositionReconstruction
        fields = '__all__'
class CalibTimingResolutionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalibTimingResolution
        fields = '__all__'
class CalibAttenuationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalibAttenuation
        fields = '__all__'
