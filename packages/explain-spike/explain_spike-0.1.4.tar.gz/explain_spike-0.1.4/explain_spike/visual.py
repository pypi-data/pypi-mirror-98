import  matplotlib.pyplot as plt
import plotly.express as px
import shap
import lightgbm
from pandas.core import frame
import pandas as pd
import numpy as np
import dalex as dx

from . import calculate as calc

def plot_importance(features_names: list, features_values: list, n: int = 10, height: int = 300):

    """ Retorna un grafico de barras horizontal con las n features más importantes y sus valores de importancia
    Arg: 
        features_names: Nombres de las variables en orden de importancia
        features_values: Valores de las variables más importantes (en orden)
        n: Top n caracteristicas más importantes que se quieren ilustrar
        height: Altura del grafico
    """

    if n>len(features_names): n=len(features_names)
    fig = px.bar(x=features_values[:n][::-1], y=features_names[:n][::-1], orientation='h', height=height)
    fig.layout = dict(title="Variable Importance", yaxis_title='Features names', xaxis_title="Importance",
                margin=dict(t=100), height=height, plot_bgcolor='rgba(0,0,0,0)')
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='gainsboro')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='gainsboro')
    return fig

def shap_global_plots(shap_values, plot_type: str = 'beeswarm', n: int = 10):

    """ Retorna un grafico de explicacion global del modelo en base a los shap values
    Arg: 
        shap_values: Objeto explainer de los shap values
        plot_type='beeswarm': Tipo de grafico {"beeswarm", "bar", "heatmap"}
        n: Top n caracteristicas más importantes que se quieren ilustrar
    """

    if plot_type=='beeswarm':
        return shap.plots.beeswarm(shap_values, max_display=n, show=False)
    elif plot_type=='bar':
        return shap.plots.bar(shap_values, max_display=n, show=True)
    elif plot_type=='heatmap':
        return shap.plots.heatmap(shap_values)
    else:
        raise ValueError('plot_type={"beeswarm", "bar", "heatmap"}')

def lgbm_importance(model, importance_type: str = 'split', n: int = 10, precision: int = 0):

    """ Retorna un grafico de barras de las variables más importantes para el modelo de lightgbm segun la metrica especificada
    Arg: 
        model: Modelo LightGBM entrenado
        importance_type: Metrica de importancia
            "gain": el promedio de ganancia de las variables cuando son usadas en los arboles
            "split": numero de veces que una caracteristica es utilizada para dividir la data atraves de los arboles
        n: Top n caracteristicas más importantes que se quieren ilustrar
        precision: Decimales a mostrar por valor de importancia
    """

    if importance_type=='split':
        title = 'Feature importance split'
    elif importance_type=='gain':
        title = 'Feature importance gain'
    else:
        raise ValueError('importance_type={"split", "gain"}')
    return lightgbm.plot_importance(model, title=title, max_num_features=n, importance_type=importance_type, precision=precision)


import plotly.graph_objects as go
from plotly.subplots import make_subplots

def partial_dependence_plot(part_dependence: frame, part_residual: frame = None, part_ice: frame = None, data: frame = None, group_y: bool = False, y: str = None):

    """ Grafica el partial dependence plot con las opciones de adicionar los ICE y los residuos obtenidos en una misma figura si sus
        respectivos frames son entregados en los parametros de la funcion. Adicionalmente si de le entrema un frame con los valores
        originales de la variable en feature se adicionara un histograma con la distribucion de esta variable. En caso de ser un problema
        de clasificacion existe la opcion de que el histograma de distribucion sea partida de acuerdo a las clases.
    Arg: 
        part_dependence: Frame del partial dependence calculado
        part_residual: Frame con los residuos calculados
        part_ice: Frame de los ICE calculados
        data: Frame con los valores originales de feature
        group_y: Si separar la distribucion del feature de acuerdo a la clase
        y: Nombre de la variable target
    """

    feature = part_dependence.columns[0]
    col_cache= part_dependence.loc[:, feature].copy(deep=True)

    if str(part_dependence.iloc[0,0])=='nan':
        part_dependence.iloc[0, 0] = part_dependence.iloc[1, 0] - (part_dependence.iloc[2, 0]-part_dependence.iloc[1, 0])
        if type(part_ice)!=type(None):
            part_ice.iloc[0, 0] = part_dependence.iloc[0, 0]
        ticks = [part_dependence.iloc[0, 0]] + list(part_dependence[feature])[2:][::3]
        labels = ['NaN'] + list(part_dependence[feature])[2:][::3]
    else:
        ticks, labels = None, None

    if type(part_residual)!=type(None):
        if type(part_ice)!=type(None):
            # partial dependence + residual + ice
            n_row=1
            if type(data)!=type(None):
                # distribution of feature
                fig = make_subplots(rows=3, cols=1, subplot_titles=("Distribution of {}".format(feature),
                                                    "Partial Dependence with LogLoss Residuals",
                                                    "Partial Dependence with ICE"), specs = [[{}], [{}], [{}]],
                          vertical_spacing = 0.1, row_heights=[0.1, 0.45, 0.45])

                if group_y and type(y)!=None:
                    # distribucion agrupada
                    gb = data.groupby([feature, y]).count()
                    gb['color'] = 'deeppink'
                    gb.iloc[::2, :]['color'] = 'royalblue'

                    vals = np.array([list(item) for item in gb.index.values])[::2,0]

                    bar_0 = go.Bar(x=vals, y=gb.iloc[:,0].values[::2], name='DEFAULT: 0', marker_color='royalblue')
                    bar_1 = go.Bar(x=vals, y=gb.iloc[:,0].values[1::2], name='DEFAULT: 1', marker_color='deeppink')

                    fig.add_trace(bar_0, row=n_row, col=1)
                    fig.add_trace(bar_1, row=n_row, col=1)

                else:
                    # distribucion normal
                    fig.add_trace(go.Histogram(x=data[feature], name='x density', marker=dict(color='#1f77b4', opacity=0.7), yaxis='y2', showlegend=False), row=n_row, col=1)
                n_row+=1
            else:
                #sin distribucion
                fig = make_subplots(rows=2, cols=1, subplot_titles=("Partial Dependence with LogLoss Residuals",
                                                    "Partial Dependence with ICE"), specs = [[{}], [{}]],
                          vertical_spacing = 0.1, row_heights=[0.5, 0.5])

            fig.add_trace(go.Scatter(x=part_dependence[feature], y=part_dependence['partial_dependence'], mode='lines', line=dict(color='rgb(220,20,60)', width=2), connectgaps=True, name="average"), row=n_row, col=1)
            for i, ind in enumerate(part_residual.columns[1:]):
                fig.add_trace(go.Scatter(x=part_residual[feature], y=part_residual[ind], name=ind, marker_color=px.colors.qualitative.Prism[i],
                       line = dict(dash='dash')), row=n_row, col=1)
            n_row+=1

            for i, ind in enumerate(part_ice.columns[1:]):
                fig.add_trace(go.Scatter(x=part_ice[feature], y=part_ice[ind], name=ind, marker_color=px.colors.qualitative.Vivid[i],
                       line = dict(dash='dash')), row=n_row, col=1)

            fig.add_trace(go.Scatter(x=part_dependence[feature], y=part_dependence['partial_dependence'], mode='lines', line=dict(color='rgb(220,20,60)', width=2), connectgaps=True, name="average"), row=n_row, col=1)

            fig.update_layout(height=1000, width=1000, title_text="Partial Dependence", plot_bgcolor='rgba(0,0,0,0)')

            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='gainsboro', row=1, col=1)
            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='gainsboro', row=2, col=1)
            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='gainsboro', row=3, col=1)

            if type(ticks)!=type(None):
                fig.update_xaxes(title_text=feature, showgrid=True, gridwidth=1, gridcolor='gainsboro', row=1, col=1)
                fig.update_xaxes(title_text=feature, showgrid=True, gridwidth=1, gridcolor='gainsboro', tickmode = 'array', tickvals = ticks, ticktext = labels, row=2, col=1)
                fig.update_xaxes(title_text=feature, showgrid=True, gridwidth=1, gridcolor='gainsboro', tickmode = 'array', tickvals = ticks, ticktext = labels, row=3, col=1)
            else:
                fig.update_xaxes(title_text=feature, showgrid=True, gridwidth=1, gridcolor='gainsboro', row=1, col=1)
                fig.update_xaxes(title_text=feature, showgrid=True, gridwidth=1, gridcolor='gainsboro', row=2, col=1)
                fig.update_xaxes(title_text=feature, showgrid=True, gridwidth=1, gridcolor='gainsboro', row=3, col=1)

        else:
            # partial dependence + residual
            n_row=1
            if type(data)!=type(None):
                # con distribucion
                fig = make_subplots(rows=2, cols=1, subplot_titles=("Distribution of {}".format(feature),
                                                    "Partial Dependence with LogLoss Residuals"), specs = [[{}], [{}]],
                          vertical_spacing = 0.2, row_heights=[0.1, 0.9])

                if group_y and type(y)!=None:
                    # distribucion agrupada
                    gb = data.groupby([feature, y]).count()
                    gb['color'] = 'deeppink'
                    gb.iloc[::2, :]['color'] = 'royalblue'

                    vals = np.array([list(item) for item in gb.index.values])[::2,0]

                    bar_0 = go.Bar(x=vals, y=gb.iloc[:,0].values[::2], name='DEFAULT: 0', marker_color='royalblue')
                    bar_1 = go.Bar(x=vals, y=gb.iloc[:,0].values[1::2], name='DEFAULT: 1', marker_color='deeppink')

                    fig.add_trace(bar_0, row=n_row, col=1)
                    fig.add_trace(bar_1, row=n_row, col=1)
                else:
                    # distribucion comun
                    fig.add_trace(go.Histogram(x=data[feature], name='x density', marker=dict(color='#1f77b4', opacity=0.7), yaxis='y2', showlegend=False), row=n_row, col=1)
                n_row+=1
            else:
                #sin distribucion
                fig = make_subplots(rows=1, cols=1)

            for i, ind in enumerate(part_residual.columns[1:]):
                fig.add_trace(go.Scatter(x=part_residual[feature], y=part_residual[ind], name=ind, marker_color=px.colors.qualitative.Prism[i],
                    line = dict(dash='dash')), row=n_row, col=1)

            fig.add_trace(go.Scatter(x=part_dependence[feature], y=part_dependence['partial_dependence'], mode='lines', line=dict(color='rgb(220,20,60)', width=2), connectgaps=True, name="average"), row=n_row, col=1)

            fig.update_layout(height=700, width=1000, title_text="Partial Dependence", plot_bgcolor='rgba(0,0,0,0)')

            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='gainsboro', row=1, col=1)
            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='gainsboro', row=2, col=1)

            if type(ticks)!=type(None):
                fig.update_xaxes(title_text=feature, showgrid=True, gridwidth=1, gridcolor='gainsboro', row=1, col=1)
                fig.update_xaxes(title_text=feature, showgrid=True, gridwidth=1, gridcolor='gainsboro', tickmode = 'array', tickvals = ticks, ticktext = labels, row=2, col=1)
            else:
                fig.update_xaxes(title_text=feature, showgrid=True, gridwidth=1, gridcolor='gainsboro', row=1, col=1)
                fig.update_xaxes(title_text=feature, showgrid=True, gridwidth=1, gridcolor='gainsboro', row=2, col=1)

    else:
        if type(part_ice)!=type(None):
            # dependence + ice
            n_row=1
            if type(data)!=type(None):
                # con distribucion
                fig = make_subplots(rows=2, cols=1, subplot_titles=("Distribution of {}".format(feature),
                                                    "Partial Dependence with LogLoss Residuals"), specs = [[{}], [{}]],
                          vertical_spacing = 0.2, row_heights=[0.1, 0.9])

                if group_y and type(y)!=None:
                    # distribucion agrupada
                    gb = data.groupby([feature, y]).count()
                    gb['color'] = 'deeppink'
                    gb.iloc[::2, :]['color'] = 'royalblue'

                    vals = np.array([list(item) for item in gb.index.values])[::2,0]

                    bar_0 = go.Bar(x=vals, y=gb.iloc[:,0].values[::2], name='DEFAULT: 0', marker_color='royalblue')
                    bar_1 = go.Bar(x=vals, y=gb.iloc[:,0].values[1::2], name='DEFAULT: 1', marker_color='deeppink')

                    fig.add_trace(bar_0, row=n_row, col=1)
                    fig.add_trace(bar_1, row=n_row, col=1)
                else:
                    # distribucion comun
                    fig.add_trace(go.Histogram(x=data[feature], name='x density', marker=dict(color='#1f77b4', opacity=0.7), yaxis='y2', showlegend=False), row=n_row, col=1)
                n_row+=1
            else:
                #sin distribucion
                fig = make_subplots(rows=1, cols=1)

            for i, ind in enumerate(part_ice.columns[1:]):
                fig.add_trace(go.Scatter(x=part_ice[feature], y=part_ice[ind], name=ind, marker_color=px.colors.qualitative.Vivid[i],
                       line = dict(dash='dash')), row=n_row, col=1)

            fig.add_trace(go.Scatter(x=part_dependence[feature], y=part_dependence['partial_dependence'], mode='lines', line=dict(color='rgb(220,20,60)', width=2), connectgaps=True, name="average"), row=n_row, col=1)
            
            fig.update_layout(height=700, width=1000, title_text="Partial Dependence", plot_bgcolor='rgba(0,0,0,0)')

            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='gainsboro', row=1, col=1)
            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='gainsboro', row=2, col=1)

            if type(ticks)!=type(None):
                fig.update_xaxes(title_text=feature, showgrid=True, gridwidth=1, gridcolor='gainsboro', row=1, col=1)
                fig.update_xaxes(title_text=feature, showgrid=True, gridwidth=1, gridcolor='gainsboro', tickmode = 'array', tickvals = ticks, ticktext = labels, row=2, col=1)
            else:
                fig.update_xaxes(title_text=feature, showgrid=True, gridwidth=1, gridcolor='gainsboro', row=1, col=1)
                fig.update_xaxes(title_text=feature, showgrid=True, gridwidth=1, gridcolor='gainsboro', row=2, col=1)

        else:
            n_row=1
            #dependence
            if type(data)!=type(None):
                # con distribucion
                fig = make_subplots(rows=2, cols=1, subplot_titles=("Distribution of {}".format(feature),
                                                    "Partial Dependence with LogLoss Residuals"), specs = [[{}], [{}]],
                          vertical_spacing = 0.2, row_heights=[0.1, 0.9])

                if group_y and type(y)!=None:
                    # distribucion agrupada
                    gb = data.groupby([feature, y]).count()
                    gb['color'] = 'deeppink'
                    gb.iloc[::2, :]['color'] = 'royalblue'

                    vals = np.array([list(item) for item in gb.index.values])[::2,0]

                    bar_0 = go.Bar(x=vals, y=gb.iloc[:,0].values[::2], name='DEFAULT: 0', marker_color='royalblue')
                    bar_1 = go.Bar(x=vals, y=gb.iloc[:,0].values[1::2], name='DEFAULT: 1', marker_color='deeppink')

                    fig.add_trace(bar_0, row=n_row, col=1)
                    fig.add_trace(bar_1, row=n_row, col=1)
                else:
                    # distribucion comun
                    fig.add_trace(go.Histogram(x=data[feature], name='x density', marker=dict(color='#1f77b4', opacity=0.7), yaxis='y2', showlegend=False), row=n_row, col=1)
                n_row+=1
            else:
                #sin distribucion
                fig = make_subplots(rows=1, cols=1)
            fig.add_trace(go.Scatter(x=part_dependence[feature], y=part_dependence['partial_dependence'], mode='lines', line=dict(color='rgb(220,20,60)', width=2), connectgaps=True, name="average"), row=n_row, col=1)
            
            fig.update_layout(height=700, width=1000, title_text="Partial Dependence", plot_bgcolor='rgba(0,0,0,0)')

            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='gainsboro', row=1, col=1)
            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='gainsboro', row=2, col=1)

            if type(ticks)!=type(None):
                fig.update_xaxes(title_text=feature, showgrid=True, gridwidth=1, gridcolor='gainsboro', row=1, col=1)
                fig.update_xaxes(title_text=feature, showgrid=True, gridwidth=1, gridcolor='gainsboro', tickmode = 'array', tickvals = ticks, ticktext = labels, row=2, col=1)
            else:
                fig.update_xaxes(title_text=feature, showgrid=True, gridwidth=1, gridcolor='gainsboro', row=1, col=1)
                fig.update_xaxes(title_text=feature, showgrid=True, gridwidth=1, gridcolor='gainsboro', row=2, col=1)
    
    part_dependence.loc[:, feature] = col_cache
    if type(part_ice)!=type(None):
        part_ice.iloc[0, 0] = part_dependence.iloc[0, 0]
    return fig

def shap_dependence_plot(shap_values, plot_features: list, data: frame, figsize=None):
    if type(figsize)==type(None):
        figsize = (10,len(plot_features)*3)
    fig, axes = plt.subplots(nrows=len(plot_features), ncols=1, figsize=figsize)
    if len(plot_features)==1:
        shap.dependence_plot(plot_features[0], shap_values.values, data, ax=axes, show=False)
    else:
        axes = axes.ravel()
        for i, feature in enumerate(plot_features):
            shap.dependence_plot(feature, shap_values.values, data, ax=axes[i], show=False)
    fig.tight_layout()

def ale_plot(ale_results: dict, plot_features: list):
    fig = make_subplots(rows=len(plot_features), cols=1)
    for n_row, feature in enumerate(plot_features):
        fig.add_trace(go.Scatter(x=ale_results[feature][0], y=ale_results[feature][1], mode='lines', connectgaps=True, name=feature), row=n_row+1, col=1)
    fig.update_layout(height=1000, width=1000, title_text="Accumulated Local Effects", plot_bgcolor='rgba(0,0,0,0)')
    fig['layout']['xaxis']['title']=plot_features[0]
    fig['layout']['yaxis']['title']='ALE'
    if len(plot_features)>1:
        for n_row, feature in enumerate(plot_features[1:]):
            fig['layout']['xaxis{}'.format(n_row+2)]['title']=feature
            fig['layout']['yaxis{}'.format(n_row+2)]['title']='ALE'
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='gainsboro')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='gainsboro')
    return fig

from itertools import combinations        # n choose k combinations of objects

def plot_sm_3d(frame, resolution, search_cols, z_axis_var, stat):

    """Plots 6 small multiples in a grouped subplot to display adversary search 
            results from find_adversaries.
    
    Args:
        frame: Pandas DataFrame containing potential adversaries generated by 
                  find_adversaries.
        resolution: The number of points across the domain of the variables in 
                    search_cols in find_adversaries. 
        search_cols: List of search_cols used in find_adversaries.
        z_axis_var: The name of the variable by which to group the frame and
                    that will appear in the title and z-axis label of the 
                    generated plot.
        stat: Groupby stat for z_axis_var and frame.
    
        """
    
    max_ = frame[z_axis_var].max() # establish z-axis high limit
    
    fig = plt.figure(figsize=plt.figaspect(0.67)*2.5) # init 2 x 3 plot

    _2d_shape = (resolution, resolution) # correct shape for 3-D display of 1-D arrays

    # loop through 2-way combos of search_cols
    for i, two_way_combo in enumerate(list(combinations(search_cols, 2))):

        # many unique values exist for each 2-way combo of search_cols values 
        # summarize by stat to plot concisely
        
        # execute groupby
        groups = eval('frame[[two_way_combo[0], two_way_combo[1], z_axis_var]]\
                        .groupby([two_way_combo[0], two_way_combo[1]]).' + stat + '()')

        groups = groups.reset_index() # convert groupby vals to cols (from index)

        ax = fig.add_subplot(2, 3, (i + 1), projection='3d') # subplot placement
            
        # values and labels for each axis
        x = np.asarray(groups[two_way_combo[0]]).reshape(_2d_shape)
        ax.set_xlabel('\n' + two_way_combo[0])
        y = np.asarray(groups[two_way_combo[1]]).reshape(_2d_shape)
        ax.set_ylabel('\n' + two_way_combo[1])
        z = np.asarray(groups[z_axis_var]).reshape(_2d_shape)
        ax.set_zlabel('\n' + stat + ' ' + str(z_axis_var))
        ax.set_zlim3d(0, max_) # ensure constant scale
        
        # plot
        surf = ax.plot_surface(x, y, z, 
                               cmap=cm.coolwarm, 
                               linewidth=0.05, 
                               rstride=1, 
                               cstride=1, 
                               antialiased=True)
        
    # main title and display    
    fig.suptitle(stat.title() + ' ' + str(z_axis_var) + ' for ' + str(search_cols))    
    plt.tight_layout()
    _ = plt.show()

def plot_random_attack(frame_wo_nan, frame_w_nan):

    """ Compara las predicciones del modelo para dos sets de datos identicos con la unica diferencia que uno contiene valores faltantes.
        Cada instancia es graficada en base a su orden ascendente en la prediccion del modelo
    Arg: 
        frame_wo_nan: Frame de instancias sin valores faltantes
        frame_w_nan: Frame de instancias con valores faltantes
    """

    perc_miss= round(frame_w_nan.isna().sum().sum()/(frame_wo_nan.shape[0]*frame_wo_nan.shape[1]),2)
    fig = make_subplots(rows=1, cols=1)
    fig.add_trace(go.Scatter(y=frame_wo_nan.sort_values(by='prediction').reset_index()['prediction'], mode='lines', connectgaps=True, name='0% Missing Data'), row=1, col=1)
    fig.add_trace(go.Scatter(y=frame_w_nan.sort_values(by='prediction').reset_index()['prediction'], mode='lines', connectgaps=True, name='{}% Missing Data'.format(perc_miss)), row=1, col=1)
    fig.layout = dict(title="Ranked Predictions on Random Data",
                                    xaxis_title='Ranked Row Index',
                                    yaxis_title="Predicted",
                                    showlegend=True,
                                    margin=dict(t=50),
                                    hovermode='closest',
                                    bargap=0,
                                    plot_bgcolor='rgba(0,0,0,0)',
                                    )
    fig.update_layout(xaxis = dict(showticklabels=False))
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='gainsboro')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='gainsboro')
    return fig

def shap_local_exp(shap_values, id_: list, data: frame = None, plot_type='bar', max_display: int = 10, labels=None):

    """ Entrega distintas figuras para la explicacion local en base a los SHAP values de una instancia en particular o bien un grupo de estas.
    Arg: 
        shap_values: Objeto explainer de los shap values
        id_: Lista de las instancias a las cuales obtener su explicacion local. 
             En caso de ser indices del frame de data es necesario entregar este parametro, en caso contrario se tomara el indice
             como la posicion de la instancia en el orden original de data
        data: Datos con los cuales fueron creados los shap_values
        plot_type: Tipo de grafico a crear {"bar", "force_plot", "decision_plot", "waterfall"}
        max_display: Maximo numero de variables a mostrar (solo para "bar" y "waterfall")
        labels: Etiquetas para las instancias a graficar (solo para "decision_plot")
    """

    shap.initjs()
    if plot_type=='bar':
        if type(data)==type(None):
            if len(id_)==1:
                ind=id_[0]
        else:
            if len(id_)==1:
                ind = data.index.get_loc(id_[0])
            else:
                ind = [data.index.get_loc(i) for i in id_]
        return shap.plots.bar(shap_values[ind], show=False, max_display=max_display)

    elif plot_type=='force_plot':
        if type(data)==type(None):
            if len(id_)==1:
                ind=id_[0]
                return shap.plots.force(shap_values[ind], show=False)
            else:
                return shap.force_plot(shap_values.base_values[0], shap_values.values[id_], shap_values.data, show=False)
        else:
            if len(id_)==1:
                ind = data.index.get_loc(id_[0])
                return shap.plots.force(shap_values[ind], show=False)
            else:
                ind = [data.index.get_loc(i) for i in id_]
                return shap.force_plot(shap_values.base_values[0], shap_values.values[ind], shap_values.data, show=False)

    elif plot_type=='decision_plot':
        if type(data)==type(None):
            if len(id_)==1:
                ind=id_[0]
                return shap.decision_plot(shap_values.base_values[ind], shap_values.values[ind], shap_values.data, show=False)
            else:
                shap.decision_plot(shap_values.base_values[0], shap_values.values[id_,:], shap_values.data,
                   legend_labels=labels, legend_location='lower right')
        else:
            if len(id_)==1:
                ind = data.index.get_loc(id_[0])
                return shap.decision_plot(shap_values.base_values[ind], shap_values.values[ind], data, show=False)
            else:
                ind = [data.index.get_loc(i) for i in id_]
        return shap.decision_plot(shap_values.base_values[0], shap_values.values[ind,:], data,
                   legend_labels=labels, legend_location='lower right')
    elif plot_type=='waterfall':
        if type(data)==type(None):
            if len(id_)==1:
                ind=id_[0]
                return shap.plots.waterfall(shap_values[ind], show=False, max_display=max_display)
            else:
                raise ValueError('for waterfall plot the list in id_ must contains a single value')
        else:
            if len(id_)==1:
                ind = data.index.get_loc(id_[0])
                return shap.plots.waterfall(shap_values[ind], show=False, max_display=max_display)
            else:
                raise ValueError('for waterfall plot the list in id_ must contains a single value')
    else:
        raise ValueError('plot_type={"bar", "force_plot", "decision_plot", "waterfall"}')

def dalex_local_exp(model, data_x:frame, row, plot_type: str = 'break_down', label: str = None, B: int = 10):

    """ Entrega distintas figuras para la explicacion local que da como opcion la libreria externa de dalex
    Arg: 
        model: Modelo entrenado
        data_x: Datos de entrada del modelo
        plot_type: Tipo de grafico a crear {"break_down", "shap"}
    """

    dalex_explainer = dx.Explainer(model, data_x, model.predict(data_x), verbose=False)
    if plot_type == 'break_down' or plot_type=='shap':
        local_exp = dalex_explainer.predict_parts(row, type=plot_type, B = B, label=label)
        return local_exp.plot()
    else:
        raise ValueError('plot_type={"break_down", "shap"}')

def plot_residuals(frame: frame, y: str, yhat: str, resid: str):

    """ Grafica los residuos para las dos clases del problema de clasificacion acorde va aumentando la probabilidad predecida
    Arg: 
        frame: Frame que contiene los valores objetivo, las predicciones del modelo y los residuos calculados
        y: Nombre de la columna con los valores objetivo
        yhat: : Nombre de la columna con las predicciones
        resid: Nombre de la columna con los residuos
    """

    fig = make_subplots(rows=1, cols=1)
    color_list = ['royalblue', 'magenta'] 
    c_idx = 0
    groups = frame.groupby(y)
    for name, group in groups:
        fig.add_trace(go.Scatter(x=group[yhat].values, y=group[resid].values, name=' '.join([y, str(name)]), mode='markers', marker_color=color_list[c_idx]), row=1, col=1)
        c_idx+=1
    fig.layout = dict(title='Global Logloss Residuals',
                                    xaxis_title=yhat,
                                    yaxis_title=resid,
                                    showlegend=True,
                                    margin=dict(t=50),
                                    plot_bgcolor='rgba(0,0,0,0)',
                                    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='gainsboro')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='gainsboro')
    return fig

import seaborn as sns

def residual_analisis(feature: str, frame: frame, y: str, yhat: str, resid: str, discrete: bool = False, bins: int = 11):

    """ Grafica los residuos para las dos clases del problema de clasificacion acorde va aumentando la probabilidad predecida
        para distintos valores de la variable entregada en feature
    Arg: 
        feature: Nombre de la variable por la cual cambiar su valor y analizar sus residuos
        frame: Frame que contiene los valores objetivo, las predicciones del modelo, los residuos calculados y la variable a estudiar su efecto
        y: Nombre de la columna con los valores objetivo
        yhat: Nombre de la columna con las predicciones
        resid: Nombre de la columna con los residuos
        discrete: Si discretizar o no la variable en estudio (recomendable cuando este es continua y toma muchos valores distintos)
        bins: Cantidad de cuantiles en los que discretizar la variable de estudio
    """

    sns.set(font_scale=0.9)                                         # legible font size
    sns.set_style('whitegrid', {'axes.grid': False})                # white background, no grid in plots
    sns.set_palette(sns.color_palette(["#4169e1", "#ff00ff"]))

    if discrete:
        test_yhat_q = frame.copy()
        q_columns=['q_{}_segment'.format(feature), 'q_{}'.format(feature)]
        test_yhat_q[q_columns[0]]=pd.qcut(test_yhat_q[feature],q)
        test_yhat_q[q_columns[1]]=pd.qcut(test_yhat_q[feature],q,labels=list(range(q)))
        sorted_ = test_yhat_q.sort_values(by='q_{}'.format(feature))                     # sort for better layout of by-groups
        g = sns.FacetGrid(sorted_, col='q_{}_segment'.format(feature), hue=y, col_wrap=4)      # init grid
    else:
        sorted_ = frame.sort_values(by=feature)                     # sort for better layout of by-groups
        g = sns.FacetGrid(sorted_, col=feature, hue=y, col_wrap=4)      # init grid
    _ = g.map(plt.scatter, yhat, resid, alpha=0.4)                  # plot points
    _ = g.add_legend(bbox_to_anchor=(0.82, 0.2)) 

def shap_comparation(shap_contrib, shap_logloss, X, n: int = 10):

    """ Entrega dos graficos de barra para comparar los SHAP values para la contribucion de la prediccion del modelo
        y la contribucion al residuo logloss obtenido por el modelo
    Arg: 
        feature: Nombre de la variable por la cual cambiar su valor y analizar sus residuos
        frame: Frame que contiene los valores objetivo, las predicciones del modelo, los residuos calculados y la variable a estudiar su efecto
        y: Nombre de la columna con los valores objetivo
        yhat: Nombre de la columna con las predicciones
        resid: Nombre de la columna con los residuos
        discrete: Si discretizar o no la variable en estudio (recomendable cuando este es continua y toma muchos valores distintos)
        bins: Cantidad de cuantiles en los que discretizar la variable de estudio
    """

    contrib_features, contrib_values = calc.shap_importance(pd.Index(X), shap_contrib, n=n)
    logloss_features, logloss_values = calc.shap_importance(pd.Index(X), shap_logloss, n=n)

    reverse_ = lambda x: x.reverse()
    contrib_values, logloss_values = list(contrib_values), list(logloss_values)
    list(map(reverse_, [contrib_features, contrib_values, logloss_features, logloss_values]))

    fig = make_subplots(rows=1, cols=2, subplot_titles=("Global Shapley Contributions to Prediction",
                                                    "Global Shapley Contributions to Logloss"), specs = [[{}, {}]],
                        horizontal_spacing = 0.15, column_width=[0.5, 0.5])

    bar_pred = go.Bar(x=contrib_values, y=contrib_features, orientation='h')
    bar_loss = go.Bar(x=logloss_values, y=logloss_features, orientation='h')

    fig.add_trace(bar_pred, row=1, col=1)
    fig.add_trace(bar_loss, row=1, col=2)

    fig.update_xaxes(title_text="mean(|SHAP Contrib.|)", showgrid=True, gridwidth=1, gridcolor='gainsboro', row=1, col=1)
    fig.update_xaxes(title_text="mean(|SHAP Contrib.|)", showgrid=True, gridwidth=1, gridcolor='gainsboro', row=1, col=2)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='gainsboro',  row=1, col=1)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='gainsboro',  row=1, col=2)
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', showlegend=False)

    return fig