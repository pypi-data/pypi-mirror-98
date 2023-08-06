
# ファイル単位並列計算 [mult]

import sys
import time
import random
from sout import sout
from relpath import add_import_path
add_import_path("../../")
from _develop_mult import slave

# 実行したい処理
def heavy_process(num):
	print("処理中...")
	time.sleep(random.random()*3)
	return 2**num

# 入力を得る (マスターから受け取る) [mult]
num = slave.get_input()

# 実行したい処理
result = heavy_process(num)

# 出力を返す (マスターに返す) [mult]
slave.send_output(result)
