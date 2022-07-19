"""SiFiCCData URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'api/series', views.SeriesViewSet)
router.register(r'api/measurements', views.MeasurementsViewSet)
router.register(r'api/fibers', views.FibersViewSet)
router.register(r'api/hypmed_needles', views.HypmedNeedlesViewSet)
router.register(r'api/calib_hypmed_positions', views.CalibHypmedPositionsViewSet)
router.register(r'api/calib_hypmed_energies', views.CalibHypmedEnergiesViewSet)
router.register(r'api/calib_energy_reconstructions', views.CalibEnergyReconstructionsViewSet)
router.register(r'api/calib_light_collections', views.CalibLightCollectionsViewSet)
router.register(r'api/calib_peak_fittings', views.CalibPeakFittingsViewSet)
router.register(r'api/calib_position_reconstructions', views.CalibPositionReconstructionsViewSet)
router.register(r'api/calib_timing_resolutions', views.CalibTimingResolutionsViewSet)
router.register(r'api/calib_attenuations', views.CalibAttenuationsViewSet)

urlpatterns = [
    path('', include(router.urls) ),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework') ),
    path('', views.index, name='index'),
    path('geometry/<int:measurement_id>/', views.geometry, name='geometry'),
    path('measurement/<int:measurement_id>/', views.view, name='view'),
]
