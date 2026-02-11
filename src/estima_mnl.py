import biogeme.database as db
import biogeme.biogeme as bio
from biogeme import models
from biogeme.expressions import Beta, Variable, log

def clean_database(crude_df):

    cleaned_df = crude_df.copy()
    cleaned_df = cleaned_df[["tv1","c1","ta1","f1",
                             "tv2","c2","ta2","f2",
                             "choice"]]



def crear_variables(n):
    variables = {}
    for i in range(2*(n-1) + 1, 2*n + 1):
        variables[f'c_a{i}'] = Variable(f'c_a{i}') 
        variables[f'tv_a{i}'] = Variable(f'tv_a{i}')
    return variables

def crear_params(n):
    params = {}
    for i in range(n, n+1):
        params[f'ASC{i}'] = Beta(f'ASC{i}', 0, None, None, 0)
        params[f'c{i}'] = Beta(f'c{i}', 0, None, None, 0)
        params[f'tv{i}'] = Beta(f'tv{i}', 0, None, None, 0)
    return params

def crear_utilidades(variables, params, n):
    utilities = {}
    for i in range(2*(n-1) + 1, 2*n + 1):

        if i % 2 == 0:
            dis = int(i / 2)
        else:
            dis = int((i + 1) / 2)
        
        utilities[i] = (
            params[f'c{dis}'] * variables[f'c_a{i}'] +
            params[f'tv{dis}'] * variables[f'tv_a{i}']
        )

        if i % 2 == 0:
            utilities[i] += params[f'ASC{dis}']

    return utilities

def crear_disponibilidades(n):
    availability = {}
    for i in range(2 * (n-1) + 1, 2*n + 1):
        availability[i] = Variable(f'av_{i}')
    return availability



def estima_mnl(df,n):
    """
    Estima un modelo MNL utilizando Biogeme.

    Parameters:
    individuo_df (DataFrame): DataFrame de pandas con los datos de entrada.

    Returns:
    DataFrame: Resultados de la estimación.
    """
    
    # Cargar tu DataFrame de pandas
    # Supongamos que se llama df
    database = db.Database('my_data', df)
    
    # Variables
    vars_dict = crear_variables(n)

    # Parametros a estimar
    params_dict = crear_params(n)

    # Utilidades
    V = crear_utilidades(vars_dict, params_dict, n)

    # Disponibilidades
    av = crear_disponibilidades(n)

    # Modelo de elección
    prob = models.logit(V, av, Variable('n_choice'))
    logprob = log(prob)

    # Estimación
    biogeme = bio.BIOGEME(database, logprob, generate_html =False)
    biogeme.modelName = "Modelo_PD"
    results = biogeme.estimate()

    # Resultados
    # Obtener resultados como DataFrame
    results_df = results.get_estimated_parameters()

    # Estadísticos generales
    stats = results.get_general_statistics()

    correlation_matrix = results.getCorrelationResults()
    print(correlation_matrix)

    summary_stats = {
        'Obs Totales': stats['Sample size'].value,
        'Obs Promedio por Tarjeta': round(stats['Sample size'].value / 9,1),
        'Log-likelihood inicial': round(stats['Init log likelihood'].value,1),
        'Log-likelihood final': round(stats['Final log likelihood'].value,1),
        'Rho-cuadrado': round(stats['Rho-square for the init. model'].value,4),
        'Rho-cuadrado ajustado': round(stats['Rho-square-bar for the init. model'].value,4),
        'AIC': round(stats['Akaike Information Criterion'].value,1),
        'BIC': round(stats['Bayesian Information Criterion'].value,1)
    }

    return {
        'parametros_estimados': results_df,
        'estadisticos_modelo': summary_stats
    }