from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import User


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def is_owner(user):

    return (
        user.is_authenticated
        and user.role == User.Role.OWNER
    )


def is_owner_user(user):

    return (
        user.is_authenticated
        and user.role == User.Role.OWNER
    )


def is_super_admin(user):

    return (
        user.is_authenticated
        and user.role == User.Role.SUPER_ADMIN
    )


def is_admin_user(user):

    # Super Admin only
    #
    # IMPORTANT:
    # Owner is NOT treated as Admin.
    # Owner access must be restricted
    # to his own Company.

    return is_super_admin(user)


def is_branch_user(user):

    return (
        user.is_authenticated
        and user.role == User.Role.BRANCH
        and hasattr(
            user,
            "branch_profile"
        )
        and user.branch_profile is not None
    )


# =========================================================
# OWNER / BRANCH LOGIN
# =========================================================

def owner_login(request):

    # -----------------------------------------------------
    # ALREADY LOGGED IN
    # -----------------------------------------------------

    if request.user.is_authenticated:

        # Branch user -> Customer Management
        if is_branch_user(request.user):

            return redirect(
                "customer_list"
            )

        # Owner / Super Admin -> Dashboard
        if (
            is_owner_user(request.user)
            or is_super_admin(request.user)
        ):

            return redirect(
                "owner_dashboard"
            )

        # Unknown user
        logout(request)

        return redirect(
            "owner_login"
        )


    # -----------------------------------------------------
    # LOGIN POST
    # -----------------------------------------------------

    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            # -------------------------------------------------
            # BRANCH USER
            # -------------------------------------------------

            if (
                user.role == User.Role.BRANCH
                and hasattr(
                    user,
                    "branch_profile"
                )
                and user.branch_profile is not None
            ):

                login(
                    request,
                    user
                )

                return redirect(
                    "customer_list"
                )


            # -------------------------------------------------
            # OWNER
            # -------------------------------------------------

            if user.role == User.Role.OWNER:

                login(
                    request,
                    user
                )

                return redirect(
                    "owner_dashboard"
                )


            # -------------------------------------------------
            # SUPER ADMIN
            # -------------------------------------------------

            if user.role == User.Role.SUPER_ADMIN:

                login(
                    request,
                    user
                )

                return redirect(
                    "owner_dashboard"
                )


            # -------------------------------------------------
            # INVALID / UNASSIGNED USER
            # -------------------------------------------------

            return render(
                request,
                "login.html",
                {
                    "error": (
                        "This account does not have "
                        "a valid role."
                    )
                }
            )


        # -----------------------------------------------------
        # INVALID LOGIN
        # -----------------------------------------------------

        return render(
            request,
            "login.html",
            {
                "error": (
                    "Invalid username or password."
                )
            }
        )


    return render(
        request,
        "login.html"
    )


# =========================================================
# OWNER DASHBOARD
# =========================================================

@login_required
def owner_dashboard(request):

    # -----------------------------------------------------
    # BRANCH USER MUST NEVER SEE ADMIN DASHBOARD
    # -----------------------------------------------------

    if is_branch_user(request.user):

        return redirect(
            "customer_list"
        )


    # -----------------------------------------------------
    # ONLY OWNER / SUPER ADMIN
    # -----------------------------------------------------

    if (
        not is_owner_user(request.user)
        and not is_super_admin(request.user)
    ):

        return redirect(
            "owner_login"
        )


    return render(
        request,
        "dashboard.html"
    )


# =========================================================
# LOGOUT
# =========================================================

@login_required
def user_logout(request):

    logout(request)

    return redirect(
        "owner_login"
    )
