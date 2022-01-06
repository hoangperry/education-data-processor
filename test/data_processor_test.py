import unittest

import pandas as pd

import utils.processor as processor


class TestStringMethods(unittest.TestCase):
    examples_csv_string = 'World Rank 	Institution 	Location 	National Rank 	Quality of Education 	' \
                   'Alumni Employment 	Quality of Faculty 	Research Performance 	Quality Publications 	' \
                   'Influence 	Citations 	Score\n1	Harvard University	USA	1	2	1	1	1	1	1	1	100\n' \
                   '2	Stanford University	USA	2	10	3	2	10	4	3	2	96.7\n' \
                   '3	Massachusetts Institute of Technology	USA	3	3	11	3	> 1000	15	2	6	95.1'

    def test_byte_convert_to_df(self):
        df = processor.byte_to_df(bytes(self.examples_csv_string, 'utf-8'))
        self.assertIsInstance(df, pd.DataFrame)

    def test_parse_year_from_file_name(self):
        self.assertEquals(processor.parse_year_from_file_name('data-2018.csv'), 2018)
        self.assertEquals(processor.parse_year_from_file_name('data-1923.xxx'), 1923)
        self.assertEquals(processor.parse_year_from_file_name('hello-1999.txt'), 1999)
        self.assertEquals(processor.parse_year_from_file_name('2345.xxx'), 2345)
        self.assertEquals(processor.parse_year_from_file_name('2100'), 2100)
        self.assertEquals(processor.parse_year_from_file_name('data-0151.xxx'), 151)

    def test_duckduckgo_api_caller(self):
        api_res = processor.duckduckgo_api('Havard')
        self.assertIsInstance(api_res[0], dict)
        self.assertIsInstance(api_res[1], str)
        self.assertEquals(api_res[1], 'https://api.duckduckgo.com/?q=Havard&format=json&pretty=1')

    def test_process_data(self):
        df = processor.byte_to_df(bytes(self.examples_csv_string, 'utf-8'))
        result = processor.process_data(df)
        self.assertIsInstance(result, list)
        self.assertEquals(result.__len__(), 3)
        self.assertEquals(result[0].get('institution'), 'Harvard University')
        for i in result:
            self.assertIsInstance(i.get('quality of education'), int)
            self.assertIsInstance(i.get('national rank'), int)
            self.assertIsInstance(i.get('alumni employment'), int)

    def test_clean_university(self):
        uni_example = {
            'World rank': 1,
            'Institution': 'Harvard University',
            'Location': 'USA',
            'National rank': 1,
            'Quality of education': '> 100',
            'Alumni employment': 1,
            'Quality of faculty': 1,
            'Research performance': 1,
            'quality publications': 1,
            'influence': 1,
            'citations': 1,
            'score': 100.0,
            'description': 'Harvard University is a private Ivy League research university in Cambridge',
            'duckduckgo_search': 'https://api.duckduckgo.com/?q=Harvard%20University&format=json&pretty=1'
        }
        result = processor.clean_university(uni_example)
        self.assertIsInstance(result, dict)

        # Test lower case
        for i in result:
            self.assertRegex(i, r'[a-z]+')
        self.assertEquals(result['Quality of education'], 100)


if __name__ == '__main__':
    unittest.main(verbosity=2)
