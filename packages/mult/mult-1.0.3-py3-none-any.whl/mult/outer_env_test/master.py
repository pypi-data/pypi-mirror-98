from mult import master

input_ls = [i for i in range(10)]
output_ls = master.call(
	"./slave.py",	# スレーブファイル名
	input_ls,	# 入力のリスト (ジョブごと)
	n = 4,	# 並列数
	job_order = "ordered",	# ジョブ実行順序 (random, ordered)
	progress = True	# 進捗表示
)
print(output_ls)	# 結果の確認
