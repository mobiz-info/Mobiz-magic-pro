from django import forms

from .models import (
    BusinessType,
    Country,
    State,
    District,
    Area,
    EventName,
)


# =========================================================
# BUSINESS TYPE FORM
# =========================================================

class BusinessTypeForm(forms.ModelForm):

    class Meta:
        model = BusinessType
        fields = [
            "name",
            "status",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Business Type",
                }
            ),

            "status": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }

    def clean_name(self):

        name = self.cleaned_data.get(
            "name",
            ""
        ).strip()

        if not name:

            raise forms.ValidationError(
                "Business Type name is required."
            )

        if BusinessType.objects.filter(
            name__iexact=name
        ).exclude(
            pk=self.instance.pk
        ).exists():

            raise forms.ValidationError(
                "This Business Type already exists."
            )

        return name


# =========================================================
# COUNTRY FORM
# =========================================================
class CountryForm(forms.ModelForm):

    class Meta:
        model = Country

        fields = [
            "name",
            "currency_code",
            "emblem",
            "dial_code",
        ]

        widgets = {

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Country Name",
                }
            ),

            "currency_code": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. INR, AED",
                }
            ),

            "emblem": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. 🇮🇳",
                }
            ),

            "dial_code": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. +91",
                }
            ),
        }

# =========================================================
# STATE FORM
# =========================================================

class StateForm(forms.ModelForm):

    class Meta:
        model = State

        fields = [
            "country",
            "name",
        ]

        widgets = {

            "country": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "State Name",
                }
            ),
        }

    def clean(self):

        cleaned_data = super().clean()

        country = cleaned_data.get(
            "country"
        )

        name = cleaned_data.get(
            "name",
            ""
        ).strip()

        if not name:

            self.add_error(
                "name",
                "State name is required."
            )

        if country and name:

            duplicate = State.objects.filter(
                country=country,
                name__iexact=name
            ).exclude(
                pk=self.instance.pk
            ).exists()

            if duplicate:

                self.add_error(
                    "name",
                    "This State already exists under the selected Country."
                )

        return cleaned_data


# =========================================================
# DISTRICT FORM
# =========================================================

class DistrictForm(forms.ModelForm):

    class Meta:
        model = District

        fields = [
            "state",
            "name",
        ]

        widgets = {

            "state": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "District Name",
                }
            ),
        }

    def clean(self):

        cleaned_data = super().clean()

        state = cleaned_data.get(
            "state"
        )

        name = cleaned_data.get(
            "name",
            ""
        ).strip()

        if not name:

            self.add_error(
                "name",
                "District name is required."
            )

        if state and name:

            duplicate = District.objects.filter(
                state=state,
                name__iexact=name
            ).exclude(
                pk=self.instance.pk
            ).exists()

            if duplicate:

                self.add_error(
                    "name",
                    "This District already exists under the selected State."
                )

        return cleaned_data


# =========================================================
# AREA FORM
# =========================================================

class AreaForm(forms.ModelForm):

    class Meta:
        model = Area

        fields = [
            "district",
            "name",
        ]

        widgets = {

            "district": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Area Name",
                }
            ),
        }

    def clean(self):

        cleaned_data = super().clean()

        district = cleaned_data.get(
            "district"
        )

        name = cleaned_data.get(
            "name",
            ""
        ).strip()

        if not name:

            self.add_error(
                "name",
                "Area name is required."
            )

        if district and name:

            duplicate = Area.objects.filter(
                district=district,
                name__iexact=name
            ).exclude(
                pk=self.instance.pk
            ).exists()

            if duplicate:

                self.add_error(
                    "name",
                    "This Area already exists under the selected District."
                )

        return cleaned_data


# =========================================================
# EVENT NAME FORM
# =========================================================

class EventNameForm(forms.ModelForm):

    class Meta:
        model = EventName

        fields = [
            "name",
            "status",
        ]

        widgets = {

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Event Name",
                }
            ),

            "status": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }

    def clean_name(self):

        name = self.cleaned_data.get(
            "name"
        ) or ""

        name = name.strip()

        if not name:

            raise forms.ValidationError(
                "Event Name is required."
            )

        if EventName.objects.filter(
            name__iexact=name
        ).exclude(
            pk=self.instance.pk
        ).exists():

            raise forms.ValidationError(
                "This Event Name already exists."
            )

        return name