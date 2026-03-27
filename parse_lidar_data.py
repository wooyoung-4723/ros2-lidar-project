import json
import mysql.connector
import pandas as pd


DB_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': '0000',   
    'database': 'lidar_db'
}


def load_lidar_data():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)

    sql = """
    SELECT id, ranges, `when`, action
    FROM lidardata
    ORDER BY id ASC
    """
    cursor.execute(sql)
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows


def parse_ranges(rows):
    parsed_data = []

    for row in rows:
        raw_ranges = row['ranges']
        action = row['action']

        
        if isinstance(raw_ranges, str):
            ranges_list = json.loads(raw_ranges)
        else:
            ranges_list = raw_ranges

        if len(ranges_list) < 360:
            ranges_list = ranges_list + [None] * (360 - len(ranges_list))
        elif len(ranges_list) > 360:
            ranges_list = ranges_list[:360]

        one_row = {}
        for i in range(360):
            one_row[f'range_{i}'] = ranges_list[i]

        one_row['action'] = action
        parsed_data.append(one_row)

    return parsed_data


def main():
    rows = load_lidar_data()
    print(f'불러온 원본 행 개수: {len(rows)}')

    parsed_data = parse_ranges(rows)
    df = pd.DataFrame(parsed_data)

    print('\n데이터프레임 shape:')
    print(df.shape)

    print('\n앞 5행:')
    print(df.head())

    output_path = 'lidar_dataset.csv'
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f'\nCSV 저장 완료: {output_path}')


if __name__ == '__main__':
    main()