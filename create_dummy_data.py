import pandas as pd
import random
from datetime import datetime, timedelta

random.seed(42)

# =====================================================================
# Q1/Q2 自由回答で使うサービス名（揺れ表記含む）
# =====================================================================
Q12_SERVICE_POOL = [
    # ビズリーチ variants
    'ビズリーチ', 'ビザリーチ', 'ビスリーチ', 'bizreach', 'BizReach', 'Biz',
    # JAC
    'JAC Recruitment', 'JACリクルートメント', 'JAC', 'jac',
    # doda X
    'doda X', 'dodax', 'デューダX', 'デューダエックス',
    # doda
    'doda', 'デューダ', 'ドゥーダ',
    # リクルート系
    'リクルートエージェント', 'リクルートダイレクトスカウト', 'ダイレクトスカウト',
    'リクルートエグゼクティブエージェント', 'リクルートエグゼクティブ', 'リクルート',
    # マイナビ
    'マイナビエージェント', 'マイナビ転職', 'マイナビ',
    # LinkedInなど
    'LinkedIn', 'linked in', 'リンクトイン',
    # 外資系
    'Robert Walters', 'ロバートウォルターズ', 'Michael Page', 'マイケルペイジ',
    'Hays', 'ヘイズ', 'en world', 'エンワールド',
    # その他主要サービス
    'パソナキャリア', 'アクシスコンサルティング', 'ムービン・ストラテジック・キャリア',
    'KOTORA', 'コトラ', 'CareerCross', 'キャリアクロス', 'ミドルの転職',
    'LHH転職エージェント', 'Randstad', 'ランスタッド', 'エン転職', 'エン',
    # 無回答・その他
    'なし', '特になし', 'わからない', '', '',  # 空白を増やして未回答を模擬
]

def rand_q12_answer():
    """Q1/Q2の1枠の回答を返す（約30%は空白）"""
    if random.random() < 0.30:
        return ''
    return random.choice(Q12_SERVICE_POOL)

def gen_q12_row():
    """S1-S5を生成。S1が空の場合は全て空にする"""
    s1 = rand_q12_answer()
    if not s1:
        return ['', '', '', '', '']
    count = random.randint(1, 5)
    answers = [s1]
    for _ in range(4):
        answers.append(rand_q12_answer() if len(answers) < count else '')
    return answers[:5]

# =====================================================================
# 基本属性の設定値
# =====================================================================
PREFS = ['東京都', '大阪府', '神奈川県', '愛知県', '福岡県', '北海道', '宮城県', '広島県', '兵庫県', '埼玉県']
JOBS  = [1, 2, 3, 4, 5, 6, 7, 8]   # 職種コード
CELL  = [1, 2, 3, 4]               # セルコード

# Q3/Q4 の選択肢数（1-30）
Q34_OPTION_COUNT = 30

# Q5/Q7/Q8 対象サービス数（PANEL_SERVICE_INDEX と同じ1-17）
PANEL_SERVICE_COUNT = 17

# Q6 チャネル数（1-28）
CHANNEL_COUNT = 28

# =====================================================================
# 行生成
# =====================================================================
num_rows = 200
base_date = datetime(2025, 10, 1)
data = []

for i in range(num_rows):
    row = {}

    # --- 基本属性 (A-M) ---
    row['SAMPLEID']   = f'S{10000 + i}'
    row['ANSWERDATE'] = (base_date + timedelta(days=random.randint(0, 30))).strftime('%Y/%m/%d')
    sex = random.choice([1, 2])
    row['SEX']        = sex
    age = random.randint(28, 58)
    row['AGE']        = age
    row['AGEID']      = (age - 20) // 10 + 1   # 年代コード (1=20代, 2=30代, ...)
    row['PREFECTURE'] = random.choice(PREFS)
    row['AREA']       = random.randint(1, 9)
    row['MARRIED']    = random.choice([1, 2])   # 1=既婚, 2=未婚
    row['CHILD']      = random.choice([0, 1, 2, 3])
    row['HINCOME']    = random.choice([3, 4, 5, 6, 7, 8, 9, 10])   # 世帯年収コード
    row['PINCOME']    = random.choice([3, 4, 5, 6, 7, 8])          # 個人年収コード
    row['JOB']        = random.choice(JOBS)
    row['CELL']       = random.choice(CELL)

    # --- Q1 自由回答 (S1-S5) ---
    q1 = gen_q12_row()
    for j, ans in enumerate(q1, 1):
        row[f'Q1S{j}FA'] = ans

    # --- Q2 自由回答 (S1-S5) ---
    q2 = gen_q12_row()
    for j, ans in enumerate(q2, 1):
        row[f'Q2S{j}FA'] = ans

    # --- Q3 フラグ (1-30) + FA ---
    # 約40%の人が複数回答、選択数は1-6個
    q3_selected = set()
    if random.random() > 0.10:  # 90%が何かを選択
        n_select = random.randint(1, 6)
        q3_selected = set(random.sample(range(1, 29), min(n_select, 28)))
        # 29(その他)を低確率で追加
        if random.random() < 0.05:
            q3_selected.add(29)
        # 30(特にない)は他と排他的
        if not q3_selected and random.random() < 0.05:
            q3_selected.add(30)
    else:
        q3_selected.add(30)  # 特にない
    for opt in range(1, Q34_OPTION_COUNT + 1):
        row[f'Q3_{opt}'] = 1 if opt in q3_selected else 0
    row['Q3_29FA'] = 'その他サービス' if 29 in q3_selected else ''

    # --- Q4 フラグ (1-30) + FA ---
    q4_selected = set()
    if random.random() > 0.15:
        n_select = random.randint(1, 5)
        q4_selected = set(random.sample(range(1, 29), min(n_select, 28)))
        if random.random() < 0.05:
            q4_selected.add(29)
    else:
        q4_selected.add(30)
    for opt in range(1, Q34_OPTION_COUNT + 1):
        row[f'Q4_{opt}'] = 1 if opt in q4_selected else 0
    row['Q4_29FA'] = 'その他' if 29 in q4_selected else ''

    # --- Q5 認知 (1=内容まで知っている, 2=名前だけ, 3=知らない) ---
    for s in range(1, PANEL_SERVICE_COUNT + 1):
        # 有名サービス（1-3番）は認知率高め
        if s <= 3:
            row[f'Q5S{s}'] = random.choices([1, 2, 3], weights=[40, 40, 20])[0]
        elif s <= 9:
            row[f'Q5S{s}'] = random.choices([1, 2, 3], weights=[25, 35, 40])[0]
        else:
            row[f'Q5S{s}'] = random.choices([1, 2, 3], weights=[10, 25, 65])[0]

    # --- Q6 接触チャネル (0/1) 各サービス × 28チャネル ---
    # Q5で「知らない(3)」の場合はチャネルなし
    for s in range(1, PANEL_SERVICE_COUNT + 1):
        q5_val = row[f'Q5S{s}']
        if q5_val == 3:
            # 知らないのでチャネルは全て0
            for ch in range(1, CHANNEL_COUNT + 1):
                row[f'Q6S{s}_{ch}'] = 0
        else:
            # 1-3チャネルをランダムに選択
            n_ch = random.randint(1, 4)
            ch_selected = set(random.sample(range(1, 28), min(n_ch, 27)))
            for ch in range(1, CHANNEL_COUNT + 1):
                if ch == 28:  # 特にない（排他）
                    row[f'Q6S{s}_{ch}'] = 0
                else:
                    row[f'Q6S{s}_{ch}'] = 1 if ch in ch_selected else 0

    # --- Q7 興味度 (1=とても興味がある, ..., 5=まったく興味がない) ---
    for s in range(1, PANEL_SERVICE_COUNT + 1):
        q5_val = row[f'Q5S{s}']
        if q5_val == 3:
            row[f'Q7S{s}'] = random.choices([3, 4, 5], weights=[30, 40, 30])[0]
        elif q5_val == 2:
            row[f'Q7S{s}'] = random.choices([1, 2, 3, 4, 5], weights=[10, 25, 35, 20, 10])[0]
        else:  # q5==1: 詳しく知っている
            row[f'Q7S{s}'] = random.choices([1, 2, 3, 4, 5], weights=[25, 35, 25, 10, 5])[0]

    # --- Q8 利用意向 (1=とても利用したい, ..., 5=まったく利用したくない) ---
    for s in range(1, PANEL_SERVICE_COUNT + 1):
        q7_val = row[f'Q7S{s}']
        if q7_val in (1, 2):
            row[f'Q8S{s}'] = random.choices([1, 2, 3, 4, 5], weights=[30, 35, 20, 10, 5])[0]
        elif q7_val == 3:
            row[f'Q8S{s}'] = random.choices([1, 2, 3, 4, 5], weights=[5, 20, 40, 25, 10])[0]
        else:
            row[f'Q8S{s}'] = random.choices([1, 2, 3, 4, 5], weights=[2, 8, 20, 35, 35])[0]

    data.append(row)

# =====================================================================
# DataFrame作成・出力
# =====================================================================
df = pd.DataFrame(data)

# カラム順を明示的に指定
basic_cols = ['SAMPLEID', 'ANSWERDATE', 'SEX', 'AGE', 'AGEID', 'PREFECTURE', 'AREA',
              'MARRIED', 'CHILD', 'HINCOME', 'PINCOME', 'JOB', 'CELL']
q1_cols = [f'Q1S{j}FA' for j in range(1, 6)]
q2_cols = [f'Q2S{j}FA' for j in range(1, 6)]
q3_cols = [f'Q3_{opt}' for opt in range(1, 31)] + ['Q3_29FA']
q4_cols = [f'Q4_{opt}' for opt in range(1, 31)] + ['Q4_29FA']
q5_cols = [f'Q5S{s}' for s in range(1, PANEL_SERVICE_COUNT + 1)]
q6_cols = [f'Q6S{s}_{ch}' for s in range(1, PANEL_SERVICE_COUNT + 1)
           for ch in range(1, CHANNEL_COUNT + 1)]
q7_cols = [f'Q7S{s}' for s in range(1, PANEL_SERVICE_COUNT + 1)]
q8_cols = [f'Q8S{s}' for s in range(1, PANEL_SERVICE_COUNT + 1)]

all_cols = basic_cols + q1_cols + q2_cols + q3_cols + q4_cols + q5_cols + q6_cols + q7_cols + q8_cols
df = df[all_cols]

output_path = 'dummy_survey_data.xlsx'
df.to_excel(output_path, index=False)

print(f"OK: {output_path} ({len(df)} rows x {len(df.columns)} cols)")
print(f"  Basic: {len(basic_cols)} cols (A-M)")
print(f"  Q1/Q2 FA: {len(q1_cols)+len(q2_cols)} cols")
print(f"  Q3/Q4 flags: {len(q3_cols)+len(q4_cols)} cols")
print(f"  Q5 recognition: {len(q5_cols)} cols")
print(f"  Q6 channels: {len(q6_cols)} cols")
print(f"  Q7 interest: {len(q7_cols)} cols")
print(f"  Q8 usage intent: {len(q8_cols)} cols")
