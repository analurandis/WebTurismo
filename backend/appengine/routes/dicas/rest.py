# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required
from routes.dicas.modulo import Dicas, DicasForm, Cidade
from tekton.gae.middleware.json_middleware import JsonUnsecureResponse


@login_not_required
@no_csrf
def apagar(dica_id):
    key = ndb.Key(Dicas, int(dica_id))
    key.delete()
    return JsonUnsecureResponse('') # para setar cabeçalho para aplpication/json


@login_not_required
@no_csrf
def listar():
    form = DicasForm()
    dicas = Dicas.query_ordenada_por_nome().fetch()
    dicas = [form.fill_with_model(p) for p in dicas]
    return JsonUnsecureResponse(dicas)


@login_not_required
@no_csrf
def salvar(_resp, **propriedades):
    propriedades['cidade']=Cidade.get_by_id(int(propriedades['cidade']))
    form = DicasForm(**propriedades)
    erros = form.validate()
    if not erros:
        dica = form.fill_model()
        dica.put()
        dct = form.fill_with_model(dica)
        return JsonUnsecureResponse(dct)
    _resp.set_status(400)
    return JsonUnsecureResponse(erros)