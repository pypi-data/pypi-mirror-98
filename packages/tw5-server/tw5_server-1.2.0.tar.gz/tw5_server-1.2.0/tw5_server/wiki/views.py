from flask import abort, current_app, request, send_file
from flask.views import MethodView
from . import auth, bp, storage


class WikiView(MethodView):
    decorators = (auth.view_permission_required, )

    def get(self, wiki_name='demo'):
        wiki = storage.Wiki(wiki_name)
        if not wiki.file.exists():
            abort(404)
        return send_file(wiki.file)

    def post(self, wiki_name='demo'):
        params = self.split_params(request.form.get('UploadPlugin', ''))
        password = params.get('password')
        if not auth.can_write(wiki_name, password):
            abort(401)
        file_obj = request.files.get('userfile')
        if not file_obj or file_obj.mimetype != 'text/html':
            abort(400)
        wiki = storage.GitStorage(wiki_name)
        if not wiki.exists():
            abort(404)
        wiki.update(file_obj.stream)
        return '0 - '

    @staticmethod
    def split_params(param_str):
        dct = {}
        for param in param_str.split(';'):
            if not param:
                continue
            try:
                key, value = param.split('=', 1)
            except ValueError:
                continue
            dct[key] = value
        return dct


bp.add_url_rule('/<string:wiki_name>',
                view_func=WikiView.as_view('wiki'),
                methods=['GET', 'POST'])
