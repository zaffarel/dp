from django.contrib import admin
from collector.models.skillsinline import SkillInline
from collector.models.blessingcursesinline import BlessingCurseInline
from collector.models.benefices_afflictions import BeneficeAfflictionInline
from collector.models.talentsinline import TalentInline
from collector.models.weaponsinline import WeaponInline
from collector.models.armorsinline import ArmorInline
from collector.models.shieldsinline import ShieldInline

def cast_to_dem(modeladmin, request, queryset):
  queryset.update(epic=1)
  short_description = "Cast to the Deus Ex Machina epic."

def cast_to_blank(modeladmin, request, queryset):
  queryset.update(epic=2)
  short_description = "Cast to no epic."

def make_invisible(modeladmin, request, queryset):
  queryset.update(visible=False)
  short_description = "Make invisible"

def make_visible(modeladmin, request, queryset):
  queryset.update(visible=True)
  short_description = "Make visible"

def make_teutonic(modeladmin, request, queryset):
  queryset.update(castspecies=1)
  short_description = "Make teutonic"

def make_kaanic(modeladmin, request, queryset):
  queryset.update(castspecies=25)
  short_description = "Make kaanic"

def make_castillan(modeladmin, request, queryset):
  queryset.update(castspecies=22)
  short_description = "Make castillan"

def make_enquist(modeladmin, request, queryset):
  queryset.update(castspecies=23)
  short_description = "Make enquist"

class CharacterAdmin(admin.ModelAdmin):
  list_display = ('full_name','castspecies','castrole','castprofile','species','alliance','PA_TOTAL','SK_TOTAL','BA_TOTAL','BC_TOTAL','TA_TOTAL','OP','visible','epic')
  inlines = [
    SkillInline,
    BlessingCurseInline,
    BeneficeAfflictionInline,
    TalentInline,
    WeaponInline,
    ArmorInline,
    ShieldInline,
  ]  
  ordering = ['epic','full_name',]
  actions = [cast_to_blank, cast_to_dem, make_invisible, make_visible, make_teutonic, make_kaanic, make_castillan, make_enquist]

  
