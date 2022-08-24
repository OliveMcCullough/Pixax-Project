from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models.functions import Lower
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import RedirectView, CreateView, FormView, ListView, DeleteView, UpdateView, TemplateView

from .forms import AlbumCreateForm, PictureUploadForm, RateAndSortIntroForm, RateAndSortActiveForm
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
        qs = super().get_queryset()
        unsorted_pictures = qs.filter(user=self.request.user, albums=None)
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
    form_class = PictureUploadForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        picture_files = self.request.FILES.getlist('picture_files')
        user = self.request.user
        same_or_different_albums = form.cleaned_data.get("same_or_different_albums")
        album_ids = form.cleaned_data.get("which_albums")
        self.same_or_different_albums=same_or_different_albums

        form_valid = super().form_valid(form)
        
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
        self.same_or_different_albums = same_or_different_albums
        return form_valid

    def get_success_url(self):
        if self.same_or_different_albums=="same":
            return reverse_lazy("main:albums")
        else:
            return reverse_lazy("main:unsorted")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class RateSortIntroBaseView(FormView):
    form_class = RateAndSortIntroForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        ordering = self.request.GET.get('order_by', '-rating')
        if not ordering in ["-rating", "rating", "-date_uploaded", "date_uploaded"]:
            ordering = "-rating"
        ordering = [ordering, "-id"]
        kwargs["default_ordering"] = ordering
        return kwargs

    def form_valid(self, form):
        form_valid = super().form_valid(form)

        sort_group_id = self.get_sort_group_name()
        sort_group_order = form.cleaned_data.get("order_select")
        sort_group_action = form.cleaned_data.get("rate_sort_select")
        sort_group_limit_rating_to_unrated = form.cleaned_data.get("only_rate_unrated_pics")
        sort_group_excluded_ids = []

        try:
            sorting_sets = self.request.session["sorting_sets"]
        except:
            sorting_sets= {}

        sorting_set = {"order":sort_group_order, "action": sort_group_action, "limit_rating_to_unrated":sort_group_limit_rating_to_unrated, "excluded_ids":sort_group_excluded_ids}

        sorting_sets[sort_group_id] = sorting_set

        self.request.session["sorting_sets"] = sorting_sets

        return form_valid


class UnsortedRateSortIntroView(RateSortIntroBaseView):
    template_name = "unsorted_organise.html"
    success_url=reverse_lazy("main:unsorted_organise_active")

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user = self.request.user
        unsorted_pictures = Picture.objects.filter(user=user, albums=None)
        if unsorted_pictures.count() == 0:
            raise Http404
        return context

    def get_sort_group_name(self):
        return "unsorted"


class AlbumRateSortIntroView(RateSortIntroBaseView):
    template_name = "album_organise.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        album_id=self.kwargs['pk']
        album = Album.objects.filter(id=album_id).first()
        if album.author != self.request.user:
            raise Http404
        if album.pictures.count() == 0:
            raise Http404
        context["album"] = album
        return context

    def get_success_url(self):
        album_id=self.kwargs['pk']
        return reverse_lazy('main:album_organise_active', kwargs={'pk': album_id})

    def get_sort_group_name(self):
        return self.kwargs['pk']


class RateSortActiveViewBase(FormView):
    form_class = RateAndSortActiveForm
    template_name = "organise_active.html"

    def get(self, request, *args, **kwargs):
        if self.get_object() == None:
            return redirect(reverse('main:albums'))
        get = super().get(request, *args, **kwargs)
        return get

    def get_context_data(self, **kwargs):
        sort_group_name = self.get_sort_group_name()
        context = super().get_context_data(**kwargs)
        try:
            ruleset = self.request.session["sorting_sets"][str(sort_group_name)]
        except:
            raise Http404
        picture = self.get_object()
        
        action = ruleset["action"]
        limit_rating_to_unrated = ruleset["limit_rating_to_unrated"]

        if action == "rate_only" or action == "both":
            show_rating = True
            if limit_rating_to_unrated and picture.rating != None:
                show_rating = False
        else:
            show_rating = False

        if action == "sort_only" or action == "both":
            show_sort = True
        else:
            show_sort = False

        possible_albums = picture.suggested_albums.all()
        current_albums = picture.albums.all()
        suggested_albums = (possible_albums | current_albums).distinct()

        other_albums = Album.objects.all().exclude(id__in=suggested_albums)

        suggested_albums=suggested_albums.order_by(Lower("name"))
        other_albums=other_albums.order_by(Lower("name"))

        

        context["picture"] = picture
        context["show_rating"] = show_rating
        context["show_sort"] = show_sort
        context["albums_main"] = suggested_albums
        context["albums_other"] = other_albums
        return context

    def get_object(self):
        sort_group_name = self.get_sort_group_name()
        try:
            ruleset = self.request.session["sorting_sets"][str(sort_group_name)]
        except:
            raise Http404
        
        order = ruleset["order"]
        action = ruleset["action"]
        limit_rating_to_unrated = ruleset["limit_rating_to_unrated"]
        excluded_ids = ruleset["excluded_ids"]
        if action == "rate_only" and limit_rating_to_unrated == True:
            exclude_rated = True
        else:
            exclude_rated = False
        
        picture_set = self.base_picture_set()
        
        picture_set = picture_set.exclude(id__in=excluded_ids)
        if exclude_rated:
            picture_set = picture_set.filter(rating=None)
        picture_set = picture_set.order_by(order, "-id")
        if picture_set.count() == 0:
            return None
        picture=picture_set.first()
        return picture

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['instance'] = self.get_object()
        return kwargs

    def form_valid(self, form):
        sort_group_name = self.get_sort_group_name()
        form_valid = super().form_valid(form)
        picture = Picture.objects.filter(id=form.cleaned_data.get("id")).first()
        user = self.request.user
        if picture.user_id != user.id:
            form.add_error("id", "This picture belongs to someone else, you cannot edit it.")
            return super().form_invalid(form)
        rating = form.cleaned_data.get("rating")
        albums = form.cleaned_data.get("albums")
        picture.rating = rating
        picture.albums.set(albums)
        if len(albums)!=0:
            picture.suggested_albums.clear()
        picture.save()
        sorting_sets = self.request.session["sorting_sets"]
        sorting_set = sorting_sets[str(sort_group_name)]

        excluded_ids = sorting_set["excluded_ids"] 
        excluded_ids.append(form.cleaned_data.get("id"))
        
        sorting_set["excluded_ids"] = excluded_ids
        
        sorting_sets[str(sort_group_name)] = sorting_set

        self.request.session["sorting_sets"] = sorting_sets

        return form_valid


class AlbumRateSortActiveView(RateSortActiveViewBase):
    def base_picture_set(self):
        album_id=self.kwargs['pk']
        album = Album.objects.filter(id=album_id).first()
        return album.pictures


    def get_success_url(self):
        album_id = self.kwargs['pk']
        return reverse_lazy("main:album_organise_active", kwargs={'pk': album_id})
        

    def get_sort_group_name(self):
        return self.kwargs['pk']


class UnsortedRateSortActiveView(RateSortActiveViewBase):
    success_url = reverse_lazy("main:unsorted_organise_active")

    def base_picture_set(self):
        return Picture.objects.filter(albums=None)

    def get_sort_group_name(self):
        return "unsorted"


class AboutView(TemplateView):
    template_name = "about.html"
