def stratified_random_sampling(file_path):
    original_data = pd.read_csv(file_path)
    #Dropping rows which have error
    data = original_data[original_data['Error'].isna()]
    
    #Dropping the audio moth codes of the specified values
    data = data[~data['AudioMothCode'].isin(['AM-8','AM-19','AM-21','AM-28'])]
    
    #Choosing only minute long recordings
    data = data[(data['Duration'] >= 60.00) & (data['Duration'] < 61.00)]
    
    #Fltering on file size (gt 46 MB)
    data = data[(data['FileSize'].notna()) & (data['FileSize'] > 46 * 10 ** 6)]
    
    #The StartDateTime previously that I used contained some NA values for some rows of WWF
    data['date_time'] = data['Comment'].apply(lambda x: datetime.strptime(' '.join(x.split()[2:4]),'%H:%M:%S %d/%m/%Y'))

    data['hour'] = data['date_time'].dt.hour
    
    #Removing such rows where we dont have enough samples for an 'AudioMothCode'
    final = data.groupby(['AudioMothCode','hour'], group_keys=False).apply(lambda x: x.sample(1))
    grouped = final.groupby('AudioMothCode')
    final = grouped.filter(lambda x: len(x) >= 24)
    
    #After the preprocessing steps we save this to csv file
    if(final.size > 0):
        final.to_csv('ST_random_samples.csv', index=False)
        return True

    return False
    
 
file_creation = stratified_random_sampling('Peru_2019_AudioMoth_Data_Full.csv')
print(file_creation)