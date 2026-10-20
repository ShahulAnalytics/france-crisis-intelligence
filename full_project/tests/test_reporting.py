from france_crisis.reporting import generate_report

def test_report_without_data_is_transparent(tmp_path):
 target=generate_report(tmp_path,tmp_path/'report.md')
 content=target.read_text(encoding='utf-8')
 assert 'No processed CSV datasets' in content
 assert 'not proof of a crisis' in content
