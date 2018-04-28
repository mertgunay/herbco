from django.conf.urls import url
from django.contrib.auth.views import LoginView ,LogoutView

from profiles.views import (
    UserLoginView,
    UserCreateView,
    DistributorCreateView,
    DistributorPendingListView,
    confirm_distributor, # FBV
    DistributorItemsListView,
)
urlpatterns = [
    url(r'^login/$', UserLoginView.as_view(redirect_authenticated_user=True), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^register/$', UserCreateView.as_view(), name='register'),
    url(r'^distributors/create/$', DistributorCreateView.as_view(), name='distributor_create'),
    url(r'^distributors/pending/$', DistributorPendingListView.as_view(), name='distributors'),
    url(r'^distributors/pending/confirm/$', confirm_distributor, name='distributor_confirm'),
    url(r'^distributors/my-items/$', DistributorItemsListView.as_view(), name='distributor_items'),

]
