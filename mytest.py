import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

def autoclean(input_dataframe, drop_nans=False, copy=False, encoder=None,
              encoder_kwargs=None, ignore_update_check=False):
    """Performs a series of automated data cleaning transformations on the provided data set

    Parameters
    ----------
    input_dataframe: pandas.DataFrame
        Data set to clean
    drop_nans: bool
        Drop all rows that have a NaN in any column (default: False)
    copy: bool
        Make a copy of the data set (default: False)
    encoder: category_encoders transformer
        The a valid category_encoders transformer which is passed an inferred cols list. Default (None: LabelEncoder)
    encoder_kwargs: category_encoders
        The a valid sklearn transformer to encode categorical features. Default (None)
    ignore_update_check: bool
        Do not check for the latest version of datacleaner

    Returns
    ----------
    output_dataframe: pandas.DataFrame
        Cleaned data set

    """
    '''global update_checked
    if ignore_update_check:
        update_checked = True

    if not update_checked:
        update_check('datacleaner', __version__)
        update_checked = True'''

    if copy:
        input_dataframe = input_dataframe.copy()

    if drop_nans:
        input_dataframe.dropna(inplace=True)

    if encoder_kwargs is None:
        encoder_kwargs = {}

    for column in input_dataframe.columns.values:
        # Replace NaNs with the median or mode of the column depending on the column type
        try:
            print('hit try block')
            input_dataframe[column].fillna(input_dataframe[column].median(), inplace=True)
        except TypeError:
            print('caught type error')
            most_frequent = input_dataframe[column].mode()
            # If the mode can't be computed, use the nearest valid value
            # See https://github.com/rhiever/datacleaner/issues/8
            if len(most_frequent) > 0:
                input_dataframe[column].fillna(input_dataframe[column].mode()[0], inplace=True)
            else:
                input_dataframe[column].fillna(method='bfill', inplace=True)
                input_dataframe[column].fillna(method='ffill', inplace=True)


        # Encode all strings with numerical equivalents
        if str(input_dataframe[column].values.dtype) == 'object':
            if encoder is not None:
                column_encoder = encoder(**encoder_kwargs).fit(input_dataframe[column].values)
            else:
                column_encoder = LabelEncoder().fit(input_dataframe[column].values)

            input_dataframe[column] = column_encoder.transform(input_dataframe[column].values)

    return input_dataframe

def test_type_error():
    d = {'A': ['a',np.nan,'c'], 'B': [np.nan,'e',np.nan]}
    df = pd.DataFrame(data = d)
    print(df)
    print(df['A'].dtypes)
    cleaned_data = autoclean(df)
    print(cleaned_data)

def main():
    test_type_error()

if __name__ == '__main__':
    main()
