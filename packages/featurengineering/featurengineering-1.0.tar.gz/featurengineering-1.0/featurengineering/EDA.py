class EDA():
    def __init__(self, df):
        '''
        Initialising a feature engineering instance is only used on a certain dataframe
        '''
        self.df = df
        self.continuous = []
        self.categorical = []
        self.discrete = []
        self.numerical = []

    def info(self):
        '''
        Viewing Info of the dataframe
        '''

        print(self.df.info())

    def missing(self):
        '''
        printing percentages of missing values in each column in the dateframe
        '''
        print(df.isnull().mean())

    def categorize_features(self):
        '''
        creating different categories for features, either continuous, catgorical or discrete
        '''
        self.categorical = [
            var for var in self.df.columns if self.df[var].dtypes == 'O'
        ]
        self.numerical = [
            var for var in self.df.columns if self.df[var].dtypes != 'O'
        ]
        self.discrete = []
        for var in numerical:
            if self.df[var].nunique() < 20:
                discrete.append(var)
        self.continuous = [var for var in numerical if var not in discrete]

    def heatmap(self):
        '''
        A heat map of the numerical features in the dataframe
        '''
        sns.heatmap(self.df[self.discrete + self.continuous].corr())