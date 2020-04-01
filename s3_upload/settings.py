# ------------------------------------------
# 
# Program created by Maksim Kumundzhiev
#
#
# email: kumundzhievmaxim@gmail.com
# github: https://github.com/KumundzhievMaxim
# -------------------------------------------


APP = dict(
    name='S3_Uploader',
    source='tfl-accidents',
    description='Data Uploader Job to upload data to dedicated S3 bucket.',
    epilog="""
    To Run Script Successfully it is Required to Use Arguments:\n
        --id   - TFL Application ID
        --key  - TFL Application KEY
        --year - Year of accidents to be downloaded
    """
    )

