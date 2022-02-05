import sys
import struct
import datetime

args = sys.argv
if args[1] == '':
    print('Usage:  python ct2.py your_file.lg8')

block_offset = 0

#ctestwin tables
table_Mode = {
"0": "CW",
"1": "RTTY",
"2": "SSB",
"3": "FM",
"4": "AM",
"5": "ATV",
"6": "SSTV",
"7": "PSK",
"8": "GMSK",
"9": "MFSK",
"10": "QPSK",
"11": "FSK",
"12": "D-STAR",
"13": "C4FM",
"14": "JT65",
"15": "JT9",
"16": "ISCAT",
"17": "FT8",
"18": "JT4",
"19": "QRA64",
"20": "MSK144",
"21": "WSPR",
"22": "JTMS",
"23": "FT4",
"24": "FST4",
}

table_Freq = {
"0": "1.9M",
"1": "3.5M",
"2": "7M",
"3": "10M",
"4": "14M",
"5": "18M",
"6": "21M",
"7": "24M",
"8": "28M",
"9": "50M",
"10": "144M",
"11": "430M",
"12": "1200M",
"13": "2400M",
"14": "5600M",
"15": "10G",
"16": "24G",
"17": "47G",
"18": "75G",
"19": "77G",
"20": "135G",
"21": "248G",
"22": "136K",
}

table_Contest = {
"0": "マルチチェック無し",
"1": "All JAコンテスト",
"2": "6m and downコンテスト",
"3": "XPO 他 (RST+県ﾅﾝﾊﾞｰ)",
"4": "全市全郡",
"5": "関東UHF他(RST+市郡ﾅﾝﾊﾞｰ)",
"6": "All JA8",
"7": "CQ WW DX (RST+Zone)",
"8": "All Asian DX (DXCC country)",
"9": "ARRL (RST+State/Province)",
"10": "WPX (Prefix)",
"11": "6m and down / Field Day (旧ﾙｰﾙ)",
"12": "ﾛｰｶﾙｺﾝﾃｽﾄ(RST+市郡or県ﾅﾝﾊﾞｰ)",
"13": "東京UHFコンテスト",
"14": "ﾕｰｻﾞ定義ﾏﾙﾁのｺﾝﾃｽﾄ",
"15": "JA0 VHFｺﾝﾃｽﾄ（2005年以前の旧ルール）",
"16": "ﾕｰｻﾞ定義ﾏﾙﾁのｺﾝﾃｽﾄ(点数付)",
"17": "JIDX",
"18": "ARRL 10m",
"19": "Marconi Memorial contest（2013年以前の旧ルール）",
"20": "広島WAS",
"21": "関西 VHF(旧ルール)",
"22": "オール大阪",
"23": "オール三重(2010年以前の旧ルール)",
"24": "奈良VUHF",
"25": "KCWA CW",
"26": "ALL JA0 3.5,7,21/28MHz(管外局)",
"27": "ALL JA0 3.5,7,21/28MHz(管内局)",
"28": "京都ｺﾝﾃｽﾄ(府外局)",
"29": "京都ｺﾝﾃｽﾄ(府内局)",
"30": "ALL JA8 (2003年特別ﾙｰﾙ)",
"31": "静岡コンテスト",
"32": "オール千葉（旧ルール）",
"33": "オール神奈川コンテスト(県内局)",
"34": "鹿児島コンテスト（2010年以前の旧ルール）",
"35": "新潟2400ｺﾝﾃｽﾄ",
"36": "Oceania DX",
"37": "IARU HF world championship",
"38": "RSGB IOTA（2011年以前の旧ルール）",
"39": "SEANETコンテスト (2013年以前の旧ルール)",
"40": "RAC Canada Day/Winter",
"41": "関西VHF",
"42": "高校コンテスト",
"43": "Russian DX",
"44": "South America(旧ルール)",
"45": "ｴｽｶﾙｺﾞ 6m CW",
"46": "ﾃﾚｺﾑQSOﾊﾟｰﾃｨ",
"47": "Hungarian DXコンテスト (2019年以前の旧ルール)",
"48": "SP DXコンテスト",
"49": "Helvetiaコンテスト (2018年以前の旧ルール)",
"50": "ギガヘルツコンテスト",
"51": "ALL滋賀コンテスト(県外局)(2012年以前の旧ルール)",
"52": "ALL滋賀コンテスト(県内局)(2010年以前の旧ルール)",
"53": "Venezuelan Independence Day Contest",
"54": "The King of Spain Contest（2004年以前の旧ルール）",
"55": "ARI International DXコンテスト",
"56": "YO DXコンテスト",
"57": "KCJコンテスト (2020年以前の旧ルール)",
"58": "Scandinavian Activityコンテスト",
"59": "大分ｺﾝﾃｽﾄ（2010年以前の旧ルール）",
"60": "JA9ｺﾝﾃｽﾄ VU (2013年以前の旧ルール)",
"61": "JLRSﾊﾟｰﾃｨｺﾝﾃｽﾄ(OM局)",
"62": "JLRSﾊﾟｰﾃｨｺﾝﾃｽﾄ(YL局)",
"63": "TOEC World Wide Gridコンテスト",
"64": "Field Dayコンテスト",
"65": "REFコンテスト",
"66": "Portugal Day DXコンテスト（2011年以前の旧ルール）",
"67": "RSGB 21/28MHzコンテスト（2015年以前の旧ルール）",
"68": "Asia-Pacific sprintコンテスト/DMC RTTYコンテスト(2016年以降の新ルール)",
"69": "Worked All Germanyコンテスト",
"70": "東海マラソンコンテスト",
"71": "OK-OM DX CWコンテスト",
"72": "LZ DXコンテスト",
"73": "YU DXコンテスト（2005年以前の旧ルール）",
"74": "Croatian CWコンテスト",
"75": "Ukrainian DXコンテスト",
"76": "石狩後志コンテスト(管外局)（2005年以前の旧ルール）",
"77": "石狩後志コンテスト(管内局)（2005年以前の旧ルール）",
"78": "North American QSO Party",
"79": "Holyland DXコンテスト",
"80": "UBA DXコンテスト",
"81": "Dutach PACCコンテスト (2015年以前の旧ルール)",
"82": "オール山口コンテスト(個人局)2005年ﾙｰﾙ",
"83": "オール山口コンテスト(クラブ局)2005年ﾙｰﾙ",
"84": "DXCOLOMBIA INTERNATIONALコンテスト",
"85": "EA RTTYコンテスト (2013年以前の旧ルール)",
"86": "WPX RTTYコンテスト",
"87": "Anatolian WW RTTYコンテスト",
"88": "Mexico International RTTYコンテスト",
"89": "BARTG HF RTTYコンテスト",
"90": "ハムランド サマーコンテスト(2005年ルール)",
"91": "South America",
"92": "The King of Spain(2005年～2012年ルール)",
"93": "TARA Grid Dip PSK-RTTYコンテスト",
"94": "オール千葉県外局（2005-07ルール）",
"95": "オール千葉県内局（2005-07ルール）",
"96": "CQ WW RTTY DX　コンテスト",
"97": "JARTS RTTY コンテスト",
"98": "OK DX RTTY コンテスト",
"99": "JA0 VHFコンテスト（2006～2012年の旧ルール）",
"100": "YUDXコンテスト（2006年以降の新ルール）",
"101": "山梨コンテスト (2015年以前の旧ルール)",
"102": "オール山口コンテスト(個人局)2006年～2010年のルール",
"103": "オール山口コンテスト(クラブ局)2006年～2010年のルール",
"104": "ハムランド サマーコンテスト2006年のルール",
"105": "胆振日高ＱＳＯコンテスト",
"106": "ハムランド サマーコンテスト2007年以降の新ルール",
"107": "A1クラブコンテスト 2009年以前の旧ルール",
"108": "愛・地球博記念コンテスト（2008年以前の旧ルール）",
"109": "オール千葉県外局（新ルール）",
"110": "オール千葉県内局（新ルール）",
"111": "電信電話記念日コンテスト",
"112": "オール横浜コンテスト(2008年の60周年記念ルール)",
"113": "オール横浜コンテスト(2015年以前の旧ルール)",
"114": "JLRS３・３雛コンテスト",
"115": "7MHz帯拡大記念QSOパーティー",
"116": "愛・地球博記念コンテスト(2009年以降の新ルール)",
"117": "全日本CW王座決定戦",
"118": "The Australian Shires コンテスト",
"119": "FCWA CW QSOパーティー",
"120": "東京CWコンテスト",
"121": "年末コンテスト",
"122": "QRP/QRPpコンテスト (2015年以前の旧ルール)",
"123": "CQ WW 160mコンテスト",
"124": "QRP Sprintコンテスト",
"125": "KANHAMコンテスト (2013年以前の旧ルール)",
"126": "BIRTHDAYコンテスト",
"127": "SARTG WW RTTYコンテスト",
"128": "A1クラブコンテスト 2010年以降の新ルール",
"129": "UNDXコンテスト",
"130": "宮崎コンテスト（県外局）",
"131": "宮崎コンテスト（県内局）",
"132": "TAC(TOP OF OPERATORS ACTIVITY CONTEST)",
"133": "ARRL RTTY ROUNDUP CONTEST",
"134": "オール山口コンテスト(個人局)2011年～2017年のルール",
"135": "オール山口コンテスト(クラブ局,OM局)2011年～2017年のルール",
"136": "オール三重",
"137": "福岡コンテスト",
"138": "大分コンテスト（2011年から2014年の旧ルール及び2017年のルール）",
"139": "ALL滋賀コンテスト県内局（2011年以降の新ルール）",
"140": "鹿児島コンテスト（2011年以降の新ルール）",
"141": "WAE (Worked All Europe DX Contest) CW, SSB",
"142": "Japan International (海外局)",
"143": "CQ-M International DX contest",
"144": "Portugal Day DXコンテスト(2012年以降の新ルール)",
"145": "RSGB IOTA（2012年以降の新ルール）",
"146": "Russian RADIO RTTY WW Contest",
"147": "UK DX RTTY Contest",
"148": "電通大コンテスト",
"149": "CW Openコンテスト (2012年以前の旧ルール)",
"150": "BARTG SPRINTコンテスト",
"151": "TRIATHLON DX Contest",
"152": "JA0 VHFコンテスト（2013年～2019年の旧ルール）",
"153": "All JA8コンテスト 2013年特別規約",
"154": "YU DXコンテスト (2013年～2018年のルール)",
"155": "WAPC DXコンテスト  (2018年以前の旧ルール)",
"156": "SP DX RTTYコンテスト  (2018年以前の旧ルール)",
"157": "羽曳野コンテスト",
"158": "DRCG Long Distance Contest",
"159": "ALL滋賀コンテスト県外局  (2013年以降の新ルール)",
"160": "DL-DX RTTYコンテスト",
"161": "The King of Spain(2013年以降の新ルール)",
"162": "CW Openコンテスト (2013年以降の新ルール)",
"163": "PMCコンテスト",
"164": "WAE (Worked All Europe DX Contest) RTTY",
"165": "STEW PERRY TOPBAND DISTANCE CHALLENGE",
"166": "OK-OM DX SSBコンテスト",
"167": "KANHAMコンテスト(2014～2018年のルール)",
"168": "VOLTA RTTYコンテスト",
"169": "EA RTTY コンテスト(2014年以降の新ルール)",
"170": "DRCG WW RTTYコンテスト",
"171": "Marconi Memorial contest (2014年～2017年のルール)",
"172": "SEANET コンテスト(2014年以降の新ルール)",
"173": "JA9ｺﾝﾃｽﾄ VU(2014年以降の新ルール)",
"174": "SCC RTTY CHAMPIONSHIP",
"175": "DMC RTTYコンテスト (2015年以降の旧ルール)",
"176": "Russian WW Digital Contest",
"177": "Polska WW BPSK63 Contest",
"178": "EPC Ukraine DX Contest",
"179": "UBA PSK63 Prefix Contest (2016年以前の旧ルール)",
"180": "EPC WW DX Contest",
"181": "Russian WW PSK Contest",
"182": "UKRAINIAN DX DIGI CONTEST",
"183": "European PSK DX Contest",
"184": "The Makrothen Contest",
"185": "TARA Skirmish Digital Prefix Contest",
"186": "オール神奈川コンテスト(県外局)",
"187": "DigiFest",
"188": "Hawaii QSO party",
"189": "UK/EI DX contest",
"190": "Dutach PACCコンテスト(2016年以降の新ルール)",
"191": "山梨コンテスト(2016年以降の新ルール)",
"192": "CQMM DX contest",
"193": "SA Sprint contest",
"194": "CQ World-Wide VHF Contest",
"195": "QRPコンテスト",
"196": "RSGB International DX Contest",
"197": "UBA PSK63 Prefix Contest(2017年以降の新ルール)",
"198": "JAGコンテスト（2020年以前の旧ルール）",
"199": "AEGEAN RTTYコンテスト",
"200": "YB DX Contest",
"201": "いわて雪まつりコンテスト",
"202": "オール山口コンテスト(2018年以降の新ルール)",
"203": "オール横浜コンテスト(2018年以降の新ルール)",
"204": "Marconi Memorial contest (2018年以降の新ルール)",
"205": "Jakarta RTTY contest",
"206": "YB DX RTTY Contest",
"207": "WAPC DXコンテスト (2019年の旧ルール)",
"208": "YU DX contest (2019年以降の新ルール)",
"209": "SPDX RTTY contest (2019年以降の新ルール)",
"210": "HELVETIA contest (2019年以降の新ルール)",
"211": "KANHAMコンテスト(2019年以降の新ルール)",
"212": "World Wide Digi DX Contest",
"213": "ARRL 160-Meter Contest",
"214": "Hungarian DXコンテスト(2020年以降の新ルール)",
"215": "WAPCコンテスト(2020年以降の新ルール)",
"216": "JA0 VHFコンテスト管内局(2020年以降の新ルール)",
"217": "JA0 VHFコンテスト管外局(2020年以降の新ルール)",
"218": "大分コンテスト(2020年以降の新ルール)",
"219": "Batavia FT8 Contest",
"220": "オール旭川コンテスト",
"221": "KCJコンテスト(2021年以降の新ルール)",
"222": "Open Ukraine RTTY Championship",
"223": "YOTA contest",
"224": "JAGコンテスト(2021年以降の新ルール)",
"225": "YBDXPI FT8 Contest"
}


# QSOブロック読み込むときに16 Byteのヘッダー分ずらす設定 
block_offset += 16
#QSOブロック一つの長さ
qso_block_size = 170

# Datatypes:
# ===================================================================================================
# Type    Definition                                          Directive for Python's String#unpack
# ---------------------------------------------------------------------------------------------------
# char[]  bytes                                               s
# long    UInt64LE                                            Q
# byte    UInt8                                               B
# short   UInt16LE                                            H
# int     UInt32LE                                            L
# float   FloatLE (32 bits IEEE 754 floating point number)    f
# ---------------------------------------------------------------------------------------------------

# 各項目のオフセットとデータ型を定義
header_def = {
    'totalQSO'      : {'offset':  0, 'type': '<H'}
  }
block_def = {
    'callsign'      : {'offset':  0, 'type': '<20s'},
    'my'            : {'offset': 20, 'type': '<30s'},
    'ur'            : {'offset': 50, 'type': '<30s'},
    'mode'          : {'offset': 80, 'type': '<H'},
    'freq'          : {'offset': 82, 'type': '<H'},
    #'padding'         : {'offset': 84, 'type': '<Q'}, #unknown
    'time'          : {'offset': 88, 'type': '<Q'},
    'op'            : {'offset': 96, 'type': '<20s'},
    'fDup'          : {'offset':116, 'type': '<H'},
    'Remarks'       : {'offset':118, 'type': '<50s'},
    'padding'       : {'offset':168, 'type': '<H'} #\x01\x80
}

footer_def = {
    'cuurentMode'   : {'offset':  0, 'type': '<H'},
    'fs001'         : {'offset':  2, 'type': '<H'},
    'fCWPhoneDup'   : {'offset':  4, 'type': '<H'},
    'currentFreq'   : {'offset':  6, 'type': '<H'},
    'contest'       : {'offset':  8, 'type': '<H'},
    'twice'         : {'offset': 10, 'type': '<H'},
    'pointFreqPhone': {'offset': 12, 'type': '<23H'},
    'pointFreqCW'   : {'offset': 58, 'type': '<23H'},
    'opNames'       : {'offset':104, 'type': '<600s'} #max 30人分
  }

logfile = args[1][:args[1].rfind('.')]
print(logfile)

with open('%s_output.csv' % logfile, 'w') as f_raw:
    title = ','.join(['callsign', 'my', 'ur', 'mode', 'freq', 'time', 'op', 'fDup', 'Remarks']) + '\n'
    f_raw.write(title)

    alive_counter = 0

    with open(args[1], 'br') as f:
        data = f.read()
        print(len(data))

        #ヘッダーブロックの処理
        #Get Total QSO count
        QSOs = struct.unpack_from(header_def['totalQSO']['type'], data, header_def['totalQSO']['offset'])
        #Set total size of qso blocks 
        qso_size = qso_block_size * QSOs[0]
        print(qso_size)
        cQSO = 0

        #QSOブロック全体のループ
        while block_offset < qso_size:
            cQSO += 1
            h = {}
            if alive_counter % 100 == 0:
                print('%d done...' % round(100.0*block_offset/qso_size))
            #各QSO
            for k, v in block_def.items():
                t_offset = block_offset + v['offset']
                h[k] = struct.unpack_from(v['type'], data, t_offset)
                #文字列のフィールドはパディング\x00を検索して切り詰め ペタルに戻さないといけないか?
                if v['type'][-1:] == 's': #https://qiita.com/tanuk1647/items/276d2be36f5abb8ea52e
                    #My = My[0][0:My[0].find (b'\x00')].strip(b'\x00').decode()
                    #print("before;", h[k])
                    h[k] = h[k][0][0:h[k][0].find (b'\x00')].strip(b'\x00').decode('sjis')
                #print(k)
                if k == 'mode':
                    index = h[k][0]
                    h[k] = table_Mode [str(index)] 
                if k == 'freq':
                    index = h[k][0]
                    h[k] = table_Freq [str(index)] 
                if k == 'time':
                    seconds = h[k][0]
                    td = datetime.timedelta(seconds=seconds)
                    epoch = datetime.datetime(year=1970, month=1, day=1, hour = 9) #JST = 9
                    resultDate = td + epoch
                    h[k] = resultDate
                #print(h[k])
                #print(block_offset, v['offset'], t_offset) 
            block_offset += qso_block_size
            # 1行のデータにまとめる
            csv_line = ','.join([h['callsign'], h['my'], h['ur'], h['mode'], h['freq'], str(h['time']), h['op'], str(h['fDup'][0]), h['Remarks']]) + '\n'
            f_raw.write(csv_line)


print('Read up to block_offset %d' % block_offset)
print('Total QSO # is', cQSO)
#print(block_offset)
#フッターブロックの処理
#コンテストとMDファイルの置換テーブルを今後作成する。ロカコンとその他? 
block_offset -= 2 #最後QSOレコード間のパディングが入ってないので引く
f = {}
for k, v in footer_def.items():
    t_offset = block_offset + v['offset']
    f[k] = struct.unpack_from(v['type'], data, t_offset)
    #文字列のフィールドはパディング\x00を検索して切り詰め ペタルに戻さないといけないか?
    if v['type'][-1:] == 's': #https://qiita.com/tanuk1647/items/276d2be36f5abb8ea52e
        #insert loop
        f[k] = f[k][0][0:f[k][0].find (b'\x00')].strip(b'\x00').decode('sjis')
    if k == 'cuurentMode':
        index = f[k][0]
        f[k] = table_Mode [str(index)] 
    if k == 'currentFreq':
        index = f[k][0]
        f[k] = table_Freq [str(index)] 
    if k == 'contest':
        index = f[k][0]
        f[k] = table_Contest [str(index)] 
        contestName = f['contest']
    if k == 'pointFreqPhone':
        #insert loop
        f[k] = f[k]
    if k == 'pointFreqCW':
        #insert loop
        f[k] = f[k]
    if k == 'opNames':
        #insert loop
        f[k] = f[k]

#QSOデータ書き込み
with open('%s_output.csv' % logfile, "r+", encoding='utf_8_sig') as f:
    original_data = f.read()
    f.seek(0)
    f.write(contestName + '\n')
    f.write(original_data)
