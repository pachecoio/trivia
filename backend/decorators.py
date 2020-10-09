from functools import wraps
from flask import request, jsonify
from marshmallow import ValidationError


def parse_with(schema, many=False):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data = {}
            form_data = request.form
            if form_data:
                for key in form_data.keys():
                    if form_data.getlist(key) and len(form_data.getlist(key)) > 1:
                        data[key] = form_data.getlist(key)
                    else:
                        data[key] = form_data[key]
            else:
                data = request.get_json()
            try:
                entity = schema(many=many).load(data)
            except ValidationError as err:
                return jsonify(error=True, messages=err.messages), 400
            return f(entity, *args, **kwargs)

        return decorated_function

    return decorator


def marshal_with(schema):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            response = f(*args, **kwargs)
            return jsonify(schema.dump(response))

        return decorated_function

    return decorator


def parse_request(arguments):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data = dict(**kwargs)
            params = request.args
            for argument in arguments:
                if params.get(argument.name):
                    data[argument.name] = params.get(argument.name)
                elif argument.default:
                    data[argument.name] = argument.default
                elif argument.required:
                    return (
                        jsonify(
                            error=True,
                            messages="Parameter {} is required".format(argument.name),
                        ),
                        400,
                    )
            return f(*args, **data)

        return decorated_function

    return decorator


class Argument(object):
    def __init__(
        self,
        name,
        default=None,
        type=str,
        required=False,
    ):
        self.name = name
        self.default = default
        self.type = type
        self.required = required