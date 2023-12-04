from domain.report.report_schema import ReportInput
from util import generate_unique_id

def file_report(file_report: ReportInput, conn, reporter_uid):
    cursor = conn.cursor()
    data = []
    report_id = generate_unique_id(conn, 'T', 'REPORT', 'report_id')
    sql = "INSERT INTO report (report_id, reason, reported_uid, reporter_uid) VALUES \
        (:1, :2, :3, :4)"
    data = [(report_id, file_report.reason, file_report.reported_uid, reporter_uid)]

    try:
        cursor.executemany(sql, data)
        result = "신고가 정상적으로 접수되었습니다."
        conn.commit()
    except:
        result = "신고 접수 중 에러가 발생하였습니다."
    cursor.close()
    conn.close()
    return result

def list_report(user_id, conn):
    report_list = []
    cursor = conn.cursor()
    sql = "SELECT * FROM report"
    if user_id is not None: # get report with user_id
        sql = f"{sql} WHERE report.reporter_uid = '{user_id}'"
    cursor.execute(sql)

    # report format:
    # ('T0000001', 1, 'U1001001', 'U1000001');
    for row in cursor:
        report = f"report_id = {row[0]}, reason = {row[1]}, reported_uid = {row[2]}, reporter_uid = {row[3]}"
        report_list.append(report)
    cursor.close()
    conn.close()
    return report_list

def check_report_exists(reporter_uid, reported_uid, conn):
    cursor = conn.cursor()
    sql = "SELECT COUNT(*) FROM report WHERE reporter_uid = :reporter_uid AND reported_uid = :reported_uid"
    cursor.execute(sql, [reporter_uid, reported_uid])
    (count,) = cursor.fetchone()
    return count > 0
