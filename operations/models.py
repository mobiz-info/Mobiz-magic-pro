from django.db import models

from core.models import User

from masters.models import (
    BusinessType,
    Country,
    State,
    District,
    Area,
    EventName,
)


# =========================================================
# CLIENT
# =========================================================

class Client(models.Model):

    company_name = models.CharField(
        max_length=200
    )

    owner = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="client"
    )

    email = models.EmailField(
        blank=True,
        null=True
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    address = models.TextField(
        blank=True,
        null=True
    )

    business_type = models.ForeignKey(
        BusinessType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="clients"
    )

    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="clients"
    )

    state = models.ForeignKey(
        State,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="clients"
    )

    district = models.ForeignKey(
        District,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="clients"
    )

    area = models.ForeignKey(
        Area,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="clients"
    )

    status = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.company_name


# =========================================================
# BRANCH
# =========================================================

class Branch(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="branch_profile"
    )

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="branches"
    )

    name = models.CharField(
        max_length=200
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    email = models.EmailField(
        blank=True,
        null=True
    )

    address = models.TextField(
        blank=True,
        null=True
    )

    status = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["client", "name"],
                name="unique_branch_per_client"
            )
        ]

        ordering = ["-id"]

    def __str__(self):
        return f"{self.name} - {self.client.company_name}"


# =========================================================
# CUSTOMER
# =========================================================

class Customer(models.Model):

    class NotificationMethod(models.TextChoices):
        SMS = "SMS", "SMS"
        WHATSAPP = "WHATSAPP", "WhatsApp"

    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name="customers"
    )

    name = models.CharField(
        max_length=200
    )

    phone = models.CharField(
        max_length=20
    )

    email = models.EmailField(
        blank=True,
        null=True
    )

    address = models.TextField(
        blank=True,
        null=True
    )

    pincode = models.CharField(
        max_length=10,
        blank=True,
        null=True
    )

    notification_method = models.CharField(
        max_length=20,
        choices=NotificationMethod.choices,
        default=NotificationMethod.WHATSAPP
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"{self.name} ({self.phone})"


# =========================================================
# CUSTOMER EVENT
# =========================================================

class CustomerEvent(models.Model):

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="events"
    )

    event_name = models.ForeignKey(
        EventName,
        on_delete=models.PROTECT,
        related_name="customer_events"
    )

    event_date = models.DateField()

    repeat_yearly = models.BooleanField(
        default=True
    )

    notes = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = [
            "event_date",
            "-id"
        ]

    def __str__(self):
        return f"{self.customer.name} - {self.event_name.name}"