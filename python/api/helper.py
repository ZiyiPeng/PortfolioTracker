import traceback


def response_on_error(error_msg, error_code):
    def decorator(fun):
        def applicator(*args, **kwargs):
            try:
                return_body, code = fun(*args, **kwargs)
                return {'data': return_body}, code
            except Exception as e:
                error_body = {
                    'message': error_msg,
                    'error': str(e),
                    'stack_trace': traceback.format_exc()
                }
                return {'data': error_body}, error_code
        return applicator
    return decorator
