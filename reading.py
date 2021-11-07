import pandas as pd
def read_and_parse(file_path, input_source = 'csv', list_attributes_of_entities,input_reading_kwargs = None):
    '''

    :param file_path: the path where the file can be found
    :param input_source: csv file, other file format or database
    :param input_reading_kwargs: keyword args such as user name and password for database, delimiter for csv, start of file for excel
    :return:
    '''
    #TEST
    file_path = 'input.csv'
    input_source = 'csv'
    input_reading_kwargs = None#{'header' : 0}#None
    ###
    if input_source == 'csv':
        if input_reading_kwargs is None or 'header' not in input_reading_kwargs.keys():
            data = pd.read_csv(file_path)
        else:
            data = pd.read_csv(file_path, header = input_reading_kwargs['header'])

        data = data.applymap(lambda x: cleanup_text(x)) #currently there is one column - support multiple columns
        if input_reading_kwargs is None or 'parse_col' not in input_reading_kwargs.keys():
            parse_col = 0
        else:
            parse_col = input_reading_kwargs['parse_col']
        parsed_data = parse_csv(data,parse_col,list_attributes_of_entities)
    return parsed_data

def parse_csv(data, parse_col,list_attributes_of_entities):
    word_columns = data[parse_col].str.split(expand = True)
    entities_df = pd.DataFrame(index= data.index)
    num_entities = len(list_attributes_of_entities)
    for index, row in word_columns.iterrows():
        found_entities = 0
        for attribute_of_entity in list_attributes_of_entities:
            for word in row:
                if attribute_of_entity.get('digits', None) is not None and word.isdigit():
                    entities_df.loc[index, attribute_of_entity['name']] = int(word)
                if attribute_of_entity.get('word_code', None) is not None and word.find('yr') > 0:
                    entities_df.loc[index, attribute_of_entity['name']] = word.replace('yr', '')

                if attribute_of_entity.get('word_code', None) is not None and \
                        attribute_of_entity.get('uppercase', None) is not None and word.isupper() \
                        and len(word) == attribute_of_entity['length_code']:
                    entities_df.loc[index, attribute_of_entity['name']] = word

                if found_entities == num_entities:
                    break

            #TODO - handle 'some' and 5000009a
def cleanup_text(text):
    '''clean up is needed so that parsing can be correct'''
    #could do a replace dict in pandas
    new_text = text.replace('?').replace('MM', '000000').replace(' years', 'yr').\
        replace(' yr', 'yr').replace('Please','').\
        replace('us','').replace('for','')
    return  new_text



