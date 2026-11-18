from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import CustomeUserCreationForm, ProfileUpdateForm
from .models import CustomUser


class SignUpView(CreateView):
    form_class = CustomeUserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")


class ProfileUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    UpdateView
):
    model = CustomUser
    form_class = ProfileUpdateForm
    template_name = "accounts/profile.html"
    success_url = reverse_lazy("profile")

    def test_func(self):
        return self.request.user.role == CustomUser.Role.RESIDENT

    def get_object(self, queryset=None):
        return self.request.user