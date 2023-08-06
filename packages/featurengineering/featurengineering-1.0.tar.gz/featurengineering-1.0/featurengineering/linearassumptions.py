class Linear():
    
    def __init__(self, df):
        '''
        Initialising a feature engineering instance is only used on a certain dataframe
        '''
        self.df = df


    def diagnostic_plots(self, feature):
        '''
        A function for plotting kde, boxplot, and distribution plots
        Aimed at disgnosing 
        1. skewed/not normal distributions
        2. Outliers

        @param DataFrame, feature
        '''

        plt.figure(figsize=(12, 7), dpi=200)
        plt.subplot(1, 3, 1)
        self.df[feature].plot.kde()

        plt.subplot(1, 3, 2)
        self.df.boxplot(column=var)

        plt.subplot(1, 3, 3)
        stats.probplot(self.df[feature], dist="norm", plot=plt)

        plt.show()
