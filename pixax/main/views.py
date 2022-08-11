from django.shortcuts import redirect
from django.views.generic import RedirectView


class RootRedirectView(RedirectView):
    permanent = True
    query_string = False
    pattern_name = 'users:register'

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return super().get_redirect_url(*args, **kwargs)            
        else:
            return redirect('users:register')