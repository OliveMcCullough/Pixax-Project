from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models.functions import Lower
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import RedirectView, CreateView

from .forms import AlbumCreateForm
from .models import Album


class RootRedirectView(RedirectView):
    permanent = True
    query_string = False
    pattern_name = 'main:albums'

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return super().get_redirect_url(*args, **kwargs)            
        else:
            return reverse('users:register')


class MyAlbumsView(CreateView):
    template_name = "albums.html"
    model = Album
    success_url = reverse_lazy("main:albums")
    form_class = AlbumCreateForm
    paginate_by = 11

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        albums_with_same_name_by_user = Album.objects.filter(name=form.instance.name, author=form.instance.author)
        if albums_with_same_name_by_user.exists():
            form.add_error("name", "You already have an album named \"" + form.instance.name + "\".")
            return super().form_invalid(form)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        page_number = int(self.request.GET.get("page", 1))
        query = str(self.request.GET.get("q",""))
        albums = Album.objects.filter(author=self.request.user, name__icontains=query).order_by(Lower('name'))
        paginator = Paginator(albums, self.paginate_by)
        page = paginator.get_page(page_number)
        start_item = self.paginate_by * (page_number-1)
        end_item = self.paginate_by * page_number
        kwargs['albums'] = albums[start_item:end_item]
        kwargs['page_obj'] = page
        kwargs['query'] = query
        return super().get_context_data(**kwargs)
