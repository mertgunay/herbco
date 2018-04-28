from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import (
    FormView,
    CreateView,
    ListView,
    UpdateView,
)
from .models import Distributor
from shop.models import Item
from .forms import RegisterForm, DistributorCreateForm, Distributor

@login_required(redirect_field_name='/users/login')
def confirm_distributor(request):
    if request.method == 'POST':
        list_of_input_ids=request.POST.getlist('inputs')
        for dist_id in list_of_input_ids:
            distributor = get_object_or_404(Distributor, pk=dist_id)
            if 'reject_dist' in request.POST:
                distributor.delete()
            elif 'accept_dist' in request.POST:
                distributor.is_approveled = True
                distributor.user.user_type = '3'
                distributor.save()
                distributor.user.save()
    return HttpResponseRedirect('/users/distributors/pending/')

class UserLoginView(LoginView):
    template_name = 'profiles/login.html'

class UserCreateView(FormView):
    form_class = RegisterForm
    template_name = 'profiles/register.html'
    success_url = '/users/login'

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Successfully, You can login now.')
        return super(UserCreateView, self).form_valid(form)

class DistributorCreateView(LoginRequiredMixin, CreateView):
    form_class = DistributorCreateForm
    template_name = 'profiles/distributor_create.html'
    success_url = '/'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        return super(DistributorCreateView, self).form_valid(form)

class DistributorPendingListView(LoginRequiredMixin, ListView):
    template_name = 'profiles/distributor_pending.html'
    queryset = Distributor.objects.filter(is_approveled=False)
    context_object_name = 'distributors'

    def get_context_data(self, *args, **kwargs):
        context = super(DistributorPendingListView, self).get_context_data(*args ,**kwargs)
        context['dist_count'] = Distributor.objects.filter(is_approveled=False).count()
        return context

class DistributorItemsListView(LoginRequiredMixin, ListView):
    template_name ="profiles/distributor_items.html"
    context_object_name = 'items'

    def get_queryset(self):
        if self.request.user.user_type == '3':
            queryset = self.request.user.distributor_set.first().item_set.all().filter(is_deleted=False)
        else:
            queryset = None
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(DistributorItemsListView, self).get_context_data(*args ,**kwargs)
        context['deleted_items'] = self.request.user.distributor_set.first().item_set.all().filter(is_deleted=True)
        return context
