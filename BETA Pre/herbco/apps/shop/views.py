from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.views.generic import (
    ListView,
    CreateView,
    FormView,
    DetailView,
    TemplateView,
    UpdateView,
)

from shop.models import Item, ShoppingCart, Category, ItemExtra, Order, Comment
from profiles.models import Distributor
from .forms import ItemCreateForm

def search(request):
    search = request.GET.get("search")
    category_id = request.GET.get("category")
    queryset = None
    if search:
        queryset = Item.objects.filter(is_approvaled=True).filter(is_updated=False).filter(is_deleted=False)
        queryset = queryset.filter(name__icontains=search)
        if not category_id == '0':
            category = get_object_or_404(Category, pk=category_id)
            queryset = queryset.filter(category=category)
        if not queryset:
            messages.warning(request, 'There is no item with these search')
            return HttpResponseRedirect("/")
    else:
        messages.warning(request, 'You have to write something to search !!')
        return HttpResponseRedirect("/")
    context = {
        'items': queryset,
        'categories': Category.objects.all()
    }
    return render(request, 'shop/search.html', context)

@login_required(redirect_field_name='/users/login')
def confirm_item(request):
    if request.method == 'POST':
        list_of_input_ids = request.POST.getlist('inputs')
        for item_id in list_of_input_ids:
            item_id = get_object_or_404(Item, pk=item_id)
            item_id.is_approvaled = True
            item_id.save()
    return HttpResponseRedirect('/items/pending/')

@login_required(redirect_field_name='/users/login')
def confirm_u_item(request):
    if request.method == 'POST':
        list_of_input_ids = request.POST.getlist('inputs')
        for item_id in list_of_input_ids:
            item_id = get_object_or_404(Item, pk=item_id)
            item_id.is_updated = False
            item_id.save()
    return HttpResponseRedirect('/items/updated/')

@login_required(redirect_field_name='/users/login')
def confirm_deleted_item(request):
    if request.method == 'POST':
        list_of_input_ids = request.POST.getlist('inputs')
        for item_id in list_of_input_ids:
            item_id = get_object_or_404(Item, pk=item_id)
            item_id.delete()
    return HttpResponseRedirect('/items/deleted/')

class HomeView(ListView):
    template_name = 'shop/home.html'
    queryset = Item.objects.filter(is_approvaled=True).filter(is_updated=False).filter(is_deleted=False)
    context_object_name = 'items'

    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(*args ,**kwargs)
        queryset_last_5 = Item.objects.filter(is_approvaled=True).filter(is_updated=False).filter(is_deleted=False).order_by('-timestamp')[:5]
        queryset_best_seller = Item.objects.filter(is_approvaled=True).filter(is_updated=False).filter(is_deleted=False).order_by('-sold')[:5]
        context['lastfive'] = queryset_last_5
        context['bestseller'] = queryset_best_seller
        context['dist_count'] = Distributor.objects.filter(is_approveled=False).count()
        context['item_count'] = Item.objects.filter(is_approvaled=False).filter(is_deleted=False).count()
        context['item_u_count'] = Item.objects.filter(is_updated=True).filter(is_deleted=False).count()
        context['item_delete_count'] = Item.objects.filter(is_deleted=True).count()
        context['categories'] = Category.objects.all()
        return context

class ContactUsTemplateView(TemplateView):
    template_name = "shop/contact_us.html"

class ItemCreateView(LoginRequiredMixin, CreateView):
    template_name = 'shop/item_create.html'
    form_class = ItemCreateForm
    success_url = '/'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.owner = self.request.user.distributor_set.first()
        return super(ItemCreateView, self).form_valid(form)

class ItemDetailView(DetailView):
    template_name = "shop/item_detail.html"
    context_object_name = 'item'

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        obj = get_object_or_404(Item, slug=slug)
        return obj

class ItemPendingListView(LoginRequiredMixin, ListView):
    template_name = 'shop/item_pending.html'
    queryset = Item.objects.filter(is_approvaled=False)
    context_object_name = 'items_pend'

    def get_context_data(self, *args, **kwargs):
        context = super(ItemPendingListView, self).get_context_data(*args ,**kwargs)
        context['item_count'] = Item.objects.filter(is_approvaled=False).filter(is_deleted=False).count()
        return context

class ItemDeletedListView(LoginRequiredMixin, ListView):
    template_name = 'shop/item_deleted.html'
    queryset = Item.objects.filter(is_deleted=True)
    context_object_name = 'items_deleted'

class ItemUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'shop/item_update.html'
    model = Item
    fields = [
        'name',
        'stock',
        'price',
    ]

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.is_updated = True
        return super(ItemUpdateView, self).form_valid(form)

class ItemUpdatingListView(LoginRequiredMixin, ListView):
    template_name = 'shop/item_updated.html'
    queryset = Item.objects.filter(is_updated=True).filter(is_deleted=False)
    context_object_name = 'items_updated'

@login_required(redirect_field_name='/users/login')
def item_delete(request, pk=None):
    item = get_object_or_404(Item, pk=pk)
    if request.user.distributor_set.first() == item.owner:
        item.is_deleted = True
        item.save()
        messages.info(request, 'We send a request to delete your item')
    else:
        messages.warning(request, 'You are not owner for this item')
    return HttpResponseRedirect("/users/distributors/my-items/")


@login_required(redirect_field_name='/users/login')
def add_to_cart(request, id=None):
    if not request.user.user_type == '4':
        messages.warning(request, 'You are not customer, so you cannot add to basket any item')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    item = get_object_or_404(Item, pk=id)
    quantity = request.POST.get("q", 1)
    if item.stock == 0:
        messages.warning(request, 'There is no stock for this product')
    else:
        shop_cart = get_object_or_404(ShoppingCart, owner=request.user)
        if item in shop_cart.items.all():
            messages.warning(request, 'This item is already in your basket')
        else:
            shop_cart.items.add(item)
            ItemExtra.objects.get_or_create(itemex=item, shopcart=shop_cart, quantity=quantity)
            if item.related_product:
                r_item = get_object_or_404(Item, pk=item.related_product.pk)
                shop_cart.items.add(r_item)
                ItemExtra.objects.get_or_create(itemex=r_item, shopcart=shop_cart, quantity=quantity)
                messages.success(request, 'Related item add you basket.')
            messages.success(request, 'Item added to your basket.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(redirect_field_name='/users/login')
def delete_from_cart(request, id=None):
    item = get_object_or_404(Item, pk=id)
    shop_cart = get_object_or_404(ShoppingCart, owner=request.user)
    itemex = get_object_or_404(ItemExtra, itemex=item, shopcart=shop_cart)
    itemex.delete()
    shop_cart.items.remove(item)
    return HttpResponseRedirect("/cart")

class ShoppingCartListView(LoginRequiredMixin, ListView):
    template_name = "shop/shopping_cart.html"
    context_object_name = 'cart_items'

    def get_queryset(self):
        cart = ShoppingCart.objects.get(owner=self.request.user)
        queryset = cart.items.filter(is_updated=False).filter(is_deleted=False)
        return queryset

class CategoryListView(ListView):
    template_name = "shop/category.html"
    context_object_name = 'items'

    def get_queryset(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        category = Category.objects.get(slug=slug)
        queryset = Item.objects.filter(category=category).filter(is_deleted=False)
        return queryset

class CheckOut(LoginRequiredMixin, ListView):
    template_name = "shop/checkout.html"
    context_object_name = 'items'

    def get_queryset(self):
        cart = ShoppingCart.objects.get(owner=self.request.user)
        queryset = cart.items.all()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(CheckOut, self).get_context_data(*args ,**kwargs)
        total = 0
        queryset = self.get_queryset()
        for item in queryset:
            total += item.price
        context['total'] = total
        return context

@login_required(redirect_field_name='/users/login')
def checkout_final(request):
    if request.method == 'POST':
        list_of_input_ids = request.POST.getlist('items')
        shop_cart = get_object_or_404(ShoppingCart, owner=request.user)
        order = Order.objects.create(owner=request.user, shop_cart=shop_cart)
        for item_id in list_of_input_ids:
            order_item = get_object_or_404(Item, pk=item_id)
            order_item.stock = order_item.stock - order_item.itemex.quantity
            order_item.sold = order_item.sold + order_item.itemex.quantity
            order_item.save()
            order.order_items.add(order_item)
            #order_item.itemex.delete()
            if order_item.related_product:
                order_item.related_product.stock - order_item.itemex.quantity
                order_item.related_product.sold = order_item.sold + order_item.itemex.quantity
                order_item.related_product.save()
                order.order_items.add(order_item.related_product)
                #order_item.related_product.itemex.delete()
        order.save()
        shop_cart.itemextra_set.all().delete()
        shop_cart.items.clear()
    return render(request, 'shop/checkout_final.html', {})

@login_required(redirect_field_name='/users/login')
def confirm_deleted_item(request):
    if request.method == 'POST':
        list_of_input_ids = request.POST.getlist('inputs')
        for item_id in list_of_input_ids:
            item_id = get_object_or_404(Item, pk=item_id)
            item_id.delete()
    return HttpResponseRedirect('/items/deleted/')

class StaticsListView(LoginRequiredMixin, ListView):
    template_name = "shop/show_statics.html"
    context_object_name = "distributors"

    def get_queryset(self):
        if not self.request.user.user_type == '2':
            messages.warning(self.request, 'You do not have permission for this page')
            return HttpResponseRedirect("/")
        queryset = Distributor.objects.all()
        return queryset

class MyOrdersListView(LoginRequiredMixin, ListView):
    template_name = 'shop/my_orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        queryset = Order.objects.filter(owner=self.request.user)
        return queryset

class FeedBacksListView(LoginRequiredMixin, ListView):
    template_name = 'shop/feedbacks.html'
    queryset = Comment.objects.all()
    context_object_name = 'feedbacks'

@login_required(redirect_field_name='/users/login')
def comment(request):
    print(request.POST)
    user = request.user
    comment = request.POST.get("comment")
    Comment.objects.create(owner=user, comment=comment)
    messages.info(request, 'Message sended.')
    return HttpResponseRedirect("/")

@login_required(redirect_field_name='/users/login')
def update_quantity(request):
    quantity = request.GET.get("quantity")
    item_id = request.GET.get("item")
    item = get_object_or_404(Item, pk=item_id)
    item.itemex.quantity = quantity
    item.itemex.save()
