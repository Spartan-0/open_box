#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install pdfplumber


# In[7]:


#1st table
import pdfplumber
import pandas as pd

pdf_file = 'CSMVol2_PaxService.pdf'

# Extract tables from PDF pages 14 to 111
table_data = []
with pdfplumber.open(pdf_file) as pdf:
    for page_number in range(16, 115):  # Pages 14 to 111
        page = pdf.pages[page_number - 1]  # Page numbers are 1-based
        table = page.extract_table()
        if table:
            table_data.extend(table)

# Convert to Pandas DataFrame
df = pd.DataFrame(table_data[1:], columns=table_data[0])

# Remove empty or NaN columns
df = df.dropna(axis=1, how='all')

# Reset the index
df = df.reset_index(drop=True)


# In[9]:


#2nd Table
#import pdfplumber
#import pandas as pd

#pdf_file = 'CSMVol2_PaxService.pdf'

table_data = []

with pdfplumber.open(pdf_file) as pdf:
    for page_number in range(146, 148):  # Pages 14 to 111
        page = pdf.pages[page_number - 1]  # Page numbers are 1-based
        table = page.extract_table()
        if table:
            table_data.extend(table)

# Convert to Pandas DataFrame
df = pd.DataFrame(table_data[1:], columns=table_data[0])

# Remove empty or NaN columns
df = df.dropna(axis=1, how='all')

# Reset the index
df = df.reset_index(drop=True)


# In[18]:


#3rd Table

table_data = []

with pdfplumber.open(pdf_file) as pdf:
    for page_number in range(164, 165):  # Pages 14 to 111
        page = pdf.pages[page_number - 1]  # Page numbers are 1-based
        table = page.extract_table()
        if table:
            table_data.extend(table)

# Convert to Pandas DataFrame
df = pd.DataFrame(table_data[1:], columns=table_data[0])

# Remove empty or NaN columns
df = df.dropna(axis=1, how='all')

# Reset the index
df = df.reset_index(drop=True)


# In[25]:


#4th Table ---->Pending

table_data = []

with pdfplumber.open(pdf_file) as pdf:
    for page_number in range(172, 173):  # Pages 14 to 111
        page = pdf.pages[page_number - 1]  # Page numbers are 1-based
        table = page.extract_table()
        if table:
            table_data.extend(table)

# Convert to Pandas DataFrame
df = pd.DataFrame(table_data[1:], columns=table_data[0])

# Remove empty or NaN columns
df = df.dropna(axis=1, how='all')

# Reset the index
df = df.reset_index(drop=True)


# In[31]:


#5th Table 

table_data = []

with pdfplumber.open(pdf_file) as pdf:
    for page_number in range(183, 184):  # Pages 14 to 111
        page = pdf.pages[page_number - 1]  # Page numbers are 1-based
        table = page.extract_table()
        if table:
            table_data.extend(table)

# Convert to Pandas DataFrame
df = pd.DataFrame(table_data[0:])

# Remove empty or NaN columns
df = df.dropna(axis=1, how='all')

# Reset the index
df = df.reset_index(drop=True)


# In[34]:


#6th Table

table_data = []

with pdfplumber.open(pdf_file) as pdf:
    for page_number in range(186, 188):  # Pages 14 to 111
        page = pdf.pages[page_number - 1]  # Page numbers are 1-based
        table = page.extract_table()
        if table:
            table_data.extend(table)

# Convert to Pandas DataFrame
df = pd.DataFrame(table_data[1:], columns=table_data[0])

# Remove empty or NaN columns
df = df.dropna(axis=1, how='all')

# Reset the index
df = df.reset_index(drop=True)


# In[40]:


#7th Table

table_data = []

with pdfplumber.open(pdf_file) as pdf:
    for page_number in range(193, 194):  # Pages 14 to 111
        page = pdf.pages[page_number - 1]  # Page numbers are 1-based
        table = page.extract_table()
        if table:
            table_data.extend(table)

# Convert to Pandas DataFrame
df = pd.DataFrame(table_data[1:], columns=table_data[0])

# Remove empty or NaN columns
df = df.dropna(axis=1, how='all')

# Reset the index
df = df.reset_index(drop=True)


# In[55]:


#8th Table

table_data = []

with pdfplumber.open(pdf_file) as pdf:
    for page_number in range(201, 202):  # Pages 14 to 111
        page = pdf.pages[page_number - 1]  # Page numbers are 1-based
        table = page.extract_table()
        if table:
            table_data.extend(table)

# Convert to Pandas DataFrame

df = pd.DataFrame(table_data[2:], columns=table_data[1])

# Remove empty or NaN columns
df = df.dropna(axis=1, how='all')

# Reset the index
df = df.reset_index(drop=True)


# In[56]:


#9th Table

table_data = []

with pdfplumber.open(pdf_file) as pdf:
    for page_number in range(202, 203):  # Pages 14 to 111
        page = pdf.pages[page_number - 1]  # Page numbers are 1-based
        table = page.extract_table()
        if table:
            table_data.extend(table)

# Convert to Pandas DataFrame
column_names = table_data[1]
default_name = "unknown_column"
column_names = [default_name if (col is None or col.strip() == '') else col for col in column_names]
df = pd.DataFrame(table_data[2:], columns=column_names)

# Remove empty or NaN columns
df = df.dropna(axis=1, how='all')

# Reset the index
df = df.reset_index(drop=True)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[57]:


df


# In[ ]:





# In[ ]:





# In[ ]:





# In[59]:


import pandas as pd
from sqlalchemy import create_engine

# Replace with your PostgreSQL database connection details.
# Format: "postgresql://username:password@host:port/database_name"
# Example: "postgresql://myuser:mypassword@localhost:5432/mydatabase"
db_connection = "postgresql://pgadmin:#GenAI-POC-23=@pg-gen-ai-dev-db.postgres.database.azure.com:5432/postgres"

# Replace 'your_dataframe' with your DataFrame.
# Replace 'your_table_name' with the name you want for the new table in the database.
#table_name = 'section_4-customer_service_200-customer_service_agent_task_definitions'
#table_name = 'section_5-check-in_100-check-in_upgrade_check-in_options_elite_tire_check-in_options'
#An error occurred: Identifier 'section_4-customer_service_200-customer_service_agent_task_definitions' exceeds maximum length of 63 characters
table_name = 'section_5-check-in_100-check-in_codeshare_ceme-l2f1_policy'

try:
    # Create a database connection using SQLAlchemy.
    engine = create_engine(db_connection)

    # Save the DataFrame to the database as a new table.
    df.to_sql(table_name, engine, if_exists='replace', index=False)

    print(f"DataFrame saved as a new table '{table_name}' in the PostgreSQL database.")

except Exception as e:
    print(f"An error occurred: {e}")


# In[37]:


table_name = 'section_5-check-in_100-check-in_upgrade_check-in_options_elite_tire'


# In[38]:


len(table_name)


# In[ ]:




