from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, FormView
from limited_paginator.limitpaging import LimitedPaginator
from .forms import SystemSourceForm, SystemSourceFilterForm, SystemSourceUploadForm, SystemSourceDownloadForm
from .models import SystemSource
from .utils import LoginRequiredMixin, ss_handle_uploaded_file


# logger = logging.getLogger(__name__)


class ActionMixin:
    @property
    def action(self):
        msg = "{0} is missing action.".format(self.__class__)
        raise NotImplementedError(msg)

    def form_valid(self, form):
        msg = "System {0}!".format(self.action)
        messages.success(self.request, msg)
        return super(ActionMixin, self).form_valid(form)


class SystemSourceObject:
    def get_object(self, queryset=None):
        return SystemSource.objects.get(code=self.kwargs["sys"])


class SystemSourceList(ListView):
    paginate_by = 5
    template_name = "converter/systemsource/list.html"
    paginator_class = LimitedPaginator

    def get_queryset(self):
        return SystemSource.objects.all()

    def get_paginate_by(self, queryset):
        return self.request.COOKIES.get("paginate_by", self.paginate_by)

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            data = {
                "data": "test_string",
            }
            return JsonResponse(data)
        else:
            return super(SystemSourceList, self).get(request, *args, **kwargs)


class SystemSourceCreate(LoginRequiredMixin, ActionMixin, CreateView):
    model = SystemSource
    form_class = SystemSourceForm
    template_name = "converter/systemsource/form.html"
    action = "created"

    def get_success_url(self):
        return reverse_lazy("ss_list")

    def get_context_data(self, **kwargs):
        result = super(SystemSourceCreate, self).get_context_data(**kwargs)
        result["caption"] = "Добавление"
        return result


class SystemSourceUpdate(LoginRequiredMixin, SystemSourceObject, ActionMixin, UpdateView):
    form_class = SystemSourceForm
    template_name = "converter/systemsource/form.html"
    action = "updated"

    def get_success_url(self):
        return reverse_lazy("ss_list")

    def get_context_data(self, **kwargs):
        result = super(SystemSourceUpdate, self).get_context_data(**kwargs)
        result["caption"] = "Обновление"
        return result


class SystemSourceDelete(LoginRequiredMixin, SystemSourceObject, DeleteView):
    template_name = "converter/systemsource/confirm_delete.html"

    def get_success_url(self):
        messages.success(self.request, "deleted")
        return reverse_lazy("ss_list")


class SystemSourceDetail(SystemSourceObject, DetailView):
    template_name = "converter/systemsource/detail.html"


class SystemSourceUpload(LoginRequiredMixin, FormView):
    form_class = SystemSourceUploadForm
    template_name = "converter/systemsource/upload.html"

    def post(self, request, *args, **kwargs):
        ss_handle_uploaded_file(request.FILES['file'])
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, "uploaded")
        return reverse_lazy("ss_list")

    def form_invalid(self, form):
        print("invalid")

class SystemSourceDownload(LoginRequiredMixin, FormView):
    form_class = SystemSourceDownloadForm
    template_name = "converter/systemsource/download.html"
    # success_url = reverse_lazy("ss_list")
    #
    # def post(self, request, *args, **kwargs):
    # ss_handle_uploaded_file(request.FILES['file'])
    # return super().post(request, *args, **kwargs)


class SystemSourceFilter(FormView):
    form_class = SystemSourceFilterForm
    template_name = "converter/systemsource/filter.html"
    success_url = reverse_lazy("ss_list")

    def get(self, request, *args, **kwargs):
        self.form_class.base_fields["code"].widget.attrs["value"] = request.session.get("ss_filter_code", "")
        self.form_class.base_fields["fullname"].widget.attrs["value"] = request.session.get("ss_filter_fullname", "")
        return super(SystemSourceFilter, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        request.session["ss_filter_code"] = request.POST.get("code", "")
        request.session["ss_filter_fullname"] = request.POST.get("fullname", "")
        return super(SystemSourceFilter, self).post(request, *args, **kwargs)
