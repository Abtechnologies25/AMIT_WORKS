from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    DEPARTMENT_CHOICES = [
        # ('JOURNAL TEAM', 'JOURNAL TEAM'),
        # ('RESEARCH WORK DEVELOPMENT TEAM', 'RESEARCH WORK DEVELOPMENT TEAM'),
        # ('SOFTWARE PROJECT DEVELOPMENT TEAM', 'SOFTWARE PROJECT DEVELOPMENT TEAM'),
        ('HARDWARE PROJECT DEVELOPMENT TEAM', 'HARDWARE PROJECT DEVELOPMENT TEAM'),
        # ('TECHNICAL TEAM', 'TECHNICAL TEAM'),
        ('ADMIN TEAM', 'ADMIN TEAM'),
        ('ADMIN-MANAGEMENT WORK TEAM', 'ADMIN-MANAGEMENT WORK TEAM'),
    ]

    BRANCH_CHOICES = [
        ('NAGERCOIL', 'NAGERCOIL'),
        # ('TIRUNELVELI', 'TIRUNELVELI'),
        # ('CHENNAI', 'CHENNAI'),
        # ('PUDUKOTTAI', 'PUDUKOTTAI'),
        # ('VIJAYAWADA','VIJAYAWADA')
        
    ]
    employee_name = models.CharField(max_length=100, null=True, blank=True)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    branch = models.CharField(max_length=20, choices=BRANCH_CHOICES)
    is_team_leader = models.BooleanField(default=False) 
    is_approved = models.BooleanField(default=False)   

    def __str__(self):
        return f"{self.username} - {self.department} - {self.branch} - {'Approved' if self.is_approved else 'Pending'}"

class WorkStatusGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    branch = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    S_NO=models.CharField(max_length=100)
    DATE = models.DateField()

    def __str__(self):
        return f"{self.user.username} - {self.DATE}"

class WorkStatus(models.Model):
    group = models.ForeignKey(WorkStatusGroup, on_delete=models.CASCADE, related_name='statuses')
    WORK_CODE = models.CharField(max_length=50)
    WORK_DETAILS = models.TextField()
    STARTING_DATE = models.DateField(null=True, blank=True)
    ENDING_DATE = models.DateField(null=True, blank=True)

    STATUS_CHOICES = [
        ('IN PROGRESS', 'IN PROGRESS'),
        ('COMPLETED', 'COMPLETED'),
        ('-', '-')
    ]
    WORK_STATUS = models.CharField(max_length=50, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.WORK_CODE} - {self.WORK_STATUS}"


class AbstractPaymentVoucher(models.Model):
    S_NO=models.IntegerField()
    DATE = models.DateField()
    VC_NO = models.CharField(max_length=100, unique=True)
    PURPOSE = models.TextField()
    ONLINE_PAYMENT = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Online (A/C)")
    CASH_PAYMENT = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cash")

    class Meta:
        abstract = True  

    def __str__(self):
        return f"VC No: {self.VC_NO} - {self.PURPOSE}"



class NagercoilPaymentVoucher(AbstractPaymentVoucher):
    class Meta:
        verbose_name = "Nagercoil Payment Voucher"
        verbose_name_plural = "Nagercoil Payment Vouchers"

class TirunelveliPaymentVoucher(AbstractPaymentVoucher):
    class Meta:
        verbose_name = "Tirunelveli Payment Voucher"
        verbose_name_plural = "Tirunelveli Payment Vouchers"

class PudukottaiPaymentVoucher(AbstractPaymentVoucher):
    class Meta:
        verbose_name = "Pudukottai Payment Voucher"
        verbose_name_plural = "Pudukottai Payment Vouchers"

class ChennaiPaymentVoucher(AbstractPaymentVoucher):
    class Meta:
        verbose_name = "Chennai Payment Voucher"
        verbose_name_plural = "Chennai Payment Vouchers"


class AbstractProductRegistration(models.Model):
    S_NO=models.IntegerField()
    DATE = models.DateField()
    REG_CODE = models.CharField(max_length=100, unique=True)
    NAME = models.CharField(max_length=255)
    DEPARTMENT = models.CharField(max_length=255)
    TYPE = models.CharField(max_length=255)
    COLLEGE_UNIVERSITY = models.CharField(max_length=255)
    MOBILE_NO = models.CharField(max_length=15)
    EMAIL_ID = models.EmailField(null=True, blank=True)
    TOTAL_AMOUNT = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True,default=0)

    AMOUNT_PAID  = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True,default=0)
    AMOUNT_BALANCE = models.DecimalField(max_digits=10, decimal_places=2, editable=False,null=True, blank=True)
    STATUS_CHOICES = [
        ('IN PROGRESS', 'IN PROGRESS'),
        ('COMPLETED', 'COMPLETED'),
        ('NA', 'NA'),
        ('CANCELLED', 'CANCELLED'),
    ]
    STATUS=models.CharField(max_length=50, choices=STATUS_CHOICES,default='NA')

    class Meta:
        abstract = True  

    def save(self, *args, **kwargs):
        # Automatically calculate balance, handle None values
        total = self.TOTAL_AMOUNT if self.TOTAL_AMOUNT is not None else 0
        paid = self.AMOUNT_PAID if self.AMOUNT_PAID is not None else 0
        self.AMOUNT_BALANCE = total - paid
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.NAME} - {self.REG_CODE} - {self.PRODUCT_TYPE}"


class NagercoilProductRegistration(AbstractProductRegistration):
    class Meta:
        verbose_name = "Nagercoil Product Registration"
        verbose_name_plural = "Nagercoil Product Registrations"

class TirunelveliProductRegistration(AbstractProductRegistration):
    class Meta:
        verbose_name = "Tirunelveli Product Registration"
        verbose_name_plural = "Tirunelveli Product Registrations"

class PudukottaiProductRegistration(AbstractProductRegistration):
    class Meta:
        verbose_name = "Pudukottai Product Registration"
        verbose_name_plural = "Pudukottai Product Registrations"

class ChennaiProductRegistration(AbstractProductRegistration):
    class Meta:
        verbose_name = "Chennai Product Registration"
        verbose_name_plural = "Chennai Product Registrations"

class AbstractInternshipRegistration(models.Model):
    S_NO=models.IntegerField()
    DATE = models.DateField()
    REG_CODE = models.CharField(max_length=100, unique=True)
    NAME = models.CharField(max_length=255)
    DEPARTMENT = models.CharField(max_length=255)
    INTERNSHIP_TYPE = models.CharField(max_length=100)
    COLLEGE_UNIVERSITY = models.CharField(max_length=255)
    MOBILE_NO = models.CharField(max_length=15)
    EMAIL_ID = models.EmailField()
    TOTAL_AMOUNT = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    AMOUNT_PAID = models.DecimalField(max_digits=10, decimal_places=2)
    AMOUNT_BALANCE = models.DecimalField(max_digits=10, decimal_places=2,editable=False)
    STATUS_CHOICES = [
        ('IN PROGRESS', 'IN PROGRESS'),
        ('COMPLETED', 'COMPLETED'),
        ('NA', 'NA'),
        ('CANCELLED', 'CANCELLED'),
        
    ]
    STATUS=models.CharField(max_length=50, choices=STATUS_CHOICES,default='NA')


    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # Automatically calculate balance
        self.AMOUNT_BALANCE = self.TOTAL_AMOUNT - self.AMOUNT_PAID
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.NAME} - {self.REG_CODE}"

class NagercoilInternshipRegistration(AbstractInternshipRegistration):
    class Meta:
        verbose_name = "Nagercoil Internship Registration"
        verbose_name_plural = "Nagercoil Internship Registrations"

class TirunelveliInternshipRegistration(AbstractInternshipRegistration):
    class Meta:
        verbose_name = "Tirunelveli Internship Registration"
        verbose_name_plural = "Tirunelveli Internship Registrations"

class PudukottaiInternshipRegistration(AbstractInternshipRegistration):
    class Meta:
        verbose_name = "Pudukottai Internship Registration"
        verbose_name_plural = "Pudukottai Internship Registrations"

class ChennaiInternshipRegistration(AbstractInternshipRegistration):
    class Meta:
        verbose_name = "Chennai Internship Registration"
        verbose_name_plural = "Chennai Internship Registrations"

MONTH_CHOICES = [
    ('January', 'January'), ('February', 'February'), ('March', 'March'),
    ('April', 'April'), ('May', 'May'), ('June', 'June'),
    ('July', 'July'), ('August', 'August'), ('September', 'September'),
    ('October', 'October'), ('November', 'November'), ('December', 'December'),
]

YEAR_CHOICES = [(year, str(year)) for year in range(2020, 2031)]

PAYMENT_STATUS_CHOICES = [
    ('PARTIALLY PAID', 'PARTIALLY PAID'),
    ('25% PAID', '25% PAID'),
    ('50% PAID', '50% PAID'),
    ('75% PAID', '75% PAID'),
    ('FULLY PAID', 'FULLY PAID'),
    ('CANCELLED', 'CANCELLED')    
]

class AbstractBill(models.Model):
    S_NO=models.IntegerField()
    DATE = models.DateField()
    MONTH = models.CharField(max_length=10, choices=MONTH_CHOICES,blank=True,default='February')
    YEAR = models.IntegerField(choices=YEAR_CHOICES,default=2026)
    BILL_NUMBER = models.CharField(max_length=100)
    REGISTRATION_NUMBER = models.CharField(max_length=100)
    NAME = models.CharField(max_length=255)
    CASH_RECEIVED = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # MODE_CHOICES = [
    #     ('ONLINE', 'ONLINE'),
    #     ('OFFLINE', 'OFFLINE'),
        
    # ]
    # modeofpayment = models.CharField(max_length=50, choices=MODE_CHOICES)
    ONLINE_RECEIVED = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.NAME} - {self.BILL_NUMBER}"

class NAGERCOILINTERNSHIPBILL(AbstractBill):
    class Meta:
        verbose_name = "Nagercoil Internship Bill"
        verbose_name_plural = "Nagercoil Internship Bills"

class TIRUNELVELIINTERNSHIPBILL(AbstractBill):
    class Meta:
        verbose_name = "Tirunelveli Internship Bill"
        verbose_name_plural = "Tirunelveli Internship Bills"

class PUDUKOTTAIINTERNSHIPBILL(AbstractBill):
    class Meta:
        verbose_name = "Pudukottai Internship Bill"
        verbose_name_plural = "Pudukottai Internship Bills"

class CHENNAIINTERNSHIPBILL(AbstractBill):
    class Meta:
        verbose_name = "Chennai Internship Bill"
        verbose_name_plural = "Chennai Internship Bills"

class NAGERCOILPRODUCTBILL(AbstractBill):
    class Meta:
        verbose_name = "Nagercoil Project Bill"
        verbose_name_plural = "Nagercoil Project Bills"

class TIRUNELVELIPRODUCTBILL(AbstractBill):
    class Meta:
        verbose_name = "Tirunelveli Project Bill"
        verbose_name_plural = "Tirunelveli Project Bills"

class PUDUKOTTAIPRODUCTBILL(AbstractBill):
    class Meta:
        verbose_name = "Pudukottai Project Bill"
        verbose_name_plural = "Pudukottai Project Bills"

class CHENNAIPRODUCTBILL(AbstractBill):
    class Meta:
        verbose_name = "Chennai Project Bill"
        verbose_name_plural = "Chennai Project Bills"

class AbstractTaxInvoice(models.Model):
    INVOICE_NO = models.CharField(max_length=100)
    DATE = models.DateField()
    BILL_TO = models.TextField()
    TOTAL_AMOUNT = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    GST_18 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    TOTAL_AMOUNT_WITH_GST = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ROUND_OFF = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    GRAND_TOTAL = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    AMOUNT_IN_WORDS = models.TextField()

    class Meta:
        abstract = True

    def __str__(self):
        return f"Invoice {self.invoice_no} - {self.date}"

class AbstractTaxInvoiceItem(models.Model):
    S_NO = models.IntegerField()
    DESCRIPTION = models.TextField()
    QTY = models.IntegerField()
    UNIT_PRICE = models.DecimalField(max_digits=10, decimal_places=2)
    TOTAL_VALUE = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        abstract = True

class NAGERCOILTAXINVOICE(AbstractTaxInvoice):
    class Meta:
        verbose_name = "Nagercoil Tax Invoice"
        verbose_name_plural = "Nagercoil Tax Invoices"

class NagercoilTAXINVOICEITEM(AbstractTaxInvoiceItem):
    invoice = models.ForeignKey(NAGERCOILTAXINVOICE, on_delete=models.CASCADE, related_name='items')

class TIRUNELVELITAXINVOICE(AbstractTaxInvoice):
    class Meta:
        verbose_name = "Tirunelveli Tax Invoice"
        verbose_name_plural = "Tirunelveli Tax Invoices"

class TIRUNELVELITAXINVOICEITEM(AbstractTaxInvoiceItem):
    invoice = models.ForeignKey(TIRUNELVELITAXINVOICE, on_delete=models.CASCADE, related_name='items')

class PUDUKOTTAITAXINVOICE(AbstractTaxInvoice):
    class Meta:
        verbose_name = "Pudukottai Tax Invoice"
        verbose_name_plural = "Pudukottai Tax Invoices"

class PUDUKOTTAITAXINVOICEITEM(AbstractTaxInvoiceItem):
    invoice = models.ForeignKey(PUDUKOTTAITAXINVOICE, on_delete=models.CASCADE, related_name='items')

class CHENNAITAXINVOICE(AbstractTaxInvoice):
    class Meta:
        verbose_name = "Chennai Tax Invoice"
        verbose_name_plural = "Chennai Tax Invoices"

class CHENNAITAXINVOICEITEM(AbstractTaxInvoiceItem):
    invoice = models.ForeignKey(CHENNAITAXINVOICE, on_delete=models.CASCADE, related_name='items')
