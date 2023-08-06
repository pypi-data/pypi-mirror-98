# Mindset Requests
![pyver](https://img.shields.io/badge/python-3.6%2B-blue)
[![codecov](https://codecov.io/bb/grupolinsferrao/pypck-lins-mindset-requests/branch/master/graph/badge.svg?token=0xs0SKv68m)](https://codecov.io/bb/grupolinsferrao/pypck-lins-mindset-requests)

Pacote para consumo dos endpoints da [Api Mindset](http://apis-sandbox.lojaspompeia.com.br/mindset/v1).

### Variáveis de ambiente

Este projeto depende das variáveis de ambiente abaixo.

```python
API_INTEGRACAO_URL="http://api-mindset-url"
API_INTEGRACAO_USERNAME="api-mindset-username"
API_INTEGRACAO_PASSWORD="api-mindset-password"
DATA_PADRAO_INTEGRACAO="2020-04-01T00:00:00.000"
REQUEST_TIMEOUT="5" # Inteiro. Define o tempo máximo de espera pela resposta (opcional). Se não definida o padrão são 5 segundos.
```

# Servico

Módulo responsável pelas operações no endpoint **servico**

```python
>>> from mindset.api_requests import Servico
>>> servico = Servico('novo_servico')
```

## servico.get_or_create(service_params={})

**service_params:dict (opcional)**

Exceto pelo **filtrar**, todos os métodos da classe dependem da chamada anterior do **.get_or_create()**

Caso o `service_params` não seja informado, e o serviço não exista o mesmo será criado com os seguintes dados:


```python
self.service_params = {
  'servico': self.nome_servico, # 'novo_servico'
  'hora_agendamento': '01:00',
  'forcar_execucao': True,
  'ativo': True,
  'tipo': 'entrada',
}
```
Se informado os dados acima serão atualizados e o serviço criado.
```python
>>> response, json = servico.get_or_create()  # <-- REQUIREMENT: Chamar a função get or create.
>>> json
>>> {'_id': '5fad3131ede2d05c6f5ba65d',
 'servico': 'teste',
 'hora_agendamento': '01:00:00',
 'forcar_execucao': True,
 'ativo': True,
 'tipo': 'entrada'}
```

Essa função retorna uma tupla `(response, json)` pois quando o servico existe, o json retorna em uma lista e quando é criado retorna um json. Internamente, o método trabalha para retornar o json.

## servico.filtrar(filter_params={})
Método estático

**filter_params:dict (opcional)**

```python
>>> len(Servico.filtrar().json()) # Sem o filter params, retorna todos os servicos
>>> 25
>>> response = servico.filtrar({'forcar_execucao': False, 'servico': 'minmaxitem-GANG'})
>>> response.json()
>>> [{'_id': '5fabf3cfd96a08315416997b',
  'servico': 'minmaxitem-GANG',
  'hora_agendamento': '01:00:00',
  'forcar_execucao': False,
  'ativo': True,
  'tipo': 'entrada'}]
```

Para mais informações dos filtros, consulte [Mindset Servicos](http://apis-sandbox.lojaspompeia.com.br/mindset/v1#!/servicos/servicos_list).

## servico.get_id()

Retorna o id do servico

```python
>>> servico.get_id()
>>> '5fac5958d96a0831541699ca'
```

## servico.forcar_execucao()

Retorna se a execução forçada do servico é True ou False

```python
>>> servico.forcar_execucao()
>>> True
```

## servico.inicia_integracao()

Define o status do servico como "E" (execução).

```python
>>> response = servico.inicia_integracao()
>>> response.json()
>>> {'data': 'Status do Serviço definido como "E"!'}
```

Retorna 400 se o status já está definido como "E"

```python
>>> response = servico.inicia_integracao()
>>> response.json()
>>> {'code': 400,
 'error_code': 'invalid',
 'message': 'Entrada inválida.',
 'data': {'general': ['Processo de Integração já está em execução!']}}
```

## servico.sucesso_integracao()

Define o status do servico como "S" (sucesso).

```python
>>> response = servico.sucesso_integracao()
>>> response.json()
>>> {'data': 'Status do Serviço definido como "S"!'}
```

Retorna 400 se o servico não está setado como "E".

```python
>>> response = servico.sucesso_integracao()
>>> response.json()
>>> {'code': 400,
 'error_code': 'invalid',
 'message': 'Entrada inválida.',
 'data': {'general': ['Processo de Integração não está em execução!']}}
```

## servico.falha_integracao()

Define o status do servico como "F" (falha).

```python
>>> response = servico.falha_integracao()
>>> response.json()
>>> {'data': 'Status do Serviço definido como "F"!'}
```

Retorna 400 se o servico não está setado como "E".

```python
>>> response = servico.falha_integracao()
>>> response.json()
>>> {'code': 400,
 'error_code': 'invalid',
 'message': 'Entrada inválida.',
 'data': {'general': ['Processo de Integração não está em execução!']}}
```


## servico.get_data_ultima_integracao(filter_params={})
Busca, trata e retorna a data da última integração do serviço ou o valor da variável de ambiente `DATA_PADRAO_INTEGRACAO`.


**filter_params:dict** (opcional)

Este método possui esses valores de busca padrão:
```python
{
  '_id_servico': self.id, # busca id do servico pela função get_id()
  'status': 'S',
  'fields': 'inicio_execucao',
  'sort': '-inicio_execucao',
  'per_page': 1,
}
```
Caso queira modificar, informe os parâmetros no filter_params e os dados acima serão atualizados.

```python
>>> query_params.get_data_ultima_integracao()
>>> '2020-11-12T00:00:00'
```

## servico.update(json)
Atualiza dados do servico.

```python
>>> response, json = servico.get_or_create()
>>> json
>>> {'_id': '5fac5958d96a0831541699ca',
 'servico': 'teste',
 'hora_agendamento': '01:00:00',
 'forcar_execucao': False,
 'ativo': True,
 'tipo': 'entrada'}
>>> response = servico.update({'forcar_execucao': True, 'hora_agendamento': '02:00:00'})
>>> response.json()
>>> {'_id': '5fac5958d96a0831541699ca',
 'servico': 'teste',
 'hora_agendamento': '02:00:00',
 'forcar_execucao': True,
 'ativo': True,
 'tipo': 'entrada'}
```

## servico.delete()
Remove servico.

```python
>>> response = servico.delete()
>>> response.json()
>>> {'data': 'Serviço deletado com sucesso.'}
```

## servico.status()
Retorna todos os status do serviço

```python
>>> response = servico.status()
>>> response.json()
>>> [{'_id': '5fad8dc2ca8d874caa8154e0',
  '_id_servico': '5fad8dc1ca8d874caa8154de',
  'inicio_execucao': '2020-11-12T19:32:18.312000',
  'fim_execucao': '2020-11-12T19:32:18.506000',
  'status': 'S'}]
```

## servico.em_execucao()
Retorna se o servico está definido como "em execução".

```python
>>> servico.em_execucao()
>>> False
>>> servico.inicia_integracao()
>>> <Response [200]>
>>> servico.em_execucao()
>>> True
```

## servico.executado()
Retorna se o servico foi ou não executado.

```python
>>> servico.executado()
>>> False
```

## servico.pode_integrar()
Retorna se o servico pode ser integrado.

```python
>>> servico.pode_integrar()
>>> False
```

# Controle

Módulo responsável pelas operações no endpoint **controle**.

Os métodos desta classe são estáticos.

## Controle.get(filter_params={})

**filter_params:dict** (opcional)

```python
>>> len(Controle.get().json()) # Retorna todos os controles
>>> 25
```

```python
>>> response = Controle.get({'per_page': 2}) # Filtragem por limite
>>> response.json()
>>> [{'servico': 'produtos-POMPEIA',
  '_id': '5edfdfc57a6f51710fa6ef90',
  '_id_servico': '5edfdfc57a6f51710fa6ef8f',
  'executado': False},
 {'servico': 'pedidos_gang-GANG',
  '_id': '5edfecdb1421779a4f49cf57',
  '_id_servico': '5edfecdb1421779a4f49cf56',
  'executado': False}]
```

Para mais informações dos filtros, consulte [Mindset Controle](http://apis.lojaspompeia.com.br/mindset/v1#!/controle/controle_list).


## Controle.limpar(id_servico, executado)

**id_servico:string**
**executado:bool**


```python
>>> Controle.limpar(servico.get_id(), False)
>>> <Response [200]>
```

# Status

Módulo responsável pelas operações no endpoint **status**.

Os métodos desta classe são estáticos.

## Status.get()
Retorna todos os status, ou filtrados caso o `filter_param` seja informado.

**filter_params:dict** (opcional)

```python
>>> len(Status.get().json()) # Retorna todos os status sem o filter params
>>> 25
>>> response = Status.get({'_id_servico': servico.get_id()})
>>> response.json()
>>> [{'_id': '5fad5131d96a083154169a00',
  '_id_servico': '5fad5130d96a0831541699fe',
  'inicio_execucao': '2020-11-12T15:13:53.658000',
  'fim_execucao': '2020-11-12T15:13:53.846000',
  'status': 'S'}]
```

Para mais informações dos filtros, consulte [Mindset Status](http://apis.lojaspompeia.com.br/mindset/v1#!/status/status_list).

## Status.atuais():
Retorna todos os status atuais registrados.

```python
>>> len(Status.atuais().json())
>>> 26
>>> Status.atuais().json()[0]
>>> {'_id': '5f2dbe80b4d3c2d250dcc06a',
 '_id_servico': '5edfdfc57a6f51710fa6ef8f',
 'inicio_execucao': '2020-08-07T20:50:08.518000',
 'fim_execucao': '2020-08-07T20:51:19.542000',
 'status': 'S',
 'servico': {'_id': '5edfdfc57a6f51710fa6ef8f',
  'servico': 'produtos-POMPEIA',
  'hora_agendamento': '01:00:00',
  'forcar_execucao': False,
  'ativo': True,
  'tipo': 'saida'}}
```
