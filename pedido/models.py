# -*- encoding: utf-8 -*-

from django.db import models
from sgo.models import OtifModel
from grade.models import Grade
from cliente.models import Cliente

"""
Modelo de pedidos importados do Totvs ERP via arquivo txt.
Dados importados não estão normalizados.
Modelo possue dados de Cliente, Produtos, Pedidos, NF e Transportadora

Aplicação: Otif

    Modelo: OtifModel (base para todas os modelos)
        dt_atlz
        id_usr_atlz

Aplicação: Pedido

    Modelo: Base
        cd_estab            Código do estabelecimento (JDF, STO, JAG ou OSA)
        nm_ab_cliente       Código do cliente
        nr_nota_fis         Número da Nota fiscal
        nr_pedido           Número do pedido do cliente
        ds_ordem_compra     Número da ordem de compra
        ds_placa            Placa do veículo
        ds_transp           Nome da transportadora
        nr_lacre            Número do Lacre
        dt_hr_chegada       Data e Hora da chegada
        dt_hr_ini_carga     Data e Hora do inicio do carregamento
        dt_hr_fim_carga     Data e Hora do fim do carregamento
        dt_hr_liberacao     Data e Hora da liberação do caminhão

        ds_status_cheg      Calculado (Se hr_chegada > (data e Hr Grade - Limite carga da tabela
                            ARZ_LIMITE_CLIENTE) então "Atrasado" senão "No Horário")

        ds_status_lib       Calculado (Se Hr de Liberação > (data e Hr Grade + Limite Liberacao da tabela
                            ARZ_LIMITE_CLIENTE) então "Atrasado" senão "No Horário")

        ds_obs_carga        Conteúdo livre
        id_no_show          S ou N
        vl_fixo             Valor fixo da multa
        vl_base_multa       Valor base da multa
        vl_multa            Calculado (Se "id_no_show" = S então (("Valor base
                            multa" * 0,05)+"vl_fixo") senão, 0)

    Modelo: Item
        cd_estab            Código do estabelecimento (JDF, STO, JAG ou OSA)
        nm_ab_cliente       Código do cliente
        nr_nota_fis         Número da Nota fiscal
        dt_saida            Data de saída do pedido
        hr_grade            Hora da grade do cliente
        cd_produto          Código do produto
        un_embalagem        Unidade de embalagem
        qt_embalagem        Quantidade de embalagens
        qt_pilha            Quantidade da pilha
        qt_carregada        Quantidade carregada
        qt_falta            Quantidade faltante
        id_motivo
        qt_pallet           Quantidade de pallets
        vl_base_multa       Valor base da multa
        vl_multa            Calculado (Se "id_no_show" = S então (("Valor base
                            multa" * 0,05)+"vl_fixo") senão, 0)
"""



class Base(OtifModel):
    cd_estab = models.CharField('Código do estab.', max_length=3, null='true', blank='true', )
    cliente = models.ForeignKey(Cliente, verbose_name='Cliente', to_field='nm_ab_cli', blank='true', null='true',
                                db_column='nm_ab_cli')
    nr_nota_fis = models.CharField('Número da Nota fiscal', max_length=32, null='true', blank='true', )

    dt_saida = models.DateField('Data de saída do Carregamento', null='true', blank='true', )
    grade = models.ForeignKey(Grade, verbose_name='Hora da grade do cliente', null='true', blank='true', )
    ds_placa = models.CharField('Placa do veículo', max_length=8, null='true', blank='true', )
    ds_transp = models.CharField('Nome da transportadora', max_length=30, null='true', blank='true', )
    nr_lacre = models.CharField('Número do lacre', max_length=10, null='true', blank='true', )
    dt_hr_chegada = models.DateTimeField('Chegada do caminhão', null='true', blank='true', )
    dt_hr_ini_carga = models.DateTimeField('Inicio do carregamento', null='true', blank='true', )
    dt_hr_fim_carga = models.DateTimeField('Fim do carregamento', null='true', blank='true', )
    dt_hr_liberacao = models.DateTimeField('Liberação do caminhão', null='true', blank='true', )
    ds_status_cheg = models.CharField('Status de chegada', max_length=15, null='true', blank='true')
    ds_get_status_lib = models.CharField('Status de liberação', max_length=15, null='true', blank='true')
    ds_obs_carga = models.CharField('Obs', max_length=500, null='true', blank='true', )
    id_no_show = models.CharField('No Show', max_length=1, default= 'N')
    # TODO: separar campos de multa para outra app devido a controle de acesso
    vl_fixo = models.DecimalField('Valor fixo da multa', null='true', blank='true', max_digits=17,
                                  decimal_places=2)
    vl_base_multa = models.DecimalField('Valor base da multa', null='true', blank='true', max_digits=17,
                                        decimal_places=2)
    vl_multa = models.DecimalField('Valor da multa', null='true', blank='true', max_digits=17, decimal_places=2)

    st_chegada = models.CharField('Status de Chegada', max_length=15, null='true', blank='true', default='No Horário')
    st_libera = models.CharField('Status de Liberação', max_length=15, null='true', blank='true', default='No Horário')

    def __unicode__(self):
        return '' or ''.join([self.cd_estab, ]) #' - ', self.cliente.nm_ab_cli, self.nr_nota_fis])

    def set_chegada(self):
        pass

    def set_inicio(self):
        pass

    def set_fim(self):
        pass

    def set_liberacao(self):
        pass

class Item(OtifModel):
    cd_estab = models.CharField('Código do estab.', max_length=3, null='true', blank='true', )
    cliente = models.ForeignKey(Cliente, verbose_name='Cliente', to_field='nm_ab_cli', blank='true', null='true',
                                db_column='nm_ab_cli')
    nr_nota_fis = models.CharField('Número da Nota fiscal', max_length=32, null='true', blank='true', )

    nr_pedido = models.CharField('Número do pedido do cliente', max_length=24, null='true', blank='true', )
    ds_ord_compra = models.CharField('Número da ordem de compra', max_length=15, null='true', blank='true', )
    cd_produto = models.CharField('Código do produto', max_length=32, null='true', blank='true', )
    un_embalagem = models.CharField('Unidade de embalagem', max_length=3, null='true', blank='true', )
    qt_embalagem = models.IntegerField('Quantidade de embalagens', null='true', blank='true', )
    qt_pilha = models.CharField('Quantidade da pilha', max_length=10, null='true', blank='true', )
    qt_carregada = models.IntegerField('Quantidade carregada', null='true', blank='true', )
    qt_falta = models.IntegerField('Quantidade em falta', null='true', blank='true', )
    id_motivo = models.IntegerField('Motivo', null='true', blank='true', )
    qt_pallet = models.IntegerField('Quantidade de Pallets', null='true', blank='true', )
    # TODO: separar campos de multa para outra app devido a controle de acesso
    vl_base_multa = models.DecimalField ('Valor base da multa', null='true', blank='true', max_digits=17,
                                         decimal_places=2)
    vl_multa =  models.DecimalField ('Valor da multa', null='true', blank='true', max_digits=17, decimal_places=2)
    base = models.ForeignKey(Base)
    def __unicode__(self):
        return self.cd_produto or ''
