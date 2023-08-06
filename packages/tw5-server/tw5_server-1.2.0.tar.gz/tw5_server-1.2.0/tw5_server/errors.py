from flask import make_response, render_template


def unauthorized(e):
    resp = make_response(render_template('401.html'))
    resp.headers['WWW-Authenticate'] = 'Basic realm=""'
    resp.status_code = 401
    return resp


def page_not_found(e):
    return render_template('404.html')


def permission_denied(e):
    return render_template('403.html')


def register_errors(app):
    app.register_error_handler(401, unauthorized)
    app.register_error_handler(403, permission_denied)
    app.register_error_handler(404, page_not_found)
