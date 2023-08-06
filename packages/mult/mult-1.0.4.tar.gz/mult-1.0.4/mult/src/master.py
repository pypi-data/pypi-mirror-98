
# ファイル単位並列計算 (マスター側) [mult]

import os
import sys
import pickle
import random
import subprocess
from sout import sout
from fileinit import fileinit

# 前回の進捗コメント
pre_comment_shell = ["init"]

# 進捗表示関数
def show_progress(job_pool, slave_debug):
	all_n = len(job_pool)	# 全ジョブ数
	done_n = job_pool.count(status = "done")	# 指定ステータスのジョブの数をカウントする
	doing_idx_ls = job_pool.get_all_idx(status = "doing")	# 指定ステータスのジョブ(index)をすべて取得
	doing_str = ", ".join([str(e) for e in doing_idx_ls])
	show_str = "[mult] running jobs [done: %d/%d, doing: %s]..."%(done_n, all_n, doing_str) + " "*5
	# 前回とコメントの違いがない場合はスキップ
	if show_str == pre_comment_shell[0]: return None
	end_s = ("\n" if slave_debug else "\r")
	print(show_str, end = end_s)
	pre_comment_shell[0] = show_str

# popenをたたく際のデフォルト処理 (単に「python」コマンドを使う)
def default_popen_call_func(slave_filename, job_id, slave_debug):
	# ディレクトリ名を取り除いたファイル名を取得
	slave_basename = os.path.basename(slave_filename)
	# 標準・エラー出力の扱い
	std_args = ({} if slave_debug else {"stdout": subprocess.PIPE, "stderr": subprocess.PIPE})
	# 子プロセスを叩く
	subprocess.Popen(
		["python", slave_basename, job_id],
		cwd = slave_filename+"/../",	# slaveファイルが存在するディレクトリ
		**std_args	# 標準・エラー出力の扱い
	)

# 16進数の記号
symbol_16 = [str(i) for i in range(10)] + list("abcdef")

# ランダムな接頭辞の生成 (ジョブ識別記号に用いる)
def gen_random_prefix(n):
	ls = [random.choice(symbol_16) for _ in range(n)]
	return "".join(ls)

# ジョブ管理
class JobPool:
	# 初期化処理
	def __init__(self):
		# 全ジョブの一覧
		self._job_ls = []
		# ステータス引き当て辞書
		self._status_dic = {}
		self._status_inv_dic = {}	# 逆引き
	# ジョブを追加
	def add_job(self, job, status):
		# 追記
		self._job_ls.append(job)
		# ステータス辞書追記
		new_idx = len(self._job_ls) - 1
		if status not in self._status_dic:
			self._status_dic[status] = []
		self._status_dic[status].append(new_idx)
		# ステータス逆引き辞書追記
		self._status_inv_dic[new_idx] = status
	# 指定ステータスのジョブの数をカウントする
	def count(self, status):
		# 指定ステータスのジョブ(index)をすべて取得
		idx_ls = self.get_all_idx(status)
		return len(idx_ls)
	# 全ジョブ数を数える
	def __len__(self):
		return len(self._job_ls)
	# 指定ステータスのジョブ(index)をすべて取得
	def get_all_idx(self, status):
		if status not in self._status_dic: return []
		return self._status_dic[status]
	# インデックスでジョブを取得
	def get_job(self, job_idx):
		return self._job_ls[job_idx]
	# ジョブのステータスを変更
	def update_status(self, job_idx, new_status):
		# 変更前のステータス取得
		old_status = self._status_inv_dic[job_idx]
		# 逆引き辞書を更新
		self._status_inv_dic[job_idx] = new_status
		# ステータス辞書を更新
		self._status_dic[old_status].remove(job_idx)
		if new_status not in self._status_dic: self._status_dic[new_status] = []
		self._status_dic[new_status].append(job_idx)

# ジョブ識別記号からジョブの識別インデックスの取り出し
def to_idx(job_id):
	_, str_idx = job_id.split("_")
	return int(str_idx)

# リストから1つの要素を取得
def choose_one(arg_ls, arg_order):
	# リスト長を確かめる
	if len(arg_ls) == 0: raise Exception("[error] arg_lsは要素数1以上のリストである必要があります")
	# モードに従って選ぶ
	if arg_order == "random":
		return random.choice(arg_ls)
	if arg_order == "ordered":
		return arg_ls[0]
	# arg_orderの指定が不正
	raise Exception("[error] arg_orderの指定が不正です")

# ジョブの投入
def throw_job(job, data_dir, slave_filename, popen_call_func, slave_debug):
	# ジョブ識別記号
	job_id = job["job_id"]
	# 入力オブジェクト
	input_obj = job["input_obj"]
	# inputデータの設置
	input_filename = "%s/input_%s.pickle"%(data_dir, job_id)
	fileinit(input_filename, overwrite = True)
	with open(input_filename, "wb") as f:
		pickle.dump(input_obj, f)
	# popenをたたく処理
	popen_call_func(slave_filename, job_id, slave_debug)

# 指定したジョブが完了していれば結果を返す (未完了の場合はNoneを返す)
def get_job_result(job_id, data_dir):
	# 入出力ファイル名
	input_filename = "%s/input_%s.pickle"%(data_dir, job_id)
	output_filename = "%s/output_%s.pickle"%(data_dir, job_id)
	in_progress_filename = "%s/_writing_in_progress_%s"%(data_dir, job_id)
	# outputデータ読み込む
	if os.path.exists(in_progress_filename) is True: return None
	if os.path.exists(output_filename) is False: return None
	with open(output_filename, "rb") as f:
		result_obj = pickle.load(f)
	# お掃除 (子プロセスの入出力で使用したファイルの削除)
	os.remove(input_filename)	# ファイルを削除する
	os.remove(output_filename)
	return result_obj

# ファイル単位並列計算 (マスター側) [mult]
def call(
	slave_filename,	# スレーブファイル名
	input_ls,	# 入力のリスト (ジョブごと)
	n,	# 並列数
	job_order = "ordered",	# ジョブ実行順序 (random, ordered)
	progress = False,	# 進捗表示
	popen_call_func = None,	# popenをたたく際のカスタム処理 (デフォルトのNone指定で単に「python」コマンドを使う; 引数はslave_filename, job_idx, slave_debug)
	slave_debug = False	# スレーブの標準出力の表示 (debug)
):
	# デフォルトのpopenの場合
	if popen_call_func is None:
		popen_call_func = default_popen_call_func
	# 入出力データの設置場所
	data_dir = "%s/../__mult_temp_data__/"%slave_filename
	# ジョブ識別記号
	jid_prefix = gen_random_prefix(n = 16)	# ランダムな接頭辞の生成 (ジョブ識別記号に用いる)
	# ジョブ投入を部分適用 (引数が多くてわかりにくいため)
	throw_job_partial = lambda job: throw_job(job, data_dir, slave_filename, popen_call_func, slave_debug)	# ジョブの投入
	# jobを列挙
	job_pool = JobPool()	# ジョブ管理
	for idx, input_obj in enumerate(input_ls):
		job = {"job_id": "%s_%d"%(jid_prefix, idx), "input_obj": input_obj}
		job_pool.add_job(job, status = "todo")	# ジョブを追加
	# メインループ
	output_ls = [None for _ in input_ls]
	while True:
		# 進捗表示
		if progress is True: show_progress(job_pool, slave_debug)	# 進捗表示関数
		# 完了判定
		done_n = job_pool.count(status = "done")	# 指定ステータスのジョブの数をカウントする
		if done_n == len(job_pool): break	# すべてdoneの場合
		# ジョブの投入
		todo_n = job_pool.count(status = "todo")	# 指定ステータスのジョブの数をカウントする
		doing_n = job_pool.count(status = "doing")	# 指定ステータスのジョブの数をカウントする
		if todo_n > 0 and doing_n < n:
			todo_idx_ls = job_pool.get_all_idx(status = "todo")	# 指定ステータスのジョブ(index)をすべて取得
			job_idx = choose_one(todo_idx_ls, job_order)	# リストから1つの要素を取得
			job = job_pool.get_job(job_idx)	# インデックスでジョブを取得
			throw_job_partial(job)	# ジョブ投入 (部分適用されたもの)
			job_pool.update_status(job_idx, "doing")	# ジョブのステータスを変更
		# 完了したジョブの対処
		doing_idx_ls = job_pool.get_all_idx(status = "doing")	# 指定ステータスのジョブ(index)をすべて取得
		for job_idx in doing_idx_ls:
			job_id = job_pool.get_job(job_idx)["job_id"]
			# 指定したジョブが完了していれば結果を返す (未完了の場合はNoneを返す)
			result_obj = get_job_result(job_id, data_dir)
			if result_obj is None: continue
			idx = to_idx(job_id)	# ジョブ識別記号からジョブの識別インデックスの取り出し
			output_ls[idx] = result_obj	# 結果の格納
			job_pool.update_status(job_idx, "done")	# ジョブのステータスを変更
	if progress is True: print("■■■[mult] completed all jobs!■■■"+" "*5)	# 完了表示
	return output_ls
