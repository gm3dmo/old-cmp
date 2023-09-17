from django.db import models
from datetime import datetime
from string import capitalize
from string import upper
from django.contrib import admin

from urllib import urlencode
import re 
import os

def badge_decide(year, special_case=False):
    """Helper function to decide badges. The indian companies thing 
       messes everything up. The MPSC doesn't help either.
       Maybe we should pre-compute all of these"""
    if special_case == 'india' and year >= 1936:
        return (
                 'Corps of Military Police (India)', 
                 'cmp_badge_g6i.png', 
                 'Cap Badge of the Corps of Military Police India (King George VI)',
                )
    elif special_case == 'mpsc' and year < 1936:
        return (
                 'Military Provost Staff Corps', 
                 'mpsc_badge_g5.png', 
                 'Cap Badge of the Military Police Service Corps (King George V)',
                )
    elif special_case == 'mpsc' and year >= 1936:
        return (
                 'Military Provost Staff Corps', 
                 'mpsc_badge_g6.png', 
                 'Cap Badge of the Military Police Service Corps (King George V)',
                )
    elif special_case == 'mpsc' and year == None:
        return (
                 'Military Provost Staff Corps', 
                 'mpsc_badge_g6.png', 
                 'Cap Badge of the Military Police Service Corps (King George V)',
                )
    elif special_case == 'nodate':
        return (
                 'Military Provost Staff Corps', 
                 'cmp-masthead-sm.png', 
                 'unknown year no badge'
                )
    elif year < 1936:
        return (
                'Corps of Military Police', 
                'cmp_badge_g5.png', 
                'Cap Badge of the Corps of Military Police (King George V)',
               )
    elif year > 1936 and year <= 1946:
        return (
                'Corps of Military Police', 
                'cmp_badge_g6.png', 
                'Cap Badge of the Corps of Military Police (King George VI)',
               )
    elif year > 1946 and year <= 1952:
        return (
                'Royal Military Police',
                'rmp_badge_g6.png', 
                'Cap Badge of the Royal Military Police (King George VI)',
               )
    elif year > 1952:
        return (
                'Royal Military Police',
                'rmp_badge_e2.png',
                'Cap Badge of the Royal Military Police (Queen Elizabeth II)',
               )


def company_is_indian(company):
    """Special case to find if a company is indian"""
    indian_companies = ( 'CMP(I',  )
    for pattern in indian_companies:
        if pattern in company.upper():
            return True
    return False     


def notes_is_indian(soldier):
    """Special case to find if notes contains CMP(I """
    indian_companies = ( 'CMP(I', 'CMP (I'  )
    for pattern in indian_companies:
        if pattern in soldier.Notes.upper():
            return True
    return False     


def company_is_mpsc(company):
    """Special case to find if a company is MPSC"""
    mpsc_companies = ( 'MPSC',  )
    for pattern in mpsc_companies:
        if pattern in company.upper():
            return True
    return False     

class Country(models.Model):
    class Meta:
        verbose_name_plural='Countries'
        ordering = ["Name"]
    Name          = models.CharField(max_length=50)
    Alpha2        = models.CharField(max_length=2)
    Alpha3        = models.CharField(max_length=3)
    CountryNumber = models.CharField(max_length=4)
    FipsCode      = models.CharField(max_length=50)
    def __unicode__(self):
        return '%s' % (self.Name)

class Cemetery(models.Model):
    class Meta:
        verbose_name_plural='Cemeteries'
        ordering = ["Name", "Country"]
    Name = models.CharField(max_length=100)
    Country = models.ForeignKey(Country)
    Latitude = models.CharField(max_length=100, blank=True)
    Longitude = models.CharField(max_length=100, blank=True)
    def __unicode__(self):
        return '%s' % (self.Name)

    def country_flag(self):
        """return lowercase of country code. Used to point to flag icon """
        return self.Country.Alpha2.lower()

class Theatre(models.Model):
    class Meta:
        verbose_name_plural='Theatres'
        ordering = ["Name", ]
    Name = models.CharField(max_length=100, help_text="Theatre of Operations e.g. Normandy B.E.F. France & Flanders. DO NOT PUT Countries in here.")
    def __unicode__(self):
        return '%s' % (self.Name)


class POWCamp(models.Model):
    class Meta:
        verbose_name_plural='POW Camps'
        ordering = ["Name"]
    Name = models.CharField(max_length=50)
    NearestCity = models.CharField(max_length=50, verbose_name="Nearest City")
    Notes = models.TextField(max_length=50000, blank=True)
    WartimeCountry = models.TextField(max_length=200, blank=True, verbose_name="Wartime Country")
    PresentCountry = models.ForeignKey(Country, default='276', verbose_name="Country")
    Latitude = models.CharField(max_length=50, blank=True)
    Longitude = models.CharField(max_length=50, blank=True)
    def __unicode__(self):
        return '%s' % (self.Name)

    def country_flag(self):
        """return lowercase of country code. Used to point to flag icon """
        return self.PresentCountry.Alpha2.lower()

class Rank(models.Model):
    class Meta:
        verbose_name_plural='Ranks'
        ordering = ["Name"]
    RankTypes = (('OR','Other Rank'),('NC','Non Commisioned Officer'),('OF','Officer'))
    Name = models.CharField(max_length=50, unique=True)
    Abbr = models.CharField(max_length=50, blank=True)
    Class = models.CharField(max_length=2, blank=True, choices=RankTypes,default='Other Rank')
    details_link  = models.URLField(verify_exists=False, blank=True, null=True)
    def __unicode__(self):
        return '%s' % (self.Name)

class Company(models.Model):
    class Meta:
        verbose_name_plural='Companies'
        ordering = ["Name"]
    Name = models.CharField(max_length=50, unique=True, primary_key=True)
    Notes = models.TextField(max_length=50000, blank=True)
    def __unicode__(self):
        return '%s' % (self.Name)

class Decoration(models.Model):
    class Meta:
        verbose_name_plural='Decorations'
        ordering = ["Name"]
    Name = models.CharField(max_length=50, unique=True)
    Notes = models.TextField(max_length=50000, blank=True)
    Country = models.ForeignKey(Country, blank=True)
    details_link  = models.URLField(verify_exists=False, blank=True, null=True)
    Abbr = models.CharField(max_length=10, blank=True)
    def __unicode__(self):
        return '%s' % (self.Name)

class Soldier(models.Model):
    class Meta:
        verbose_name_plural='Soldiers'
        ordering = ["Surname"]
    Surname = models.CharField(max_length=50, verbose_name="Surname")
    Initials = models.CharField(max_length=50, blank=True)
    Army_number = models.CharField(unique=True, max_length=50)
    Rank = models.ForeignKey(Rank, null=True, blank=True, default="79")
    Notes = models.TextField(max_length=50000, blank=True)
    def __unicode__(self):
        return '%s %s %s %s' % (self.Surname, self.Initials, self.Rank, self.Army_number)
        #return [ self.Surname, self.Rank ]

    def CapitalizeSurname (self):
        return ("%s") % capitalize(self.Surname) 
    CapitalizeSurname.short_description = 'Name'

    def clean_initials(self):
        clean_dots = self.Initials.replace('.','')
        clean_space = clean_dots.replace(' ','')
        return clean_space

    def dot_initials(self):
        """Return a dotted initial e.g. HW -> H.W."""
        cl = self.clean_initials()
        if cl == "":
            return ""
        else:
            return '%s.' % (".".join(cl) )

    def first_initial(self):
        """Return the first initial"""
        if self.Initials:
            return self.Initials[0]
        else:
            return ""

#class ProvostOfficer(models.Model):
#    class Meta:
#        verbose_name_plural='Provost Officers'
#        ordering = ["Soldier", "Date"]
#    Soldier  = models.OneToOneField(Soldier)
#    Date     = models.DateField(null=True, blank=True)
#    Company  = models.ForeignKey(Company, blank=True, null=True, default="UNKNOWN")
#    Regiment = models.ForeignKey(Regiment, blank=True, null=True, default="UNKNOWN")
#    def __unicode__(self):
#        return '%s %s' % (self.Company, self.Regiment)

class SoldierDeath(models.Model):
    class Meta:
        verbose_name_plural='Soldier Death'
        ordering = ["Soldier", "Date"]
    Soldier  = models.OneToOneField(Soldier)
    Date     = models.DateField(null=True, blank=True)
    company  = models.ForeignKey(Company, blank=True, null=True, default="UNKNOWN")
    cemetery = models.ForeignKey(Cemetery, blank=True, null=True, default=110)
    cwgc_id  = models.IntegerField(blank=True, null=True, unique=True, verbose_name="War Graves ID")
    def __unicode__(self):
        return '%s %s %s' % (self.Soldier, self.Date, self.cemetery)

    def cwgc_url(self):
        """Build a URL for a link to CWGC site."""
        wg_site =  'http://www.cwgc.org'
        if self.cwgc_id:
           wg_string = 'find-war-dead/casualty/%s/' % (self.cwgc_id)
           wg_url = '%s/%s' % (wg_site, wg_string )
           return wg_url
        else:
            dk = self.Date
            wg_string = 'search/SearchResults.aspx?surname=%s&initials=%s&war=0&yearfrom=%s&yearto=%s&force=%s&nationality=&send.x=26&send.y=19"' % (self.Soldier.Surname, self.Soldier.first_initial(), dk.year, dk.year, 'Army')
        wg_url = '%s/%s' % (wg_site, wg_string )
        return wg_url
 
    def grave_photo(self):
        photo_dir = '/sites/corpsofmilitarypolice.org/www/media/grave_images'
        id_photo_dir = '/sites/corpsofmilitarypolice.org/www/media/grave_images/soldier_id'
        """Determine whether or not a photograph exists
        for a soldier with a particular army number"""
        army_number = self.Soldier.Army_number
        modded_an = re.sub('\/','_',army_number,1)
        photo_name = modded_an + ".jpg"
        id_photo_name = str(self.Soldier.id) + ".jpg"
        photo_file = '%s/%s' %  (photo_dir,  photo_name)
        id_photo_file = '%s/%s' %  (id_photo_dir,  id_photo_name)
        if os.path.isfile(photo_file):
            return photo_name
        elif os.path.isfile(id_photo_file):
            return 'soldier_id/%s' % id_photo_name
        else:
            return None

class SoldierDecoration(models.Model):
    class Meta:
        verbose_name_plural='Soldier Decorations'
        ordering = ["Soldier", "GztDate"]
    Soldier     = models.ForeignKey(Soldier)
    Company = models.ForeignKey(Company, blank=True, null=True )
    Decoration  = models.ForeignKey(Decoration, blank=True, null=True)
    GztIssue = models.CharField(max_length=50,    blank=True)
    GztPage = models.CharField(max_length=50,    blank=True)
    GztDate = models.DateField(null=True,    blank=True)
    Theatre = models.ForeignKey(Theatre, blank=True, null=True, help_text="Theatre of Operations e.g. Normandy, B.E.F. France & Flanders. NOT Country names")
    Country = models.ForeignKey(Country, blank=True, null=True)
    Citation    = models.TextField(max_length=50000, blank=True)
    Notes       = models.TextField(max_length=50000, blank=True)
    def __unicode__(self):
        return '%s' % (self.Decoration)

    def GztURL(self):
        """Build a URL for the London Gazette. This will not handle Edinburgh gazette"""
        gz_site =  'http://www.thegazette.co.uk'
        # "${gz_url}/SearchResults.aspx?GeoType=${gz_type}&st=${sc_type}&sb=issue&issue=${gz_issue}&gpn=${gz_page}&"
        gz_type = 'london'  
        sc_type = 'adv'
        #gz_string = "SearchResults.aspx?GeoType=${gz_type}&st=${sc_type}&sb=issue&issue=${gz_issue}&gpn=${gz_page}&" 
        gz_string = "%s/London/issue/%s/supplement/%s" % (gz_site, self.GztIssue, self.GztPage )
        gz_url = gz_string 
        return gz_url

class SoldierImprisonment(models.Model):
    class Meta:
        verbose_name_plural='Soldier Imprisonment'
        ordering = ["Soldier"]
    Soldier = models.OneToOneField(Soldier)
    Company = models.ForeignKey(Company, blank=True, null=True, default="UNKNOWN")
    POWNumber = models.CharField(max_length=50, blank=True)
    POWCamp = models.ForeignKey(POWCamp)
    DateFrom = models.DateField(null=True, blank=True)
    DateTo = models.DateField(null=True, blank=True)
    Notes = models.TextField(max_length=50000, blank=True)
    def __unicode__(self):
        return '%s' % (self.Soldier)

class DeathAdmin(admin.StackedInline):
    model = SoldierDeath
    fieldsets = ( 
        ('Death', { 'classes':('collapse',),
        'fields': ('Date','company','cemetery','cwgc_id')
         }),
    )

class DecorationAdmin(admin.StackedInline):
    model = SoldierDecoration
    name_hierarchy = 'Surname'
    list_filter = ('Surname',)
    list_display = ('id', 'CapitalizeSurname', 'Initials', 'Army_number','Rank')
    search_fields = ['Surname','Army_number']
    fieldsets = ( 
        ('Decoration', { 'classes':('collapse',),
        'fields': ('Company','Decoration','Citation','GztIssue','GztPage','GztDate','Theatre','Country')
         }),
    )

class POWAdmin(admin.StackedInline):
    model = SoldierImprisonment
    fieldsets = ( 
        ('POW', { 'classes':('collapse',),
        'fields': ('POWNumber','Company','POWCamp','DateFrom','DateTo')
         }),
    )

class SoldierAdmin(admin.ModelAdmin):
    name_hierarchy = 'Surname'
    list_filter = ('Surname',)
    list_display = ('id', 'CapitalizeSurname', 'Initials', 'Army_number','Rank')
    search_fields = ['Surname','Army_number']
    inlines = [
        DeathAdmin,
        POWAdmin,
        DecorationAdmin,
    ]

class SoldierDeathAdmin(admin.ModelAdmin):
    name_hierarchy = 'CapitalizeSurname'
    list_filter = ('Surname',)
    list_display = ('id', 'CapitalizeSurname', 'Initials', 'Army_number','Rank')
    search_fields = ['Surname','Army_number']
    inlines = [
        DeathAdmin,
    ]

class CemeteryAdmin(admin.ModelAdmin):
    name_hierarchy = 'Name'
    list_filter = ('Name','Country')
    list_display = ('id','Name', 'Country', 'Latitude', 'Longitude')
    search_fields = ['Name', 'Country']

class TheatreAdmin(admin.ModelAdmin):
    name_hierarchy = 'Name'
    list_filter = ('Name',)
    list_display = ('id','Name')
    search_fields = ['Name']

class CountryAdmin(admin.ModelAdmin):
    name_hierarchy = 'Name'
    list_filter = ('Name',)
    list_display = ('Name',)
    search_fields = ['Name']

class RankAdmin(admin.ModelAdmin):
    name_hierarchy = 'Name'
    list_filter = ('Name',)
    list_display = ('id','Name','Abbr','Class')
    search_fields = ['Name']

class POWCampAdmin(admin.ModelAdmin):
    name_hierarchy = 'Name'
    list_filter = ('id','Name')
    list_display = ('id','Name')
    search_fields = ['Name']

class DecorationAdmin2(admin.ModelAdmin):
    name_hierarchy = 'Name'
    list_filter = ('Name',)
    list_display = ('id','Name')
    search_fields = ['Name']

