import pandas as pd
import tableauserverclient as TSC
import csv

# makes a list of all LUIDs for workbooks that haven't been accessed recently
def check_null_and_add_id(df, field, id_field='Item LUID', type_field='Item Type', null_list=[]):
    for index, row in df.iterrows():
        if pd.isnull(row[field]) and row[type_field]=='Workbook':
            null_list.append(row[id_field])
    return null_list

def garbage_truck(df):

    #get values from csv
    pat_name, pat_secret, site_name, tab_url, dest_name = '', '', '', '', ''

    with open('garbage-truck-params.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            pat_name= row["pat-name"]
            pat_secret= row["pat-secret"]
            site_name= row["site-name"]
            tab_url= 'https://' + row["tab-pod"] + '.online.tableau.com'
            dest_name= row["dest-name"]
            break

    #authenticate to Tableau Cloud
    tableau_auth = TSC.PersonalAccessTokenAuth(pat_name, pat_secret, site_id=site_name)
    server = TSC.Server(tab_url, use_server_version=True)
    with server.auth.sign_in(tableau_auth):

        #get a list of all workbooks that have a last accessed date of null
        null_list = check_null_and_add_id(df, 'Last Accessed At (Local)')

        #collection of all project names and ids
        proj_id_name_df = pd.DataFrame(columns=['Name', 'Id'])

        #fetching the LUID of the project folder you designated
        all_project_items, pagination_item = server.projects.get()
        for i, proj in enumerate(all_project_items):
            new_item = {'Name': proj.name, 'Id': proj.id}
            proj_id_name_df.loc[i] = new_item
        dest_id = proj_id_name_df.loc[proj_id_name_df['Name'] == dest_name, 'Id'].values[0]

        #iterate through all workbooks on the site and move them
        for luid in null_list:
            # get the workbook item from the site
            workbook = server.workbooks.get_by_id(luid)

            # change to the new project ID
            workbook.project_id = dest_id

            # call the update method
            workbook = server.workbooks.update(workbook)
    return df
