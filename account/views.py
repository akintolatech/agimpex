from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy

from .models import Profile

from .forms import (
    UserRegistrationForm,
    UserEditForm,
    ProfileEditForm
)




class CustomLoginView(LoginView):
    template_name = 'registration/login.html'  # your custom login page

    def get_success_url(self):
        user = self.request.user

        # Staff users go to admin/administration page
        if user.is_staff:
            return reverse_lazy('administration:administration')  # change to your admin page name

        # Normal users go to normal dashboard
        return reverse_lazy('website:index')


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password in hash
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create the user profile
            Profile.objects.create(user=new_user)
            return render(
                request,
                'account/register_done.html',
                {'new_user': new_user},
            )
    else:
        user_form = UserRegistrationForm()
    return render(
        request,
        'account/register.html',
        {'user_form': user_form}
    )


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(
            instance=request.user,
            data=request.POST
        )
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES,
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(
        request,
        'account/edit.html',
        {
            'user_form': user_form,
            'profile_form': profile_form
        },
    )


@login_required()
def dashboard(request):
    context = {
        "msg": "Wired"
    }
    return render(
        request,
        'account/dashboard.html',
        context,
    )