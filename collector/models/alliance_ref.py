'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from colorfield.fields import ColorField
from django.db import models
from django.contrib import admin
import json


ALLIANCE_CATEGORIES = (
    ('nobility',"Royale Nobility"),
    ('minor_nobility',"Nobility"),
    ('church',"Church"),
    ('minor_sects',"Minor Sects of the Church"),
    ('guild',"Guild"),
    ('minor_guild',"Minor Guilds"),
    ('outlaw',"Terrorist Groups"),
    ('foes',"Enemies of the Crown"),
    ('other',"Other"),
)

def json_default(value):
    import datetime
    if isinstance(value, datetime.date):
        return dict(year=value.year, month=value.month, day=value.day)
    else:
        return value.__dict__

class AllianceRef(models.Model):
    class Meta:
        verbose_name = "FICS: Alliance"
        ordering = ['reference', 'category', ]
    reference = models.CharField(max_length=128,default='')
    category = models.CharField(max_length=20,choices=ALLIANCE_CATEGORIES,default='other')
    color_front = ColorField(default='#AAAAAA')
    color_back = ColorField(default='#666666')
    color_highlight = ColorField(default='#111111')
    faction = models.CharField(max_length=128, default='', blank=True)
    icon_simple = models.CharField(max_length=3, default='', blank=True)
    icon_complex = models.CharField(max_length=258, default='', blank=True)
    color_icon_stroke = ColorField(default='#888888')
    color_icon_fill = ColorField(default='#333333')


    def __str__(self):
        return f'{self.reference} ({self.get_category_display()})'

    # def toJSON(self):
    #     """ Returns JSON of object """
    #     return json.dumps(self, default=json_default,sort_keys=True, indent=4)

class AllianceRefAdmin(admin.ModelAdmin):
    ordering = ['category', 'reference']
    list_display = ['reference', 'faction','category', 'color_front', 'color_back','color_highlight']
    list_filter = ['category']
    search_fields = ['category']
