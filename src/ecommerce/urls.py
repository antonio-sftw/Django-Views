from django.urls import path

from ecommerce import views

urlpatterns = [
    path("", views.home, name="home"),
    path("productos", views.list_products, name="products"),
    path("productos/<int:product_id>", views.detail_products, name="detail_products"), # Se pasa el id del registro como parámetro y se especifica que es un entero
    path("productos/create", views.create_products, name="create_products"),
    path("productos/<int:product_id>/update", views.update_products, name="update_products"), # Se pasa el id del registro como parámetro y se especifica que es un entero
    path("productos/<int:product_id>/delete", views.delete_products, name="delete_products"), # Se pasa el id del registro como parámetro y se especifica que es un entero
    path("redirect", views.redirect_to_about, name="about"),
]
