from django import forms
from django.contrib.auth import get_user_model

from .models import (
    Client,
    Branch,
    Customer,
    CustomerEvent,
)

from masters.models import (
    EventName,
)


User = get_user_model()


class ClientForm(forms.ModelForm):

    class Meta:
        model = Client

        fields = [
            "company_name",
            "email",
            "phone",
            "address",
            "business_type",
            "country",
            "state",
            "district",
            "area",
            "status",
        ]

        widgets = {

            "company_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Company Name",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Company Email",
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Phone Number",
                }
            ),

            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Company Address",
                    "rows": 4,
                }
            ),

            "business_type": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "country": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "state": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "district": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "area": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "status": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }

    def clean_company_name(self):

        company_name = self.cleaned_data.get(
            "company_name",
            ""
        ).strip()

        if not company_name:
            raise forms.ValidationError(
                "Company name is required."
            )

        if Client.objects.filter(
            company_name__iexact=company_name
        ).exclude(
            pk=self.instance.pk
        ).exists():

            raise forms.ValidationError(
                "This Company already exists."
            )

        return company_name

    def clean(self):

        cleaned_data = super().clean()

        country = cleaned_data.get("country")
        state = cleaned_data.get("state")
        district = cleaned_data.get("district")
        area = cleaned_data.get("area")

        if country and state:

            if state.country_id != country.id:

                self.add_error(
                    "state",
                    "Selected State does not belong to the selected Country."
                )

        if state and district:

            if district.state_id != state.id:

                self.add_error(
                    "district",
                    "Selected District does not belong to the selected State."
                )

        if district and area:

            if area.district_id != district.id:

                self.add_error(
                    "area",
                    "Selected Area does not belong to the selected District."
                )

        return cleaned_data


class ClientOwnerForm(ClientForm):

    owner_username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Username",
            }
        )
    )

    owner_first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "First Name",
            }
        )
    )

    owner_last_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Last Name",
            }
        )
    )

    owner_email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Login Email",
            }
        )
    )

    owner_phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Login Phone Number",
            }
        )
    )

    owner_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password",
            }
        )
    )

    owner_confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirm Password",
            }
        )
    )

    def clean_owner_username(self):

        username = self.cleaned_data.get(
            "owner_username",
            ""
        ).strip()

        if not username:

            raise forms.ValidationError(
                "Username is required."
            )

        existing_user = User.objects.filter(
            username__iexact=username
        ).first()

        if not self.instance.pk:

            if existing_user:

                raise forms.ValidationError(
                    "This username already exists."
                )

        else:

            current_owner = self.instance.owner

            if existing_user and (
                not current_owner
                or existing_user.pk != current_owner.pk
            ):

                raise forms.ValidationError(
                    "This username already exists."
                )

        return username

    def clean_owner_email(self):

        email = self.cleaned_data.get(
            "owner_email",
            ""
        ).strip()

        if not email:

            raise forms.ValidationError(
                "Login email is required."
            )

        return email

    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get(
            "owner_password"
        )

        confirm_password = cleaned_data.get(
            "owner_confirm_password"
        )

        if not self.instance.pk:

            if not password:

                self.add_error(
                    "owner_password",
                    "Password is required."
                )

            if not confirm_password:

                self.add_error(
                    "owner_confirm_password",
                    "Please confirm the password."
                )

        if password or confirm_password:

            if password != confirm_password:

                self.add_error(
                    "owner_confirm_password",
                    "Passwords do not match."
                )

        return cleaned_data

    def save(self, commit=True):

        client = super().save(commit=False)

        owner = client.owner

        if owner is None:

            owner = User(
                username=self.cleaned_data[
                    "owner_username"
                ],

                first_name=self.cleaned_data[
                    "owner_first_name"
                ],

                last_name=self.cleaned_data.get(
                    "owner_last_name",
                    ""
                ),

                email=self.cleaned_data[
                    "owner_email"
                ],

                phone=self.cleaned_data.get(
                    "owner_phone"
                ),

                role=User.Role.OWNER,
                is_active=True,
            )

            owner.set_password(
                self.cleaned_data[
                    "owner_password"
                ]
            )

            if commit:
                owner.save()

        else:

            owner.username = self.cleaned_data[
                "owner_username"
            ]

            owner.first_name = self.cleaned_data[
                "owner_first_name"
            ]

            owner.last_name = self.cleaned_data.get(
                "owner_last_name",
                ""
            )

            owner.email = self.cleaned_data[
                "owner_email"
            ]

            owner.phone = self.cleaned_data.get(
                "owner_phone"
            )

            owner.role = User.Role.OWNER
            owner.is_active = True

            password = self.cleaned_data.get(
                "owner_password"
            )

            if password:
                owner.set_password(password)

            if commit:
                owner.save()

        client.owner = owner

        if commit:
            client.save()

        return client


# ============================================================
# CLIENT SELECT WITH COUNTRY DIAL CODE
# ============================================================

class ClientDialCodeSelect(forms.Select):

    def create_option(
        self,
        name,
        value,
        label,
        selected,
        index,
        subindex=None,
        attrs=None,
    ):

        option = super().create_option(
            name,
            value,
            label,
            selected,
            index,
            subindex,
            attrs,
        )

        if value:

            try:

                client_id = (
                    value.value
                    if hasattr(value, "value")
                    else value
                )

                client = Client.objects.select_related(
                    "country"
                ).get(
                    pk=client_id
                )

                if (
                    client.country
                    and client.country.dial_code
                ):

                    option["attrs"][
                        "data-dial-code"
                    ] = client.country.dial_code

            except (
                Client.DoesNotExist,
                ValueError,
                TypeError,
            ):

                pass

        return option


class BranchForm(forms.ModelForm):

    branch_username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Branch Login Username",
            }
        )
    )

    branch_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Branch Login Password",
            }
        )
    )

    branch_confirm_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirm Branch Password",
            }
        )
    )

    class Meta:

        model = Branch

        fields = [
            "client",
            "name",
            "phone",
            "email",
            "address",
            "status",
        ]

        widgets = {

            "client": ClientDialCodeSelect(
                attrs={
                    "class": "form-control",
                }
            ),

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Branch Name",
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Phone Number",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Branch Email",
                }
            ),

            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Branch Address",
                    "rows": 4,
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
                "Branch name is required."
            )

        return name

    def clean_branch_username(self):

        username = self.cleaned_data.get(
            "branch_username",
            ""
        ).strip()

        if not username:

            raise forms.ValidationError(
                "Branch login username is required."
            )

        existing_user = User.objects.filter(
            username__iexact=username
        ).first()

        current_branch_user = None

        if self.instance.pk:

            current_branch_user = getattr(
                self.instance,
                "user",
                None
            )

        if existing_user:

            if (
                current_branch_user is None
                or existing_user.pk != current_branch_user.pk
            ):

                raise forms.ValidationError(
                    "This username already exists."
                )

        return username

    def clean(self):

        cleaned_data = super().clean()

        client = cleaned_data.get("client")

        name = cleaned_data.get(
            "name",
            ""
        ).strip()

        if client and name:

            duplicate = Branch.objects.filter(
                client=client,
                name__iexact=name
            ).exclude(
                pk=self.instance.pk
            ).exists()

            if duplicate:

                self.add_error(
                    "name",
                    "This Branch already exists under the selected Client."
                )

        password = cleaned_data.get(
            "branch_password"
        )

        confirm_password = cleaned_data.get(
            "branch_confirm_password"
        )

        current_branch_user = None

        if self.instance.pk:

            current_branch_user = getattr(
                self.instance,
                "user",
                None
            )

        if current_branch_user is None:

            if not password:

                self.add_error(
                    "branch_password",
                    "Branch login password is required."
                )

            if not confirm_password:

                self.add_error(
                    "branch_confirm_password",
                    "Please confirm the branch password."
                )

        if password or confirm_password:

            if password != confirm_password:

                self.add_error(
                    "branch_confirm_password",
                    "Passwords do not match."
                )

        return cleaned_data

    def save(self, commit=True):

        branch = super().save(
            commit=False
        )

        username = self.cleaned_data[
            "branch_username"
        ]

        password = self.cleaned_data.get(
            "branch_password"
        )

        branch_user = getattr(
            branch,
            "user",
            None
        )

        if branch_user is None:

            branch_user = User(
                username=username,
                role=User.Role.BRANCH,
                is_active=True,
            )

            branch_user.set_password(
                password
            )

            branch_user.save()

        else:

            branch_user.username = username
            branch_user.role = User.Role.BRANCH
            branch_user.is_active = True

            if password:

                branch_user.set_password(
                    password
                )

            branch_user.save()

        branch.user = branch_user

        if commit:

            branch.save()

        return branch


class CustomerForm(forms.ModelForm):

    class Meta:

        model = Customer

        fields = [
            "branch",
            "name",
            "phone",
            "email",
            "address",
            "pincode",
            "notification_method",
        ]

        widgets = {

            "branch": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Customer Name",
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Mobile Number",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Email Address",
                }
            ),

            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Customer Address",
                    "rows": 4,
                }
            ),

            "pincode": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Pincode",
                }
            ),

            "notification_method": forms.RadioSelect(
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
                "Customer name is required."
            )

        return name

    def clean_phone(self):

        phone = self.cleaned_data.get(
            "phone",
            ""
        ).strip()

        if not phone:

            raise forms.ValidationError(
                "Mobile number is required."
            )

        return phone


class BranchCustomerForm(forms.ModelForm):

    class Meta:

        model = Customer

        fields = [
            "name",
            "phone",
            "email",
            "address",
            "pincode",
            "notification_method",
        ]

        widgets = {

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Customer Name",
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Mobile Number",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Email Address",
                }
            ),

            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Customer Address",
                    "rows": 4,
                }
            ),

            "pincode": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Pincode",
                }
            ),

            "notification_method": forms.RadioSelect(
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
                "Customer name is required."
            )

        return name

    def clean_phone(self):

        phone = self.cleaned_data.get(
            "phone",
            ""
        ).strip()

        if not phone:

            raise forms.ValidationError(
                "Mobile number is required."
            )

        return phone


class CustomerEventForm(forms.ModelForm):

    event_name = forms.ModelChoiceField(
        queryset=EventName.objects.none(),
        required=True,
        empty_label="Select Event Name",
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ),
    )

    class Meta:

        model = CustomerEvent

        fields = [
            "event_name",
            "event_date",
            "repeat_yearly",
            "notes",
        ]

        widgets = {

            "event_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "repeat_yearly": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),

            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Notes",
                    "rows": 4,
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(
            *args,
            **kwargs
        )

        active_events = EventName.objects.filter(
            status=True
        ).order_by("name")

        current_event_name_id = getattr(
            self.instance,
            "event_name_id",
            None
        )

        if current_event_name_id:

            self.fields[
                "event_name"
            ].queryset = (
                active_events
                | EventName.objects.filter(
                    pk=current_event_name_id
                )
            ).distinct().order_by("name")

        else:

            self.fields[
                "event_name"
            ].queryset = active_events

    def clean_event_name(self):

        event_name = self.cleaned_data.get(
            "event_name"
        )

        if not event_name:

            raise forms.ValidationError(
                "Please select an event name."
            )

        return event_name
