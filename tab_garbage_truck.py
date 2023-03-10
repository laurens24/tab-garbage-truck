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
    
    pat_name = {name}
    pat_secret= {secret}
    site_name= {site name}
    tab_url= 'https://' + {pod} + '.online.tableau.com'
    dest_name= {folder}

    #authenticate to Tableau Cloud
    tableau_auth = TSC.PersonalAccessTokenAuth(pat_name, pat_secret, site_id=site_name)
    server = TSC.Server(tab_url, use_server_version=True)
    with server.auth.sign_in(tableau_auth):
        
        #get a list of all workbooks that have a last accessed date of null
        null_list = check_null_and_add_id(df, 'Last Accessed At (Local)')
        
        dest_id=''

        #fetching the LUID of the project folder you designated 
        all_projects, pagination_item = server.projects.get()
        for i, proj in enumerate(all_projects):
            if proj.name == dest_name:
                dest_id=proj.id

        # if you haven't created the project yet, creates a new one with your name 
        if dest_id == '':
            new_project = TSC.ProjectItem(name=dest_name, content_permissions='LockedToProject', 
                                          description='Destination folder for the Tableau Garbage Truck script')
            new_project = server.projects.create(new_project)
            dest_id=new_project.id
            
        #iterate through all workbooks on the site and move them
        for luid in null_list:
          
            # get the workbook item from the site
            workbook = server.workbooks.get_by_id(luid)

            # change to the new project ID, and rename the workbook to include the previous project folder
            workbook.project_id = dest_id
            workbook.name = workbook.name + ':  From ' + workbook.project_name + ' Project'

            # call the update method
            workbook = server.workbooks.update(workbook)
            
    return df
