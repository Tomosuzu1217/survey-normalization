// Node.js normalization test
// Usage: node test_norm.js
const fs = require('fs');

function norm(s) {
    return String(s).trim().normalize('NFKC').replace(/[\s\u3000]+/g, '').toLowerCase();
}

const SERVICE_DICT = [
    {
        name: 'ビズリーチ', variants: [
            'ビズリーチ', 'ビザリーチ', 'ビスリーチ', 'ビズリーーチ', 'ピザリーチ', 'バスリーチ',
            'びずりーち', 'びすりーち', 'バズリーチ', 'ビズリート', 'ビズリサーチ', 'ビズビーチ', 'ビズーリーチ',
            'ビズリチ', 'ビィズリーチ', 'ビバリーチ', 'ヒズリーチ', 'リズビーチ', 'リブリーチ', 'ビズリ-チ',
            'bizreach', 'bizreech', 'bizrearch', 'bzreach', 'bizpeach', 'bizrrach', 'biz reach', 'biz-reach',
            'bizuri-chi', 'bizurichi', 'ビズリーチビズリーチ', 'ビズ', 'biz',
            'ビズリーチ（bizreach）', 'ビズリーチ（bizreach）エグゼクティブ',
            'Bizリーチ', 'bizsearch', 'bizreach（ビズリーチ）',
            'ビズりーち', 'びずリーチ', 'びずりーci', 'ビズビーach',
        ], fuzzy: [
            /b[a-z]*[- ]?r[eai][a-z]*ch/i,
            /ビズ.{0,4}[リり].{0,3}[チチ]/,
            /[ビび][スズ].{0,4}[リり].{0,3}[チチ]/,
            /biz[a-z]*reach/i,
        ]
    },
    {
        name: 'doda X', variants: [
            'dodax', 'dudax', 'doda x', 'doda.x', 'doda-x', 'doda ex', 'dodaex',
            'デューダx', 'デューダex', 'デューだx', 'デューだex', 'ヂューダx', 'ヂューダex',
            'デューダエックス', 'doda xls', 'doda_x',
        ], fuzzy: [
            /doda[\s.\-_]?x$/i,
            /doda[\s.\-_]?ex/i,
            /デ[ュゅ][ーウ]ダ[\s.]?[xｘex]/,
            /ヂ[ュゅ][ーウ]ダ[\s.]?[xｘ]/,
        ]
    },
    {
        name: 'doda', variants: [
            'doda', 'duda', 'dida', 'dod', 'doだ',
            'ドゥーダ', 'デューダ', 'ティーダ', 'ドユーダ', 'デュダ', 'ヂューダ', 'デューだ',
            'どだ', 'ｄつーだ', 'デュウダー', 'どゅーだ', 'でゅーだ', 'でゆーだ', 'でゆーだー',
            'どゆわーだ', 'ドューダ', 'デユーダ', 'でゅーだー', 'ドゥダ', 'でゅ-だ',
            'ドゥーだ', 'どぅーだ', 'どぅださ', 'doda c', 'どった',
        ], fuzzy: [
            /^d[ouaã]?d[ouaã]?[a-z]?$/i,
            /^デ[ュゅ][ーウ]ダ$/,
            /^ド[ゥぅ][ーウ]?ダ$/,
        ]
    },
    {
        name: 'JAC Recruitment', variants: [
            'jac', 'jac recruitment', 'jac recruiting', 'jacrecruitment', 'jacrecruiting',
            'jac recruit', 'jac リクルートメント', 'jcリクルートメント', 'jcリクルート',
            'jrcリクルートメント', 'jrc', 'jacr', 'jax', 'joc', 'jra', 'jrac',
            'j o c', 'jo c', 'j&a', 'じなっく', 'jac executive',
            'jacリクルートメント', 'jacリクルート', 'jacリサーチ',
            'jacリクルートめんと', 'jacリクルートメンと',
            'jrクルートメント', 'jac リクルート', 'ｊo c',
        ], fuzzy: [/^j[aoa][ckrg][\s.]?(r[e]?c[r]?)?/i]
    },
    {
        name: 'リクルートダイレクトスカウト', variants: [
            'ダイレクトスカウト', 'リクナビダイレクト',
            'リクルートダイレクトスカウト', 'リクルートダイレクトキャッチ',
            'リクルートダイレクトサービス', 'リクルートダイレクトスカウティング',
            'リクルートダイレクトスタッフィング', 'リクルートダイレクト',
            'リクルートダイレ、クティブ、スカウト', 'リクルート ダイレクト スカウト',
        ], fuzzy: [/ダイレクト.{0,4}スカウト/, /recruit.*direct/i]
    },
    {
        name: 'リクルートエグゼクティブエージェント', variants: [
            'リクルートエグゼクティブエージェント', 'リクルートエグゼクティブ', 'recruit executive',
        ], fuzzy: [/リクルートエグゼ/]
    },
    {
        name: 'リクルートエージェント', variants: [
            'リクルートエージェント', 'リクルートエージェンシー', 'リクルートキャリア',
            'リクルートエイジェント', 'リクルートaじぇんんと', 'リクルートスカウト',
            'リクルートスタッフィング', 'リクルート エージェント',
            'recruiteragent', 'recruit agent', 'リクルートエージェント?',
            'リクルートaじぇんんと', 'リクルートaじぇんんと',
        ], fuzzy: [/リクルート.{0,4}エージェント/, /recruit.{0,6}agent/i]
    },
    {
        name: 'リクルート', variants: [
            'リクルート', 'リクラート', 'りくるーと', 'リクールト', 'リスクル', 'リスクる',
            'リクルート転職', 'リクルートサービス', 'リクルート 転職', 'recruit',
        ], fuzzy: [/^リクルート$/, /^recruit$/i]
    },
    {
        name: 'リクナビNEXT', variants: [
            'リクナビnext', 'リクナビネクスト', 'リクナビ転職', 'リクナビ 転職',
            'rikunabi', 'リクナビエージェント', 'リクナビエージ泡',
            'リクナビエージェントダイレクトスカウト', 'リクナビダイレクト', 'リクナビ',
        ], fuzzy: [/リクナビ/, /rikunabi/i]
    },
    {
        name: 'マイナビ', variants: [
            'マイナビ', 'マイマビ', 'まいなひ', 'まいなび', 'マリナビ', 'マイナビ転職',
            'マイナビエージェント', 'マイナビネクスト', 'まいなびあじぇんと', 'まいなびてんしょく',
        ], fuzzy: [/マイ.{0,2}ナビ/, /my\s?navi/i]
    },
    {
        name: 'エン転職', variants: [
            'エン転職', 'en転職', 'エン', 'エンジャパン', 'エン職', 'えんてんしょく', 'エンてんしよく',
            'エンシニア', 'エンゲージ', 'エンゲージメント', 'エンミドルの転職', 'enジャパン',
            'enミドルの転職', 'enてんしょく', 'えんてんしょく', 'エンていしょく', 'en職',
            'enjapan', 'enjp', 'えんてんしよく', 'エンミドル', 'en', 'えんてんしよく',
        ], fuzzy: [/^エン(転職|ジャパン|ミドル|ゲージ)?$/, /^en(japan|転職|ミドル)?$/i]
    },
    {
        name: 'LinkedIn', variants: [
            'linkedin', 'linked in', 'linkdin', 'リンクドイン', 'linkdn', 'linkedln', 'link in',
        ], fuzzy: [/link[e]?d?\s*i?n/i]
    },
    {
        name: 'Indeed', variants: [
            'indeed', 'インディード', 'インリード', 'インニード', 'インディど', 'インでーど', 'inndeed',
            'いんでぃーお', 'インディーど', 'インディーズ', 'indeedプラス', 'indeed+', 'indeedハイクラス',
            'indeedplus', 'インでーどプラス', 'インじど', 'いんでーど', 'インでーど', 'インディード+',
            'いんでぃーど', 'インででーど', 'インディーど',
        ], fuzzy: [/in+d[e]?e?d/i, /インデ[ィイ][ー]?[どドd]/]
    },
    {
        name: 'ロバート・ウォルターズ', variants: [
            'ロバートウォルターズ', 'ロバートウォーターズ', 'robertwalters', 'robert walters',
            'ロンザン', 'ロバートウォーターズ',
        ], fuzzy: [/robert\s*walters?/i, /ロバート/]
    },
    { name: 'コーン・フェリー', variants: ['コーンフェリー', 'コーン・フェリー', 'korn ferry', 'kornferry'], fuzzy: [/korn.?ferry/i] },
    { name: 'エゴンゼンダー', variants: ['エゴンゼンダー', 'egon zehnder', 'egonzehnder'], fuzzy: [/egon.?zehnder/i] },
    { name: 'スペンサースチュアート', variants: ['スペンサースチュアート', 'spencer stuart', 'spencerstuart'], fuzzy: [/spencer.?stuart/i] },
    { name: 'ランスタッド', variants: ['ランスタッド', 'ランドスタッド', 'randstad'], fuzzy: [/randstad/i, /ラン.?スタッド/] },
    { name: 'クライス＆カンパニー', variants: ['クライスアンドカンパニー', 'クライス＆カンパニー', 'クライス&カンパニー', 'クライス'], fuzzy: [/クライス/] },
    { name: 'パソナ', variants: ['パソナ', 'パソナキャリア', 'パソナエグゼクティブ', 'パソナ エグゼクティブサービス'], fuzzy: [/パソナ/] },
    { name: 'レバテック', variants: ['レバテック', 'レバテックキャリア', 'レバウェル', 'レバ鉄'], fuzzy: [/レバテック/] },
    { name: 'Hays', variants: ['hays', 'ヘイズ', 'hays recruitment'], fuzzy: [/^hays$/i] },
    { name: 'ミドルの転職', variants: ['ミドルの転職', 'ミドル転職', 'enミドルの転職'], fuzzy: [/ミドル.?転職/] },
    { name: 'ハローワーク', variants: ['ハローワーク', 'ハロワ'], fuzzy: [/ハロ.?ワ/] },
    { name: 'コーンフェリー', variants: ['コーンフェリー'], fuzzy: [] },
    { name: 'AMBI', variants: ['ambi'], fuzzy: [/^ambi$/i] },
    { name: 'キャリコネ', variants: ['キャリコネ'], fuzzy: [] },
    { name: 'ギークリー', variants: ['ギークリー', 'ギークリ'], fuzzy: [/ギークリ/] },
    { name: 'Findy', variants: ['findy'], fuzzy: [/^findy$/i] },
    { name: 'ムービン', variants: ['ムービン', 'ムーヴィン'], fuzzy: [/ムービン/] },
    { name: 'コトラ', variants: ['コトラ'], fuzzy: [] },
    { name: 'CxOサーチ', variants: ['cxoサーチ', 'cxo'], fuzzy: [/cxo/i] },
    { name: 'パーソル', variants: ['パーソル', 'パーソルキャリア'], fuzzy: [/パーソル/] },
    { name: 'レイノス', variants: ['レイノス'], fuzzy: [] },
    { name: '縄文アソシエイツ', variants: ['縄文アソシエイツ'], fuzzy: [] },
    { name: 'Professional Bank', variants: ['professional bank', 'professionalbank'], fuzzy: [/professional\s*bank/i] },
    { name: 'コンコード', variants: ['コンコード'], fuzzy: [] },
    { name: 'インスパイア', variants: ['インスパイア'], fuzzy: [] },
    { name: 're就活', variants: ['re就活'], fuzzy: [/re就活/i] },
    { name: 'AXISコンサルティング', variants: ['axisエージェント', 'axis'], fuzzy: [/axis.{0,5}(エージェント|agent)/i] },
];

const GENERIC_TERMS_RE = /^(ヘッドハンティング|ヘッドハンター|ヘッドハント|ベッドハンティング|ヘットハンティング|ヘッドハンター|転職エージェント|転職支援|転職ナビ|転職サイト|スカウト|スカウトサービス|スカウト会社|求人オファー|マッチング|マッチングサービス|エージェント|外資系|高額案件|高収入|高給料|年収|管理職|部長|社長|取締役|ハイクラス(転職|の転職|向け転職)?|エグゼクティブ(転職|案件|案内)?|ハイマネジメント|非公開求人|個人対応|個別対応|シニア対応|CxOクラス|リテイナーサーチ|サーチファーム|ハイプロ|ダイレクトリクルーティング|ヘッドハンター|支援|転職|エージェント|スカウト|ハイ転職|高額|高卒|昇給|厳選|資料|ハイクラス|クラス|即戦力)$/i;

const INVALID_RE = /^(なし|とくに|特に|ない|無い|無し|なきか|なき|なさ|わから|分から|解ら|判ら|わかな|思い(出せ|浮かば|つか|付か)|知(ら|りません)|しらな|ありません|ありがとう|よろしく|不明|ふめい|none|ok|nan|使いやす|ナッシング|興味ない|何も知らな|ハードルが高|検討したい|多々ある|全部|プラチナ|高い$|高額$|即戦力$|ハイクラス$|です$|ます$|いたします|覚えてな|浮かばな|です。|ます。|ないです|ないです。|ない。|しらない|しらなし|興味な|とくにな$|よく知らな|いろいろ|リクエスト|時なし|転機|不動産|東レ|楽天|Amazon|Google|LINE|au|ソニー|サントリー|旭化成|ベンツ|サイバーエージェント|タウンワーク|バイトル|日清食品|じゃらん|はたらいく|日経キャリア|日経)$/i;

const LOOKUP = new Map();
for (const rule of SERVICE_DICT) {
    for (const v of rule.variants) {
        LOOKUP.set(norm(v), rule.name);
    }
}

const CAT_OTHER = 'その他・総称';

function normalizeText(raw) {
    if (!raw) return null;
    const s = String(raw).trim();
    if (!s) return null;
    const sc = s.replace(/[\s\u3000]/g, '');
    if (INVALID_RE.test(sc) || INVALID_RE.test(s)) return null;
    if (/(.)\1{4,}/.test(sc)) return null;
    if (/^[\u3041-\u3093]{1,3}$/.test(sc) && !/^(えん|えんにし)$/.test(sc)) return null;
    if (/^[a-z0-9]{1,3}$/i.test(sc)) return null;
    if (/^[\u3041-\u3093\u30a1-\u30f3\u4e00-\u9faf]{1}$/.test(sc)) return null;
    if (/^(.{1,5})\1{3,}$/.test(sc)) return null;
    const key = norm(s);
    if (LOOKUP.has(key)) return LOOKUP.get(key);
    for (const rule of SERVICE_DICT) {
        for (const re of rule.fuzzy) {
            if (re.test(s) || re.test(key)) return rule.name;
        }
    }
    if (GENERIC_TERMS_RE.test(sc) || GENERIC_TERMS_RE.test(s)) return CAT_OTHER;
    if (sc.length < 2) return null;
    if (/^[!-\/:-@[-`{-~]+$/.test(sc)) return null;
    if (/^[a-z]{3,}$/.test(key) && !/(recruit|doda|jac|biz|link|indeed|hays|ambi|findy)/i.test(key)) {
        if (sc.length <= 5) return null;
    }
    return s;
}

const lines = fs.readFileSync('揺れ.txt', 'utf8').split(/\r?\n/).map(l => l.trim()).filter(l => l.length > 0);
const results = { normalized: {}, unknown: [], dropped: [] };

for (const line of lines) {
    const result = normalizeText(line);
    if (result === null) {
        results.dropped.push(line);
    } else {
        if (!results.normalized[result]) results.normalized[result] = [];
        results.normalized[result].push(line);
    }
}

console.log('\n========== 正規化結果 ==========\n');
const sortedServices = Object.keys(results.normalized).sort((a, b) => results.normalized[b].length - results.normalized[a].length);
for (const svc of sortedServices) {
    const variants = results.normalized[svc];
    const unique = [...new Set(variants)];
    console.log(`[${svc}] (${variants.length}件, ${unique.length}種類の表記)`);
    if (unique.length > 1) {
        unique.forEach(v => v !== svc && console.log(`  <- ${v}`));
    }
}

console.log('\n========== 除外（無効）==========');
console.log(`計 ${results.dropped.length} 件（なし/わからない等）`);
results.dropped.slice(0, 10).forEach(v => console.log(`  ${v}`));
if (results.dropped.length > 10) console.log(`  ... 他 ${results.dropped.length - 10} 件`);

console.log('\n========== 未登録（そのまま残るもの）==========');
const unknowns = sortedServices.filter(s => !SERVICE_DICT.some(r => r.name === s) && s !== CAT_OTHER);
unknowns.forEach(u => console.log(`  "${u}"`));
