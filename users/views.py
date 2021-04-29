from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


class RegisterView(View):
    template_name = 'users/register.html'

    def get(self, request: HttpRequest):
        form = UserRegisterForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request: HttpRequest):
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            #username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You\'re ready to log in!')
            return redirect(to='users:login')

        messages.warning(request, 'Form is not valid')
        return render(request, self.template_name, {'form': form})


@login_required
def profile(request: HttpRequest):
    if request.method == 'POST' and request.user.is_authenticated:
        user_form = UserUpdateForm(data=request.POST, instance=request.user)

        profile_form = ProfileUpdateForm(
            data=request.POST,
            files=request.FILES,
            instance=request.user.profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile Updated')
            return redirect(to='users:profile')
    elif request.method == 'GET':
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'users/profile.html', context)
