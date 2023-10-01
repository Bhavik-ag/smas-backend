from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = CustomUser
        fields = ("email","name","roll_no")
        
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email.endswith("@iiitdmj.ac.in"):
            self._update_errors(
                ValidationError(
                    {
                        "email": ["Email must be @iiitdmj.ac.in"]
                    }
                )
            )
        return email
        
class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("email", "name", "roll_no")