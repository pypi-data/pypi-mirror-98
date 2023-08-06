# gmpyinfr

Módulos úteis ao dia-a-dia de uma equipe de Ciência de Dados.

## Instalação

**Não há cobertura para utilização no Windows**. Este pacote e o passo-a-passo de instalação tem funcionamento garantido nas seguintes distros:

**Debian**

- 8 (jessie)
- 9 (stretch)
- 10 (buster)

**Ubuntu**

- 20.04 (focal)
- 19.04 (disco)
- 18.04 (bioni)
- 16.04 (xenial)
- 14.04 (trusty)

Demais distribuições linux devem funcionar sem problemas mas têm comandos e processo de instalação diferentes. Caso este seja o seu caso, por favor verifique a documentação do [`Apache Arrow`](https://arrow.apache.org/install/) e [`Miniconda`](https://docs.conda.io/en/latest/miniconda.html).

> Este pacote conta com instalações extras conforme a necessidade de utilização. Para instalar apenas o pacote básico, o comando é
>
> ```bash
> pip install gmpyinfr
> ```
>
> Já para instalar um pacote extra, o comando tem a seguinte sintaxe
>
> ```bash
> pip install gmpyinfr[extra]
> ```
>
> onde `extra` pode ser um dos seguintes pacotes extras:
>
> - `all` - contém todos os pacotes extras, recomendados para os cientistas que irão prototipar soluções em suas máquinas. Atente para o fato de que a instalação deste extra implica na leitura das demais documentações e instalação de todas bibliotecas necessárias para pleno funcionamento.
> - `db` - contém o pacote [`gmpyinfr-dbutils`](https://github.com/anewmanvs/gmpyinfr_dbutils). Responsável pela comunicação com os bancos de dados, incluindo rotinas de leitura/escrita rápida. Leia a [documentação](https://github.com/anewmanvs/gmpyinfr_dbutils) para passos de instalação prévios à instalação do pacote python.
> - `bot` - contém o pacote [`gmpyinfr-telegram`](). Responsável pela comunicação com a API do Telegram para envio de mensagens a partir de um Bot. Leia a [documentação]() para mais detalhes.

### Conda

Recomendamos que a instalação seja realizada através do [`Miniconda`](https://docs.conda.io/en/latest/miniconda.html). Deste modo, a instalação dos pacotes C++ é faciltada e o cientista pode iniciar imediatamente seus trabalhos. A versão a ser instalada deve ser 64bits para garantir compatibilidade com os demais pacotes. Após a instalação com sucesso do Anaconda/Miniconda, execute os seguintes comandos num novo terminal:

```bash
conda install -y python=3.7 'pyarrow>=3.0.0'
```

### Instalação nativa / Docker

Nos casos onde o usuário preferir não instalar através do Anaconda/Miniconda, ou tiver que realizar a instalação em uma imagem Docker*, deve-se realizar a instalação manual através dos seguintes comandos

> \* No caso de uma instalação em imagem Docker, desconsidere o `sudo`.
> \* Se a imagem Docker for do [repositório oficial python](https://hub.docker.com/_/python), a Etapa 2 é desnecessária.

#### Etapa 1 - compiladores C e C++ e essenciais

```bash
sudo apt update
sudo apt install -y gcc g++ git cmake
```

#### Etapa 2 - python3.7

```bash
sudo apt install -y python3 python3-dev python3-pip
echo "alias python=python3" >> ~/.bashrc
echo "alias pip=pip3" >> ~/.bashrc
source ~/.bashrc
python -m pip install --upgrade pip
pip install setuptools
```

