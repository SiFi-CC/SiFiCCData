from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import JsonResponse, Http404
from .models import *
from .serializers import *
from rest_framework import viewsets, permissions
from rest_framework.response import Response
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
        raise Http404("Data does not exist.")
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
    def list(self, request):
        q = self.request.query_params.get('q')
        if q == "list":
            self._paginator = None
            queryset = Series.objects.values_list('id', flat=True)
            return Response(queryset)
        if q == "type":
            self._paginator = None
            run = self.request.query_params.get('measurement')
            key = Measurement.objects.filter(id=run).values_list('series_id', flat=True)
            # allows only the first element, but with filter by id, it will always be one(first) element
            queryset = Series.objects.filter(id=key[0]).values()[0]
            return Response(queryset)
class MeasurementsViewSet(viewsets.ModelViewSet):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, pk, format=None):
        if pk is not None:
            try:
                measurement = Measurement.objects.get(pk=pk)
                #update stop_time, and calculate duration when run ends
                if measurement.stop_time == measurement.start_time:
                    measurement.save()
                    timedelta = measurement.stop_time - measurement.start_time
                    measurement.duration = timedelta.seconds / 60
                    measurement.save()
            except:
                raise Http404("Data does not exist.")
        else:
            #create new run row
            measurement = Measurement()
            measurement.series = request.data['series']
            measurement.datadir = request.data['datadir']
            measurement.source_pos = request.data['source_pos']
            measurement.save()
        return JsonResponse({"success":200})
    def get_queryset(self):
        q = self.request.query_params.get('q')
        if q == "all":
            self._paginator = None
            queryset = Measurement.objects.all()
        if q == "last_inserted_id":
            self._paginator = None
            # get last inserted Measurement
            queryset = Measurement.objects.all().order_by('-id')[:1]
        return queryset
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
    def get_queryset(self):
        queryset = CalibPeakFitting.objects.all()
        if self.request.query_params.get('q'):
            q = self.request.query_params.get('q')
            if q == "all":
                self._paginator = None
            if q.isnumeric():
                queryset = CalibPeakFitting.objects.filter(fiber_id=q)
                self._paginator = None
        return queryset
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
