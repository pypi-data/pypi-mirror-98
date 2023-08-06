def call_right_serializer_by_instance(meth):

    def _wrapper(self, instance, *args, **kwargs):

        # Check if there is a fields data in the arguments
        # if exists take type of the new data instead of the
        # instance type.
        if args:
            field = args[0]
            type_id = field[self.lookup_field]
        else:
            type_id = getattr(instance, self.lookup_field)

        kwargs.pop('context', {})
        serializer = self.get_right_serializer(type_id)
        meth_name = getattr(serializer, meth.__name__)
        return meth_name(instance, *args, **kwargs)

    return _wrapper


def call_right_serializer_by_attrs(meth):

    def _wrapper(self, attrs, *args, **kwargs):
        lookup = self.lookup_field
        serializer = self.get_right_serializer(attrs[lookup])
        context = kwargs.pop('context', {})
        serializer.custom_context = context
        meth_name = getattr(serializer, meth.__name__)
        return meth_name(attrs, *args, **kwargs)

    return _wrapper


def call_all_serializer(meth):

    def _wrapper(self, *args, **kwargs):
        kwargs.pop('context', {})
        for serializer in self.get_all_serializer():
            meth_name = getattr(serializer, meth.__name__)
            return meth_name(*args, **kwargs)

    return _wrapper


class LazyChildProxy:

    def __init__(self, register):
        self.lookup_field = register.lookup_field
        self.register = {
            key: value() for key, value in register.items()
        }

    def get_right_serializer(self, type_id):
        return self.register[type_id]

    def get_all_serializer(self):
        return [serializer for serializer in self.register.values()]

    @call_right_serializer_by_instance
    def to_representation(self, instance):
        pass

    @call_all_serializer
    def bind(self, *args, **kwargs):
        pass

    @call_right_serializer_by_attrs
    def run_validation(self, context=None):
        pass

    @call_right_serializer_by_attrs
    def create(self, attrs):
        pass

    @call_right_serializer_by_instance
    def update(self, instance, validated_data):
        pass
