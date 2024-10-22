#To do
#Make a method out of ccs limit
#Add unit test to ccs limit method

import unittest
from unittest.mock import patch
import pandas as pd
from datetime import datetime
import coverage

FILENAME = 'code_quality_test.xlsx'
INTEGRATION_TEST_FILENAME = 'code_quality_integration_test.xlsx'

def process_ccs(filename):
    # Read the Excel file
    def read_excel(filename):
        df = pd.read_excel(filename)
        return df

    # Ensure critical code smells (ccs) are never more than lines of code and add ccs_limit column
    def validate_ccs(df):
        df['Critical code smells'] = df.apply(
            lambda row: min(row['Critical code smells'], row['Lines of code']), axis=1
        )
        df['ccs_limit'] = df['Critical code smells'].apply(
            lambda ccs: 'within limit' if ccs <= 150 else 'limit breached'
        )

    def ccs_limit(ccs):
        return 'within limit' if ccs <= 150 else 'limit breached'

    def add_comments(df):
        df['comments'] = 'no change'
        for i in range(1, len(df)):
            if is_new_project_or_module(df, i):
                df.at[i, 'comments'] = 'no change'
            else:
                df.at[i, 'comments'] = determine_comment(df, i)

    def is_new_project_or_module(df, i):
        return df.at[i, 'Project'] != df.at[i-1, 'Project'] or df.at[i, 'Module'] != df.at[i-1, 'Module']

    def determine_comment(df, i):
        diff = df.at[i, 'Critical code smells'] - df.at[i-1, 'Critical code smells']
        if diff > 0:
            return 'increase'
        elif diff < 0:
            return 'decrease'
        else:
            return 'no change'

    # Save the updated DataFrame back to the Excel file
    def write_excel(df, filename):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        updated_filename = f'{filename.split(".")[0]}_updated_{timestamp}.xlsx'
        df.to_excel(updated_filename, index=False)
        df.to_excel(filename, index=False)

    df = read_excel(filename)
    validate_ccs(df)
    add_comments(df)
    write_excel(df, filename)

    return df

mydf = process_ccs(FILENAME)

########################### START OF UNIT TESTS ################################

class TestIntegration(unittest.TestCase):

    def test_integration_increase_decrease_comments(self):
        updated_df = process_ccs(INTEGRATION_TEST_FILENAME)
        
        # Check if the comments column has the expected values
        expected_comments = ['no change', 'increase','increase', 
                             'no change', 'decrease','increase', 
                             'no change', 'no change','no change']
        
        self.assertListEqual(updated_df['comments'].tolist(), expected_comments)
        print("after assert")
        print(updated_df['comments'].tolist())


if __name__ == '__main__':
    cov = coverage.Coverage()
    cov.start()

    unittest.main(exit=False)

    cov.stop()
    cov.save()
    cov.report()