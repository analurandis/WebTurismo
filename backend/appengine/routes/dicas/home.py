# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required
from routes.dicas.modulo import Dicas, Cidade


@login_not_required
@no_csrf
def index():
    contexto = {'dicas_lista' : Dicas.query_ordenada_por_data().fetch()}
    return TemplateResponse(contexto,template_path='/dicas/home.html')

