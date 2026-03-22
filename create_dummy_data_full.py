"""
Generate a realistic 1000-row dummy survey dataset (1695 columns) as Excel.
Uses random.seed(42) for reproducibility.
"""

import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

random.seed(42)
np.random.seed(42)

N = 1000

# ---------------------------------------------------------------------------
# 揺れ.txt entries (read from file)
# ---------------------------------------------------------------------------
with open(r"c:\Users\cy131\Downloads\正規化\揺れ.txt", encoding="utf-8") as f:
    yure_raw = []
    for line in f:
        line = line.strip()
        if not line:
            continue
        # format: "number→text" or just "number→"
        if "→" in line:
            text = line.split("→", 1)[1].strip()
            if text:
                yure_raw.append(text)

# Classify entries
service_names_correct = [
    "ビズリーチ", "BizReach", "JAC Recruitment", "JACリクルートメント",
    "doda X", "doda", "リクルートエージェント", "リクルートダイレクトスカウト",
    "LinkedIn", "マイナビ転職", "マイナビエージェント", "エン転職",
    "ミドルの転職", "インディード", "パソナ", "ロバートウォルターズ",
    "Robert Walters", "HAYS", "コトラ", "クライスアンドカンパニー",
    "ランスタッド", "リクナビNEXT", "リクナビネクスト", "indeed",
    "マイナビ", "パソナキャリア", "リクルートエグゼクティブエージェント",
]

service_names_typo = [
    "ビザリーチ", "ビスリーチ", "ビズリーーチ", "バズリーチ", "ピザリーチ",
    "びずりーち", "びすりーち", "ビズリート", "ビズリ-チ", "バスリーチ",
    "リズビーチ", "ビズーリーチ", "ビィズリーチ", "ビズビーチ", "ヒズリーチ",
    "bzreach", "bizreach", "biz reach", "BIZSEARCH", "bizpeach",
    "Bizリーチ", "ビズりーち", "ビバリーチ", "リブリーチ",
    "Duda", "DIDA", "dida", "デュダ", "ドゥーダ", "でゆーだー", "ドユーダ",
    "デューダ", "デューダX", "DODAX", "dudaX", "デューダEX", "DODA EX",
    "JCリクルートメント", "JACリクルート", "JACリクルートめんと", "jrac", "JACR",
    "JAC", "JRC", "JRA", "JACリサーチ",
    "リクルートエージェンシー", "リクナビエージェント", "リクルートキャリア",
    "linked in", "linkdin", "Linkedin",
    "インリード", "インニード", "インディーど", "inndeed",
    "enジャパン", "エンジャパン", "えんてんしょく",
]

no_answer = [
    "なし", "特になし", "特にない", "ない", "わからない", "無い",
    "分からない", "知らない", "思い浮かばない", "思い出せない",
    "とくになし", "解らない", "覚えてない", "無いです", "しらない",
    "思いつかない", "無し", "特にありません", "わかりません", "分かりません",
    "特に無い", "特に思い浮かばない", "知りません", "特にございません",
    "不明", "ありません", "ないです", "特に無し", "とくにない",
    "思いつきません", "特にはない", "よく知らない",
]

garbage = [
    "Jvuuggf", "ygcvh", "ぐっづg", "uf", "oi", "hg", "vj", "fs",
    "ゃなやまやまなまなまなまなまなま", "やたやたやたやたやたやたやたやたや",
    "らまらならな", "ゃ/;", "oooi", "Gtg", "Fcc", "GRG", "Vuuvvuvuc",
    "いぢxkcm", "zjぉxmxl", "ｊｆｚ", "Ygvuu", "oko", "Ccc",
    "早苗地獄に堕ちろ", "ありがとうございます。", "買いました",
]

generic_terms = [
    "転職エージェント", "ハイクラス転職", "スカウト", "ヘッドハンティング",
    "転職サービス", "転職", "エグゼクティブ", "スカウトサービス",
    "ハイクラス", "転職ナビ", "転職サイト", "高年収",
]


def pick_free_text(slot_num):
    """Generate free text for Q1/Q2 with realistic distribution."""
    # Higher slot numbers are more likely to be empty
    empty_prob = 0.30 + 0.15 * (slot_num - 1)  # S1=30%, S2=45%, S3=60%, S4=75%, S5=90%
    if random.random() < empty_prob:
        return ""
    r = random.random()
    if r < 0.40:
        return random.choice(service_names_correct)
    elif r < 0.70:
        return random.choice(service_names_typo)
    elif r < 0.85:
        return random.choice(no_answer)
    elif r < 0.90:
        return random.choice(garbage)
    else:
        return random.choice(generic_terms)


# ---------------------------------------------------------------------------
# 17 services (for Q5-Q9, Q10, etc.)
# ---------------------------------------------------------------------------
SERVICES_17 = [
    "JAC Recruitment", "CareerCross", "BizReach", "doda X", "LinkedIn",
    "RECRUIT DIRECT SCOUT", "ミドルの転職", "doda", "LHH転職エージェント",
    "KOTORA", "ムービン・ストラテジック・キャリア", "KREIS＆Company Inc.",
    "アクシスコンサルティング", "RECRUIT AGENT", "Robert Walters", "Hays",
    "Michael Page",
]

# 9 corporations (for Q12-Q15)
CORPS_9 = [
    "JAC Recruitment", "PERSOL Holdings", "RECRUIT Holdings",
    "マイナビ", "エン・ジャパン", "BizReach", "Michael Page",
    "Robert Walters", "Hays",
]

# Recognition base rates per service (1-indexed, services 1-3 higher)
SVC_RECOG = [0.55, 0.20, 0.80, 0.45, 0.50, 0.60, 0.35, 0.70, 0.15,
             0.12, 0.08, 0.10, 0.10, 0.65, 0.18, 0.12, 0.10]

# 47 prefectures, weighted toward Kanto/Kansai
PREF_WEIGHTS = np.ones(47)
# Kanto (8-14 = 茨城-東京-神奈川, 0-indexed 7-13)
PREF_WEIGHTS[7:14] = 5.0
PREF_WEIGHTS[12] = 15.0  # Tokyo
# Kansai
PREF_WEIGHTS[24:30] = 3.0  # Shiga - Nara
PREF_WEIGHTS[26] = 8.0   # Osaka
# Aichi
PREF_WEIGHTS[22] = 5.0
PREF_WEIGHTS /= PREF_WEIGHTS.sum()

# Region mapping (0-indexed pref)
def get_region(sq1):
    """Return region: 'kanto', 'kansai', 'other' based on SQ1 (1-indexed)."""
    if 8 <= sq1 <= 14:
        return "kanto"
    elif 25 <= sq1 <= 30:
        return "kansai"
    else:
        return "other"


# ---------------------------------------------------------------------------
# Build data row by row
# ---------------------------------------------------------------------------
rows = []

for i in range(N):
    row = {}

    # --- Demographics ---
    row["SAMPLEID"] = f"S{10001 + i}"

    # ANSWERDATE: random in Oct-Nov 2025
    base_date = datetime(2025, 10, 1)
    row["ANSWERDATE"] = (base_date + timedelta(days=random.randint(0, 60))).strftime("%Y/%m/%d")

    # SEX
    sex = random.choices([1, 2], weights=[0.65, 0.35])[0]
    row["SEX"] = sex

    # AGE (25-64, skewed toward 35-54)
    age = int(np.clip(np.random.normal(44, 9), 25, 64))
    row["AGE"] = age

    # AGEID (match AGE)
    if age < 12:
        ageid = 1
    elif age <= 19:
        ageid = 2
    elif age <= 24:
        ageid = 3
    elif age <= 29:
        ageid = 4
    elif age <= 34:
        ageid = 5
    elif age <= 39:
        ageid = 6
    elif age <= 44:
        ageid = 7
    elif age <= 49:
        ageid = 8
    elif age <= 54:
        ageid = 9
    elif age <= 59:
        ageid = 10
    else:
        ageid = 11
    row["AGEID"] = ageid

    # MARRIED, CHILD
    row["MARRIED"] = random.choices([1, 2], weights=[0.35, 0.65])[0]
    row["CHILD"] = random.choices([1, 2], weights=[0.40, 0.60])[0] if row["MARRIED"] == 2 else random.choices([1, 2], weights=[0.90, 0.10])[0]

    # SQ1 prefecture
    sq1 = int(np.random.choice(range(1, 48), p=PREF_WEIGHTS))
    row["SQ1"] = sq1
    region = get_region(sq1)

    # SQ2 occupation (1-28)
    row["SQ2"] = random.randint(1, 28)

    # SQ3 income - high class focus (5-17 = 600万+)
    sq3 = random.choices(
        list(range(1, 20)),
        weights=[1, 2, 3, 4, 8, 8, 7, 6, 5, 4, 3, 2, 2, 1, 1, 1, 1, 1, 1]
    )[0]
    row["SQ3"] = sq3

    # SQ4 position (1-8)
    sq4 = random.choices(list(range(1, 9)), weights=[3, 3, 8, 12, 10, 6, 3, 2])[0]
    row["SQ4"] = sq4

    # SQ4_8FA
    row["SQ4_8FA"] = random.choice(["フリーランス", "自営業", "個人事業主", "顧問", "アドバイザー"]) if sq4 == 8 else ""

    # SQ5 job change intent (1-7)
    row["SQ5"] = random.choices(list(range(1, 8)), weights=[5, 6, 8, 10, 15, 8, 5])[0]

    # CELL (1-114) and CELLNAME
    cell = random.randint(1, 114)
    row["CELL"] = cell
    # Simplified cell name
    sex_label = "男性" if sex == 1 else "女性"
    age_range = f"{(age // 10) * 10}-{(age // 10) * 10 + 9}歳"
    row["CELLNAME"] = f"セル{cell}_{sex_label}{age_range}"

    # --- Q1S1FA-Q1S5FA, Q2S1FA-Q2S5FA ---
    for q in ["Q1", "Q2"]:
        for s in range(1, 6):
            row[f"{q}S{s}FA"] = pick_free_text(s)

    # --- Q3 (MA, 30 flags) - awareness of services ---
    q3_flags = [0] * 30
    for j in range(30):
        if j < 17:
            prob = SVC_RECOG[j] * 0.8
        else:
            prob = 0.05
        q3_flags[j] = 1 if random.random() < prob else 0
    # Ensure at least 1 selected
    if sum(q3_flags) == 0:
        q3_flags[random.randint(0, 29)] = 1
    for j in range(30):
        row[f"Q3_{j+1}"] = q3_flags[j]

    # Q3_29FA (only if Q3_29 = 1)
    row["Q3_29FA"] = random.choice(service_names_typo + service_names_correct) if q3_flags[28] == 1 else ""

    # --- Q4 (MA, 30 flags) - usage ---
    q4_flags = [0] * 30
    for j in range(30):
        # Can only use if aware (roughly)
        if q3_flags[j] == 1:
            q4_flags[j] = 1 if random.random() < 0.35 else 0
        else:
            q4_flags[j] = 1 if random.random() < 0.02 else 0
    if sum(q4_flags) == 0:
        q4_flags[random.randint(0, 29)] = 1
    for j in range(30):
        row[f"Q4_{j+1}"] = q4_flags[j]

    row["Q4_29FA"] = random.choice(service_names_typo + service_names_correct) if q4_flags[28] == 1 else ""

    # --- Q5S1-Q5S17 (SA, 1-3: 1=知っている, 2=聞いたことがある, 3=知らない) ---
    q5 = []
    for s in range(17):
        prob_know = SVC_RECOG[s]
        val = random.choices([1, 2, 3], weights=[prob_know, prob_know * 0.5, 1 - prob_know * 1.5 if prob_know < 0.6 else 0.05])[0]
        q5.append(val)
        row[f"Q5S{s+1}"] = val

    # --- Q6: 17 services x 28 channels (MA flags) ---
    for s in range(1, 18):
        known = q5[s - 1] in [1, 2]
        for c in range(1, 29):
            if known:
                row[f"Q6S{s}_{c}"] = 1 if random.random() < 0.08 else 0
            else:
                row[f"Q6S{s}_{c}"] = 0
    # Q6 FA columns (Q6S1_27FA - Q6S17_27FA)
    for s in range(1, 18):
        if row.get(f"Q6S{s}_27", 0) == 1:
            row[f"Q6S{s}_27FA"] = random.choice(["SNS", "友人紹介", "口コミサイト", "知人", "広告"])
        else:
            row[f"Q6S{s}_27FA"] = ""

    # --- Q7S1-Q7S17 (SA, 1-5: interest) ---
    for s in range(1, 18):
        if q5[s - 1] == 1:
            row[f"Q7S{s}"] = random.choices([1, 2, 3, 4, 5], weights=[15, 25, 30, 20, 10])[0]
        elif q5[s - 1] == 2:
            row[f"Q7S{s}"] = random.choices([1, 2, 3, 4, 5], weights=[5, 15, 30, 30, 20])[0]
        else:
            row[f"Q7S{s}"] = random.choices([1, 2, 3, 4, 5], weights=[2, 5, 20, 35, 38])[0]

    # --- Q8S1-Q8S17 (SA, 1-5: usage intent) ---
    for s in range(1, 18):
        q7val = row[f"Q7S{s}"]
        if q7val <= 2:
            row[f"Q8S{s}"] = random.choices([1, 2, 3, 4, 5], weights=[20, 30, 25, 15, 10])[0]
        elif q7val == 3:
            row[f"Q8S{s}"] = random.choices([1, 2, 3, 4, 5], weights=[5, 15, 35, 30, 15])[0]
        else:
            row[f"Q8S{s}"] = random.choices([1, 2, 3, 4, 5], weights=[2, 8, 20, 35, 35])[0]

    # --- Q9: 17 services x 30 image options (MA flags) ---
    for s in range(1, 18):
        known = q5[s - 1] in [1, 2]
        for o in range(1, 31):
            if known:
                row[f"Q9S{s}_{o}"] = 1 if random.random() < 0.07 else 0
            else:
                row[f"Q9S{s}_{o}"] = 0
    # Q9 FA columns
    for s in range(1, 18):
        if row.get(f"Q9S{s}_29", 0) == 1:
            row[f"Q9S{s}_29FA"] = random.choice(service_names_correct + generic_terms)
        else:
            row[f"Q9S{s}_29FA"] = ""

    # --- Q10S1 (MA, 30 flags - all used services), Q10S2 (subset - most used) ---
    q10s1 = [0] * 30
    for j in range(30):
        if j < 17 and q5[j] == 1:
            q10s1[j] = 1 if random.random() < 0.25 else 0
        else:
            q10s1[j] = 1 if random.random() < 0.02 else 0
    if sum(q10s1) == 0:
        q10s1[random.randint(0, 29)] = 1
    for j in range(30):
        row[f"Q10S1_{j+1}"] = q10s1[j]

    # Q10S2 is subset of Q10S1
    q10s2 = [0] * 30
    used_indices = [j for j in range(30) if q10s1[j] == 1]
    if used_indices:
        n_most = max(1, len(used_indices) // 2)
        for j in random.sample(used_indices, min(n_most, len(used_indices))):
            q10s2[j] = 1
    for j in range(30):
        row[f"Q10S2_{j+1}"] = q10s2[j]

    # Q10 FA
    row["Q10S1_29FA"] = random.choice(service_names_correct) if q10s1[28] == 1 else ""
    row["Q10S2_29FA"] = random.choice(service_names_correct) if q10s2[28] == 1 else ""

    # --- Q11S1 (MA, 30 flags - all important), Q11S2 (subset - most important) ---
    q11s1 = [0] * 30
    for j in range(30):
        q11s1[j] = 1 if random.random() < 0.10 else 0
    if sum(q11s1) == 0:
        q11s1[random.randint(0, 29)] = 1
    for j in range(30):
        row[f"Q11S1_{j+1}"] = q11s1[j]

    q11s2 = [0] * 30
    imp_indices = [j for j in range(30) if q11s1[j] == 1]
    if imp_indices:
        n_most = max(1, len(imp_indices) // 2)
        for j in random.sample(imp_indices, min(n_most, len(imp_indices))):
            q11s2[j] = 1
    for j in range(30):
        row[f"Q11S2_{j+1}"] = q11s2[j]

    row["Q11S1_29FA"] = random.choice(generic_terms) if q11s1[28] == 1 else ""
    row["Q11S2_29FA"] = random.choice(generic_terms) if q11s2[28] == 1 else ""

    # --- Q12S1-Q12S9 (SA, 1-3: corporate recognition) ---
    q12 = []
    corp_recog_rates = [0.50, 0.40, 0.70, 0.60, 0.35, 0.75, 0.10, 0.18, 0.12]
    for s in range(9):
        p = corp_recog_rates[s]
        val = random.choices([1, 2, 3], weights=[p, p * 0.4, 1 - p * 1.4 if p < 0.7 else 0.05])[0]
        q12.append(val)
        row[f"Q12S{s+1}"] = val

    # --- Q13S1-Q13S9 (SA, 1-5: corporate attractiveness) ---
    for s in range(9):
        if q12[s] in [1, 2]:
            row[f"Q13S{s+1}"] = random.choices([1, 2, 3, 4, 5], weights=[10, 20, 35, 25, 10])[0]
        else:
            row[f"Q13S{s+1}"] = random.choices([1, 2, 3, 4, 5], weights=[2, 8, 25, 35, 30])[0]

    # --- Q14S1-Q14S9 (SA, 1-5: want to work there) ---
    for s in range(9):
        if q12[s] in [1, 2]:
            row[f"Q14S{s+1}"] = random.choices([1, 2, 3, 4, 5], weights=[8, 18, 35, 25, 14])[0]
        else:
            row[f"Q14S{s+1}"] = random.choices([1, 2, 3, 4, 5], weights=[2, 5, 20, 38, 35])[0]

    # --- Q15: 9 corps x 29 image options (MA flags) ---
    for s in range(1, 10):
        known = q12[s - 1] in [1, 2]
        for o in range(1, 30):
            if known:
                row[f"Q15S{s}_{o}"] = 1 if random.random() < 0.07 else 0
            else:
                row[f"Q15S{s}_{o}"] = 0
    # Q15 FA
    for s in range(1, 10):
        if row.get(f"Q15S{s}_28", 0) == 1:
            row[f"Q15S{s}_28FA"] = random.choice(generic_terms)
        else:
            row[f"Q15S{s}_28FA"] = ""

    # --- Q16S1-Q16S10 (SA, 1-3: JAC features awareness) ---
    q16 = []
    for s in range(10):
        val = random.choices([1, 2, 3], weights=[0.25, 0.25, 0.50])[0]
        q16.append(val)
        row[f"Q16S{s+1}"] = val

    # --- Q17 (MA, 31 flags - work values) ---
    for o in range(1, 32):
        row[f"Q17_{o}"] = 1 if random.random() < 0.15 else 0

    # --- BD columns ---
    # BD1: 割付別1 (1=一般有職者, 2=エグゼクティブ部長以上&年収1500万+, 3=キャリア20代×600万+)
    if sq4 <= 2 and sq3 >= 16:  # 部長以上 & 1500万+
        bd1 = 2
    elif age < 30 and sq3 >= 5:  # 20代 & 600万+
        bd1 = 3
    else:
        bd1 = 1
    row["BD1"] = bd1

    # BD2: 割付別2 (1=一般, 2-10=region×income)
    if sq3 < 5:
        bd2 = 1
    else:
        if region == "kanto":
            if sq3 <= 7:
                bd2 = 2
            elif sq3 <= 9:
                bd2 = 3
            else:
                bd2 = 4
        elif region == "kansai":
            if sq3 <= 7:
                bd2 = 5
            elif sq3 <= 9:
                bd2 = 6
            else:
                bd2 = 7
        else:
            if sq3 <= 7:
                bd2 = 8
            elif sq3 <= 9:
                bd2 = 9
            else:
                bd2 = 10
    row["BD2"] = bd2

    # BD3: ハイクラスエリア別 (1=関東600+, 2=関西600+, 3=東海/その他600+)
    if sq3 >= 5:
        if region == "kanto":
            bd3 = 1
        elif region == "kansai":
            bd3 = 2
        else:
            bd3 = 3
    else:
        bd3 = random.choice([1, 2, 3])
    row["BD3"] = bd3

    # BD4: ハイクラス800万～エリア別
    if sq3 >= 7:
        if region == "kanto":
            bd4 = 1
        elif region == "kansai":
            bd4 = 2
        else:
            bd4 = 3
    else:
        bd4 = random.choice([1, 2, 3])
    row["BD4"] = bd4

    # BD5: MA, 3 flags (年収600+, 800+, 1000+)
    row["BD5_1"] = 1 if sq3 >= 5 else 0
    row["BD5_2"] = 1 if sq3 >= 7 else 0
    row["BD5_3"] = 1 if sq3 >= 9 else 0

    # BD6: 全国年収600万+×性年代別① (6 cats)
    if sq3 >= 5:
        if sex == 1:
            if age <= 39:
                bd6 = 1
            elif age <= 54:
                bd6 = 2
            else:
                bd6 = 3
        else:
            if age <= 39:
                bd6 = 4
            elif age <= 54:
                bd6 = 5
            else:
                bd6 = 6
    else:
        bd6 = random.randint(1, 6)
    row["BD6"] = bd6

    # BD7: 全国年収800万+×性年代別①
    if sq3 >= 7:
        if sex == 1:
            if age <= 39:
                bd7 = 1
            elif age <= 54:
                bd7 = 2
            else:
                bd7 = 3
        else:
            if age <= 39:
                bd7 = 4
            elif age <= 54:
                bd7 = 5
            else:
                bd7 = 6
    else:
        bd7 = random.randint(1, 6)
    row["BD7"] = bd7

    # BD8: 全国年収600万+×性年代別② (8 cats, 10-year bands)
    if sq3 >= 5:
        if sex == 1:
            if age <= 34:
                bd8 = 1
            elif age <= 44:
                bd8 = 2
            elif age <= 54:
                bd8 = 3
            else:
                bd8 = 4
        else:
            if age <= 34:
                bd8 = 5
            elif age <= 44:
                bd8 = 6
            elif age <= 54:
                bd8 = 7
            else:
                bd8 = 8
    else:
        bd8 = random.randint(1, 8)
    row["BD8"] = bd8

    # BD9: same as BD8 but for 800万+
    if sq3 >= 7:
        row["BD9"] = bd8  # same sex/age grouping
    else:
        row["BD9"] = random.randint(1, 8)

    # BD10: 全国年収600万+×転職意向
    sq5 = row["SQ5"]
    if sq3 >= 5:
        if sq5 <= 6:
            bd10 = sq5
        else:
            bd10 = 6  # collapse 6&7 to 6
    else:
        bd10 = random.randint(1, 6)
    row["BD10"] = bd10

    # BD11: same for 800万+
    if sq3 >= 7:
        row["BD11"] = bd10
    else:
        row["BD11"] = random.randint(1, 6)

    # BD12: 全国年収800万+×職種 (17 cats, map SQ2 to groups)
    sq2 = row["SQ2"]
    if sq3 >= 7 and sq2 <= 17:
        row["BD12"] = sq2
    else:
        row["BD12"] = random.randint(1, 17)

    # BD13: MA, 17 flags (800万+, usage intent top2 for each service)
    for s in range(1, 18):
        if sq3 >= 7 and row[f"Q8S{s}"] <= 2:
            row[f"BD13_{s}"] = 1
        else:
            row[f"BD13_{s}"] = 0

    # BD14: エグゼクティブ合計 (1 if executive)
    row["BD14"] = 1 if sq4 <= 1 else 0

    # --- AGEID_10 (decade grouping: 1=20代, 2=30代, 3=40代, 4=50代, 5=60代) ---
    decade = (age - 20) // 10 + 1
    row["AGEID_10"] = max(1, min(5, decade))

    # --- SEXAGE (1-6) ---
    if sex == 1:
        if age <= 39:
            sa = 1
        elif age <= 54:
            sa = 2
        else:
            sa = 3
    else:
        if age <= 39:
            sa = 4
        elif age <= 54:
            sa = 5
        else:
            sa = 6
    row["SEXAGE"] = sa

    # --- NCELL (1-15) ---
    if sq3 < 5:
        ncell = 1
    elif sq4 <= 1:  # 役員=エグゼクティブ
        ncell = 14
    elif age < 30 and sq3 >= 5:  # キャリア20代
        ncell = 15
    else:
        # region × income bracket
        if region == "kanto":
            if sq3 <= 7:
                ncell = 2
            elif sq3 <= 9:
                ncell = 3
            elif sq3 <= 15:
                ncell = 4
            else:
                ncell = 5
        elif region == "kansai":
            if sq3 <= 7:
                ncell = 6
            elif sq3 <= 9:
                ncell = 7
            elif sq3 <= 15:
                ncell = 8
            else:
                ncell = 9
        else:
            if sq3 <= 7:
                ncell = 10
            elif sq3 <= 9:
                ncell = 11
            elif sq3 <= 15:
                ncell = 12
            else:
                ncell = 13
    row["NCELL"] = ncell

    # NCELL2 (1-4)
    if ncell == 1:
        ncell2 = 1
    elif ncell == 14:
        ncell2 = 3
    elif ncell == 15:
        ncell2 = 4
    else:
        ncell2 = 2
    row["NCELL2"] = ncell2

    # --- NQ5 (derived: NQ5_s = 1 if Q5Ss in [1,2]) ---
    for s in range(1, 18):
        row[f"NQ5_{s}"] = 1 if row[f"Q5S{s}"] in [1, 2] else 0

    # --- NQ12 (derived: NQ12_s = 1 if Q12Ss in [1,2]) ---
    for s in range(1, 10):
        row[f"NQ12_{s}"] = 1 if row[f"Q12S{s}"] in [1, 2] else 0

    # --- NQ16 (derived: NQ16_s = 1 if Q16Ss in [1,2]) ---
    for s in range(1, 11):
        row[f"NQ16_{s}"] = 1 if row[f"Q16S{s}"] in [1, 2] else 0

    # --- Flag_1, Flag_2 ---
    row["Flag_1"] = 1  # 全体ベース (everyone)
    row["Flag_2"] = 1 if row["SQ5"] <= 5 else 0  # 転職意向者ベース

    # --- WB (weight-back, mean~1.0, range 0.3-3.0) ---
    wb = float(np.clip(np.random.lognormal(0, 0.35), 0.3, 3.0))
    row["WB"] = round(wb, 4)

    rows.append(row)

# ---------------------------------------------------------------------------
# Build DataFrame in correct column order (1695 columns)
# ---------------------------------------------------------------------------
columns = []

# 1: SAMPLEID
columns.append("SAMPLEID")
# 2: ANSWERDATE
columns.append("ANSWERDATE")
# 3: SEX
columns.append("SEX")
# 4: AGE
columns.append("AGE")
# 5: AGEID
columns.append("AGEID")
# 6: MARRIED
columns.append("MARRIED")
# 7: CHILD
columns.append("CHILD")
# 8: CELL
columns.append("CELL")
# 9: CELLNAME
columns.append("CELLNAME")
# 10: SQ1
columns.append("SQ1")
# 11: SQ2
columns.append("SQ2")
# 12: SQ3
columns.append("SQ3")
# 13: SQ4
columns.append("SQ4")
# 14: SQ4_8FA
columns.append("SQ4_8FA")
# 15: SQ5
columns.append("SQ5")
# 16-20: Q1S1FA-Q1S5FA
for s in range(1, 6):
    columns.append(f"Q1S{s}FA")
# 21-25: Q2S1FA-Q2S5FA
for s in range(1, 6):
    columns.append(f"Q2S{s}FA")
# 26-55: Q3_1 through Q3_30
for j in range(1, 31):
    columns.append(f"Q3_{j}")
# 56: Q3_29FA
columns.append("Q3_29FA")
# 57-86: Q4_1 through Q4_30
for j in range(1, 31):
    columns.append(f"Q4_{j}")
# 87: Q4_29FA
columns.append("Q4_29FA")
# 88-104: Q5S1-Q5S17
for s in range(1, 18):
    columns.append(f"Q5S{s}")
# 105-580: Q6S1_1 through Q6S17_28
for s in range(1, 18):
    for c in range(1, 29):
        columns.append(f"Q6S{s}_{c}")
# 581-597: Q6S1_27FA through Q6S17_27FA
for s in range(1, 18):
    columns.append(f"Q6S{s}_27FA")
# 598-614: Q7S1-Q7S17
for s in range(1, 18):
    columns.append(f"Q7S{s}")
# 615-631: Q8S1-Q8S17
for s in range(1, 18):
    columns.append(f"Q8S{s}")
# 632-1141: Q9S1_1 through Q9S17_30
for s in range(1, 18):
    for o in range(1, 31):
        columns.append(f"Q9S{s}_{o}")
# 1142-1158: Q9S1_29FA through Q9S17_29FA
for s in range(1, 18):
    columns.append(f"Q9S{s}_29FA")
# 1159-1188: Q10S1_1 through Q10S1_30
for j in range(1, 31):
    columns.append(f"Q10S1_{j}")
# 1189-1218: Q10S2_1 through Q10S2_30
for j in range(1, 31):
    columns.append(f"Q10S2_{j}")
# 1219: Q10S1_29FA
columns.append("Q10S1_29FA")
# 1220: Q10S2_29FA
columns.append("Q10S2_29FA")
# 1221-1250: Q11S1_1 through Q11S1_30
for j in range(1, 31):
    columns.append(f"Q11S1_{j}")
# 1251-1280: Q11S2_1 through Q11S2_30
for j in range(1, 31):
    columns.append(f"Q11S2_{j}")
# 1281: Q11S1_29FA
columns.append("Q11S1_29FA")
# 1282: Q11S2_29FA
columns.append("Q11S2_29FA")
# 1283-1291: Q12S1-Q12S9
for s in range(1, 10):
    columns.append(f"Q12S{s}")
# 1292-1300: Q13S1-Q13S9
for s in range(1, 10):
    columns.append(f"Q13S{s}")
# 1301-1309: Q14S1-Q14S9
for s in range(1, 10):
    columns.append(f"Q14S{s}")
# 1310-1570: Q15S1_1 through Q15S9_29
for s in range(1, 10):
    for o in range(1, 30):
        columns.append(f"Q15S{s}_{o}")
# 1571-1579: Q15S1_28FA through Q15S9_28FA
for s in range(1, 10):
    columns.append(f"Q15S{s}_28FA")
# 1580-1589: Q16S1-Q16S10
for s in range(1, 11):
    columns.append(f"Q16S{s}")
# 1590-1620: Q17_1 through Q17_31
for o in range(1, 32):
    columns.append(f"Q17_{o}")
# 1621: BD1
columns.append("BD1")
# 1622: BD2
columns.append("BD2")
# 1623: BD3
columns.append("BD3")
# 1624: BD4
columns.append("BD4")
# 1625-1627: BD5_1 through BD5_3
for j in range(1, 4):
    columns.append(f"BD5_{j}")
# 1628: BD6
columns.append("BD6")
# 1629: BD7
columns.append("BD7")
# 1630: BD8
columns.append("BD8")
# 1631: BD9
columns.append("BD9")
# 1632: BD10
columns.append("BD10")
# 1633: BD11
columns.append("BD11")
# 1634: BD12
columns.append("BD12")
# 1635-1651: BD13_1 through BD13_17
for s in range(1, 18):
    columns.append(f"BD13_{s}")
# 1652: BD14
columns.append("BD14")
# 1653: AGEID_10
columns.append("AGEID_10")
# 1654: SEXAGE
columns.append("SEXAGE")
# 1655: NCELL
columns.append("NCELL")
# 1656: NCELL2
columns.append("NCELL2")
# 1657-1673: NQ5_1 through NQ5_17
for s in range(1, 18):
    columns.append(f"NQ5_{s}")
# 1674-1682: NQ12_1 through NQ12_9
for s in range(1, 10):
    columns.append(f"NQ12_{s}")
# 1683-1692: NQ16_1 through NQ16_10
for s in range(1, 11):
    columns.append(f"NQ16_{s}")
# 1693-1694: Flag_1, Flag_2
columns.append("Flag_1")
columns.append("Flag_2")
# 1695: WB
columns.append("WB")

print(f"Expected columns: 1695, Actual column list: {len(columns)}")

df = pd.DataFrame(rows)

# Ensure all columns exist (fill missing with empty string)
for col in columns:
    if col not in df.columns:
        df[col] = ""

df = df[columns]

print(f"DataFrame shape: {df.shape[0]} rows x {df.shape[1]} columns")

# Save to Excel
output_path = r"c:\Users\cy131\Downloads\正規化\dummy_survey_1000.xlsx"
df.to_excel(output_path, index=False, engine="openpyxl")
print(f"Saved to: {output_path}")
