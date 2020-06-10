def datacleaner_students():

    import pandas as pd
    import re

    df = pd.read_csv("~/store_files_airflow/raw_student_data.csv")

    def clean_student_id(st_id):
        matches = re.findall(r'\d+', st_id)
        if matches:
            return matches[0]
        return st_id

#    df['STUDENT_ID'] = df['STUDENT_ID'].map(lambda x: clean_student_id(x))

    df.to_csv('~/store_files_airflow/clean_student_data.csv', index=False)

