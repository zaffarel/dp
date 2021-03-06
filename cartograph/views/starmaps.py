from cartograph.models.system import System
from cartograph.utils.fics_references import NEW_ROUTES, NEW_SYSTEMS
from collector.utils.basic import get_current_config
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404
from django.template.loader import get_template


def show_jumpweb(request):
    if request.is_ajax:
        campaign = get_current_config()
        context = {}
        context['data'] = {}
        context['campaign'] = campaign
        context['data']['mj'] = 1 if request.user.profile.is_gamemaster else 0
        context['data']['new_routes'] = "|".join(NEW_ROUTES)
        context['data']['new_systems'] = "|".join(NEW_SYSTEMS)
        context['data']['nodes'] = []
        context['data']['links'] = []
        for s in System.objects.all():
            system = {}
            system['id'] = s.id
            system['name'] = s.name
            system['alliance'] = s.alliance
            system['sector'] = s.sector
            # system['jumproads'] = s.jumproads
            system['x'] = s.x
            system['y'] = s.y
            system['jump'] = s.jump
            system['group'] = s.group
            system['color'] = s.color
            system['orbital_map'] = 1 if s.orbital_map != '' else 0
            system['discovery'] = s.discovery
            system['dtj'] = s.dtj
            system['garrison'] = s.garrison
            system['tech'] = s.tech
            system['symbol'] = s.symbol
            system['population'] = s.population
            context['data']['nodes'].append(system)
            for j in s.jumproads.all():
                lnk = {}
                if j.id > s.id:
                    lnk['source'] = s.id
                    lnk['target'] = j.id
                else:
                    lnk['source'] = j.id
                    lnk['target'] = s.id
                context['data']['links'].append(lnk)
        template = get_template('cartograph/jumpweb.html')
        html = template.render(context)
        return HttpResponse(html, content_type='text/html')
    else:
        return Http404


def show_orbital_map(request, id):
    if request.is_ajax:
        campaign = get_current_config()
        system = get_object_or_404(System, pk=id)
        context = {'data': {}}
        context['campaign'] = campaign
        context['data']['mj'] = 1 if request.user.profile.is_gamemaster else 0
        context['data']['title'] = f'{system.name}'
        context['data']['alliance'] = f'{system.alliance}'
        context['data']['symbol'] = f'{system.symbol}'
        context['data']['planets'] = []

        context['data']['zoom_val'] = system.zoom_val if system.zoom_val else 0
        context['data']['zoom_factor'] = system.zoom_factor if system.zoom_factor else 0
        for oi in system.orbitalitem_set.all():
            orbital_item = {'name': oi.name, 'AU': oi.distance, 'tilt': oi.tilt, 'speed': oi.speed, 'tone': oi.color,
                            'type': oi.get_category_display(), 'azimut': oi.azimut, 'size': oi.size, 'moon': oi.moon,
                            'description': oi.description, 'rings': oi.rings}
            context['data']['planets'].append(orbital_item)
        template = get_template('cartograph/orbital_map.html')
        html = template.render(context)
        return HttpResponse(html, content_type='text/html')
    else:
        return Http404
