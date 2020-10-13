from functools import wraps
from flask import request, jsonify
from marshmallow import ValidationError
from error_handlers import ApiError


def parse_with(schema):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            form_data = request.form
            if form_data:
                data = {}
                for key in form_data.keys():
                    if form_data.getlist(key) and len(form_data.getlist(key)) > 1:
                        data[key] = form_data.getlist(key)
                    else:
                        data[key] = form_data[key]
            else:
                data = request.get_json()
            try:
                entity = schema.load(data)
            except ValidationError as err:
                if args:
                    api_error = args[0]
                    if isinstance(api_error, ApiError):
                        return (
                            jsonify({"error": True, "message": api_error.message}),
                            api_error.status_code,
                        )
                return jsonify(error=True, messages=err.messages), 400
            return f(entity, *args, **kwargs)

        return decorated_function

    return decorator


def get_status_code_success(method):
    if method == "POST":
        return 201
    if method == "DELETE":
        return 202
    return 200


def marshal_with(schema):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            response = schema.dump(f(*args, **kwargs))
            status_code = response.get(
                "status_code", get_status_code_success(request.method)
            )
            return jsonify(response), status_code

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
                    data[argument.name] = argument.type(params.get(argument.name))
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