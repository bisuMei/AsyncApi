"""App constants."""


class ConstantContainer(type):
    """Add some handy methods to container class."""

    def __new__(mcs, name, bases, attrs):
        """Attach method to class."""
        cls = super().__new__(mcs, name, bases, attrs)
        constant_values = []
        for attr_name, attr_value in attrs.items():
            if not attr_name.startswith("__"):
                constant_values.append(attr_value)
        cls.get_constant_values = lambda: tuple(constant_values)
        return cls


ACCESS_TOKEN_TTL = 1  # one hour


class USER_ROLES(metaclass=ConstantContainer):

    admin = "ADMIN"
    superuser = "SUPERUSER"
    subscriber = "SUBSCRIBER"
    default = "USER"


class ACTION(metaclass=ConstantContainer):

    films = "films"
    persons = "persons"
    genres = "genres"
    film_by_id = "film_by_id"
    film_by_person = "film_by_person"
    genre_by_id = "genre_by_id"
    person_by_id = "person_by_id"


class PERMISSIONS(metaclass=ConstantContainer):

    superuser_permissions = {
        'ALL_PERMISSION': {
            'read': True,
            'create': True,
            'update': True,
            'delete': True,
        }
    }

    default_permissions = {
        'MOVIES': {
            'create': False,
            'read': True,
            'update': False,
            'delete': False,
        },
    }

    subscriber_permissions = {
        'MOVIES': {
            'read': True,
            'create': False,
            'update': False,
            'delete': False,
        },
        'GENRES': {
            'read': True,
            'create': False,
            'update': False,
            'delete': False,
        },
    }

    admin_permissions = {
        'MOVIES': {
            'create': True,
            'read': True,
            'update': True,
            'delete': True,
        },
        'GENRES': {
            'read': True,
            'create': False,
            'update': False,
            'delete': False,
        },
        'PERSONS': {
            'read': True,
            'create': False,
            'update': False,
            'delete': False,
        },
    }


ALLOWED_USER_ROLES_SUBSCRIBER_ACCESS = (
    USER_ROLES.superuser,
    USER_ROLES.admin,
    USER_ROLES.subscriber,
)
