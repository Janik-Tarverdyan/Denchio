from django import forms
from django.http import QueryDict
from .models import Token
from utils.exchange import get_token_info


class TokenCreationForm(forms.ModelForm):

    class Meta:
        model = Token
        fields = ("address",)

    def is_valid(self):
        token_info = get_token_info(self.data["address"])
        token_attributes = token_info.get("attributes", {})
        self.dict_data = self.data.dict()
        self.dict_data["name"] = token_attributes.get("name")
        self.dict_data["symbol"] = token_attributes.get("symbol")
        self.dict_data["image_url"] = token_attributes.get("image_url")
        self.dict_data["decimals"] = token_attributes.get("decimals")
        if not all((
            self.dict_data["name"],
            self.dict_data["symbol"],
            self.dict_data["image_url"],
            self.dict_data["decimals"],
        )):
            return False
        self.data = QueryDict("", True)
        self.data.update(self.dict_data)
        return super().is_valid()
