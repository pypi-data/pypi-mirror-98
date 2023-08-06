from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from souschef.order.views import (
    OrderList,
    OrderDetail,
    CreateOrder,
    CreateOrdersBatch,
    UpdateOrder,
    UpdateOrderStatus,
    CreateDeleteOrderClientBill,
    DeleteOrder)

app_name = "order"

urlpatterns = [
    url(_(r'^list/$'), OrderList.as_view(), name='list'),
    url(_(r'^view/(?P<pk>\d+)/$'), OrderDetail.as_view(), name='view'),
    url(_(r'^create/$'), CreateOrder.as_view(), name='create'),
    # Multiple orders as once
    url(_(r'^create/batch$'),
        CreateOrdersBatch.as_view(), name='create_batch'),

    url(_(r'^update/(?P<pk>\d+)/$'), UpdateOrder.as_view(), name='update'),
    url(
        _(r'^update/(?P<pk>\d+)/status$'),
        UpdateOrderStatus.as_view(),
        name='update_status'
    ),
    url(
        _(r'^update/(?P<pk>\d+)/client_bill$'),
        CreateDeleteOrderClientBill.as_view(),
        name='update_client_bill'
    ),
    url(_(r'^delete/(?P<pk>\d+)/$'), DeleteOrder.as_view(), name='delete'),
]
