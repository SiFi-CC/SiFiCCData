from django.db import models
from django.contrib import admin
from .models import *
from .forms import ImageWidget

import matplotlib.pyplot as plt
import io, urllib, base64
from django.utils.html import format_html
# Register your models here.

@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
  list_display = [field.name for field in Series._meta.get_fields()]
  list_display.remove('measurement')
  def get_measurements(self, obj):
      return list(obj.measurement_set.all() )
  list_display.append('get_measurements')
@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
  formfield_overrides = {
      models.ImageField: {'widget': ImageWidget},
  }
  list_display = [field.name for field in Measurement._meta.get_fields()]
  list_display.remove('fiber')
  list_display.remove('calibhypmedposition')
  list_display.remove('calibhypmedenergy')
  def get_fibers(self, obj):
      x = []
      y = []
      coords = list(obj.fiber_set.values('lay', 'fib') )
      for coord in coords:
          x.append(coord['fib'])
          y.append(coord['lay'])
      fig, ax = plt.subplots(1, 1, figsize=(8, 1) )
      if len(x) == 0:
          return ""
      ax.scatter(x, y)
      plt.axis('off')
      fig.tight_layout()
      fig = plt.gcf()
      buf = io.BytesIO()
      fig.savefig(buf, format='png')
      plt.close(fig)
      buf.seek(0)
      string = base64.b64encode(buf.read() )
      uri = urllib.parse.quote(string)
      return format_html('<img class="photo" style="height: 20px;" src="data:;base64,{}">', uri)
  list_display.append('get_fibers')
  def get_result(self, obj):
      html = ""
      if obj.result is not None:
          html = format_html('<img class="photo" style="height: 100px;" src="/media/{}"/>', obj.result)
      return html
  list_display.remove('result')
  list_display.append('get_result')
@admin.register(Fiber)
class FibersAdmin(admin.ModelAdmin):
  list_display = [field.name for field in Fiber._meta.get_fields()]
  list_display.remove('calibenergyreconstruction')
  list_display.remove('caliblightcollection')
  list_display.remove('calibpeakfitting')
  list_display.remove('calibpositionreconstruction')
  list_display.remove('calibtimingresolution')
  list_display.remove('calibattenuation')
@admin.register(HypmedNeedle)
class HypmedNeedleAdmin(admin.ModelAdmin):
  list_display = [field.name for field in HypmedNeedle._meta.get_fields()]
  list_display.remove('calibhypmedposition')
  list_display.remove('calibhypmedenergy')
  def get_calibhypmedposition(self, obj):
      return list(obj.calibhypmedposition_set.all() )
  list_display.append('get_calibhypmedposition')
  def get_calibhypmedenergy(self, obj):
      return list(obj.calibhypmedenergy_set.all() )
  list_display.append('get_calibhypmedenergy')
@admin.register(CalibHypmedPosition)
class CalibHypmedPositionAdmin(admin.ModelAdmin):
  list_display = [field.name for field in CalibHypmedPosition._meta.get_fields()]
@admin.register(CalibHypmedEnergy)
class CalibHypmedEnergyAdmin(admin.ModelAdmin):
  list_display = [field.name for field in CalibHypmedEnergy._meta.get_fields()]
@admin.register(CalibPeakFitting)
class CalibPeakFittingAdmin(admin.ModelAdmin):
  list_display = [field.name for field in CalibPeakFitting._meta.get_fields()]
@admin.register(CalibEnergyReconstruction)
class CalibEnergyReconstructionAdmin(admin.ModelAdmin):
  list_display = [field.name for field in CalibEnergyReconstruction._meta.get_fields()]
@admin.register(CalibLightCollection)
class CalibLightCollectionAdmin(admin.ModelAdmin):
  list_display = [field.name for field in CalibLightCollection._meta.get_fields()]
@admin.register(CalibAttenuation)
class CalibAttenuationAdmin(admin.ModelAdmin):
  list_display = [field.name for field in CalibAttenuation._meta.get_fields()]
@admin.register(CalibPositionReconstruction)
class CalibPositionReconstructionAdmin(admin.ModelAdmin):
  list_display = [field.name for field in CalibPositionReconstruction._meta.get_fields()]
@admin.register(CalibTimingResolution)
class CalibTimingResolutionAdmin(admin.ModelAdmin):
  list_display = [field.name for field in CalibTimingResolution._meta.get_fields()]
