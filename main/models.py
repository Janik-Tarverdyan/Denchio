from django.db import models
from ckeditor.fields import RichTextField

from datetime import date
import os


class Whitepaper(models.Model):
    title = models.CharField("Վերնագիր", max_length=250)
    content = RichTextField("Կոնտենտ")
    file = models.FileField(
        "Ֆայլ",
        upload_to="Whitepaper",
        blank=True,
        null=True,
    )

    def filename(self):
        return os.path.basename(self.file.name)

    def __str__(self):
        return self.title


class Partner(models.Model):
    name = models.CharField("Անուն", max_length=250)
    address = models.CharField("Հասցե", blank=True, null=True, max_length=250)
    phone = models.CharField("Հեռախոս", blank=True, null=True, max_length=250)
    website = models.CharField("Կայք", blank=True, null=True, max_length=250)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "գործընկեր"
        verbose_name_plural = "Գործընկերներ"


class Subscribe(models.Model):
    email = models.EmailField("Էլ․ հասցե")
    is_active = models.BooleanField("Ակտիվ է՝", default=True)
    date_joined = models.DateTimeField("Միացել է՝", auto_now_add=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "բաժանորդ"
        verbose_name_plural = "Բաժանորդներ"


def year_choices():
    return [(str(i), i) for i in range(date.today().year, 2017, -1)]


QUARTER_CHOICES = (
    ("1", "Առաջին Եռամսյակ"),
    ("2", "Երկրորդ Եռամսյակ"),
    ("3", "Երրերդ Եռամսյակ"),
    ("4", "Չորորդ Եռամսյակ"),
)


class RoadMap(models.Model):
    year = models.CharField("Տարի", max_length=5, choices=year_choices)
    quarter = models.CharField(
        "Եռամսյակ", max_length=2, choices=QUARTER_CHOICES
    )
    description = models.TextField("Նկարագրություն")

    def __str__(self):
        return f"{self.year} Q{self.quarter} - {self.description}"

    class Meta:
        verbose_name = "օբյեկտ"
        verbose_name_plural = "Ճանապարհային քարտեզ"
        ordering = ("year", "quarter")
        unique_together = ("year", "quarter")
