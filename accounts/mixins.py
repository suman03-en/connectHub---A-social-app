from django.core.exceptions import ValidationError


class UsernameEmailUniqueCheckMixin:
    """
    Mixin to enforce unique username validation, excluding the current instance.
    Requires the form to be a ModelForm and accept a 'user' instance.
    """

    def clean_username(self):
        username = self.cleaned_data["username"]

        Model = self._meta.model

        qs = Model.objects.filter(username=username)

        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise ValidationError(f"The username {username} is already taken by another user.")
        return username
    
    def clean_email(self):
        email = self.cleaned_data["email"]
        Model = self._meta.model

        qs = Model.objects.filter(email=email)

        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise ValidationError(f"The email {email} is already registered.")
        
        return email