from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.db.models.deletion import ProtectedError

from .models import (
    BusinessType,
    Country,
    State,
    District,
    Area,
    EventName,
)

from .forms import (
    BusinessTypeForm,
    CountryForm,
    StateForm,
    DistrictForm,
    AreaForm,
    EventNameForm,
)

from core.views import is_admin_user


# =========================================================
# BUSINESS TYPE
# =========================================================

@login_required
def business_type_list(request):

    if not is_admin_user(request.user):
        return redirect(
            "owner_login"
        )

    search = request.GET.get(
        "search",
        ""
    ).strip()

    business_types = BusinessType.objects.all()

    if search:

        business_types = business_types.filter(
            name__icontains=search
        )

    business_types = business_types.order_by(
        "-created_at"
    )

    paginator = Paginator(
        business_types,
        10
    )

    page_obj = paginator.get_page(
        request.GET.get("page")
    )

    return render(
        request,
        "magic_pro/business_type_list.html",
        {
            "page_obj": page_obj,
            "search": search,
        }
    )


# =========================================================
# CREATE BUSINESS TYPE
# =========================================================

@login_required
def business_type_create(request):

    if not is_admin_user(request.user):
        return redirect(
            "owner_login"
        )

    if request.method == "POST":

        form = BusinessTypeForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Business Type created successfully."
            )

            return redirect(
                "business_type_list"
            )

    else:

        form = BusinessTypeForm()

    return render(
        request,
        "magic_pro/business_type_form.html",
        {
            "title": "Add Business Type",
            "form": form,
            "edit_mode": False,
        }
    )


# =========================================================
# EDIT BUSINESS TYPE
# =========================================================

@login_required
def business_type_edit(request, pk):

    if not is_admin_user(request.user):
        return redirect(
            "owner_login"
        )

    business_type = get_object_or_404(
        BusinessType,
        pk=pk
    )

    if request.method == "POST":

        form = BusinessTypeForm(
            request.POST,
            instance=business_type
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Business Type updated successfully."
            )

            return redirect(
                "business_type_list"
            )

    else:

        form = BusinessTypeForm(
            instance=business_type
        )

    return render(
        request,
        "magic_pro/business_type_form.html",
        {
            "title": "Edit Business Type",
            "form": form,
            "business_type": business_type,
            "edit_mode": True,
        }
    )


# =========================================================
# DELETE BUSINESS TYPE
# =========================================================

@login_required
def business_type_delete(request, pk):

    if not is_admin_user(request.user):
        return redirect(
            "owner_login"
        )

    business_type = get_object_or_404(
        BusinessType,
        pk=pk
    )

    business_type.delete()

    messages.success(
        request,
        "Business Type deleted successfully."
    )

    return redirect(
        "business_type_list"
    )


# =========================================================
# COUNTRY
# =========================================================
# =========================================================
# COUNTRY
# =========================================================

@login_required
def country_list(request):

    if not is_admin_user(request.user):
        return redirect(
            "owner_login"
        )

    search = request.GET.get(
        "search",
        ""
    ).strip()

    countries = Country.objects.all()

    if search:

        countries = countries.filter(
            Q(name__icontains=search) |
            Q(currency_code__icontains=search) |
            Q(emblem__icontains=search) |
            Q(dial_code__icontains=search)
        )

    countries = countries.order_by(
        "name"
    )

    paginator = Paginator(
        countries,
        10
    )

    page_obj = paginator.get_page(
        request.GET.get("page")
    )

    return render(
        request,
        "magic_pro/country/country_list.html",
        {
            "page_obj": page_obj,
            "search": search,
        }
    )


# =========================================================
# CREATE COUNTRY
# =========================================================

@login_required
def country_create(request):

    if not is_admin_user(request.user):
        return redirect(
            "owner_login"
        )

    if request.method == "POST":

        form = CountryForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Country created successfully."
            )

            return redirect(
                "country_list"
            )

    else:

        form = CountryForm()

    return render(
        request,
        "magic_pro/country/country_form.html",
        {
            "form": form,
            "title": "Add Country",
        }
    )


# =========================================================
# EDIT COUNTRY
# =========================================================

@login_required
def country_edit(request, pk):

    if not is_admin_user(request.user):
        return redirect(
            "owner_login"
        )

    country = get_object_or_404(
        Country,
        pk=pk
    )

    if request.method == "POST":

        form = CountryForm(
            request.POST,
            instance=country
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Country updated successfully."
            )

            return redirect(
                "country_list"
            )

    else:

        form = CountryForm(
            instance=country
        )

    return render(
        request,
        "magic_pro/country/country_form.html",
        {
            "form": form,
            "title": "Edit Country",
            "country": country,
        }
    )


# =========================================================
# DELETE COUNTRY
# =========================================================

@login_required
def country_delete(request, pk):

    if not is_admin_user(request.user):
        return redirect(
            "owner_login"
        )

    country = get_object_or_404(
        Country,
        pk=pk
    )

    country.delete()

    messages.success(
        request,
        "Country deleted successfully."
    )

    return redirect(
        "country_list"
    )


# =========================================================
# STATE
# =========================================================

@login_required
def state_list(request):

    if not is_admin_user(request.user):
        return redirect(
            "owner_login"
        )

    search = request.GET.get(
        "search",
        ""
    ).strip()

    states = State.objects.select_related(
        "country"
    ).all()

    if search:

        states = states.filter(
            Q(name__icontains=search) |
            Q(country__name__icontains=search)
        )

    states = states.order_by(
        "name"
    )

    paginator = Paginator(
        states,
        10
    )

    page_obj = paginator.get_page(
        request.GET.get("page")
    )

    return render(
        request,
        "magic_pro/state/state_list.html",
        {
            "page_obj": page_obj,
            "search": search,
        }
    )


# =========================================================
# CREATE STATE
# =========================================================

@login_required
def state_create(request):

    if not is_admin_user(request.user):
        return redirect(
            "owner_login"
        )

    if request.method == "POST":

        form = StateForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "State created successfully."
            )

            return redirect(
                "state_list"
            )

    else:

        form = StateForm()

    return render(
        request,
        "magic_pro/state/state_form.html",
        {
            "form": form,
            "title": "Add State",
        }
    )


# =========================================================
# EDIT STATE
# =========================================================

@login_required
def state_edit(request, pk):

    if not is_admin_user(request.user):
        return redirect(
            "owner_login"
        )

    state = get_object_or_404(
        State,
        pk=pk
    )

    if request.method == "POST":

        form = StateForm(
            request.POST,
            instance=state
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "State updated successfully."
            )

            return redirect(
                "state_list"
            )

    else:

        form = StateForm(
            instance=state
        )

    return render(
        request,
        "magic_pro/state/state_form.html",
        {
            "form": form,
            "title": "Edit State",
            "state": state,
        }
    )


# =========================================================
# DELETE STATE
# =========================================================

@login_required
def state_delete(request, pk):

    if not is_admin_user(request.user):
        return redirect(
            "owner_login"
        )

    state = get_object_or_404(
        State,
        pk=pk
    )

    state.delete()

    messages.success(
        request,
        "State deleted successfully."
    )

    return redirect(
        "state_list"
    )


# =========================================================
# DISTRICT
# =========================================================

@login_required
def district_list(request):

    if not is_admin_user(request.user):
        return redirect(
            "owner_login"
        )

    search = request.GET.get(
        "search",
        ""
    ).strip()

    districts = District.objects.select_related(
        "state",
        "state__country"
    ).all()

    if search:

        districts = districts.filter(
            Q(name__icontains=search) |
            Q(state__name__icontains=search) |
            Q(state__country__name__icontains=search)
        )

    districts = districts.order_by(
        "name"
    )

    paginator = Paginator(
        districts,
        10
    )

    page_obj = paginator.get_page(
        request.GET.get("page")
    )

    return render(
        request,
        "magic_pro/district/district_list.html",
        {
            "page_obj": page_obj,
            "search": search,
        }
    )


# =========================================================
# CREATE DISTRICT
# =========================================================

@login_required
def district_create(request):

    if not is_admin_user(request.user):
        return redirect(
            "owner_login"
        )

    if request.method == "POST":

        form = DistrictForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "District created successfully."
            )

            return redirect(
                "district_list"
            )

    else:

        form = DistrictForm()

    return render(
        request,
        "magic_pro/district/district_form.html",
        {
            "form": form,
            "title": "Add District",
        }
    )


# =========================================================
# EDIT DISTRICT
# =========================================================

@login_required
def district_edit(request, pk):

    if not is_admin_user(request.user):
        return redirect(
            "owner_login"
        )

    district = get_object_or_404(
        District,
        pk=pk
    )

    if request.method == "POST":

        form = DistrictForm(
            request.POST,
            instance=district
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "District updated successfully."
            )

            return redirect(
                "district_list"
            )

    else:

        form = DistrictForm(
            instance=district
        )

    return render(
        request,
        "magic_pro/district/district_form.html",
        {
            "form": form,
            "title": "Edit District",
            "district": district,
        }
    )


# =========================================================
# DELETE DISTRICT
# =========================================================

@login_required
def district_delete(request, pk):

    if not is_admin_user(request.user):
        return redirect(
            "owner_login"
        )

    district = get_object_or_404(
        District,
        pk=pk
    )

    district.delete()

    messages.success(
        request,
        "District deleted successfully."
    )

    return redirect(
        "district_list"
    )


# =========================================================
# AREA
# =========================================================

@login_required
def area_list(request):

    if not is_admin_user(request.user):
        return redirect(
            "owner_login"
        )

    search = request.GET.get(
        "search",
        ""
    ).strip()

    areas = Area.objects.select_related(
        "district",
        "district__state",
        "district__state__country"
    ).all()

    if search:

        areas = areas.filter(
            Q(name__icontains=search) |
            Q(district__name__icontains=search) |
            Q(district__state__name__icontains=search) |
            Q(
                district__state__country__name__icontains=search
            )
        )

    areas = areas.order_by(
        "name"
    )

    paginator = Paginator(
        areas,
        10
    )

    page_obj = paginator.get_page(
        request.GET.get("page")
    )

    return render(
        request,
        "magic_pro/area/area_list.html",
        {
            "page_obj": page_obj,
            "search": search,
        }
    )


# =========================================================
# CREATE AREA
# =========================================================

@login_required
def area_create(request):

    if not is_admin_user(request.user):
        return redirect(
            "owner_login"
        )

    if request.method == "POST":

        form = AreaForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Area created successfully."
            )

            return redirect(
                "area_list"
            )

    else:

        form = AreaForm()

    return render(
        request,
        "magic_pro/area/area_form.html",
        {
            "form": form,
            "title": "Add Area",
        }
    )


# =========================================================
# EDIT AREA
# =========================================================

@login_required
def area_edit(request, pk):

    if not is_admin_user(request.user):
        return redirect(
            "owner_login"
        )

    area = get_object_or_404(
        Area,
        pk=pk
    )

    if request.method == "POST":

        form = AreaForm(
            request.POST,
            instance=area
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Area updated successfully."
            )

            return redirect(
                "area_list"
            )

    else:

        form = AreaForm(
            instance=area
        )

    return render(
        request,
        "magic_pro/area/area_form.html",
        {
            "form": form,
            "title": "Edit Area",
            "area": area,
        }
    )


# =========================================================
# DELETE AREA
# =========================================================

@login_required
def area_delete(request, pk):

    if not is_admin_user(request.user):
        return redirect(
            "owner_login"
        )

    area = get_object_or_404(
        Area,
        pk=pk
    )

    area.delete()

    messages.success(
        request,
        "Area deleted successfully."
    )

    return redirect(
        "area_list"
    )


# =========================================================
# EVENT NAME MASTER
# =========================================================

@login_required
def event_name_list(request):

    if not is_admin_user(request.user):
        return redirect(
            "owner_login"
        )

    event_names = EventName.objects.all().order_by(
        "name"
    )

    return render(
        request,
        "magic_pro/event_names/event_name_list.html",
        {
            "event_names": event_names,
        }
    )


# =========================================================
# CREATE EVENT NAME
# =========================================================

@login_required
def event_name_create(request):

    if not is_admin_user(request.user):
        return redirect(
            "owner_login"
        )

    if request.method == "POST":

        form = EventNameForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Event Name added successfully."
            )

            return redirect(
                "event_name_list"
            )

    else:

        form = EventNameForm()

    return render(
        request,
        "magic_pro/event_names/event_name_form.html",
        {
            "form": form,
            "title": "Add Event Name",
            "edit_mode": False,
        }
    )


# =========================================================
# EDIT EVENT NAME
# =========================================================

@login_required
def event_name_edit(request, pk):

    if not is_admin_user(request.user):
        return redirect(
            "owner_login"
        )

    event_name = get_object_or_404(
        EventName,
        pk=pk
    )

    if request.method == "POST":

        form = EventNameForm(
            request.POST,
            instance=event_name
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Event Name updated successfully."
            )

            return redirect(
                "event_name_list"
            )

    else:

        form = EventNameForm(
            instance=event_name
        )

    return render(
        request,
        "magic_pro/event_names/event_name_form.html",
        {
            "form": form,
            "event_name": event_name,
            "title": "Edit Event Name",
            "edit_mode": True,
        }
    )


# =========================================================
# DELETE EVENT NAME
# =========================================================

@login_required
def event_name_delete(request, pk):

    if not is_admin_user(request.user):
        return redirect(
            "owner_login"
        )

    event_name = get_object_or_404(
        EventName,
        pk=pk
    )

    name = event_name.name

    try:

        event_name.delete()

        messages.success(
            request,
            f"Event Name '{name}' deleted successfully."
        )

    except ProtectedError:

        messages.error(
            request,
            f"'{name}' is already used by customer events and cannot be deleted."
        )

    return redirect(
        "event_name_list"
    )