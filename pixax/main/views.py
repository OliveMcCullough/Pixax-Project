from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models.functions import Lower
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import RedirectView, CreateView, FormView, ListView, DeleteView, UpdateView

from .forms import AlbumCreateForm, PictureUploadForm, RateAndSortIntroForm
from .models import Album, Picture


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
    paginate_by_default = 11

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
        query = str(self.request.GET.get("q","")).strip()
        albums = Album.objects.filter(author=self.request.user, name__icontains=query).order_by(Lower('name'))

        unsorted_pictures = Picture.objects.filter(user=self.request.user, albums=None).order_by("-rating", "-id")
        if unsorted_pictures.count()>0:
            paginate_by = self.paginate_by_default - 1
        else:
            paginate_by = self.paginate_by_default

        paginator = Paginator(albums, paginate_by)
        page = paginator.get_page(page_number)
        start_item = paginate_by * (page_number-1)
        end_item = paginate_by * page_number

        albums_sub_set = albums[start_item:end_item]
        if albums_sub_set.count() == 0 and page_number > 1:
            raise Http404
        kwargs['albums'] = albums_sub_set
        kwargs['page_obj'] = page
        kwargs['query'] = query
        kwargs['unsorted_picture'] = unsorted_pictures.first()
        return super().get_context_data(**kwargs)


class AlbumView(ListView):
    context_object_name = "pictures"
    template_name = "album.html"
    model = Picture
    paginate_by = 15

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        user = self.request.user
        album = Album.objects.filter(id=pk).first()
        if album == None:
            raise Http404
        if album.author != user:
            raise Http404
        context["album"] = album
        context["order"] = self.get_ordering()[0]
        return context

    def get_queryset(self, **kwargs):
        qs = super().get_queryset()
        pk = self.kwargs['pk']
        album = Album.objects.filter(id=pk)
        return qs.filter(albums__in=album)

    def get_ordering(self):
        ordering = self.request.GET.get('order_by', '-rating')
        if not ordering in ["-rating", "rating", "-date_uploaded", "date_uploaded"]:
            ordering = "-rating"
        ordering = [ordering, "-id"]
        return ordering


class AlbumEditNameView(UpdateView):
    model = Album
    template_name = "album_name_change.html"
    fields = ["name"]

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_object(self):
        album = super().get_object()
        if not album.author == self.request.user:
            raise Http404
        return album

    def get_success_url(self):
          album_id=self.kwargs['pk']
          return reverse_lazy('main:album', kwargs={'pk': album_id})


class AlbumDeleteView(DeleteView):
    model = Album
    template_name = "album_delete.html"
    success_url = reverse_lazy('main:albums')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_object(self):
        album = super().get_object()
        if not album.author == self.request.user:
            raise Http404
        return album


class UnsortedPicturesView(ListView):
    context_object_name = "pictures"
    template_name = "unsorted.html"
    model = Picture
    paginate_by = 15

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["order"] = self.get_ordering()[0]
        return context

    def get_queryset(self):
        unsorted_pictures = Picture.objects.filter(user=self.request.user, albums=None).order_by("-rating")
        if unsorted_pictures.count() == 0:
            raise Http404
        return unsorted_pictures

    def get_ordering(self):
        ordering = self.request.GET.get('order_by', '-rating')
        if not ordering in ["-rating", "rating", "-date_uploaded", "date_uploaded"]:
            ordering = "-rating"
        ordering = [ordering, "-id"]
        return ordering


class UploadPicturesView(FormView):
    template_name = "upload.html"
    model = Picture
    form_class = PictureUploadForm
    success_url=reverse_lazy("main:albums")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        form_valid = super().form_valid(form)
        picture_files = self.request.FILES.getlist('picture_files')
        user = self.request.user
        same_or_different_albums = form.cleaned_data.get("same_or_different_albums")
        album_ids = form.cleaned_data.get("which_albums")
        for picture_file in picture_files:
            picture = Picture(image = picture_file, user = user)
            picture.save()
            if same_or_different_albums == "same":
                for album_id in album_ids:
                    album_obj = Album.objects.get(id=int(album_id))
                    picture.albums.add(album_obj)
            else:
                for album_id in album_ids:
                    suggested_album_obj = Album.objects.get(id=int(album_id))
                    picture.suggested_albums.add(suggested_album_obj)
        return form_valid

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    
class AlbumRateSortView(FormView):
    template_name = "album_organise.html"
    form_class = RateAndSortIntroForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        album_id=self.kwargs['pk']
        album = Album.objects.filter(id=album_id).first()
        if album.author != self.request.user:
            raise Http404
        context["album"] = album
        return context

    def get_form(self):
        ordering = self.request.GET.get('order_by', '-rating')
        if not ordering in ["-rating", "rating", "-date_uploaded", "date_uploaded"]:
            ordering = "-rating"
        ordering = [ordering, "-id"]
        form = RateAndSortIntroForm(initial={'order_select':ordering})
        return form

