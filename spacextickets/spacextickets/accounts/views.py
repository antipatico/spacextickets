from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, update_session_auth_hash
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from spacextickets.orders.models import Order
from spacextickets.utils.views import bad_boy
from .forms import *


@login_required
def dashboard(request):
    return orders_list(request)


@login_required
def orders_list(request):
    orders = Order.objects.filter(user=request.user, is_temporary=False)
    return render(request=request, template_name="accounts/dashboard/orders_list.html", context={'orders': orders})


@login_required
def show_travelers(request):
    travelers = Traveler.objects.filter(user=request.user).all()
    return render(request=request, template_name="accounts/dashboard/travelers.html", context={'travelers': travelers})


@login_required
def del_traveler(request, traveler_id):
    traveler = Traveler.objects.get(id=int(traveler_id))
    if traveler.user.id != request.user.id:
        return bad_boy(request)
    traveler.user = None
    traveler.save()
    return render(request=request, template_name="accounts/dashboard/traveler_deleted_success.html")


@login_required
def edit_traveler(request, traveler_id):
    context = dict()
    try:
        t = Traveler.objects.get(id=int(traveler_id))
        if t.user.id != request.user.id:
            return bad_boy(request)
    except (Traveler.DoesNotExist, AttributeError):
        return HttpResponseRedirect(reverse("accounts:travelers"))

    form = TravelerForm()
    if request.method == 'POST':
        form = TravelerForm(request.POST)
        if form.is_valid():
            t.ssn = form.cleaned_data['ssn']
            t.first_name = form.cleaned_data['first_name']
            t.last_name = form.cleaned_data['last_name']
            t.state = form.cleaned_data['state']
            t.birthday = form.cleaned_data['birthday']
            t.phone_num = form.cleaned_data['phone_num']
            t.email = form.cleaned_data['email']
            t.save()
            context['success'] = True

    form.initial = {'ssn': t.ssn, 'first_name': t.first_name, 'last_name': t.last_name, 'state': t.state,
                    'birthday': t.birthday, 'phone_num': t.phone_num, 'email': t.email}
    context['form'] = form
    context['id'] = t.id

    return render(request=request, template_name="accounts/dashboard/edit_traveler.html", context=context)


@login_required()
def edit_user(request):
    context = dict()
    user = request.user

    if request.method == 'POST':
        user = request.user
        form = UserEditForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.gender = form.cleaned_data['gender']
            user.save()
            context['success'] = True

    form = UserEditForm(initial={'first_name': user.first_name, 'last_name': user.last_name, 'gender': user.gender})

    context['form'] = form
    context['user'] = True
    return render(request=request, template_name="accounts/dashboard/edit_user.html", context=context)


@login_required
def password_change(request):
    context = dict()
    form = PasswordChangeForm()
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        user = request.user
        if form.is_valid():
            if user.check_password(form.cleaned_data['password']):
                user.set_password(form.cleaned_data['password_new1'])
                update_session_auth_hash(request, user)
                user.save()
                context['success'] = True
            else:
                context['wrongpswd'] = True

    context['form'] = form
    return render(request=request, template_name="accounts/dashboard/password_change.html", context=context)


def register_user(request):
    context = dict()
    if request.method == 'GET':
        context['next'] = request.GET.get('next', None)
    elif request.method == "POST":
        form = UserCreationForm(request.POST)
        context['form'] = form
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            gender = form.cleaned_data['gender']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            user = User.objects.create_user(email=email, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.gender = gender
            user.save()

            login(request, user)

            next_url = request.POST.get('next', None)
            if next_url:
                return HttpResponseRedirect(next_url)
            context['success'] = True

    return render(request=request, template_name="accounts/register.html", context=context)
