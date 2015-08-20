from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, RedirectView, CreateView, DeleteView, UpdateView, DetailView
from converter.utils import LoginRequiredMixin
from .forms import ReferenceKeyValueForm
from .models import SystemSource, ReferenceKeyValue


class ReferenceKeyValueObject:
    def get_object(self, queryset=None):
        ss = SystemSource.objects.get(code=self.kwargs["sys"])
        ref = ss.references.get(code=self.kwargs["ref"])
        ref_key = ref.kvs.get(key=self.kwargs["ref_key"])
        return ref_key


class ReferenceKeyValueList(ListView):
    template_name = "converter/referencekeyvalue/list.html"
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        ss = get_object_or_404(SystemSource, code=self.kwargs["sys"])
        ref = ss.references.get(code=self.kwargs["ref"])
        self.queryset = ref.kvs.all()
        return super(ReferenceKeyValueList, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        result = super(ReferenceKeyValueList, self).get_context_data(**kwargs)
        result.update(self.kwargs)
        return result

    def get_paginate_by(self, queryset):
        return self.request.COOKIES.get("ref_kvp_paginate_by", self.paginate_by)


class ReferenceKeyValueCreate(LoginRequiredMixin, CreateView):
    template_name = "converter/referencekeyvalue/form.html"
    model = ReferenceKeyValue
    form_class = ReferenceKeyValueForm

    def get_initial(self):
        ss = get_object_or_404(SystemSource, code=self.kwargs["sys"])
        ref = ss.references.get(code=self.kwargs["ref"])
        return {"reference_id": ref.id, }

    def get_success_url(self):
        messages.success(self.request, "Created")
        return reverse_lazy("ref_kvp_list", args=[self.kwargs["sys"], self.kwargs["ref"]])

    def get_context_data(self, **kwargs):
        result = super(ReferenceKeyValueCreate, self).get_context_data(**kwargs)
        result["caption"] = "Добавление"
        result.update(self.kwargs)
        return result


class ReferenceKeyValueUpdate(LoginRequiredMixin, ReferenceKeyValueObject, UpdateView):
    template_name = "converter/referencekeyvalue/form.html"
    form_class = ReferenceKeyValueForm

    def get_success_url(self):
        messages.success(self.request, "Updated")
        return reverse_lazy("ref_kvp_list", args=[self.kwargs["sys"], self.kwargs["ref"]])

    def get_context_data(self, **kwargs):
        result = super(ReferenceKeyValueUpdate, self).get_context_data(**kwargs)
        result["caption"] = "Обновление"
        result.update(self.kwargs)
        return result


class ReferenceKeyValueDetail(ReferenceKeyValueObject, DetailView):
    template_name = "converter/referencekeyvalue/detail.html"


class ReferenceKeyValueDelete(LoginRequiredMixin, ReferenceKeyValueObject, DeleteView):
    template_name = "converter/referencekeyvalue/confirm_delete.html"

    def get_success_url(self):
        messages.success(self.request, self.kwargs.pop("ref_key", "") + " deleted")
        return reverse_lazy("ref_kvp_list", kwargs=self.kwargs)