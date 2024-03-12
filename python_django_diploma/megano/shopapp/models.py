from django.db import models


class CategoryImage(models.Model):
    """Модель для хранения иконки категории"""

    src = models.ImageField(
        upload_to="categories",
        default="categories/default.png",
        verbose_name="Ссылка",
    )
    alt = models.CharField(
        default="category image", max_length=128, verbose_name="Описание"
    )

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"


class Category(models.Model):
    title = models.CharField(blank=False, max_length=128, verbose_name="Категория")
    parent = models.ForeignKey(
        "self",
        blank=True,
        null=True,
        related_name="subcategories",
        on_delete=models.CASCADE,
    )
    image = models.ForeignKey(
        CategoryImage,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="category",
        verbose_name="Изображение",
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        index_together = ["id", "parent"]

    def __str__(self):
        return f"Категория: {self.title}, pk={self.id}"


class Tag(models.Model):
    name = models.CharField(blank=False, max_length=42)

    def __str__(self):
        return f"{self.name!r} (pk={self.pk})"


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        null=False,
        on_delete=models.CASCADE,
        related_name="product",
        verbose_name="Категория",
    )
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    count = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(blank=False, max_length=128, verbose_name="Товар")
    description = models.CharField(
        default="Описание товара", max_length=256, verbose_name="Описание товара"
    )
    fullDescription = models.TextField(
        default="Подробное описание товара", verbose_name="Подробное описание товара"
    )
    freeDelivery = models.BooleanField(default=False)
    rating = models.DecimalField(default=5, max_digits=2, decimal_places=1)
    tags = models.ManyToManyField(Tag, blank=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return f"{self.title!r} (pk={self.pk})"


def product_images_directory_path(instance: "ProductImage", filename):
    return "products/product_{pk}/images/{filename}".format(
        pk=instance.product.pk,
        filename=filename,
    )


class ProductImage(models.Model):
    """Модель для хранения изображения товара"""

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    src = models.ImageField(
        upload_to=product_images_directory_path, verbose_name="Ссылка"
    )
    alt = models.CharField(
        default="product image", max_length=128, verbose_name="Описание"
    )

    class Meta:
        verbose_name = "Изображение товара"
        verbose_name_plural = "Изображения товара"

    def __str__(self):
        return f"{self.alt} ({self.product.title!r})"


class Specification(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="specifications"
    )
    name = models.CharField(blank=False, max_length=64, verbose_name="Характеристика")
    value = models.CharField(blank=False, max_length=128, verbose_name="Значение")

    class Meta:
        verbose_name = "Характеристики"
        verbose_name_plural = "Характеристики"

    def __str__(self):
        return f"({self.product.title!r}) {self.name}: {self.value}"


class Review(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    author = models.CharField(blank=False, max_length=128, verbose_name="Автор")
    email = models.EmailField(blank=False, max_length=128, verbose_name="e-mail")
    text = models.TextField(blank=False, verbose_name="Текст отзыва")
    rate = models.PositiveSmallIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f"{self.text[:30]} ({self.product.title[:10]}) ({self.rate})"


class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="sales")
    salePrice = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name="цена со скидкой"
    )
    dateFrom = models.DateField(verbose_name="старт продаж")
    dateTo = models.DateField(verbose_name="окончание продаж")

    def price(self):
        return self.product.price

    def title(self):
        return self.product.title

    def clean(self):
        if self.dateTo < self.dateFrom:
            self.dateTo, self.dateFrom = self.dateFrom, self.dateTo

    def __str__(self):
        return f'{self.product.title} [{self.dateFrom.strftime("%m-%e")} - {self.dateTo.strftime("%m-%e")}] (${self.salePrice})'
