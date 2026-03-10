import unittest
from analyzer import parse_log_line, analyze_logs

class TestLogAnalyzer(unittest.TestCase):
    def test_parse_log_line_valid_error(self):
        line = '192.168.1.1 - - [07/Oct/2025:11:48:00] "GET /error HTTP/1.1" 500 '
        result = parse_log_line(line)
        self.assertEqual(result['ip'], '192.168.1.1')
        self.assertEqual(result['status'], '500')

    def test_parse_log_line_non_error(self):
        line = '192.168.1.1 - - [07/Oct/2025:11:48:00] "GET /home HTTP/1.1" 200 '
        result = parse_log_line(line)
        self.assertIsNone(result)

    def test_analyze_logs(self):
        # Create a temporary log file for testing
        with open('temp.log', 'w') as f:
            f.write('192.168.1.1 - - [07/Oct/2025:11:48:00] "GET /error HTTP/1.1" 500 \n')
            f.write('192.168.1.2 - - [07/Oct/2025:11:48:01] "POST /fail HTTP/1.1" 404 \n')
        report = analyze_logs('temp.log')
        self.assertEqual(report['errors_by_status']['500'], 1)
        self.assertEqual(report['errors_by_ip']['192.168.1.1'], 1)

if __name__ == '__main__':
    unittest.main()
