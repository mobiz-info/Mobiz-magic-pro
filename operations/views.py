from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages

from .models import (
    Client,
    Branch,
    Customer,
    CustomerEvent,
)

from .forms import (
    ClientForm,
    ClientOwnerForm,
    BranchForm,
    CustomerForm,
    BranchCustomerForm,
    CustomerEventForm,
)

from core.views import (
    is_admin_user,
    is_owner_user,
    is_branch_user,
)


# =========================================================
# CLIENT MANAGEMENT
# =========================================================

@login_required
def client_list(request):

    if (
        not is_admin_user(request.user)
        and not is_owner_user(request.user)
    ):
        return redirect("owner_login")

    search = request.GET.get(
        "search",
        ""
    ).strip()

    # -----------------------------------------------------
    # SUPER ADMIN
    # -----------------------------------------------------

    if is_admin_user(request.user):

        clients = Client.objects.select_related(
            "owner",
            "business_type",
            "country",
            "state",
            "district",
            "area",
        ).order_by(
            "-created_at"
        )

    # -----------------------------------------------------
    # OWNER
    # -----------------------------------------------------

    else:

        clients = Client.objects.filter(
            owner=request.user
        ).select_related(
            "owner",
            "business_type",
            "country",
            "state",
            "district",
            "area",
        ).order_by(
            "-created_at"
        )

    if search:

        clients = clients.filter(
            Q(company_name__icontains=search)
            | Q(email__icontains=search)
            | Q(phone__icontains=search)
            | Q(owner__username__icontains=search)
            | Q(owner__first_name__icontains=search)
            | Q(owner__last_name__icontains=search)
        )

    paginator = Paginator(
        clients,
        10
    )

    page_obj = paginator.get_page(
        request.GET.get("page")
    )

    return render(
        request,
        "magic_pro/client/client_list.html",
        {
            "page_obj": page_obj,
            "search": search,
        }
    )


# =========================================================
# OWNER DETAILS
# =========================================================

@login_required
def owner_details(request, pk):

    if (
        not is_admin_user(request.user)
        and not is_owner_user(request.user)
    ):

        messages.error(
            request,
            "You are not authorized to access this page."
        )

        return redirect(
            "owner_dashboard"
        )

    # -----------------------------------------------------
    # SUPER ADMIN
    # -----------------------------------------------------

    if is_admin_user(request.user):

        client = get_object_or_404(
            Client.objects.select_related(
                "owner",
                "country",
            ),
            pk=pk
        )

    # -----------------------------------------------------
    # OWNER
    # -----------------------------------------------------

    else:

        client = get_object_or_404(
            Client.objects.select_related(
                "owner",
                "country",
            ),
            pk=pk,
            owner=request.user
        )

    owner_dial_code = ""

    if client.country:

        owner_dial_code = (
            client.country.dial_code or ""
        )

    return render(
        request,
        "magic_pro/client/owner_details.html",
        {
            "client": client,
            "owner": client.owner,
            "owner_dial_code": owner_dial_code,
        }
    )


# =========================================================
# CREATE CLIENT + OWNER LOGIN
# =========================================================

@login_required
def client_create(request):

    # Only Super Admin can create a new Company
    if not is_admin_user(request.user):

        return redirect(
            "owner_dashboard"
        )

    if request.method == "POST":

        form = ClientOwnerForm(
            request.POST
        )

        if form.is_valid():

            client = form.save()

            messages.success(
                request,
                "Client and login account created successfully."
            )

            return redirect(
                "client_list"
            )

    else:

        form = ClientOwnerForm()

    return render(
        request,
        "magic_pro/client/client_form.html",
        {
            "form": form,
            "title": "Add Client",
            "client": None,
            "owner_dial_code": "",
        }
    )


# =========================================================
# EDIT CLIENT
# =========================================================

@login_required
def client_edit(request, pk):

    if (
        not is_admin_user(request.user)
        and not is_owner_user(request.user)
    ):
        return redirect(
            "owner_login"
        )

    # -----------------------------------------------------
    # SUPER ADMIN
    # -----------------------------------------------------

    if is_admin_user(request.user):

        client = get_object_or_404(
            Client.objects.select_related(
                "owner",
                "country",
            ),
            pk=pk
        )

    # -----------------------------------------------------
    # OWNER
    # -----------------------------------------------------

    else:

        client = get_object_or_404(
            Client.objects.select_related(
                "owner",
                "country",
            ),
            pk=pk,
            owner=request.user
        )

    if request.method == "POST":

        form = ClientOwnerForm(
            request.POST,
            instance=client
        )

        # -------------------------------------------------
        # PASSWORD IS OPTIONAL DURING EDIT
        # -------------------------------------------------

        form.fields[
            "owner_password"
        ].required = False

        form.fields[
            "owner_confirm_password"
        ].required = False

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Client and owner information updated successfully."
            )

            return redirect(
                "client_list"
            )

    else:

        form = ClientOwnerForm(
            instance=client
        )

        # -------------------------------------------------
        # PASSWORD IS OPTIONAL DURING EDIT
        # -------------------------------------------------

        form.fields[
            "owner_password"
        ].required = False

        form.fields[
            "owner_confirm_password"
        ].required = False

        # -------------------------------------------------
        # LOAD EXISTING OWNER DETAILS
        # -------------------------------------------------

        if client.owner:

            form.fields[
                "owner_username"
            ].initial = client.owner.username

            form.fields[
                "owner_first_name"
            ].initial = client.owner.first_name

            form.fields[
                "owner_last_name"
            ].initial = client.owner.last_name

            form.fields[
                "owner_email"
            ].initial = client.owner.email

            form.fields[
                "owner_phone"
            ].initial = client.owner.phone

    # -----------------------------------------------------
    # OWNER COUNTRY DIAL CODE
    # -----------------------------------------------------

    owner_dial_code = ""

    if client.country:

        owner_dial_code = (
            client.country.dial_code or ""
        )

    return render(
        request,
        "magic_pro/client/client_form.html",
        {
            "form": form,
            "title": "Edit Client",
            "client": client,
            "owner_dial_code": owner_dial_code,
        }
    )


# =========================================================
# DELETE CLIENT
# =========================================================

@login_required
def client_delete(request, pk):

    # Only Super Admin can delete a Company
    if not is_admin_user(request.user):

        return redirect(
            "owner_dashboard"
        )

    client = get_object_or_404(
        Client,
        pk=pk
    )

    owner = client.owner

    client.delete()

    if owner:
        owner.delete()

    messages.success(
        request,
        "Client deleted successfully."
    )

    return redirect(
        "client_list"
    )


# =========================================================
# BRANCH MANAGEMENT
# =========================================================

@login_required
def branch_list(request):

    if not is_admin_user(request.user) and not is_owner_user(request.user):

        return redirect(
            "owner_login"
        )

    search = request.GET.get(
        "search",
        ""
    ).strip()

    # -----------------------------------------------------
    # SUPER ADMIN
    # -----------------------------------------------------

    if is_admin_user(request.user):

        branches = Branch.objects.select_related(
            "client",
            "user",
        ).order_by(
            "-created_at"
        )

    # -----------------------------------------------------
    # OWNER
    # -----------------------------------------------------

    else:

        branches = Branch.objects.filter(
            client__owner=request.user
        ).select_related(
            "client",
            "user",
        ).order_by(
            "-created_at"
        )

    if search:

        branches = branches.filter(
            Q(name__icontains=search) |
            Q(phone__icontains=search) |
            Q(email__icontains=search) |
            Q(client__company_name__icontains=search)
        )

    paginator = Paginator(
        branches,
        10
    )

    page_obj = paginator.get_page(
        request.GET.get("page")
    )

    return render(
        request,
        "magic_pro/branch/branch_list.html",
        {
            "page_obj": page_obj,
            "search": search,
        }
    )


# =========================================================
# CREATE BRANCH
# =========================================================

@login_required
def branch_create(request):

    if not is_admin_user(request.user) and not is_owner_user(request.user):

        return redirect(
            "owner_login"
        )

    # -----------------------------------------------------
    # SUPER ADMIN
    # -----------------------------------------------------

    if is_admin_user(request.user):

        if request.method == "POST":

            form = BranchForm(
                request.POST
            )

            if form.is_valid():

                form.save()

                messages.success(
                    request,
                    "Branch created successfully."
                )

                return redirect(
                    "branch_list"
                )

        else:

            form = BranchForm()

    # -----------------------------------------------------
    # OWNER
    # -----------------------------------------------------

    else:

        client = get_object_or_404(
            Client,
            owner=request.user
        )

        if request.method == "POST":

            form = BranchForm(
                request.POST
            )

            # Owner can create a Branch
            # only under his own Company.
            if "client" in form.fields:

                form.fields[
                    "client"
                ].queryset = Client.objects.filter(
                    pk=client.pk
                )

            if form.is_valid():

                branch = form.save(
                    commit=False
                )

                branch.client = client

                branch.save()

                messages.success(
                    request,
                    "Branch created successfully."
                )

                return redirect(
                    "branch_list"
                )

        else:

            form = BranchForm()

            if "client" in form.fields:

                form.fields[
                    "client"
                ].queryset = Client.objects.filter(
                    pk=client.pk
                )

                form.fields[
                    "client"
                ].initial = client.pk

    return render(
        request,
        "magic_pro/branch/branch_form.html",
        {
            "form": form,
            "title": "Add Branch",
        }
    )


# =========================================================
# EDIT BRANCH
# =========================================================

@login_required
def branch_edit(request, pk):

    if not is_admin_user(request.user) and not is_owner_user(request.user):

        return redirect(
            "owner_login"
        )

    # -----------------------------------------------------
    # SUPER ADMIN
    # -----------------------------------------------------

    if is_admin_user(request.user):

        branch = get_object_or_404(
            Branch,
            pk=pk
        )

    # -----------------------------------------------------
    # OWNER
    # -----------------------------------------------------

    else:

        branch = get_object_or_404(
            Branch,
            pk=pk,
            client__owner=request.user
        )

    if request.method == "POST":

        form = BranchForm(
            request.POST,
            instance=branch
        )

        # Owner cannot move Branch
        # to another Company.
        if is_owner_user(request.user):

            client = get_object_or_404(
                Client,
                owner=request.user
            )

            if "client" in form.fields:

                form.fields[
                    "client"
                ].queryset = Client.objects.filter(
                    pk=client.pk
                )

        if form.is_valid():

            updated_branch = form.save(
                commit=False
            )

            if is_owner_user(request.user):

                updated_branch.client = get_object_or_404(
                    Client,
                    owner=request.user
                )

            updated_branch.save()

            messages.success(
                request,
                "Branch updated successfully."
            )

            return redirect(
                "branch_list"
            )

    else:

        form = BranchForm(
            instance=branch
        )

        if is_owner_user(request.user):

            client = get_object_or_404(
                Client,
                owner=request.user
            )

            if "client" in form.fields:

                form.fields[
                    "client"
                ].queryset = Client.objects.filter(
                    pk=client.pk
                )

    return render(
        request,
        "magic_pro/branch/branch_form.html",
        {
            "form": form,
            "title": "Edit Branch",
            "branch": branch,
        }
    )


# =========================================================
# DELETE BRANCH
# =========================================================

@login_required
def branch_delete(request, pk):

    if not is_admin_user(request.user) and not is_owner_user(request.user):

        return redirect(
            "owner_login"
        )

    # -----------------------------------------------------
    # SUPER ADMIN
    # -----------------------------------------------------

    if is_admin_user(request.user):

        branch = get_object_or_404(
            Branch,
            pk=pk
        )

    # -----------------------------------------------------
    # OWNER
    # -----------------------------------------------------

    else:

        branch = get_object_or_404(
            Branch,
            pk=pk,
            client__owner=request.user
        )

    branch.delete()

    messages.success(
        request,
        "Branch deleted successfully."
    )

    return redirect(
        "branch_list"
    )


# =========================================================
# CUSTOMER MANAGEMENT
# =========================================================

@login_required
def customer_list(request):

    if (
        not is_admin_user(request.user)
        and not is_owner_user(request.user)
        and not is_branch_user(request.user)
    ):
        return redirect(
            "owner_login"
        )

    search = request.GET.get(
        "search",
        ""
    ).strip()

    # -----------------------------------------------------
    # BRANCH USER
    # -----------------------------------------------------

    if is_branch_user(request.user):

        branch = request.user.branch_profile

        customers = Customer.objects.filter(
            branch=branch
        ).select_related(
            "branch",
            "branch__client",
        ).order_by(
            "-created_at"
        )

    # -----------------------------------------------------
    # OWNER
    # -----------------------------------------------------

    elif is_owner_user(request.user):

        customers = Customer.objects.filter(
            branch__client__owner=request.user
        ).select_related(
            "branch",
            "branch__client",
        ).order_by(
            "-created_at"
        )

    # -----------------------------------------------------
    # SUPER ADMIN
    # -----------------------------------------------------

    else:

        customers = Customer.objects.select_related(
            "branch",
            "branch__client",
        ).order_by(
            "-created_at"
        )

    if search:

        customers = customers.filter(
            Q(name__icontains=search) |
            Q(phone__icontains=search) |
            Q(branch__name__icontains=search) |
            Q(
                branch__client__company_name__icontains=search
            )
        )

    paginator = Paginator(
        customers,
        10
    )

    page_obj = paginator.get_page(
        request.GET.get("page")
    )

    return render(
        request,
        "magic_pro/customer/customer_list.html",
        {
            "page_obj": page_obj,
            "search": search,
            "is_branch_user": is_branch_user(request.user),
        }
    )


# =========================================================
# CUSTOMER EVENTS LIST
# =========================================================

@login_required
def customer_event_list(request):

    if (
        not is_admin_user(request.user)
        and not is_owner_user(request.user)
        and not is_branch_user(request.user)
    ):
        return redirect(
            "owner_login"
        )

    search = request.GET.get(
        "search",
        ""
    ).strip()

    selected_customer_id = request.GET.get(
        "customer",
        ""
    ).strip()

    # -----------------------------------------------------
    # BRANCH USER
    # -----------------------------------------------------

    if is_branch_user(request.user):

        customers = Customer.objects.filter(
            branch=request.user.branch_profile
        ).select_related(
            "branch",
            "branch__client",
        ).order_by(
            "name"
        )

    # -----------------------------------------------------
    # OWNER
    # -----------------------------------------------------

    elif is_owner_user(request.user):

        customers = Customer.objects.filter(
            branch__client__owner=request.user
        ).select_related(
            "branch",
            "branch__client",
        ).order_by(
            "name"
        )

    # -----------------------------------------------------
    # SUPER ADMIN
    # -----------------------------------------------------

    else:

        customers = Customer.objects.select_related(
            "branch",
            "branch__client",
        ).order_by(
            "name"
        )

    # -----------------------------------------------------
    # SEARCH BY MOBILE NUMBER
    # -----------------------------------------------------

    if search:

        customers = customers.filter(
            phone__icontains=search
        )

    selected_customer = None

    # -----------------------------------------------------
    # SELECTED CUSTOMER
    # -----------------------------------------------------

    if selected_customer_id:

        try:

            selected_customer = customers.get(
                pk=selected_customer_id
            )

        except Customer.DoesNotExist:

            selected_customer = None

    # -----------------------------------------------------
    # AUTO SELECT FIRST MATCH
    # -----------------------------------------------------

    elif search and customers.exists():

        selected_customer = customers.first()

    events = CustomerEvent.objects.none()

    if selected_customer:

        events = CustomerEvent.objects.filter(
            customer=selected_customer
        ).select_related(
            "event_name"
        ).order_by(
            "event_date",
            "-id"
        )

    return render(
        request,
        "magic_pro/customer/customer_event_list.html",
        {
            "customers": customers,
            "search": search,
            "selected_customer": selected_customer,
            "events": events,
            "is_branch_user": is_branch_user(request.user),
        }
    )


# =========================================================
# CREATE CUSTOMER EVENT
# =========================================================


@login_required
def customer_event_create(request):

    if (
        not is_admin_user(request.user)
        and not is_owner_user(request.user)
        and not is_branch_user(request.user)
    ):
        return redirect("owner_login")

    customer = None

    mobile_number = request.GET.get(
        "phone",
        ""
    ).strip()

    # =====================================================
    # SEARCH CUSTOMER BY MOBILE NUMBER
    # =====================================================

    if mobile_number:

        # -------------------------------------------------
        # BRANCH USER
        # -------------------------------------------------

        if is_branch_user(request.user):

            customer = Customer.objects.filter(
                phone=mobile_number,
                branch=request.user.branch_profile
            ).select_related(
                "branch",
                "branch__client"
            ).first()

        # -------------------------------------------------
        # OWNER
        # -------------------------------------------------

        elif is_owner_user(request.user):

            customer = Customer.objects.filter(
                phone=mobile_number,
                branch__client__owner=request.user
            ).select_related(
                "branch",
                "branch__client"
            ).first()

        # -------------------------------------------------
        # SUPER ADMIN
        # -------------------------------------------------

        else:

            customer = Customer.objects.filter(
                phone=mobile_number
            ).select_related(
                "branch",
                "branch__client"
            ).first()

    # =====================================================
    # SAVE CUSTOMER EVENT
    # =====================================================

    if request.method == "POST":

        # Customer must exist before event is created
        if not customer:

            messages.error(
                request,
                "Please search and select a customer first."
            )

            return redirect(
                f"/owner/customer-events/add/?phone={mobile_number}"
            )

        form = CustomerEventForm(
            request.POST
        )

        if form.is_valid():

            event = form.save(
                commit=False
            )

            event.customer = customer

            event.save()

            messages.success(
                request,
                "Customer event added successfully."
            )

            return redirect(
                f"/owner/customer-events/"
                f"?search={customer.phone}"
                f"&customer={customer.id}"
            )

    else:

        form = CustomerEventForm()


    # =====================================================
    # RENDER
    # =====================================================

    return render(
        request,
        "magic_pro/customer/customer_event_form.html",
        {
            "form": form,
            "customer": customer,
            "mobile_number": mobile_number,

            "customer_not_found": bool(
                mobile_number and not customer
            ),

            "edit_mode": False,
        }
    )
    

# =========================================================
# EDIT CUSTOMER EVENT
# =========================================================

@login_required
def customer_event_edit(request, pk):

    if (
        not is_admin_user(request.user)
        and not is_owner_user(request.user)
        and not is_branch_user(request.user)
    ):
        return redirect(
            "owner_login"
        )

    # -----------------------------------------------------
    # BRANCH USER
    # -----------------------------------------------------

    if is_branch_user(request.user):

        event = CustomerEvent.objects.filter(
            pk=pk,
            customer__branch=request.user.branch_profile
        ).select_related(
            "customer",
            "customer__branch",
            "event_name"
        ).first()

    # -----------------------------------------------------
    # OWNER
    # -----------------------------------------------------

    elif is_owner_user(request.user):

        event = CustomerEvent.objects.filter(
            pk=pk,
            customer__branch__client__owner=request.user
        ).select_related(
            "customer",
            "customer__branch",
            "event_name"
        ).first()

    # -----------------------------------------------------
    # SUPER ADMIN
    # -----------------------------------------------------

    else:

        event = CustomerEvent.objects.filter(
            pk=pk
        ).select_related(
            "customer",
            "customer__branch",
            "event_name"
        ).first()

    if not event:

        messages.error(
            request,
            "Customer event not found."
        )

        return redirect(
            "customer_event_list"
        )

    customer = event.customer

    if request.method == "POST":

        form = CustomerEventForm(
            request.POST,
            instance=event
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Customer event updated successfully."
            )

            return redirect(
                f"/owner/customer-events/?search={customer.phone}&customer={customer.id}"
            )

    else:

        form = CustomerEventForm(
            instance=event
        )

    return render(
        request,
        "magic_pro/customer/customer_event_form.html",
        {
            "form": form,
            "customer": customer,
            "event": event,
            "edit_mode": True,
        }
    )


# =========================================================
# DELETE CUSTOMER EVENT
# =========================================================

@login_required
def customer_event_delete(request, pk):

    if (
        not is_admin_user(request.user)
        and not is_owner_user(request.user)
        and not is_branch_user(request.user)
    ):
        return redirect(
            "owner_login"
        )

    # -----------------------------------------------------
    # BRANCH USER
    # -----------------------------------------------------

    if is_branch_user(request.user):

        event = get_object_or_404(
            CustomerEvent.objects.select_related(
                "customer",
                "customer__branch",
            ),
            pk=pk,
            customer__branch=request.user.branch_profile
        )

    # -----------------------------------------------------
    # OWNER
    # -----------------------------------------------------

    elif is_owner_user(request.user):

        event = get_object_or_404(
            CustomerEvent.objects.select_related(
                "customer",
                "customer__branch",
            ),
            pk=pk,
            customer__branch__client__owner=request.user
        )

    # -----------------------------------------------------
    # SUPER ADMIN
    # -----------------------------------------------------

    else:

        event = get_object_or_404(
            CustomerEvent.objects.select_related(
                "customer",
                "customer__branch",
            ),
            pk=pk
        )

    customer = event.customer

    event.delete()

    messages.success(
        request,
        "Customer event deleted successfully."
    )

    return redirect(
        f"/owner/customer-events/?search={customer.phone}&customer={customer.id}"
    )


# =========================================================
# CUSTOMER VISIT MESSAGE
# =========================================================

def build_customer_visit_message(customer):

    branch_name = ""
    company_name = ""

    if customer.branch:

        branch_name = customer.branch.name

        if customer.branch.client:

            company_name = (
                customer.branch.client.company_name
            )

    return (
        f"Hi {customer.name},\n\n"
        f"Thank you for visiting {branch_name} "
        f"- {company_name}.\n\n"
        f"We look forward to serving you again!"
    )


# =========================================================
# CREATE CUSTOMER
# =========================================================
# =========================================================
# CREATE CUSTOMER
# =========================================================

@login_required
def customer_create(request):

    if (
        not is_admin_user(request.user)
        and not is_owner_user(request.user)
        and not is_branch_user(request.user)
    ):
        return redirect("owner_login")

    # =====================================================
    # BRANCH USER
    # =====================================================

    if is_branch_user(request.user):

        branch = request.user.branch_profile

        if request.method == "POST":

            post_data = request.POST.copy()

            # Branch is hidden in HTML for Branch User.
            # Add the user's own branch automatically
            # before form validation.
            post_data["branch"] = branch.pk

            form = CustomerForm(
                post_data
            )

            # Only user's own branch is allowed.
            if "branch" in form.fields:

                form.fields["branch"].queryset = Branch.objects.filter(
                    pk=branch.pk
                )

            if form.is_valid():

                customer = form.save(
                    commit=False
                )

                # Security: always force own branch.
                customer.branch = branch

                customer.save()

                messages.success(
                    request,
                    "Customer created successfully."
                )

                return redirect(
                    "customer_list"
                )

        else:

            form = CustomerForm()

            if "branch" in form.fields:

                form.fields["branch"].queryset = Branch.objects.filter(
                    pk=branch.pk
                )

                form.fields["branch"].initial = branch.pk

        return render(
            request,
            "magic_pro/customer/customer_form.html",
            {
                "form": form,
                "title": "Add Customer",
                "customer": None,
                "is_branch_user": True,
                "branch": branch,
            }
        )


    # =====================================================
    # OWNER
    # =====================================================

    if is_owner_user(request.user):

        client = get_object_or_404(
            Client,
            owner=request.user
        )

        branches = Branch.objects.filter(
            client=client,
            status=True
        ).select_related(
            "client",
            "client__country",
        ).order_by(
            "name"
        )

        if request.method == "POST":

            form = CustomerForm(
                request.POST
            )

            if "branch" in form.fields:

                form.fields["branch"].queryset = branches

            if form.is_valid():

                customer = form.save(
                    commit=False
                )

                # Security check:
                # Owner can only use his own company's branch.
                if customer.branch.client_id != client.id:

                    form.add_error(
                        "branch",
                        "You can only select a branch from your own company."
                    )

                else:

                    customer.save()

                    messages.success(
                        request,
                        "Customer created successfully."
                    )

                    return redirect(
                        "customer_list"
                    )

        else:

            form = CustomerForm()

            if "branch" in form.fields:

                form.fields["branch"].queryset = branches

        return render(
            request,
            "magic_pro/customer/customer_form.html",
            {
                "form": form,
                "title": "Add Customer",
                "customer": None,
                "is_branch_user": False,
            }
        )


    # =====================================================
    # SUPER ADMIN
    # =====================================================

    branches = Branch.objects.filter(
        status=True
    ).select_related(
        "client",
        "client__country",
    ).order_by(
        "name"
    )

    if request.method == "POST":

        form = CustomerForm(
            request.POST
        )

        if "branch" in form.fields:

            form.fields["branch"].queryset = branches

        if form.is_valid():

            customer = form.save()

            messages.success(
                request,
                "Customer created successfully."
            )

            return redirect(
                "customer_list"
            )

    else:

        form = CustomerForm()

        if "branch" in form.fields:

            form.fields["branch"].queryset = branches

    return render(
        request,
        "magic_pro/customer/customer_form.html",
        {
            "form": form,
            "title": "Add Customer",
            "customer": None,
            "is_branch_user": False,
        }
    )

# =========================================================
# EDIT CUSTOMER
# =========================================================
# =========================================================
# EDIT CUSTOMER
# =========================================================

@login_required
def customer_edit(request, pk):

    if (
        not is_admin_user(request.user)
        and not is_owner_user(request.user)
        and not is_branch_user(request.user)
    ):
        return redirect("owner_login")


    # =====================================================
    # BRANCH USER
    # =====================================================

    if is_branch_user(request.user):

        branch = request.user.branch_profile

        customer = get_object_or_404(
            Customer,
            pk=pk,
            branch=branch
        )

        if request.method == "POST":

            post_data = request.POST.copy()

            # Branch field is hidden for Branch User.
            # Force their own branch into the form.
            post_data["branch"] = branch.pk

            form = CustomerForm(
                post_data,
                instance=customer
            )

            if "branch" in form.fields:

                form.fields["branch"].queryset = Branch.objects.filter(
                    pk=branch.pk
                )

            if form.is_valid():

                updated_customer = form.save(
                    commit=False
                )

                # Security:
                # Branch User can never move customer
                # to another branch.
                updated_customer.branch = branch

                updated_customer.save()

                messages.success(
                    request,
                    "Customer updated successfully."
                )

                return redirect(
                    "customer_list"
                )

        else:

            form = CustomerForm(
                instance=customer
            )

            if "branch" in form.fields:

                form.fields["branch"].queryset = Branch.objects.filter(
                    pk=branch.pk
                )

                form.fields["branch"].initial = branch.pk

        return render(
            request,
            "magic_pro/customer/customer_form.html",
            {
                "form": form,
                "title": "Edit Customer",
                "customer": customer,
                "is_branch_user": True,
                "branch": branch,
            }
        )


    # =====================================================
    # OWNER
    # =====================================================

    if is_owner_user(request.user):

        customer = get_object_or_404(
            Customer,
            pk=pk,
            branch__client__owner=request.user
        )

        client = get_object_or_404(
            Client,
            owner=request.user
        )

        branches = Branch.objects.filter(
            client=client,
            status=True
        ).select_related(
            "client",
            "client__country",
        ).order_by(
            "name"
        )

        if request.method == "POST":

            form = CustomerForm(
                request.POST,
                instance=customer
            )

            if "branch" in form.fields:

                form.fields["branch"].queryset = branches

            if form.is_valid():

                updated_customer = form.save(
                    commit=False
                )

                # Security:
                # Owner can only select branches
                # belonging to his company.
                if updated_customer.branch.client_id != client.id:

                    form.add_error(
                        "branch",
                        "You can only select a branch from your own company."
                    )

                else:

                    updated_customer.save()

                    messages.success(
                        request,
                        "Customer updated successfully."
                    )

                    return redirect(
                        "customer_list"
                    )

        else:

            form = CustomerForm(
                instance=customer
            )

            if "branch" in form.fields:

                form.fields["branch"].queryset = branches

        return render(
            request,
            "magic_pro/customer/customer_form.html",
            {
                "form": form,
                "title": "Edit Customer",
                "customer": customer,
                "is_branch_user": False,
            }
        )


    # =====================================================
    # SUPER ADMIN
    # =====================================================

    customer = get_object_or_404(
        Customer,
        pk=pk
    )

    branches = Branch.objects.filter(
        status=True
    ).select_related(
        "client",
        "client__country",
    ).order_by(
        "name"
    )

    if request.method == "POST":

        form = CustomerForm(
            request.POST,
            instance=customer
        )

        if "branch" in form.fields:

            form.fields["branch"].queryset = branches

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Customer updated successfully."
            )

            return redirect(
                "customer_list"
            )

    else:

        form = CustomerForm(
            instance=customer
        )

        if "branch" in form.fields:

            form.fields["branch"].queryset = branches

    return render(
        request,
        "magic_pro/customer/customer_form.html",
        {
            "form": form,
            "title": "Edit Customer",
            "customer": customer,
            "is_branch_user": False,
        }
    )

# =========================================================
# DELETE CUSTOMER
# =========================================================

@login_required
def customer_delete(request, pk):

    if (
        not is_admin_user(request.user)
        and not is_owner_user(request.user)
        and not is_branch_user(request.user)
    ):
        return redirect(
            "owner_login"
        )

    # -----------------------------------------------------
    # BRANCH USER
    # -----------------------------------------------------

    if is_branch_user(request.user):

        branch = request.user.branch_profile

        customer = get_object_or_404(
            Customer,
            pk=pk,
            branch=branch
        )

    # -----------------------------------------------------
    # OWNER
    # -----------------------------------------------------

    elif is_owner_user(request.user):

        customer = get_object_or_404(
            Customer,
            pk=pk,
            branch__client__owner=request.user
        )

    # -----------------------------------------------------
    # SUPER ADMIN
    # -----------------------------------------------------

    else:

        customer = get_object_or_404(
            Customer,
            pk=pk
        )

    customer.delete()

    messages.success(
        request,
        "Customer deleted successfully."
    )

    return redirect(
        "customer_list"
    )
