
from cmp.cmpm.models import *
from cmp.cmpm.forms import *
from cmp.cmpm.helper import *
from cmp.cmpm.tools import *

from django.views.generic.list_detail import object_list
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, Http404

from django.template import Context
from django.template.loader import get_template

#from django.core.paginator import Paginator, InvalidPage, EmptyPage

# corpsofmilitarypolice.org
maps_api_key = 'abc'
zoom = 6

def search_page(request):
    """Search Surnames"""
    form = SearchForm()
    soldiers = []
    show_results = False
    error = False
    if request.GET.has_key('query'):
        show_results = True
        query = request.GET['query'].strip()
        if query:
            form = SearchForm({'query' : query})
            try:
                s = int(query)
                soldiers = Soldier.objects.filter(Army_number__icontains=s)
            except:
                soldiers = Soldier.objects.filter(Surname__icontains=query)
            hits = len(soldiers)
            variables = RequestContext(request, {'form': form,
                                     'soldiers': soldiers,
                                     'hits': hits,
                                     'search_string': query,
                                     'show_results': show_results
            })
            return render_to_response('site/search.html', variables)
        else:
           error = True
       
    return render_to_response('site/search.html', {'error': error, 'form': form})

def army_number_page(request):
    """Find the original enlisted unit for an army number"""
    form = anForm()
    show_results = False
    error = False
    if request.GET.has_key('query'):
        show_results = True
        query = request.GET['query'].strip()
        if query:
            form = anForm({'query' : query})
            try:
                an = int(query)
                original_unit = originalUnit(an)
            except:
                pass
            variables = RequestContext(request, {'form': form,
                                     'army_number': an,
                                     'original_unit': original_unit,
            })
            return render_to_response('site/army_number.html', variables)
        else:
           error = True
    return render_to_response('site/army_number.html', {'error': error, 'form': form})

def browse_page(request):
    """ Browse Soldiers Page """
    return render_to_response("site/browse.html",
        {'soldiers': Soldier.objects.order_by('Surname')},
        context_instance=RequestContext(request))

def browse_cemeteries(request):
    """ Browse Cemeteries Page """
    return render_to_response("site/browse_cemeteries.html",
        {'cemeteries': Cemetery.objects.order_by('Name')},
        context_instance=RequestContext(request))

def browse_countries(request):
    """ Browse Countries Page """
    #c = Country.objects.filter(id__in=Cemetery.objects.values('Country').order_by('Country').distinct())
    country_list = []
    c = Cemetery.objects.values('Country').order_by('Country').distinct()
    for item in c:
        country_list.append(int(item['Country']))    
    return render_to_response("site/browse_countries.html",
        { 
         #'countries': Country.objects.exclude(id__in=Cemetery.objects.values('Country').order_by('Country').distinct()),
         #'countries': Country.objects.order_by('Name'),
         #'countries': c,
         'countries':  Country.objects.filter(id__in=country_list),
         #'countries': Country.objects.filter(CountryNumber__in=Cemetery.objects.values('Country').order_by('Country').distinct())
         # 'countries': Country.objects.order_by('id').filter(id__in=Cemetery.objects.values('Country').order_by('id').distinct())
        },
        context_instance=RequestContext(request))

def country_page(request, country_code):
    """ Country """
    try:
        country_code = str(country_code)
        c = Country.objects.get(Alpha2=country_code)
         
    except:
        raise Http404()
    return render_to_response("site/country.html",
        {
         'country': Country.objects.get(Alpha2=country_code),
         'cemeteries': Cemetery.objects.filter(Country=c.id),
        },
        context_instance=RequestContext(request))

def cemetery_page(request, cemetery_code):
    """ Cemetery """
    try:
        code = int(cemetery_code)
    except:
        raise Http404()

    return render_to_response("site/cemetery.html",
        {'soldiers': Soldier.objects.filter(soldierdeath__cemetery__id=code).order_by('Surname'),
         'cemetery': Cemetery.objects.get(id=code),
        },
        context_instance=RequestContext(request))


def main_page(request):
    """
    Landing Page of Site
    """
    form = SearchForm()
    soldiers = []
    show_results = False
    if request.GET.has_key('query'):
        show_results = True
        query = request.GET['query'].strip()
        if query:
            form = SearchForm({'query' : query})
            soldiers = Soldier.objects.filter(Surname__icontains=query)[:15]

    template = get_template('site/index_page.html')
    variables = Context({
                                  'form': form,
                                  'head_title': 'Corps of Military Police',
                                  'page_title': 'Welcome to CMP',
                                  'cmp_soldier_count': Soldier.objects.count(),
                                  'cmp_casualty_count': SoldierDeath.objects.count(),
                                  'cmp_prisoner_count': SoldierImprisonment.objects.count(),
                                  'cmp_decoration_count':  SoldierDecoration.objects.count(),
                                  'cmp_cemetery_count':  Cemetery.objects.count(),
                                  'cmp_countries_count':  len(Cemetery.objects.values('Country').order_by('Country').distinct())
                               })
    output = template.render(variables)
    return HttpResponse(output)

def soldier_detail(request, soldier_id):
    """Gather together details about soldier"""
    s = Soldier.objects.get(id=soldier_id)
    soldier_record = {
                          's_surname':      s.Surname,
                          's_initials':     s.dot_initials(),
                          's_rank':         s.Rank,
                          's_armynumber':   s.Army_number,
                          's_notes':        s.Notes, 
                         }

    try:
        SoldierDeath.objects.get(Soldier=soldier_id)
        soldier_record['s_cemetery']           = s.soldierdeath.cemetery
        soldier_record['s_date_killed']        = s.soldierdeath.Date
        soldier_record['s_death_company']      = s.soldierdeath.company
        soldier_record['s_grave_photo']        = s.soldierdeath.grave_photo()
        soldier_record['s_cemetery_flag']      = s.soldierdeath.cemetery.country_flag()
        soldier_record['s_cemetery_country']   = s.soldierdeath.cemetery.Country
        soldier_record['s_cemetery_latitude']  = s.soldierdeath.cemetery.Latitude
        soldier_record['s_cemetery_longitude'] = s.soldierdeath.cemetery.Longitude
        soldier_record['s_maps_api_key']       = maps_api_key
        soldier_record['s_maps_zoom']          = zoom
        soldier_record['s_is_casualty']        = True
    except SoldierDeath.DoesNotExist:
        soldier_record['s_is_casualty']        = None
             
    try:
        SoldierImprisonment.objects.get(Soldier=soldier_id)
        soldier_record['s_is_pow']             = True
        soldier_record['s_pownumber']          = s.soldierimprisonment.POWNumber
        soldier_record['s_powcamp']            = s.soldierimprisonment.POWCamp
        soldier_record['s_powcamp_country']    = s.soldierimprisonment.POWCamp.PresentCountry
        soldier_record['s_powcamp_flag']       = s.soldierimprisonment.POWCamp.country_flag()
    except SoldierImprisonment.DoesNotExist:
        soldier_record['s_is_pow']             = None

    if len(SoldierDecoration.objects.filter(Soldier=soldier_id)) > 0:
            soldier_record['s_is_decorated'] = True
            soldier_record['s_dec_count'] = len(SoldierDecoration.objects.filter(Soldier=soldier_id))
            soldier_record['s_decoration_list'] = SoldierDecoration.objects.filter(Soldier=soldier_id).select_related()
    else:
        soldier_record['s_is_decorated']     = None

    if soldier_record['s_is_casualty']:
        soldier_record['s_cwgc_search']         = s.soldierdeath.cwgc_url()
        # The only thing that determines the badge is the
        # unit or the date killed/decorated/imprisoned.
        # prisoners don't have dates!
        dk = s.soldierdeath.Date or None
        cp = str(s.soldierdeath.company)
        if company_is_indian(cp) or notes_is_indian(s):
           badge = badge_decide(dk.year, special_case='india')
           soldier_record['s_corps']         = badge[0]
           soldier_record['s_badge']         = badge[1]
           soldier_record['s_badge_alt']     = badge[2]
        elif company_is_mpsc(cp):
           badge = badge_decide(dk.year, special_case='mpsc')
           soldier_record['s_corps']         = badge[0]
           soldier_record['s_badge']         = badge[1]
           soldier_record['s_badge_alt']     = badge[2]
        else:
           badge = badge_decide(dk.year)
           soldier_record['s_corps']         = badge[0]
           soldier_record['s_badge']         = badge[1]
           soldier_record['s_badge_alt']     = badge[2]
    elif soldier_record['s_is_pow']:
        badge = badge_decide(1945)
        soldier_record['s_corps']            = badge[0]
        soldier_record['s_badge']            = badge[1]
        soldier_record['s_badge_alt']        = badge[2]
    elif soldier_record['s_is_decorated']:
        d_count =  len(soldier_record['s_decoration_list'])
        d_last = d_count - 1
        dd = soldier_record['s_decoration_list'][d_last].GztDate
        cp = str(soldier_record['s_decoration_list'][d_last].Company)
        if company_is_indian(cp) or notes_is_indian(s):
           badge = badge_decide(dd.year, special_case='india')
           soldier_record['s_corps']         = badge[0]
           soldier_record['s_badge']         = badge[1]
           soldier_record['s_badge_alt']     = badge[2]
        elif company_is_mpsc(cp):
           badge = badge_decide(None, special_case='mpsc')
           soldier_record['s_corps']         = badge[0]
           soldier_record['s_badge']         = badge[1]
           soldier_record['s_badge_alt']     = badge[2]
        else:
           try:  
               dk.year
               badge = badge_decide(dk.year)
               soldier_record['s_corps']         = badge[0]
               soldier_record['s_badge']         = badge[1]
               soldier_record['s_badge_alt']     = badge[2]
           except NameError:
               badge = badge_decide(1900, special_case='nodate')
               soldier_record['s_corps']         = badge[0]
               soldier_record['s_badge']         = badge[1]
               soldier_record['s_badge_alt']     = badge[2]

    template = get_template('site/soldier.html')
    variables = Context(
                         soldier_record 
                        )

    output = template.render(variables)
    return HttpResponse(output)

