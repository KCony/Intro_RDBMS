from django.shortcuts import render
from farmers_markets.models import Cities, Markets
from django.views import generic

# Create your views here.


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_markets = Markets.objects.all().count()

    # Farmers Markets in NY (status = 'a')
    num_markets_ny = Markets.objects.filter(state__state_abbr='NY').count()

    # The 'all()' is implied by default.
    num_cities = Cities.objects.count()

    context = {
        'num_markets': num_markets,
        'num_markets_ny': num_markets_ny,
        'num_cities': num_cities,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'farmers_markets/index.html', context=context)


class MarketsListView(generic.ListView):
    model = Markets
    paginate_by = 20


class MarketsDetailView(generic.DetailView):
    model = Markets

