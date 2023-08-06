from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class AbstractSolarluxUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username is required. Other fields are optional.
    """

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={"unique": _("A user with that username already exists.")},
    )
    first_name = models.CharField(
        _("first name"), max_length=255, null=True, blank=True
    )
    last_name = models.CharField(_("last name"), max_length=255, null=True, blank=True)

    customer_no = models.CharField(
        _("customer no"), max_length=255, null=True, blank=True
    )
    customer_name = models.CharField(
        _("customer name"), max_length=255, null=True, blank=True
    )

    language = models.CharField(_("language"), max_length=255, null=True, blank=True)

    TITLE_CHOICES = (("MR", _("Mr.")), ("MRS", _("Mrs.")))

    title = models.CharField(
        _("title"), choices=TITLE_CHOICES, max_length=255, null=True, blank=True
    )

    is_customer_admin = models.BooleanField(_("is customer admin"), default=False)

    crm_contact_id = models.UUIDField(_("CRM contact id"), null=True, blank=True)

    email = models.EmailField(_("email address"), blank=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    access_token = models.TextField("OAuth2 Access Token", null=True, blank=True)
    password = models.CharField(_("password"), max_length=128, null=True, blank=True)

    sap_pernr = models.IntegerField(_("SAP Pernr"), null=True, blank=True)
    sap_sales_org = models.CharField(_('SAP Verkaufsorganisation'), max_length=4, null=True, blank=True)
    sap_company_code = models.CharField(_('SAP Buchungskreis'), max_length=4, null=True, blank=True)
    sap_plant = models.CharField(_('SAP Werk'), max_length=4, null=True, blank=True)
    country_code = models.CharField(_('Länderkürzel'), max_length=2, null=True, blank=True)
    mobile_number = models.CharField(_('Mobilnummer'), max_length=255, null=True, blank=True)
    department = models.CharField(_('Abteilung'), max_length=50, null=True, blank=True)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        abstract = True

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        if self.first_name is not None and self.last_name is not None:
            return self.last_name + ', ' + self.first_name
        # username always has a value, regarding the attributes in Model.py and the database
        return self.username

