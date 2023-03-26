from django.shortcuts import render
from .models import Orders
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView,DeleteView



def home(request):
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