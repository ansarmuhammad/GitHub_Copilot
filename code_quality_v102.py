import unittest
from unittest.mock import patch
import pandas as pd
from datetime import datetime
import coverage

# Read the Excel file
def read_excel():
    df = pd.read_excel('code_quality_v102.xlsx')
    return df

df = read_excel()

# Ensure critical code smells (ccs) are never more than lines of code
def validate_ccs(df):
    df['Critical code smells'] = df.apply(
        lambda row: min(row['Critical code smells'], row['Lines of code']), axis=1
    )

validate_ccs(df)

# Add a comments column to mention the increase or decrease of critical code smells
def add_comments(df):
    df['comments'] = 'no change'
    for i in range(1, len(df)):
        if df.at[i, 'Project'] != df.at[i-1, 'Project'] or df.at[i, 'Module'] != df.at[i-1, 'Module']:
            df.at[i, 'comments'] = 'no change'
        else:
            diff = df.at[i, 'Critical code smells'] - df.at[i-1, 'Critical code smells']
            if diff > 0:
                df.at[i, 'comments'] = 'increase'
            elif diff < 0:
                df.at[i, 'comments'] = 'decrease'
            else:
                df.at[i, 'comments'] = 'no change'

add_comments(df)

# Save the updated DataFrame back to the Excel file
def write_excel(df):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'code_quality_v102_updated_{timestamp}.xlsx'
    df.to_excel(filename, index=False)

write_excel(df)

########################### START OF UNIT TESTS ################################

class TestReadExcel(unittest.TestCase):

    def test_read_excel_returns_dataframe(self):
        df = read_excel()
        self.assertIsInstance(df, pd.DataFrame)

    def test_read_excel_columns(self):
        df = read_excel()
        expected_columns = ['Project', 'Module', 'Critical code smells', 'Lines of code']
        self.assertTrue(all(column in df.columns for column in expected_columns))

    def test_read_excel_not_empty(self):
        df = read_excel()
        self.assertFalse(df.empty)

class TestValidateCCS(unittest.TestCase):

    def test_validate_ccs(self):
        df = pd.DataFrame({'Critical code smells': [10, 20, 30], 'Lines of code': [20, 20, 20]})
        validate_ccs(df)
        self.assertTrue(all(df['Critical code smells'] <= df['Lines of code']))

class TestAddComments(unittest.TestCase):

    def test_add_comments_increase(self):
        df = pd.DataFrame({'Project': ['A', 'A', 'A'], 'Module': ['M1', 'M1', 'M1'], 'Critical code smells': [10, 20, 30]})
        add_comments(df)
        expected_comments = ['no change', 'increase', 'increase']
        self.assertListEqual(df['comments'].tolist(), expected_comments)

    def test_add_comments_decrease(self):
        df = pd.DataFrame({'Project': ['A', 'A', 'A'], 'Module': ['M1', 'M1', 'M1'], 'Critical code smells': [30, 20, 10]})
        add_comments(df)
        expected_comments = ['no change', 'decrease', 'decrease']
        self.assertListEqual(df['comments'].tolist(), expected_comments)

    def test_add_comments_no_change(self):
        df = pd.DataFrame({'Project': ['A', 'A', 'A'], 'Module': ['M1', 'M1', 'M1'], 'Critical code smells': [10, 10, 10]})
        add_comments(df)
        expected_comments = ['no change', 'no change', 'no change']
        self.assertListEqual(df['comments'].tolist(), expected_comments)

    def test_add_comments_mixed(self):
        df = pd.DataFrame({'Project': ['A', 'A', 'A', 'A', 'A'], 'Module': ['M1', 'M1', 'M1', 'M1', 'M1'], 'Critical code smells': [10, 20, 15, 15, 25]})
        add_comments(df)
        expected_comments = ['no change', 'increase', 'decrease', 'no change', 'increase']
        self.assertListEqual(df['comments'].tolist(), expected_comments)

    def test_add_comments_project_module_change(self):
        df = pd.DataFrame({
            'Project': ['A', 'A', 'B', 'B', 'B'],
            'Module': ['M1', 'M1', 'M1', 'M2', 'M2'],
            'Critical code smells': [10, 20, 15, 15, 25]
        })
        add_comments(df)
        expected_comments = ['no change', 'increase', 'no change', 'no change', 'increase']
        self.assertListEqual(df['comments'].tolist(), expected_comments)

class TestWriteExcel(unittest.TestCase):

    @patch('code_quality_v102.datetime')
    @patch('code_quality_v102.pd.DataFrame.to_excel')
    def test_write_excel(self, mock_to_excel, mock_datetime):
        # Mock the current time
        mock_datetime.now.return_value.strftime.return_value = '20230101_120000'
        
        # Create a sample DataFrame
        df = pd.DataFrame({'Project': ['A'], 'Module': ['M1'], 'Critical code smells': [10], 'Lines of code': [20]})
        
        # Call the function
        write_excel(df)
        
        # Check if to_excel was called with the correct filename
        mock_to_excel.assert_called_once_with('code_quality_v102_updated_20230101_120000.xlsx', index=False)

if __name__ == '__main__':
    cov = coverage.Coverage()
    cov.start()

    unittest.main(exit=False)

    cov.stop()
    cov.save()
    cov.report()
