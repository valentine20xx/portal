from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader, RequestContext
from django.views.generic import View


class Login(View):
    template_name = "authorization/login.html"

    def get(self, request, *args, **kwargs):
        template = loader.get_template(self.template_name)
        context = RequestContext(request, {"auth_error": False})

        return HttpResponse(template.render(context))

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(request.GET.get("next", ""))

        template = loader.get_template(self.template_name)
        context = RequestContext(request, {"auth_error": True})

        return HttpResponse(template.render(context))


class Logout(View):
    template_name = "authorization/logout.html"

    def get(self, request, *args, **kwargs):
        logout(request)
        template = loader.get_template(self.template_name)
        context = RequestContext(request, {})

        return HttpResponse(template.render(context))