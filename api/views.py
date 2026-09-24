from django.contrib.auth import authenticate

from rest_framework import status, viewsets
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    BasePermission,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied

from rest_framework_simplejwt.tokens import RefreshToken

from core.models import User

from masters.models import (
    BusinessType,
    Country,
    State,
    District,
    Area,
    EventName,
)

from operations.models import (
    Client,
    Branch,
    Customer,
    CustomerEvent,
)

from .serializers import (
    UserSerializer,
    BusinessTypeSerializer,
    ClientSerializer,
    CountrySerializer,
    StateSerializer,
    DistrictSerializer,
    AreaSerializer,
    BranchSerializer,
    CustomerSerializer,
    EventNameSerializer,
    CustomerEventSerializer,
)


# =========================================================
# PERMISSION HELPERS
# =========================================================

class IsAdminRole(BasePermission):
    """
    Only OWNER and SUPER_ADMIN can access admin APIs.
    """

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated
            and request.user.role in [
                User.Role.OWNER,
                User.Role.SUPER_ADMIN,
            ]
        )


class IsAdminOrBranch(BasePermission):
    """
    OWNER, SUPER_ADMIN and BRANCH can access the API.
    """

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated
            and request.user.role in [
                User.Role.OWNER,
                User.Role.SUPER_ADMIN,
                User.Role.BRANCH,
            ]
        )


# =========================================================
# LOGIN API
# =========================================================

class LoginAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        username = request.data.get(
            "username"
        )

        password = request.data.get(
            "password"
        )

        if not username or not password:

            return Response(
                {
                    "detail": "Username and password are required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is None:

            return Response(
                {
                    "detail": "Invalid username or password."
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        # -------------------------------------------------
        # BRANCH USER VALIDATION
        # -------------------------------------------------

        if user.role == User.Role.BRANCH:

            branch = getattr(
                user,
                "branch_profile",
                None
            )

            if branch is None:

                return Response(
                    {
                        "detail": (
                            "This branch account is not "
                            "assigned to a branch."
                        )
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

        # -------------------------------------------------
        # ALLOWED ROLES
        # -------------------------------------------------

        if user.role not in [
            User.Role.OWNER,
            User.Role.SUPER_ADMIN,
            User.Role.BRANCH,
        ]:

            return Response(
                {
                    "detail": (
                        "You are not authorized "
                        "to use this application."
                    )
                },
                status=status.HTTP_403_FORBIDDEN
            )

        # -------------------------------------------------
        # JWT
        # -------------------------------------------------

        refresh = RefreshToken.for_user(
            user
        )

        response_data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": UserSerializer(user).data,
        }

        # -------------------------------------------------
        # BRANCH DETAILS
        # -------------------------------------------------

        if user.role == User.Role.BRANCH:

            branch = getattr(
                user,
                "branch_profile",
                None
            )

            if branch:

                response_data["branch"] = {
                    "id": branch.id,
                    "name": branch.name,
                    "client": branch.client_id,
                    "client_name": branch.client.company_name,
                }

        return Response(
            response_data,
            status=status.HTTP_200_OK
        )


# =========================================================
# ME API
# =========================================================

class MeAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        response_data = {
            "user": UserSerializer(
                request.user
            ).data
        }

        # -------------------------------------------------
        # BRANCH DETAILS
        # -------------------------------------------------

        if request.user.role == User.Role.BRANCH:

            branch = getattr(
                request.user,
                "branch_profile",
                None
            )

            if branch:

                response_data["branch"] = {
                    "id": branch.id,
                    "name": branch.name,
                    "client": branch.client_id,
                    "client_name": branch.client.company_name,
                }

        return Response(
            response_data,
            status=status.HTTP_200_OK
        )


# =========================================================
# USER API
# =========================================================

class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all().order_by(
        "id"
    )

    serializer_class = UserSerializer

    permission_classes = [
        IsAdminRole
    ]


# =========================================================
# BUSINESS TYPE API
# =========================================================

class BusinessTypeViewSet(viewsets.ModelViewSet):

    queryset = BusinessType.objects.all().order_by(
        "id"
    )

    serializer_class = BusinessTypeSerializer

    permission_classes = [
        IsAdminRole
    ]


# =========================================================
# COUNTRY API
# =========================================================

class CountryViewSet(viewsets.ModelViewSet):

    queryset = Country.objects.all().order_by(
        "id"
    )

    serializer_class = CountrySerializer

    permission_classes = [
        IsAdminRole
    ]


# =========================================================
# STATE API
# =========================================================

class StateViewSet(viewsets.ModelViewSet):

    queryset = State.objects.select_related(
        "country"
    ).all().order_by(
        "id"
    )

    serializer_class = StateSerializer

    permission_classes = [
        IsAdminRole
    ]


# =========================================================
# DISTRICT API
# =========================================================

class DistrictViewSet(viewsets.ModelViewSet):

    queryset = District.objects.select_related(
        "state",
        "state__country"
    ).all().order_by(
        "id"
    )

    serializer_class = DistrictSerializer

    permission_classes = [
        IsAdminRole
    ]


# =========================================================
# AREA API
# =========================================================

class AreaViewSet(viewsets.ModelViewSet):

    queryset = Area.objects.select_related(
        "district",
        "district__state",
        "district__state__country"
    ).all().order_by(
        "id"
    )

    serializer_class = AreaSerializer

    permission_classes = [
        IsAdminRole
    ]


# =========================================================
# CLIENT API
# =========================================================

class ClientViewSet(viewsets.ModelViewSet):

    queryset = Client.objects.select_related(
        "owner",
        "business_type",
        "country",
        "state",
        "district",
        "area",
    ).all().order_by(
        "id"
    )

    serializer_class = ClientSerializer

    permission_classes = [
        IsAdminRole
    ]


# =========================================================
# BRANCH API
# =========================================================

class BranchViewSet(viewsets.ModelViewSet):

    queryset = Branch.objects.select_related(
        "user",
        "client",
    ).all().order_by(
        "id"
    )

    serializer_class = BranchSerializer

    permission_classes = [
        IsAdminRole
    ]


# =========================================================
# CUSTOMER API
# =========================================================

class CustomerViewSet(viewsets.ModelViewSet):

    serializer_class = CustomerSerializer

    permission_classes = [
        IsAdminOrBranch
    ]

    # -----------------------------------------------------
    # QUERYSET
    # -----------------------------------------------------

    def get_queryset(self):

        queryset = Customer.objects.select_related(
            "branch",
            "branch__client",
        ).all().order_by(
            "-id"
        )

        # -------------------------------------------------
        # BRANCH USER
        # -------------------------------------------------

        if self.request.user.role == User.Role.BRANCH:

            branch = getattr(
                self.request.user,
                "branch_profile",
                None
            )

            if not branch:

                return Customer.objects.none()

            queryset = queryset.filter(
                branch=branch
            )

        return queryset

    # -----------------------------------------------------
    # CREATE
    # -----------------------------------------------------

    def create(self, request, *args, **kwargs):

        data = request.data.copy()

        # -------------------------------------------------
        # BRANCH USER
        # -------------------------------------------------

        if request.user.role == User.Role.BRANCH:

            branch = getattr(
                request.user,
                "branch_profile",
                None
            )

            if not branch:

                return Response(
                    {
                        "detail": (
                            "Branch account is not "
                            "linked to a branch."
                        )
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            # Branch is automatically assigned
            data["branch"] = branch.id

        serializer = self.get_serializer(
            data=data
        )

        serializer.is_valid(
            raise_exception=True
        )

        self.perform_create(
            serializer
        )

        headers = self.get_success_headers(
            serializer.data
        )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    # -----------------------------------------------------
    # UPDATE
    # -----------------------------------------------------

    def perform_update(self, serializer):

        if self.request.user.role == User.Role.BRANCH:

            branch = getattr(
                self.request.user,
                "branch_profile",
                None
            )

            if not branch:

                raise PermissionDenied(
                    "Branch account is not linked to a branch."
                )

            serializer.save(
                branch=branch
            )

        else:

            serializer.save()

    # -----------------------------------------------------
    # CREATE SAVE
    # -----------------------------------------------------

    def perform_create(self, serializer):

        if self.request.user.role == User.Role.BRANCH:

            branch = getattr(
                self.request.user,
                "branch_profile",
                None
            )

            if not branch:

                raise PermissionDenied(
                    "Branch account is not linked to a branch."
                )

            serializer.save(
                branch=branch
            )

        else:

            serializer.save()


# =========================================================
# EVENT NAME API
# =========================================================

class EventNameViewSet(viewsets.ModelViewSet):

    queryset = EventName.objects.all().order_by(
        "name"
    )

    serializer_class = EventNameSerializer

    permission_classes = [
        IsAdminRole
    ]


# =========================================================
# CUSTOMER EVENT API
# =========================================================

class CustomerEventViewSet(viewsets.ModelViewSet):

    serializer_class = CustomerEventSerializer

    permission_classes = [
        IsAdminOrBranch
    ]

    # -----------------------------------------------------
    # QUERYSET
    # -----------------------------------------------------

    def get_queryset(self):

        queryset = CustomerEvent.objects.select_related(
            "customer",
            "customer__branch",
            "customer__branch__client",
            "event_name",
        ).all().order_by(
            "event_date",
            "-id"
        )

        # -------------------------------------------------
        # BRANCH USER
        # -------------------------------------------------

        if self.request.user.role == User.Role.BRANCH:

            branch = getattr(
                self.request.user,
                "branch_profile",
                None
            )

            if not branch:

                return CustomerEvent.objects.none()

            queryset = queryset.filter(
                customer__branch=branch
            )

        return queryset

    # -----------------------------------------------------
    # CREATE
    # -----------------------------------------------------

    def perform_create(self, serializer):

        customer = serializer.validated_data.get(
            "customer"
        )

        if not customer:

            raise PermissionDenied(
                "Customer is required."
            )

        # -------------------------------------------------
        # BRANCH USER
        # -------------------------------------------------

        if self.request.user.role == User.Role.BRANCH:

            branch = getattr(
                self.request.user,
                "branch_profile",
                None
            )

            if not branch:

                raise PermissionDenied(
                    "Branch account is not linked to a branch."
                )

            # Customer must belong to logged-in branch
            if customer.branch_id != branch.id:

                raise PermissionDenied(
                    "You can only add events for customers "
                    "of your branch."
                )

        serializer.save()

    # -----------------------------------------------------
    # UPDATE
    # -----------------------------------------------------

    def perform_update(self, serializer):

        customer = serializer.validated_data.get(
            "customer",
            serializer.instance.customer
        )

        # -------------------------------------------------
        # BRANCH USER
        # -------------------------------------------------

        if self.request.user.role == User.Role.BRANCH:

            branch = getattr(
                self.request.user,
                "branch_profile",
                None
            )

            if not branch:

                raise PermissionDenied(
                    "Branch account is not linked to a branch."
                )

            # Customer must belong to logged-in branch
            if customer.branch_id != branch.id:

                raise PermissionDenied(
                    "You can only update events for customers "
                    "of your branch."
                )

        serializer.save()