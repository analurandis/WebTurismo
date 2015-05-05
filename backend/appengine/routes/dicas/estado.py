# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from config.template_middleware import TemplateResponse
from gaepermission.decorator import login_not_required
from tekton import router
from gaecookie.decorator import no_csrf
from routes.dicas.modulo import CidadeForm, EstadoForm, Estado


@login_not_required
@no_csrf
def index():
    contexto={'salvarEstado_path': router.to_path(salvarEstado)}
    return TemplateResponse(contexto)


@login_not_required
@no_csrf
def salvarEstado(_resp, **propriedade):
        estado_form = EstadoForm(**propriedade)
        erros = estado_form.validate()
        if erros:
           contexto = {'salvarEstado_path':router.to_path(salvarEstado),
                       'erros':erros,
                       'estado':estado_form}
           return TemplateResponse(contexto, 'dicas/estado.html')
        else:
            estado = estado_form.fill_model()
            estado.put()
            return TemplateResponse(template_path='dicas/estado.html')