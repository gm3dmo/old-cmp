from cmp.cmpm.models import Soldier
from cmp.cmpm.models import SoldierAdmin

from cmp.cmpm.models import Rank
from cmp.cmpm.models import RankAdmin

from cmp.cmpm.models import Company

from cmp.cmpm.models import Decoration
from cmp.cmpm.models import DecorationAdmin
from cmp.cmpm.models import DecorationAdmin2

from cmp.cmpm.models import SoldierDeath
from cmp.cmpm.models import SoldierDecoration
from cmp.cmpm.models import SoldierImprisonment

from cmp.cmpm.models import SoldierDeathAdmin

from cmp.cmpm.models import Cemetery
from cmp.cmpm.models import CemeteryAdmin

from cmp.cmpm.models import Theatre
from cmp.cmpm.models import TheatreAdmin

from cmp.cmpm.models import POWCamp 
from cmp.cmpm.models import POWCampAdmin

from cmp.cmpm.models import Country
from cmp.cmpm.models import CountryAdmin

from django.contrib import admin

admin.site.register(Rank, RankAdmin)
admin.site.register(Company)
admin.site.register(Soldier, SoldierAdmin)
admin.site.register(SoldierDeath)
admin.site.register(SoldierDecoration)
admin.site.register(SoldierImprisonment)
admin.site.register(Cemetery, CemeteryAdmin)
admin.site.register(Theatre, TheatreAdmin)
admin.site.register(Decoration, DecorationAdmin2)
admin.site.register(POWCamp, POWCampAdmin)
admin.site.register(Country, CountryAdmin)

