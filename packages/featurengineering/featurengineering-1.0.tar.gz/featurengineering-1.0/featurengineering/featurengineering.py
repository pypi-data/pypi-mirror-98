class FeatureEngineering():
    def __init__(self, df):
        '''
        Initialising a feature engineering instance is only used on a certain dataframe
        '''
        self.df = df

    def rare_labels(self, df, feature, threshhold):
        '''
        A function for changing the category of labels less than the threshhold as 'Other'
        @param DataFrame, feature, threshhold
        @return A rare-encoded feature df[feature]
        '''
        counts = self.df[feature].value_counts()
        # Recording the value counts of each categorical label in the feature

        common = list(counts[counts > threshhold].index)

        # Filtering the common labels based on the chosen threshhold, dicided by user.

        def rare(x):
            '''
            A sub-function for labeling the rare values based on the common ones previously dicided on.
            @param: An observation from the feature column
            @return: either 'Other', the original observation, based on either being within the common or not.
            '''
            return 'other' if x not in common else x

        self.df[feature] = self.df[feature].apply(rare)
        # overwriting the original feature column
        return self.df[feature]