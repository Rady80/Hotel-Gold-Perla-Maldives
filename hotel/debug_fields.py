# debug_fields.py

from hotel.models import Announcement

# Získání všech polí modelu Announcement
fields = Announcement._meta.get_fields()
for field in fields:
    print(f"Field name: {field.name}, Field type: {field.get_internal_type()}")