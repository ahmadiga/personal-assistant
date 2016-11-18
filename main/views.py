from django.contrib.auth import REDIRECT_FIELD_NAME, authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters


@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request, template_name='registration/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          current_app=None, extra_context=None):
    """
    Displays the login form and handles the login action.
    """
    if request.user.is_authenticated():
        return redirect(reverse("home"))

    redirect_to = request.GET.get(redirect_field_name, '/')

    form = authentication_form(request, data=request.POST or None)
    if form.is_valid():
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        auth_login(request, form.get_user())
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
        return redirect(redirect_to)

    request.session.set_test_cookie()

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template_name, context,
                  current_app=current_app)


# Create your views here.
def index(request):
    return render(request, 'main/index.html', {})
