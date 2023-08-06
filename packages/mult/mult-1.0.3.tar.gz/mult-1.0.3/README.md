This description is under construction.

Parallel Computing Tools
(This is a tool to achieve clear and safe management of memory and other resources by separating parallel computations in units of files.)

並列計算ツール
(ファイルの単位で並列計算を実施することで、メモリ等の管理を明快かつ安全に実現するツールです。)

- pythonの並列処理はメモリ管理がよくわからん (不安な気持ちになる)
- そこで、いっそのことファイルごと別プロセスで立ち上げるような並列処理を考えた

## マスター側
```python
from mult import master

input_ls = [i for i in range(10)]
output_ls = master.call(
	"path_to_slave/slave.py",	# スレーブファイル名
	input_ls,	# 入力のリスト (ジョブごと)
	n = 4,	# 並列数
	job_order = "ordered",	# ジョブ実行順序 (random, ordered)
	progress = True	# 進捗表示
)
print(output_ls)	# 結果の確認
```

## スレーブ側 (slave.py)
```python
import time, random
from mult import slave

# 実行したい処理
def heavy_process(num):
	time.sleep(random.random()*3)
	return 2**num

num = slave.get_input()
result = heavy_process(num)
slave.send_output(result)
```
