# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from compiler.pyassem import order_blocks
from google.appengine.ext import ndb
from config.template_middleware import TemplateResponse
from gaeforms.ndb.form import ModelForm
from gaegraph.model import Node



class Dicas (Node):
    cidade = ndb.KeyProperty( required=True)
    titulo = ndb.StringProperty(required=True)
    datas = ndb.DateProperty(auto_now=True)
    dica = ndb.StringProperty(required=True)
    city = ndb.StringProperty()

    @classmethod
    def query_ordenada_por_nome(cls):
        return cls.query().order(Dicas.titulo)


    @classmethod
    def query_buscar_por_ID(cls,dic_selecionada):
        if isinstance(dic_selecionada, basestring):
            dic_selecionada=ndb.Key(Dicas, int(dic_selecionada))
        return cls.query(dic_selecionada==cls.key)


    @classmethod
    def query_ordenada_por_nome_com_cidade(cls,cidID):
        return cls.query(cidID==Cidade.query_ordenada_por_nome()).order(Dicas.titulo)

    @classmethod
    def query_ordenada_por_data(cls):
        return cls.query().order(Dicas.titulo)

    @classmethod
    def query_buscarCidade(cls,cidade):
        cidadeb = Cidade.query_bucarCidade_por_ID(cidade).fetch()
        return cidadeb

    @classmethod
    def query_buscar_dica(cls, cidade_selecionada):
        if isinstance(cidade_selecionada, basestring):
            cidade_selecionada=ndb.Key(Cidade, int(cidade_selecionada))
        return cls.query(cls.cidade==cidade_selecionada).order(cls.titulo)

    @classmethod
    def query_buscar_dica_Estado(cls, estado_selecionado):
        if isinstance(estado_selecionado, basestring):
            estado_selecionado=ndb.Key(Estado, int(estado_selecionado))
        return cls.query(Cidade.estado==estado_selecionado).order(cls.titulo)


class DicasForm(ModelForm):
    _model_class = Dicas
    _include = [Dicas.titulo, Dicas.datas, Dicas.dica,Dicas.cidade,Dicas.city]





class DicasFormTable(ModelForm):
    _model_class = Dicas
    _include = [ Dicas.titulo, Dicas.datas, Dicas.dica]



class Cidade (Node):
    cidade = ndb.StringProperty(required=True)
    estado=ndb.KeyProperty(required=True)

    @classmethod
    def query_ordenada_por_nome(cls):
        return cls.query().order(Cidade.cidade)

    @classmethod
    def query_buscar_cid_por_ID(cls,cidade):
            if isinstance(cidade, basestring):
                cidade=ndb.Key(Dicas, int(cidade))
            return cls.query(cidade==cls.key)




    @classmethod
    def query_por_estado_cidade_por_nome(cls, estado_selecionada):
        if isinstance(estado_selecionada, basestring):
            estado_selecionada=ndb.Key(Estado, int(estado_selecionada))
        return cls.query(cls.estado==estado_selecionada).order(cls.cidade)





class CidadeForm(ModelForm):
    _model_class = Cidade
    _include = [Cidade.cidade, Cidade.estado]


class CidadeFormTable(ModelForm):
    _model_class = Cidade
    _include = [Cidade.cidade]




class Estado (Node):
    estado = ndb.StringProperty(required=True)
    sigla = ndb.StringProperty(required=True)

    @classmethod
    def query_ordenada_por_nome(cls):
        return cls.query().order(Estado.estado)

    @classmethod
    def query_buscarID(cls,estado_s):
        return cls.query(Estado.get_by_id==estado_s)


class EstadoForm(ModelForm):
    _model_class = Estado
    _include = [Estado.estado,Estado.sigla]


class EstadoFormTable(ModelForm):
    _model_class = Estado
    _include = [Estado.estado,Estado.sigla]
