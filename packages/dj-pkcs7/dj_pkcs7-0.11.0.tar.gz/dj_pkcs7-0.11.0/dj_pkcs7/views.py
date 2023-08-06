# Create your views here.
from django.shortcuts import render
from django.views.generic import TemplateView, FormView

from .forms import UploadFileForm
from .utils import parse_mail


class MainPageView(TemplateView):
    """MainPage"""

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        template_name = "dj_pkcs7/index.html"
        return render(request, template_name, context)


class FileFieldView(FormView):
    form_class = UploadFileForm
    template_name = 'dj_pkcs7/upload.html'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            context = self.get_context_data(**kwargs)  # prepare context data (kwargs from URL)
            files = request.FILES.getlist('file')

            result = parse_mail(files[0].file.read(), name=files[0].name)
            context.update({"file": files[0].name, "result": result})

            return render(request, 'dj_pkcs7/result.html', context)

        else:
            return self.form_invalid(form)
