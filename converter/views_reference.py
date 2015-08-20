from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from limited_paginator.limitpaging import LimitedPaginator
from .forms import ReferenceForm
from .models import Reference, SystemSource
from .utils import LoginRequiredMixin


class ReferenceObject:
    def get_object(self):
        ss = SystemSource.objects.get(code=self.kwargs["sys"])
        return ss.references.get(code=self.kwargs["ref"])


class ReferenceList(ListView):
    template_name = "converter/reference/list.html"
    paginate_by = 5
    paginator_class = LimitedPaginator

    def get_queryset(self):
        ss = SystemSource.objects.get(code=self.kwargs["sys"])
        return ss.references.all()

    def get_context_data(self, **kwargs):
        result = super(ReferenceList, self).get_context_data(**kwargs)
        result.update(self.kwargs)
        return result

    def get_paginate_by(self, queryset):
        return self.request.COOKIES.get("paginate_by", self.paginate_by)

    def get_paginator(self, queryset, per_page, orphans=0,
                      allow_empty_first_page=True, **kwargs):
        y = super(ReferenceList, self).get_paginator(queryset, per_page, orphans,
                                                     allow_empty_first_page, **kwargs)
        return LimitedPaginator(object_list=y.object_list, per_page=y.per_page, amount=5)


class ReferenceCreate(LoginRequiredMixin, CreateView):
    template_name = "converter/reference/form.html"
    model = Reference
    form_class = ReferenceForm

    def get_initial(self):
        master_id = SystemSource.objects.get(code=self.kwargs["sys"]).id
        return {"master_id": master_id, }

    def get_success_url(self):
        messages.success(self.request, "Created")
        return reverse_lazy("ref_list", args=[self.kwargs["sys"]])

    def get_context_data(self, **kwargs):
        result = super(ReferenceCreate, self).get_context_data(**kwargs)
        result["caption"] = "Добавление"
        result.update(self.kwargs)
        return result


class ReferenceDetail(ReferenceObject, DetailView):
    template_name = "converter/reference/detail.html"


class ReferenceUpdate(LoginRequiredMixin, ReferenceObject, UpdateView):
    template_name = "converter/reference/form.html"
    form_class = ReferenceForm

    def get_success_url(self):
        messages.success(self.request, "Updated")
        return reverse_lazy("ref_list", args=[self.kwargs["sys"]])

    def get_context_data(self, **kwargs):
        result = super(ReferenceUpdate, self).get_context_data(**kwargs)
        result["caption"] = "Обновление"
        result.update(self.kwargs)
        return result


class ReferenceDelete(LoginRequiredMixin, ReferenceObject, DeleteView):
    template_name = "converter/reference/confirm_delete.html"

    def get_success_url(self):
        messages.add_message(request=self.request, message="Deleted", level=messages.SUCCESS)
        return reverse_lazy("ref_list", args=[self.kwargs["sys"]])