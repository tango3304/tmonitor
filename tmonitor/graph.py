# Coding: UTF-8
# Install need
# pip install matplotlib
# pip install japanize-matplotlib
# pip install pandas
# pip install wxPython

from module.postgresql import PostgreSQLselect
from pandas import DataFrame
from matplotlib import pyplot
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
import wx
from sys import exit, exc_info
from re import compile
from traceback import print_tb, format_exception_only


class AliveMonitoringGraph:
	def get_select_values():
		try:
		# Get Database Values [データベース取得値]
			target_ipaddress = '' #検索IPアドレス
			year = 	#年
			month = #月
			day = 	#日

		# Check IPaddress [IPアドレス確認]
		#    0-99: [1-9]?[0-9]
		# 100-199: 1[0-9]{2}(1[0-9][0-9])
		# 200-249: 2[0-4][0-9]
		# 250-255: 25[0-5]
			check_ipaddress = compile(r'^(([1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$')
			if check_ipaddress.fullmatch(target_ipaddress) == None:
				print(f"\nInvalid IPaddress [無効なIPアドレスです]")
				exit(1)
			
		# Get DataBase AliveMonitoringData [データベースから死活監視データを取得]
			select_values = PostgreSQLselect.select(target_ipaddress, year, month, day)
			dataframes = DataFrame(select_values, columns=["date", "time", "status_flag", "target"])
			time = dataframes.time
			time_length = len(time)
			status_flag = dataframes.status_flag
			return time, time_length, status_flag
		except:
		# Get ErrorMessage [エラーメッセージ取得]
			exc_type, exc_message, exc_object = exc_info()
			exc_list = format_exception_only(exc_type, exc_message)
			error_message = ''.join(exc_message for exc_message in exc_list)
			print_tb(exc_object)
			print(f'  {error_message}')
			exit(1)
		

	def graph_display():
		try:
			if __name__ == '__main__':
			# 
				time, time_length, status_flag = AliveMonitoringGraph.get_select_values()

			# Window Display [ウィンドウ表示]
				app_object = wx.App()
				frame_object = wx.Frame(None, wx.ID_ANY, 'Alive Monitoring', size=(1500, 700), style=wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.RESIZE_BORDER | wx.SYSTEM_MENU | wx.CAPTION | wx.CLIP_CHILDREN)
				panel_object = wx.Panel(frame_object, wx.ID_ANY, pos=(0,0))
				layout_object = wx.BoxSizer(wx.VERTICAL)

			#Graph Create [グラフ作成]
				figure, axes = pyplot.subplots(figsize=(15,6.35), dpi=100)
				axes.plot(time, status_flag)
				axes.set_title('Alive Monitoring')
				axes.set_xlim([0, time_length])
				pyplot.xticks(rotation=90)
				axes.set_ylim([0, 1.2])
				axes.tick_params(axis='both',which='major',labelsize=6.5)
				axes.grid(True)
				campus = FigureCanvasWxAgg(panel_object, wx.ID_ANY, figure)

			# Button Create [ボタン作成]
				button_object = wx.Button(panel_object, wx.ID_ANY, "Exit")
				button_object.Bind(wx.EVT_BUTTON, exit)

			# Graph Display [グラフ表示]
				layout_object.Add(button_object, flag=wx.ALIGN_TOP)
				layout_object.Add(campus, flag=wx.GROW)
				panel_object.SetSizer(layout_object)
				frame_object.Show()
				app_object.MainLoop()
		except:
		# Get ErrorMessage [エラーメッセージ取得]
			exc_type, exc_message, exc_object = exc_info()
			exc_list = format_exception_only(exc_type, exc_message)
			error_message = ''.join(exc_message for exc_message in exc_list)
			print_tb(exc_object)
			print(f'  {error_message}')
			exit(1)


# Main Process [メイン処理]
AliveMonitoringGraph.graph_display()