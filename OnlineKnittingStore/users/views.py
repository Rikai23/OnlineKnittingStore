from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, TemplateView

from carts.models import Cart
from orders.models import OrderItem, Order
from users.forms import ProfileForm, UserLoginForm, UserRegistrationForm
from users.mixins import CacheMixin


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        return context

    def form_valid(self, form):
        session_key = self.request.session.session_key
        response = super().form_valid(form)

        if session_key:
            Cart.objects.filter(
                session_key=session_key,
                user__isnull=True
            ).update(user=self.request.user)

        return response

@login_required
def logout(request):
    auth.logout(request)
    return redirect(reverse('main:index'))

class UserRegistrationView(CreateView):
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('users:profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context

    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.instance

        if user:
            form.save()
            auth.login(self.request, user)

            if session_key:
                Cart.objects.filter(session_key=session_key).update(user=user)

        return HttpResponseRedirect(self.success_url)


class UserProfileView(CacheMixin, LoginRequiredMixin, UpdateView):
    template_name = 'users/profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Личный кабинет'
        orders = (
            Order.objects.filter(user=self.request.user).prefetch_related(
                Prefetch(
                    'orderitem_set',
                    queryset=OrderItem.objects.select_related('product')
                )
            )
            .order_by('-id')
        )
        context['orders'] = self.set_get_cache(orders, f"user_{self.request.user.id}_orders", 60)
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_staff or request.user.is_superuser:
            return redirect('/super-secret-admin/')
        return super().dispatch(request, *args, **kwargs)



class UserCartView(TemplateView):
    template_name = 'users/users_cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Корзина'
        return context


