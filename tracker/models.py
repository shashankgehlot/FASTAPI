from mongoengine import Document, StringField, DateTimeField, DictField, connect


class Event(Document):
    event_type = StringField(required=True)
    event_details = DictField()  # Store event-specific details
    timestamp = DateTimeField(required=True)
    user_id = StringField(required=True)
    device = StringField(required=True)  # Store device information
    ip_address = StringField(required=True)  # Store IP address

    meta = {
        'indexes': [
            'user_id',
            '-timestamp'
        ]
    }