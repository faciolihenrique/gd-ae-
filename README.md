# pseudo-GD[AE]
Esse é um projeto para criação do GDA + GDE, um Sistema de Avaliação de professores da Unicamp e auxilio de alunos

## Dependências
O projeto é escrito em python3.

As dependências do projeto, com suas respectivas versões, podem ser encontradas no arquivo `dependencies.txt`

É recomendado executar o código com um ambiente virtual de Python (`virtualenv`), para evitar conflitos de versões e problemas de dependencias, para isso, execute os seguintes comandos para criar o ambiente virtual e ativá-lo

```
virtualenv env
source env/bin/activate
```

Para desativar o ambiente, basta executar o comando `deactivate`, carregado ao se ativar o ambiente.

É necessário instalar as dependencias no ambiente, para isso, execute o comando

```
pip3 install -r dependencies.txt
```

### static's
Para o design html está sendo usada o framework [Foundation](http://foundation.zurb.com/sites/docs/) . Isso pode ser alterado a qualquer momento

## Rodando
O projeto utiliza-se do framework django. Para rodar execute:

```
python3 manage.py makemigrations
python3 manage.py makemigrations dacParser
python3 manage.py migrate
python3 manage.py runserver
```

Para criar um usuário administrador execute `python3 manage.py createsuperuser`.
Para fazer o download das informações do site da dac, a path é /update/disciplines


## PEP8
O projeto deve seguir as "normas" [PEP8](http://pep8.org/) utilizando o package pep8. Instale com `pip install pep8` e veja se o arquivo está nas normas usando `pep8 nome_do_arquivo.py`
Não use o autopep8 no projeto

## Todo's
