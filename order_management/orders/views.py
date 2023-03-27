from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import Orders
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView,DeleteView



def home(request):
    orders = get_object_or_404(Orders, id=request.POST.get('id'))
    is_favourite = False
    if orders.favourite.filter(id):
        is_favourite =True

    context ={
        'orders': Orders.objects.all()
    }
    return render(request, 'orders/home.html', context)

class OrdersListView(ListView):
    model = Orders
    template_name = 'orders/home.html'
    context_object_name = 'orders'
    ordering = ['-date_posted']

class OrdersDetailView(DetailView):
    model = Orders


class OrdersCreateView(LoginRequiredMixin, CreateView):
    model = Orders
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.orderer = self.request.user
        return super().form_valid(form)

class OrdersUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Orders
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.orderer = self.request.user
        return super().form_valid(form)

    def test_func(self):
        order = self.get_object()
        if self.request.user == order.orderer:
            return True
        return False

def favourite_list(request):
   # user = request.user
    new = Orders.objects.filter(favourites=request.user)
    return render(request,'orders/favourite_list.html',{'new':new})

@login_required
def favourite_add(request, id):
    orders = get_object_or_404(Orders, id=id)
    if orders.favourites.filter(id=request.user.id).exists():
        orders.favourites.remove(request.user)
    else:
        orders.favourites.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

class OrdersDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Orders
    success_url = '/'

    def test_func(self):
        order = self.get_object()
        if self.request.user == order.orderer:
            return True
        return False

def about(request):
    return render(request, 'orders/home.html')
