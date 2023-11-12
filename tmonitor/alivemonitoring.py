# Coding: UTF-8
from tping.tping import PingSocket
from module.postgresql import PostgreSQLinsert, PostgreSQLdelete#, PostgreSQLselect
from time import sleep
from itertools import repeat
from scapy.layers.inet import IP
from re import compile
from traceback import format_exception_only, print_tb
from sys import exc_info, exit


class MainProcess:
	def __init__(self,ipaddress):
	# Check IPaddress [IPアドレス確認]
	#    0-99: [1-9]?[0-9]
	# 100-199: 1[0-9]{2}(1[0-9][0-9])
	# 200-249: 2[0-4][0-9]
	# 250-255: 25[0-5]
		check_ipaddr = compile(r'(^(([1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$)')
		if check_ipaddr.fullmatch(ipaddress) == None:
			print(f"\nInvalid IPaddress [無効なIPアドレスです]")
			exit(1)
		self.ipaddr = ipaddress
	
	def alive_monitoring(self):
		timeout = 3
		sleep_time = 60
		connection_count = 0
		error_flag = 2

		try:
			for i in repeat(None):
			# Remove PastLog DateBase [過去ログをデータベースから削除]
				PostgreSQLdelete.delete()
			
			# Add NewLog DateBase [新しいログをデータベースに追加]
				connection_count = AliveMonitoring.echo_Request_reply_module(self.ipaddr, timeout, connection_count)
				if connection_count > error_flag:
					print(f'{connection_count}回連続で死活の疎通確認でエラーが発生しました')
				sleep(sleep_time)
		except KeyboardInterrupt:
		# (Ctrl + c) Process [(Ctrl + c) の処理]
			print(f'\nProcess Interrupted [処理を中断しました]')
			exit(1)
		except:
		# Get ErrorMessage [エラーメッセージ取得]
			exc_type, exc_message, exc_object = exc_info()
			exc_list = format_exception_only(exc_type, exc_message)
			error_message = ''.join(i for i in exc_list)
			print_tb(exc_object)
			print(f'\n{error_message}')
			exit(1)


class AliveMonitoring:
# Add NewLog DateBase [新しいログをデータベースに追加]
	def echo_Request_reply_module(ipaddress, timeout, count):
		try:
		# Get ReceivePacket [受信パケット取得]
			receive_icmp_result, timestamp  = PingSocket(ipaddress, timeout).ping_socket()
		
		# ReceivePacket Analysis [受信パケット解析]
		# ReceivePacket Analysis Result In DataBase [受信パケット解析結果をDBに格納]
		# TimeOutProcess [タイムアウト処理]
			if receive_icmp_result == 'Timeout' and timestamp == None:
				timeout_status = 'timeout'
				status_flag = 0
				timeout_target = ipaddress
				PostgreSQLinsert(timeout_status, status_flag, timeout_target).insert()
				count += 1
				return count
			else:
				receive_icmp_analysis = IP(receive_icmp_result)
				receive_target = receive_icmp_analysis.src
				receive_type = receive_icmp_analysis.type
				receive_code = receive_icmp_analysis.code
				normal_status = 'normal'
				status_flag = 1
			# NormalProcess [正常処理]
				if (receive_type == 0) and (receive_code == 0):
					PostgreSQLinsert(normal_status, status_flag, receive_target).insert()
					count = 0
					return count
				else:
			# ErrorProcess [エラー処理]
					error_status = 'error'
					status_flag = 0
					PostgreSQLinsert(error_status, status_flag, receive_target).insert()
					count += 1
					return count
		except KeyboardInterrupt:
		# (Ctrl + c) Process [(Ctrl + c) の処理]
			print(f'\nProcess Interrupted [処理を中断しました]')
			exit(1)
		except:
		# Get ErrorMessage [エラーメッセージ取得]
			exc_type, exc_message, exc_object = exc_info()
			exc_list = format_exception_only(exc_type, exc_message)
			error_message = ''.join(i for i in exc_list)
			print_tb(exc_object)
			print(f'\n{error_message}')
			exit(1)