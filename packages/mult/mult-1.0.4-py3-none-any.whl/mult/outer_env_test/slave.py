import time, random
from mult import slave

# 実行したい処理
def heavy_process(num):
	time.sleep(random.random()*3)
	return 2**num

num = slave.get_input()
result = heavy_process(num)
slave.send_output(result)