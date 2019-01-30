from django.forms import formset_factory

from spacextickets.accounts.forms import UserCreationForm, TravelerForm
from spacextickets.accounts.models import GuestUser, Traveler, BaseUser
from spacextickets.utils.views import BadBoy


def add_guest(request):
    if request.method != "POST":
        raise BadBoy("Invalid request method in guest creation.")

    form = UserCreationForm(request.POST, guest=True)
    if not form.is_valid():
        raise BadBoy("Invalid form data in guest creation.")

    first_name = form.cleaned_data['first_name']
    last_name = form.cleaned_data['last_name']
    gender = form.cleaned_data['gender']
    email = form.cleaned_data['email']

    user = GuestUser(email=email, first_name=first_name, last_name=last_name, gender=gender)
    user.save()
    return user


def add_travelers(request, user=None):
    travelerformset = formset_factory(TravelerForm)
    travelers = []
    user = user if user else request.user

    if request.method != 'POST':
        raise BadBoy("Invalid request method in travelers creation.")

    formset = travelerformset(request.POST)
    if not formset.is_valid():
        raise BadBoy("Invalid formset data in travelers creation.")

    for f in formset:
        traveler_id = f.cleaned_data['traveler_id']
        if traveler_id:
            t = Traveler.objects.get(id=traveler_id)
            if t.user.id != user.id:
                raise BadBoy("Trying to use a traveler not owned by the user itself.")
        else:
            ssn = f.cleaned_data['ssn']
            first_name = f.cleaned_data['first_name']
            last_name = f.cleaned_data['last_name']
            email = f.cleaned_data['email']
            state = f.cleaned_data['state']
            birthday = f.cleaned_data['birthday']
            phone_num = f.cleaned_data['phone_num']
            user = BaseUser.objects.get(id=user.id)

            t = Traveler(user=user, ssn=ssn, first_name=first_name, last_name=last_name, email=email,
                         state=state, birthday=birthday, phone_num=phone_num)
            t.save()

        travelers.append(t)
    return travelers