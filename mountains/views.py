from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Mountain, Route, MountainGallery

def rinjani_senaru_detail(request):
    """View untuk halaman detail Rinjani via Senaru"""
    # Get Rinjani mountain
    mountain = get_object_or_404(Mountain, slug='gunung-rinjani')
    
    # Get Senaru route
    route = get_object_or_404(Route, mountain=mountain, slug='jalur-senaru')
    
    # Get gallery
    gallery = MountainGallery.objects.filter(mountain=mountain, route=route)[:6]
    
    # Get other routes
    other_routes = Route.objects.filter(mountain=mountain, is_active=True).exclude(id=route.id)
    
    context = {
        'mountain': mountain,
        'route': route,
        'gallery': gallery,
        'other_routes': other_routes,
        'page_title': f'{mountain.name} via {route.name}'
    }
    return render(request, 'mountains/rinjani_senaru_detail.html', context)


class MountainListView(ListView):
    model = Mountain
    template_name = 'mountains/list.html'
    context_object_name = 'mountains'
    paginate_by = 12
    
    def get_queryset(self):
        return Mountain.objects.filter(is_active=True)


class MountainDetailView(DetailView):
    model = Mountain
    template_name = 'mountains/detail.html'
    context_object_name = 'mountain'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['routes'] = self.object.routes.filter(is_active=True)
        context['gallery'] = self.object.gallery.all()[:12]
        return context


class RouteDetailView(DetailView):
    model = Route
    template_name = 'mountains/route_detail.html'
    context_object_name = 'route'
    slug_url_kwarg = 'route_slug'
    
    def get_object(self):
        mountain = get_object_or_404(Mountain, slug=self.kwargs['mountain_slug'])
        return get_object_or_404(Route, mountain=mountain, slug=self.kwargs['route_slug'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mountain'] = self.object.mountain
        context['gallery'] = self.object.gallery.all()
        return context