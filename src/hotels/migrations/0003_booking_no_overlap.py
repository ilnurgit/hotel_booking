from django.contrib.postgres.constraints import ExclusionConstraint
from django.contrib.postgres.fields import DateRangeField
from django.contrib.postgres.fields.ranges import RangeOperators
from django.contrib.postgres.operations import BtreeGistExtension
from django.db import migrations
from django.db.models import F, Func, Value


class Migration(migrations.Migration):
    dependencies = [
        ("hotels", "0002_booking"),  # проверь, что у тебя booking именно в 0002
    ]

    operations = [
        # 1) включаем расширение btree_gist (нужно для GiST по равенству room_id)
        BtreeGistExtension(),
        # 2) добавляем ограничение "не пересекаться" по daterange
        migrations.AddConstraint(
            model_name="booking",
            constraint=ExclusionConstraint(
                name="booking_no_overlap_per_room",
                expressions=[
                    (F("room"), RangeOperators.EQUAL),
                    (
                        Func(
                            F("date_start"),
                            F("date_end"),
                            Value("[)"),
                            function="daterange",
                            output_field=DateRangeField(),
                        ),
                        RangeOperators.OVERLAPS,
                    ),
                ],
            ),
        ),
    ]
