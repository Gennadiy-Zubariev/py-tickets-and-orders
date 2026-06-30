from datetime import datetime
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket

User = get_user_model()


def create_order(
        tickets: list[dict],
        username: str,
        date: datetime | None = None
) -> Order:
    with transaction.atomic():
        user, _ = User.objects.get_or_create(username=username)
        order = Order.objects.create(user=user)
        if date:
            order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
            order.save()

        for ticket in tickets:
            Ticket.objects.create(
                order=order,
                movie_session_id=ticket["movie_session"],
                row=ticket["row"],
                seat=ticket["seat"],
            )

    return order


def get_orders(username: str | None = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
