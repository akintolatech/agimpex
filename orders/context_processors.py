from .forms import OrderCreateForm


def order_form(request):
    return {'form': OrderCreateForm}
