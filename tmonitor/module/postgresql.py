# Coding: UTF-8
import psycopg2
from datetime import datetime, timedelta
from traceback import print_tb, format_exception_only
from sys import exc_info, exit

class PostgreSQLConnection:       
	def connection():
		try:
		# PostgreSQL Infomation [PostgreSQL情報]
			USERID = ''		# postgreSQLログイン情報
			PASSWORD = ''	# postgreSQLパスワード情報
			IPADDRESS = ''	# postgreSQLIPアドレス情報
			PORT = ''		# postgreSQLポート番号情報
			DATABASE = ''	# postgreSQLデータベース情報
	
		# PostgreSQL Connection Module [PostgreSQL接続部品]
			return psycopg2.connect(f'postgresql://{USERID}:{PASSWORD}@{IPADDRESS}:{PORT}/{DATABASE}')
		except KeyboardInterrupt:
			print(f'\nProcess Interrupted [処理を中断しました]')
			exit(1)
		except:
		# Get ErrorMessage [エラーメッセージ取得]
			# get_system_information.GetSystemMessages.get_error_message()
			exc_type, exc_message, exc_object = exc_info()
			exc_list = format_exception_only(exc_type, exc_message)
			error_message = ''.join(exc_message for exc_message in exc_list)
			print_tb(exc_object)
			print(f'  {error_message}')
			exit(1)


class PostgreSQLinsert:
	def __init__(self, receive_status, receive_flag, receive_target):
		self.receive_status = receive_status
		self.receive_flag = receive_flag
		self.receive_target = receive_target

	def insert(self):
		connection = PostgreSQLConnection.connection()

	# Record Registration [レコード登録]
		with connection as con:
			with con.cursor() as con_cur:
				insert_sql = f"INSERT INTO alive (status, status_flag, target) VALUES('{self.receive_status}', {self.receive_flag}, '{self.receive_target}')"
				con_cur.execute(insert_sql)
				con.commit()


class PostgreSQLselect:
	def select():
		connection = PostgreSQLConnection.connection()

	# Record Reference [レコード参照]
		with connection as con:
			with con.cursor() as con_cur:
				select_sql = 'SELECT * FROM alive'
				con_cur.execute(select_sql)
				select_values = con_cur.fetchall()
				for ram in select_values:
					print(ram)


class PostgreSQLdelete:
	def delete():
	# Calculate LogDeleteDate [ログ削除日を計算]
	# KeepLogs Until 7Day [7日までログを保持]
		connection = PostgreSQLConnection.connection()
		datetime_now = datetime.now()
		delete_datetime = datetime_now + timedelta(days=-8)

	# Record Delete [レコード削除]
		with connection as con:
			with con.cursor() as con_cur:
				delete_sql = f"DELETE FROM alive WHERE timestamp < CAST('{delete_datetime}' AS timestamp without time zone);"
				con_cur.execute(delete_sql)
				con.commit()