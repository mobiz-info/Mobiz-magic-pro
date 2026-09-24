from django.db import models


# =========================================================
# BUSINESS TYPE
# =========================================================

class BusinessType(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
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
        return self.name


# =========================================================
# COUNTRY
# =========================================================

class Country(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    currency_code = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        help_text="e.g. INR, AED"
    )

    emblem = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        help_text="e.g. 🇮🇳, 🇦🇪"
    )

    dial_code = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        help_text="e.g. +91, +971, +44"
    )

    def __str__(self):
        return self.name


# =========================================================
# STATE / PROVINCE
# =========================================================

class State(models.Model):

    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name="states"
    )

    name = models.CharField(
        max_length=100
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["country", "name"],
                name="unique_state_per_country"
            )
        ]

    def __str__(self):
        return self.name


# =========================================================
# DISTRICT
# =========================================================

class District(models.Model):

    state = models.ForeignKey(
        State,
        on_delete=models.CASCADE,
        related_name="districts"
    )

    name = models.CharField(
        max_length=100
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["state", "name"],
                name="unique_district_per_state"
            )
        ]

    def __str__(self):
        return self.name


# =========================================================
# AREA
# =========================================================

class Area(models.Model):

    district = models.ForeignKey(
        District,
        on_delete=models.CASCADE,
        related_name="areas"
    )

    name = models.CharField(
        max_length=100
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["district", "name"],
                name="unique_area_per_district"
            )
        ]

    def __str__(self):
        return self.name


# =========================================================
# EVENT NAME MASTER
# =========================================================

class EventName(models.Model):

    name = models.CharField(
        max_length=200,
        unique=True
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
        ordering = ["name"]

    def __str__(self):
        return self.name