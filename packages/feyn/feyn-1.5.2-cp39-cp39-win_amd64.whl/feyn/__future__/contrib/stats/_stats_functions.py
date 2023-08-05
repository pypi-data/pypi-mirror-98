import numpy as np

def _residual_square_sum(actuals, expected):
    return np.sum((actuals - expected)**2)
    
def _f_statistic(rss_restricted,rss_mini, no_samples, no_parameters, no_hypoth_para):
    from scipy.stats import f
    nom = (rss_restricted - rss_mini) * (no_samples - no_parameters)
    denom = rss_mini * (no_hypoth_para)
    F = nom / denom

    dfn = no_hypoth_para
    dfd = no_samples - no_parameters
    p = 1 - f.cdf(F, dfn, dfd)

    return F, p

def _t_statistic(optimized_para, idx_para, unbiased_sample_var, no_samples, no_paras, derivative_inverse):
    from scipy.stats import t

    nom = optimized_para
    denom = unbiased_sample_var * np.sqrt(derivative_inverse[idx_para, idx_para])
    T = nom / denom

    df = no_samples - no_paras
    if T < 0:
        p = t.cdf(T, df)
    else:
        p = 1 - t.cdf(T, df)
    
    return T, p

def _g_statistic(log_likelihood_act, log_likelihood_est, degrees_of_freedom):
    from scipy.stats import chi2

    G = 2 * (log_likelihood_est - log_likelihood_act)

    df = degrees_of_freedom
    rv = chi2(df)
    p = 1 - rv.cdf(G)

    return G, p

def _calculate_no_para(graph):
    no_para = 0
    for inter in graph:
        if 'linear' in inter.spec:
            no_para += 2
        
        if 'cat' in inter.spec:
            no_para += len(inter.state.categories) + 1

    return no_para

def _amount_of_weights_on_variables_in_graph(graph):
    count = 0
    for inter in graph:
        if 'out' in inter.spec:
            break

        if 'linear' in inter.spec:
            count += 1
        
        if 'cat' in inter.spec:
            count += len(inter.state.categories)
    return count

def _get_no_samples(graph, data):
    target = graph.target
    return data[target].shape[0]

def _log_likelihood(loss, no_samples=None, errors = 'binomial'):

    if errors == 'normal':

        rss = loss
        variance = loss / no_samples
        print()
        log_like = (-no_samples/2) * np.log(variance) - (rss / (2 * variance))

    elif errors == 'binomial':

        log_like = - loss

    return log_like

def graph_f_score(graph,data):
    """
    This computes the F-statistic associated to a feyn graph under the null hypothesis.
    The null hypothesis is that every weight on each feature and category is equal to zero.
    
    If the hypothesis is true then the F-score is distributed by F(q, n - p), 
    the Fisher distribution of q and n-p degrees of freedom. Here:
    * q is the amount of weights we assume is equal to zero 
    * n is the amount of samples in data
    * p amount of parameters in the graph. The F score is calculated by:
    nom = {sum((data[target].mean - data[target])**2) - (graph.mse(data) * n)} * (n-p)
    denom = (graph.mse(data) * n) * q
    F = nom / denom

    Arguments:
        graph {[feyn.Graph]} -- Graph to test null hypothesis.
        data {[dic of numpy arrays or pandas dataframe]} -- Data to test significance of graph on.

    Returns:
        tuple -- The F score of hypothesis and p value
    """
    if 'linear' not in graph[-1].spec:
        raise Exception('Can only compute F score on regressors')

    target = graph.target
    no_samples = _get_no_samples(graph,data)

    rss_mini = graph.mse(data) * no_samples
    target_sample_mean = data[target].mean()
    rss_restricted = _residual_square_sum(data[target], target_sample_mean)
    
    no_para = _calculate_no_para(graph)
    no_hypoth_para = _amount_of_weights_on_variables_in_graph(graph)

    f_score, p_value = _f_statistic(rss_restricted, rss_mini, no_samples, no_para, no_hypoth_para)

    return f_score, p_value

def _plot_rv_score(rv, score, p_value, ax, title, label):

    x_axis = np.linspace(rv.ppf(0.01), rv.ppf(0.99), 100)
    rv_pdf = rv.pdf(x_axis)
    x_threshold = x_axis[x_axis > score]

    ax.set_title(title)
    ax.set_ylabel("Probability density")
    ax.set_xlabel('Score')

    ax.plot(x_axis, rv_pdf, alpha = 0.5, label = label)

    # Plot scores
    ax.fill_between(x_threshold, rv.pdf(x_threshold), alpha=0.3, label = f'p-value, features: {p_value: .4f}' )
    ax.axvline(score, ls = '--', lw = 2, label = f'feature score: {score: 4f}')
    ax.legend()

    return ax

def plot_graph_p_value(graph, data, title = 'Significance of graph', ax=None):
    """
    Plots the probability density function under the null hypothesis.     
       
    The null hypothesis is that every weight on each feature and category is equal to zero.

    If the graph is a regression then this plots the Fisher distribution    
    Under the null hypothesis the F-score approximately distributed by F(q, n - p), 
    with q and n-p degrees of freedom. Here:
    * q is the amount of weights we assume is equal to zero 
    * n is the amount of samples in data
    * p amount of parameters in the graph.


    If the graph is a classification then this plots the chi2 distribution    
    Under the null hypothesis the G-score is distributed by chi2(q), 
    with q degrees of freedom. Here:
    * q is the amount of weights we assume is equal to zero 
    
    This also plots vertical lines intercepting the x-axis at the F scores or G scores under each hypothesis.

    Arguments:
        graph {[feyn.Graph]} -- Graph to calculate p-values of under the null hypothesis
        data {[dic of numpy arrays or pandas dataframe]} -- Data to test significance of graph on. 

    Keyword Arguments:
        title {str} -- [Title of axes] (default: {'Significance of graph'})
        ax {[matplotlib.Axes]} -- (default: {None})

    Returns:
        [matplotlibe.Axes] -- Plots of distributions under null hypothesis
    """
    from scipy.stats import f, chi2
    import matplotlib.pyplot as plt

    if ax is None:
        ax = plt.subplot()
    
    if 'linear' in graph[-1].spec:
        f_score, p_value = graph_f_score(graph, data)

        no_para = _calculate_no_para(graph)
        no_samples = _get_no_samples(graph,data)

        dfn = _amount_of_weights_on_variables_in_graph(graph)
        dfd = no_samples - no_para
        rv = f(dfn, dfd)

        label = f'F{dfn,dfd}'
        ax = _plot_rv_score(rv, f_score, p_value, ax, title,label)

    elif 'lr' in graph[-1].spec:
        g_score, p_value = graph_g_score(graph, data)

        df = _amount_of_weights_on_variables_in_graph(graph)
        rv = chi2(df)

        label = f'chi2({df})'
        ax = _plot_rv_score(rv, g_score, p_value, ax, title, label)

    return ax

def graph_log_likelihood(graph, data):
    """
    This computes the log-likelihood of the graph evaluated on the data set.

    Arguments:
        graph {[feyn.Graph]} -- Graph to evaluate log-likelihood.
        data {[dic of numpy arrays or pandas dataframe]} -- Data to evaluate the log-likelihood on.

    Returns:
        [scalar] -- The log-likelihood of the graph on the data set.
    """

    if 'lr' in graph[-1].spec:
        errors = 'binomial'
        loss = np.sum(graph.binary_cross_entropy(data))
        log_like = _log_likelihood(loss)

    else:
        errors = 'normal'
        no_samples = _get_no_samples(graph, data)
        loss = np.sum(graph.squared_error(data))
        log_like = _log_likelihood(loss, no_samples, errors)
    
    return log_like

def _log_likelihood_null_hypothesis(actuals):

    no_samples = len(actuals)
    no_pos_class = np.sum(actuals)
    no_neg_class = np.sum(1-actuals)

    log_like = no_neg_class * np.log(no_neg_class)
    log_like += no_pos_class* np.log(no_pos_class)
    log_like -= no_samples * np.log(no_samples)

    return log_like

def graph_g_score(graph, data):
    """
    This computes the G-statistic associated to a feyn graph under the null hypothesis.
    The null hypothesis is that every weight on each feature and category is equal to zero.
    
    If the hypothesis is true then the G-score is distributed by chi2(q), 
    with q degrees of freedom. Here:
    * q is the amount of weights we assume is equal to zero 
    
    The G-statistic is calculated by:
    G = 2 * {graph_log_likelihood(graph, data) - log-likelihood of constant model}
    
    where 
    log-likelihood of constant model = #neg_class * np.log(#neg_class) + #pos_class * np.log(#pos_class) - #samples * np.log(#samples)

    Arguments:
        graph {[feyn.Graph]} -- Graph to test null hypothesis.
        data {[dic of numpy arrays or pandas dataframe]} -- Data to test significance of graph on.

    Returns:
        tuple -- The F score of hypothesis and p value
    """

    if 'lr' not in graph[-1].spec:
        raise Exception('Can only compute G score on classifiers')

    target = graph.target
    actuals = data[target]

    log_like_null = _log_likelihood_null_hypothesis(actuals)
    log_like_graph = graph_log_likelihood(graph, data)
    df = _amount_of_weights_on_variables_in_graph(graph)

    G_score, p_value = _g_statistic(log_like_null, log_like_graph, df)

    return G_score, p_value
