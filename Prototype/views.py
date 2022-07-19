from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import *
from .serializers import *
from rest_framework import viewsets, permissions
# Create your views here.
def geometry(request, measurement_id):
    try:
        measurement = Measurement.objects.get(pk=measurement_id)
        series = Series.objects.get(pk=measurement.series_id)
    except:
        raise Http404("Measurement does not exist.")
    fixed = {}
    text = series.configuration[1:-1]
    x0 = text.split(",")
    for x1 in x0:
        x = x1.split(":")
        values = x[1].split(";")
        values = [float(v) for v in values]
        fixed[x[0].strip() ] = values
    if(measurement.source_pos != "-"):
        src_xy = measurement.source_pos.split(";")
        fixed["source"] = []
        for j in range(0, int(len(src_xy)/2) ):
            fixed["source"].append([(int(src_xy[j*2])-7)*10, (int(src_xy[j*2+1])-7)*10, 0])
    return JsonResponse(fixed)
def index(request):
    try:
        measurements = Measurement.objects.all()
        paginator = Paginator(measurements, 25)
    except:
        raise Http404("Measurement does not exist.")
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'measurements/index.html', {'page_obj': page_obj})
def view(request, measurement_id):
    try:
        measurement = Measurement.objects.get(pk=measurement_id)
        series = Series.objects.get(pk=measurement.series_id)
    except:
        raise Http404("Data does not exist.")
    return render(request, 'measurements/view.html', {'measurement': measurement, 'series': series})
class SeriesViewSet(viewsets.ModelViewSet):
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer
    permission_classes = [permissions.IsAuthenticated]
class MeasurementsViewSet(viewsets.ModelViewSet):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
    permission_classes = [permissions.IsAuthenticated]
class FibersViewSet(viewsets.ModelViewSet):
    queryset = Fiber.objects.all()
    serializer_class = FiberSerializer
    permission_classes = [permissions.IsAuthenticated]
class HypmedNeedlesViewSet(viewsets.ModelViewSet):
    queryset = HypmedNeedle.objects.all()
    serializer_class = HypmedNeedleSerializer
    permission_classes = [permissions.IsAuthenticated]
class CalibHypmedPositionsViewSet(viewsets.ModelViewSet):
    queryset = CalibHypmedPosition.objects.all()
    serializer_class = CalibHypmedPositionSerializer
    permission_classes = [permissions.IsAuthenticated]
class CalibHypmedEnergiesViewSet(viewsets.ModelViewSet):
    queryset = CalibHypmedEnergy.objects.all()
    serializer_class = CalibHypmedEnergiesSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        q = self.request.query_params.get('q')
        if q == "all":
            self._paginator = None
        queryset = CalibHypmedEnergy.objects.all()
        return queryset
class CalibEnergyReconstructionsViewSet(viewsets.ModelViewSet):
    queryset = CalibEnergyReconstruction.objects.all()
    serializer_class = CalibEnergyReconstructionsSerializer
    permission_classes = [permissions.IsAuthenticated]
class CalibLightCollectionsViewSet(viewsets.ModelViewSet):
    queryset = CalibLightCollection.objects.all()
    serializer_class = CalibLightCollectionsSerializer
    permissions_classes = [permissions.IsAuthenticated]
class CalibPeakFittingsViewSet(viewsets.ModelViewSet):
    queryset = CalibPeakFitting.objects.all()
    serializer_class = CalibPeakFittingsSerializer
    permissions_classes = [permissions.IsAuthenticated]
class CalibPositionReconstructionsViewSet(viewsets.ModelViewSet):
    queryset = CalibPositionReconstruction.objects.all()
    serializer_class = CalibPositionReconstructionsSerializer
    permissions_classes = [permissions.IsAuthenticated]
class CalibTimingResolutionsViewSet(viewsets.ModelViewSet):
    queryset = CalibTimingResolution.objects.all()
    serializer_class = CalibTimingResolutionsSerializer
    permissions_classes = [permissions.IsAuthenticated]
class CalibAttenuationsViewSet(viewsets.ModelViewSet):
    queryset = CalibAttenuation.objects.all()
    serializer_class = CalibAttenuationsSerializer
    permissions_classes = [permissions.IsAuthenticated]
