# tmonitor
AliveMonitoring Module

◇Dependent ModeuleInstall

pip install git+https://github.com/tango3304/tping.git

pip install psycopg2

pip install scapy

pip install matplotlib

pip install japanize-matplotlib

pip install pandas

pip install wxPython

# PostgreSQL Infomation [PostgreSQL情報]を記載

◇tmonitor/tmonitor/module/postgresql.py

  USERID = ''		# postgreSQLログイン情報

  PASSWORD = ''	# postgreSQLパスワード情報

  IPADDRESS = ''	# postgreSQLIPアドレス情報

  PORT = ''		# postgreSQLポート番号情報

  DATABASE = ''	# postgreSQLデータベース情報

# PostgreSQL Get ValuesData Infomation

# [PostgreSQLデータ値取得情報]を記載

◇tmonitor/tmonitor/graph.py

  target_ipaddress = '' #検索IPアドレス

  year = #年

  month = #月

  day = #日
