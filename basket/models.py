from django.db import models
from books.models import Books

class Order(models.Model):
    STATUS_CHOICES = (
        ('new', 'Новый'),
        ('processing', 'В обработке'),
        ('done', 'Выполнен'),
        ('cancelled', 'Отменён'),
    )

    customer_name = models.CharField("Имя покупателя", max_length=200)
    customer_phone = models.CharField("Телефон", max_length=50, blank=True)
    customer_email = models.EmailField("Email", blank=True)
    customer_address = models.TextField("Адрес", blank=True)
    book = models.ForeignKey('books.Books', on_delete=models.CASCADE, related_name='orders', verbose_name="Книга")
    quantity = models.PositiveIntegerField("Количество", default=1)
    status = models.CharField("Статус заказа", max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    def __str__(self):
        return f"{self.customer_name} — {self.book} ({self.quantity})"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-created_at']