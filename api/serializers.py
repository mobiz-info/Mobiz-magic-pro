from rest_framework import serializers

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


# =========================================================
# USER SERIALIZER
# =========================================================

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User

        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "role",
        ]

        read_only_fields = [
            "id",
        ]


# =========================================================
# BUSINESS TYPE SERIALIZER
# =========================================================

class BusinessTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = BusinessType

        fields = [
            "id",
            "name",
            "status",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


# =========================================================
# COUNTRY SERIALIZER
# =========================================================

class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = [
            "id",
            "name",
            "currency_code",
            "emblem",
            "dial_code",
        ]

        read_only_fields = [
            "id",
        ]
# =========================================================
# STATE SERIALIZER
# =========================================================

class StateSerializer(serializers.ModelSerializer):

    class Meta:
        model = State

        fields = [
            "id",
            "country",
            "name",
        ]

        read_only_fields = [
            "id",
        ]


# =========================================================
# DISTRICT SERIALIZER
# =========================================================

class DistrictSerializer(serializers.ModelSerializer):

    class Meta:
        model = District

        fields = [
            "id",
            "state",
            "name",
        ]

        read_only_fields = [
            "id",
        ]


# =========================================================
# AREA SERIALIZER
# =========================================================

class AreaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Area

        fields = [
            "id",
            "district",
            "name",
        ]

        read_only_fields = [
            "id",
        ]


# =========================================================
# CLIENT SERIALIZER
# =========================================================

class ClientSerializer(serializers.ModelSerializer):

    owner_details = UserSerializer(
        source="owner",
        read_only=True
    )

    class Meta:
        model = Client

        fields = [
            "id",
            "company_name",
            "owner",
            "owner_details",
            "email",
            "phone",
            "address",
            "business_type",
            "country",
            "state",
            "district",
            "area",
            "status",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "owner_details",
            "created_at",
            "updated_at",
        ]


# =========================================================
# BRANCH SERIALIZER
# =========================================================

class BranchSerializer(serializers.ModelSerializer):

    user_details = UserSerializer(
        source="user",
        read_only=True
    )

    client_name = serializers.CharField(
        source="client.company_name",
        read_only=True
    )

    class Meta:
        model = Branch

        fields = [
            "id",
            "user",
            "user_details",
            "client",
            "client_name",
            "name",
            "phone",
            "email",
            "address",
            "status",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "user_details",
            "client_name",
            "created_at",
            "updated_at",
        ]


# =========================================================
# CUSTOMER SERIALIZER
# =========================================================

class CustomerSerializer(serializers.ModelSerializer):

    branch_name = serializers.CharField(
        source="branch.name",
        read_only=True
    )

    company_name = serializers.CharField(
        source="branch.client.company_name",
        read_only=True
    )

    class Meta:
        model = Customer

        fields = [
            "id",
            "branch",
            "branch_name",
            "company_name",
            "name",
            "phone",
            "email",
            "address",
            "pincode",
            "notification_method",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "branch_name",
            "company_name",
            "created_at",
            "updated_at",
        ]


# =========================================================
# EVENT NAME SERIALIZER
# =========================================================

class EventNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventName

        fields = [
            "id",
            "name",
            "status",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


# =========================================================
# CUSTOMER EVENT SERIALIZER
# =========================================================

class CustomerEventSerializer(serializers.ModelSerializer):

    customer_name = serializers.CharField(
        source="customer.name",
        read_only=True
    )

    customer_phone = serializers.CharField(
        source="customer.phone",
        read_only=True
    )

    event_name_text = serializers.CharField(
        source="event_name.name",
        read_only=True
    )

    class Meta:
        model = CustomerEvent

        fields = [
            "id",
            "customer",
            "customer_name",
            "customer_phone",
            "event_name",
            "event_name_text",
            "event_date",
            "repeat_yearly",
            "notes",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "customer_name",
            "customer_phone",
            "event_name_text",
            "created_at",
            "updated_at",
        ]