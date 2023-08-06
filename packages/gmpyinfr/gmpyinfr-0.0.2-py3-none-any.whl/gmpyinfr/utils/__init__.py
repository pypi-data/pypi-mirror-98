"""
Utils
"""

def read_file(file_path, bmode=False):
    """
    Faz a leitura de um arquivo e retorna o conteúdo.

    Params:
    	- file_path : str contendo o path do arquivo a ser lido
    	- bmode : bool (std False) indicando se devem ser lidos bytes

    Returns:
    	conteúdo do arquivo
    """

    if not isinstance(file_path, str):
    	raise ValueError("Param 'file_path' deve ser 'str'")

    mode = 'r' if not bmode else 'rb'
    with open(file_path, mode) as filecontent:
        res = filecontent.read()

    return res

def split_dataframe(dataframe, chunk_size=10000):
    """
    Separa o dataframe em partes de tamanho máximo igual a 'chunk_size'.

    Params:
        - dataframe : pandas.DataFrame a ser dividido
        - chunk_size : int (std 10000) tamanho máximo das partes

    Returns:
        lista de dataframes contendo as partes
    """

    import pandas as pd

    if not isinstance(dataframe, pd.DataFrame):
    	raise ValueError("Param 'dataframe' deve ser 'pandas.DataFrame'")

    if chunk_size <= 0:
    	raise ValueError("Param 'chunk_size' não pode ser menor ou igual a zero")

    dfs = []
    num_chunks = dataframe.shape[0] // chunk_size + 1

    for i in range(num_chunks):
        dfs.append(dataframe[i * chunk_size:((i + 1) * chunk_size)])

    if dfs and dfs[num_chunks - 1].shape[0] == 0:
        dfs.pop()

    return dfs

def df_not_in(df1, df2, keys=None):
    """
    Retorna dados de df1 que não estão presentes em df2.

    Params:
    	- df1 : pandas.DataFrame 1
    	- df2 : pandas.DataFrame 2
    	- keys : list de str contendo as colunas que serão utilizadas como chave. Se
    		keys for None, utiliza as colunas coincidentes nos dois dataframes.

	Returns:
		pandas.DataFrame com as ocorrências de df1 que não estão presentes em df2
    """

    import pandas as pd

    if df1 is None:
        return None

    if not isinstance(df1, pd.DataFrame):
    	raise ValueError("Param 'df1' deve ser 'pandas.DataFrame'")

    if df2 is not None and not isinstance(df2, pd.DataFrame):
    	raise ValueError("Param 'df2' deve ser 'pandas.DataFrame' ou 'None'")

    if df1.shape[0] == 0 or df2 is None or df2.shape[0] == 0:
        return df1

    dataframe = df1.merge(
    	df2, how='left', on=keys, suffixes=['', '_y'], indicator=True)

    return dataframe.loc[dataframe['_merge'] == 'left_only', df1.columns].copy()

def generate_hashed_DF(df, cols, colname='ROW_VERSION', fprec=4,
                       encoding='utf-8', sep='|'):
    """
    Gera um dataframe com um hash onde o hash é gerado por valores das colunas
    contidas na variavel cols

    Params:
        - df : pandas.Dataframe input
        - cols : list de str colunas que devem ser usados para o calculo do hash
        - colname : str (std 'ROW_VERSION') nome da coluna a ser criada no dataframe
        - fprec : int (std 4) precisão a considerar dos floats (número de casas
            decimais)
        - encoding : str (std 'utf-8') encoding a ser utilizado para gerar a hash
        - sep : str (std '|') separador das colunas, não pode ser vazio.

    Returns:
        pandas.DataFrame contendo uma coluna contendo o hash da linha
    """

    import pandas as pd

    if not isinstance(df, pd.DataFrame):
    	raise ValueError("Param 'df' deve ser 'pandas.DataFrame'")

    import hashlib

    if sep is None or sep == '':
        sep = '|'

    if encoding is None:
        encoding = 'utf-8'

    def generate_hash_row(hash_tuple):
        accumulator = sep.join([str(elm) for elm in hash_tuple[1:]])
        return hashlib.md5(accumulator.encode(encoding)).hexdigest()

    _df = df.copy()

    for col in _df.dtypes[_df.dtypes.astype(str).str.contains('float')].index:
        _df[col] = _df[col].round(fprec)

    hashable_DF = _df[cols]
    hash_list = []

    for row in hashable_DF.itertuples():
        hash_list.append(generate_hash_row(row))
    _df[colname] = hash_list

    return _df
