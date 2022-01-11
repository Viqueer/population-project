import statistics, math
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def bar_plots(df):
    for i in range(5):
        l = 2000+i*3
        h = l + 3
        fig, axes  = plt.subplots(1,3, figsize=(20,10))
    
        for idx, year in enumerate(range(l,h)):
            df[df['Time Period'] == year]['Observation Value'].plot.barh(ax=axes[idx])
            axes[idx].set_title(year)    
        
        fig.savefig(f'./static/images/hbars3_{i}.png')

def dispersion_plots(df):
    plt.figure(figsize=(10,10))

    def interquartile_range(sample):
        q3, q1 = np.percentile(sample, [75 ,25])
        return q3 - q1

    def quartile_range(sample):
        q3, q1 = np.percentile(sample, [75 ,25])
        return (q3 - q1)/2

    def _range(sample):
        return sample.max() - sample.min()

    def create_plot(fn, label):
        ls = []
        for year in range(2000,2015):
            ls.append(fn(df[df['Time Period'] == year]['Observation Value']))
                
        plt.plot(range(2000,2015), ls, label=label)
        plt.title('Measures of Dispersion of African Countries against Year.')
        plt.ylabel('Observation Value')
        plt.xlabel('Year')


        if label == 'Range':
            plt.savefig('./static/images/dispersion_plots.png')
        
    create_plot(statistics.mean, 'Mean')
    create_plot(statistics.variance, 'Variance')
    create_plot(statistics.stdev, 'Standard Deviation')
    create_plot(interquartile_range, 'Interquartile Range')
    create_plot(quartile_range, 'Quartile Range')
    create_plot(_range, 'Range')

    plt.legend(loc='best')

def box_plots(df):
    fig, axes  = plt.subplots(1,15, figsize=(10,10), sharey=True)
    fig.suptitle('Boxplots from 2000 to 2014')
    axes[0].set_ylabel('Observation Value')

    for idx, year in enumerate(range(2000,2015)):
        sns.boxplot(ax = axes[idx], y = df[df['Time Period'] == year]['Observation Value'])
        axes[idx].set_title(year)
        if idx > 0: axes[idx].set_ylabel('')

    fig.savefig('./static/images/boxplots.png')