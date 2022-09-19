from django.db import models
from django.utils.translation import gettext as _
from datetime import datetime

# Create your models here.
class Series(models.Model):
    detector = models.CharField(max_length=255, default="prototype stack")
    fiber_mat = models.CharField(max_length=255, default="LYSO:Ce")
    fiber_dim = models.CharField(max_length=255, default="1;1;100")
    fiber_prod = models.CharField(max_length=255, default="Shalome")
    fiber_wrap = models.CharField(max_length=255, default="Al")
    fiber_geometry = models.CharField(max_length=255, default="aligned half shift")
    n_modules = models.IntegerField(default=0)
    n_layers_per_module = models.IntegerField(default=0)
    n_fibers_per_layer = models.IntegerField(default=0)
    radiosource = models.CharField(max_length=255, default="Na22")
    photodetector = models.CharField(max_length=255, default="Ketek")
    voltage = models.FloatField(default=0.0)
    coupling_type = models.CharField(max_length=255, default="Eljen")
    coupling_size = models.CharField(max_length=255, default="1;1;1")
    daq = models.CharField(max_length=255, default="Desktop Digitizer")
    configuration = models.CharField(max_length=255, default="{'source':0, 'prototype':10.0}")
    log_file = models.TextField(blank=True, null=True)
    monitoring_file = models.TextField(blank=True, null=True)
    pos_unc = models.FloatField(default=1.5)
    mask = models.CharField(max_length=255, blank=True, null=True)
    elog_id = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return "%s" % (self.id)
    class Meta:
        verbose_name = _("Series")
        verbose_name_plural = _("Series")
        ordering = ('-id',)

class Measurement(models.Model):
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    datadir = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField(auto_now_add=True)
    stop_time = models.DateTimeField(auto_now=True)
    duration = models.IntegerField(blank=True, null=True)
    source_pos = models.TextField(blank=True, null=True)
    def __str__(self):
        return "%s" % (self.id)

class Fiber(models.Model):
    measurement = models.ForeignKey(Measurement, on_delete=models.CASCADE)
    mod = models.IntegerField()
    lay = models.IntegerField()
    fib = models.IntegerField()
    def __str__(self):
        return "M%sL%sF%s" % (self.mod, self.lay, self.fib)

class HypmedNeedle(models.Model):
    stack = models.IntegerField()
    needle = models.IntegerField()
    rel_x = models.FloatField()
    rel_y = models.FloatField()
    layer = models.IntegerField()
    def __str__(self):
        return "%s" % (self.needle)

class CalibHypmedPosition(models.Model):
    measurement = models.ForeignKey(Measurement, on_delete=models.CASCADE)
    hypmed_needle = models.ForeignKey(HypmedNeedle, on_delete=models.CASCADE)
    roi0 = models.IntegerField(blank=True, null=True)
    roi1 = models.IntegerField(blank=True, null=True)
    roi2 = models.IntegerField(blank=True, null=True)
    roi7 = models.IntegerField(blank=True, null=True)
    cogPosX0 = models.FloatField(blank=True, null=True)
    cogPosY0 = models.FloatField(blank=True, null=True)
    cogPosX1 = models.FloatField(blank=True, null=True)
    cogPosY1 = models.FloatField(blank=True, null=True)
    cogPosX2 = models.FloatField(blank=True, null=True)
    cogPosY2 = models.FloatField(blank=True, null=True)
    cogPosX7 = models.FloatField(blank=True, null=True)
    cogPosY7 = models.FloatField(blank=True, null=True)
    def __str__(self):
        return "%s %s %s %s" % (self.roi0, self.roi1, self.roi2, self.roi7)

class CalibHypmedEnergy(models.Model):
    measurement = models.ForeignKey(Measurement, on_delete=models.CASCADE)
    hypmed_needle = models.ForeignKey(HypmedNeedle, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    roi0 = models.IntegerField(blank=True, null=True)
    roi1 = models.IntegerField(blank=True, null=True)
    roi2 = models.IntegerField(blank=True, null=True)
    roi7 = models.IntegerField(blank=True, null=True)
    slope0 = models.FloatField(blank=True, null=True)
    slope_err0 = models.FloatField(blank=True, null=True)
    chi2ndf0 = models.FloatField(blank=True, null=True)
    slope1 = models.FloatField(blank=True, null=True)
    slope_err1 = models.FloatField(blank=True, null=True)
    chi2ndf1 = models.FloatField(blank=True, null=True)
    slope2 = models.FloatField(blank=True, null=True)
    slope_err2 = models.FloatField(blank=True, null=True)
    chi2ndf2 = models.FloatField(blank=True, null=True)
    slope7 = models.FloatField(blank=True, null=True)
    slope_err7 = models.FloatField(blank=True, null=True)
    chi2ndf7 = models.FloatField(blank=True, null=True)
    class Meta:
        verbose_name = _("Calib hypmed energy")
        verbose_name_plural = _("Calib hypmed energies")

class CalibEnergyReconstruction(models.Model):
    fiber = models.ForeignKey(Fiber, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    results_file = models.TextField(blank=True, null=True)
    ereco_qavg = models.FloatField()
    ereco_qavg_err = models.FloatField()
    eres_qavg = models.FloatField()
    eres_qavg_err = models.FloatField()
    ereco_all_qavg = models.FloatField()
    ereco_all_qavg_err = models.FloatField()
    eres_all_qavg = models.FloatField()
    eres_all_qavg_err = models.FloatField()
    ereco_elar = models.FloatField()
    ereco_elar_err = models.FloatField()
    eres_elar = models.FloatField()
    eres_elar_err = models.FloatField()
    ereco_all_elar = models.FloatField()
    ereco_all_elar_err = models.FloatField()
    eres_all_elar = models.FloatField()
    eres_all_elar_err = models.FloatField()

class CalibLightCollection(models.Model):
    fiber = models.ForeignKey(Fiber, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    results_file = models.TextField(blank=True, null=True)
    lcol_l = models.FloatField()
    lcol_l_err = models.FloatField()
    lcol_r = models.FloatField()
    lcol_r_err = models.FloatField()
    lcol = models.FloatField()
    lcol_err = models.FloatField()

class CalibPeakFitting(models.Model):
    fiber = models.ForeignKey(Fiber, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    results_file = models.TextField(blank=True, null=True)
    const_l = models.FloatField() 
    const_l_err = models.FloatField() 
    mean_l = models.FloatField() 
    mean_l_err = models.FloatField() 
    sigma_l = models.FloatField() 
    sigma_l_err = models.FloatField() 
    const_r = models.FloatField() 
    const_r_err = models.FloatField() 
    mean_r = models.FloatField() 
    mean_r_err = models.FloatField() 
    sigma_r = models.FloatField() 
    sigma_r_err = models.FloatField() 
    const_avg = models.FloatField() 
    const_avg_err = models.FloatField() 
    mean_avg = models.FloatField() 
    mean_avg_err = models.FloatField() 
    sigma_avg = models.FloatField() 
    sigma_avg_err = models.FloatField() 

class CalibPositionReconstruction(models.Model):
    fiber = models.ForeignKey(Fiber, on_delete=models.CASCADE)
    date = models.TextField(blank=True, null=True) 
    results_file = models.TextField(blank=True, null=True)
    posres_mlr = models.FloatField() 
    posres_mlr_err = models.FloatField() 
    posres_all_mlr = models.FloatField() 
    posres_all_mlr_err = models.FloatField()
    posres_elar = models.FloatField() 
    posres_elar_err = models.FloatField() 
    posres_all_elar = models.FloatField() 
    posres_all_elar_err = models.FloatField() 

class CalibTimingResolution(models.Model):
    fiber = models.ForeignKey(Fiber, on_delete=models.CASCADE)
    date = models.TextField(blank=True, null=True) 
    results_file = models.TextField(blank=True, null=True)
    tres_all = models.FloatField() 
    tres_all_err = models.FloatField() 
    tres_ecut = models.FloatField() 
    tres_ecut_err = models.FloatField() 

class CalibAttenuation(models.Model):
    fiber = models.ForeignKey(Fiber, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    results_file = models.TextField(blank=True, null=True)
    mlr_lambda = models.FloatField()
    mlr_lambda_err = models.FloatField()
    mlr_chi2ndf = models.FloatField()
    ela_l_lambda = models.FloatField()
    ela_l_lambda_err = models.FloatField()
    ela_l_chi2ndf = models.FloatField()
    ela_r_lambda = models.FloatField()
    ela_r_lambda_err = models.FloatField()
    ela_r_chi2ndf = models.FloatField()
    ela_lambda = models.FloatField()
    ela_lambda_err = models.FloatField()
    ela_chi2ndf = models.FloatField()
    elar_ampl = models.FloatField()
    elar_ampl_err = models.FloatField()
    elar_lambda = models.FloatField()
    elar_lambda_err = models.FloatField()
    elar_eta_l = models.FloatField()
    elar_eta_l_err = models.FloatField()
    elar_eta_r = models.FloatField()
    elar_eta_r_err = models.FloatField()
    elar_ksi = models.FloatField()
    elar_ksi_err = models.FloatField()
    elar_chi2ndf = models.FloatField()
    mlr_ecut_lambda = models.FloatField()
    mlr_ecut_lambda_err = models.FloatField()
    mlr_ecut_chi2ndf = models.FloatField()
    mlr_elar_lambda = models.FloatField()
    mlr_elar_lambda_err = models.FloatField()
    mlr_elar_chi2ndf = models.FloatField()
