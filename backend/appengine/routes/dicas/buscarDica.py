# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from config.template_middleware import TemplateResponse
from gaepermission.decorator import login_not_required
from tekton import router
from gaecookie.decorator import no_csrf
from routes.dicas.modulo import Cidade, Estado, Dicas, DicasForm
from tekton.gae.middleware.redirect import RedirectResponse


@login_not_required
@no_csrf
def index(estado_selecionado=None):
    ctx={'pesquisar_path': router.to_path(pesquisar)}
    if estado_selecionado is None:
        ctx['estado']=Estado.query_ordenada_por_nome().fetch()
        ctx['estado_selecionado'] = None
    else:
        ctx['estado_selecionado'] = Estado.get_by_id(int(estado_selecionado))
        ctx['cidade']=Cidade.query_por_estado_cidade_por_nome(estado_selecionado).fetch()
    return TemplateResponse(ctx,'dicas/buscarDica.html')



    #ctx={'salvar_path': router.to_path(salvar)}
    #return TemplateResponse(ctx,'dicas/form.html')


@login_not_required
@no_csrf
def pesquisar(_resp, estado_selecionado = None):
    ctx={'buscar_path': router.to_path(buscar)}
    if estado_selecionado is None:
        ctx['cidade']='Selecione um estado'
        ctx['estado_selecionado'] = None
    else:
        ctx['estado_selecionado'] = Estado.get_by_id(int(estado_selecionado))
        ctx['cidade']=Cidade.query_por_estado_cidade_por_nome(estado_selecionado).fetch()

    return TemplateResponse(ctx,template_path='dicas/buscarDica.html')




@login_not_required
@no_csrf
def buscar(_resp, cidade_selecionada = None, estado_selecionado=None):
    ctx={'lista_path': router.to_path(lista)}
    if cidade_selecionada is None:
        ctx['cidade'] = None
    if estado_selecionado is not None:
        ctx['dica']=Dicas.query_ordenada_por_nome().fetch()
    else:
        ctx['dica']=Dicas.query_buscar_dica(cidade_selecionada).fetch()
        if ctx['dica'] != []:
            return TemplateResponse(ctx,template_path='dicas/buscarDica.html')
    return RedirectResponse(router.to_path(index))


@login_not_required
@no_csrf
def lista(_resp, dic_selecionada):
    contexto={'dic_selecionada': dic_selecionada,
              'editar_path': router.to_path(editar),
              'excluir_path':router.to_path(excluir)}
    if dic_selecionada is None:
        contexto['dic_selecionada']=None
    else:
        dica = Dicas.get_by_id(int(dic_selecionada))
        dica_form = DicasForm()
        dica_form.fill_with_model(dica)
        contexto['dica_retorno'] = dica_form

    return TemplateResponse(contexto,template_path='dicas/editar.html')

@login_not_required
@no_csrf
def excluir(_resp, dic_selecionada, **propriedades):
        contexto = propriedades
        propriedades['cidade']=Cidade.get_by_id(int(propriedades['cidade']))
        contexto = propriedades
        dica = Dicas.get_by_id(int(dic_selecionada))
        dicas_form = DicasForm(**propriedades)
        erros = dicas_form.validate()

        if erros:
            contexto = {'editar_path':router.to_path(editar),
                        'erros':erros,
                        'dica':dicas_form}

            return TemplateResponse(contexto, 'dicas/editar.html')
        else:

            chave = ndb.Key(Dicas, int(dic_selecionada))
            chave.delete()
            return RedirectResponse(router.to_path(index))


@login_not_required
@no_csrf
def editar(_resp, dic_selecionada, **propriedades):
        _resp.write(propriedades)
        _resp.write(dic_selecionada)
        contexto = propriedades
        cidade_retorno =  propriedades['cidade']
        propriedades['cidade']=Cidade.get_by_id(int(propriedades['cidade']))
        contexto = propriedades
        dica = Dicas.get_by_id(int(dic_selecionada))
        dicas_form = DicasForm(**propriedades)
        erros = dicas_form.validate()
        if erros:
            contexto = {'editar_path':router.to_path(editar),
                        'erros':erros,
                        'dica_retorno':dicas_form,
                        'dic_selecionada':dic_selecionada,
                        'cidade_retorno':cidade_retorno}
            _resp.write('contexto               kmkkmkllmlm')
            _resp.write(contexto)

            return TemplateResponse(contexto, 'dicas/editar.html')
        else:
            dicas_form.fill_model(dica)
            dica.put()
            return RedirectResponse(router.to_path(index))