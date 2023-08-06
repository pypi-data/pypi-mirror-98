
# ファイル単位並列計算 [mult]

import sys
from sout import sout
from relpath import add_import_path
add_import_path("../")
from _develop_mult import master

input_ls = [i for i in range(10)]

# ファイル単位並列計算 (マスター側) [mult]
output_ls = master.call(
	"./slave_test/slave_test.py",	# スレーブファイル名
	input_ls,	# 入力のリスト (ジョブごと)
	n = 4,	# 並列数
	job_order = "ordered",	# ジョブ実行順序 (random, ordered)
	progress = True,	# 進捗表示
	slave_debug = False	# スレーブの標準出力の表示 (debug)
)

sout(output_ls, None)
