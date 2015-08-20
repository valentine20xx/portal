from django.forms import TextInput


class BsInput(TextInput):
    # def __init__(self, attrs={}):
    #     # attrs.setdefault("class", "")
    #     attrs["class"] = "form-control"
    #     attrs["autocomplete"] = "off"
    #
    #     super(BsInput,` self).__init__(attrs)

    def render(self, name, value, attrs={}):
        attrs["class"] = "form-control"
        attrs["autocomplete"] = "off"
        return super(BsInput, self).render(name, value, attrs)
        # class Media:
        # css = {
        #         "all": ("css/custom.css", "css/custom3.css",),
        #     }