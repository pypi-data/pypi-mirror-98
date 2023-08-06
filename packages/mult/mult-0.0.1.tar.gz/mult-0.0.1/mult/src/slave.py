
# ファイル単位並列計算 (スレーブ側) [mult]

import os
import sys
import pickle

# 入力を得る (マスターから受け取る) [mult]
def get_input():
	# ジョブ識別記号
	job_id = sys.argv[1]
	# 入力の取得
	input_filename = "./__mult_temp_data__/input_%s.pickle"%job_id
	with open(input_filename, "rb") as f:
		input_obj = pickle.load(f)
	return input_obj

# 出力を返す (マスターに返す) [mult]
def send_output(output_obj):
	# ジョブ識別記号
	job_id = sys.argv[1]
	# 出力を書き込み (一時ファイル)
	temporary_output_filename = "./__mult_temp_data__/_writing_output_%s.pickle"%job_id
	with open(temporary_output_filename, "wb") as f:
		pickle.dump(output_obj, f)
	# 一時ファイルを本ファイルに改名 (書き込みの途上でmasterプロセスが読み込み始めないようにする処置)
	output_filename = "./__mult_temp_data__/output_%s.pickle"%job_id
	os.rename(temporary_output_filename, output_filename)
