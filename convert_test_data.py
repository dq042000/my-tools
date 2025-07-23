import sys
import json
import re

print("請貼上資料，貼完後按 Ctrl+D (macOS/Linux) 或 Ctrl+Z 再 Enter (Windows)：")

raw_data = sys.stdin.read()
lines = raw_data.strip().split('\n')

# 欄位名稱
headers = re.split(r'\s+', lines[0].strip())
data_lines = lines[1:]

# 判斷是否有「具備身分」欄位
has_identity = "具備身分" in headers
identity_idx = headers.index("具備身分") if has_identity else -1

# 整數欄位
int_fields = {
    "學年度", "年級", "性別", "身高", "體重",
    "坐姿體前彎", "立定跳遠", "仰臥捲腹", "漸速耐力跑"
}

result = []

for line in data_lines:
    # 先判斷是否為 tab 分隔
    if '\t' in line:
        values = line.strip().split('\t')
    else:
        # 對於空格分隔的資料，使用固定欄位數切割
        # 這樣可以確保空欄位不會被跳過
        values = re.split(r'\s+', line.strip(), maxsplit=len(headers) - 1)
        
        # 如果有「具備身分」欄位且切割後數量少一個，在對應位置插入空字串
        if has_identity and len(values) == len(headers) - 1:
            # 檢查是否在「具備身分」位置缺少值
            values.insert(identity_idx, "")
    
    # 補欄位數不夠的空值
    while len(values) < len(headers):
        values.append("")
    
    # 如果欄位數超過標題數，取前面的欄位
    values = values[:len(headers)]

    item = {}
    for i in range(len(headers)):
        key = headers[i]
        value = values[i].strip()

        if key in int_fields:
            item[key] = int(float(value)) if value else 0
        elif key == "心肺耐力":
            item[key] = value if value else "0.0"
        else:
            item[key] = value if value else ""

    result.append(item)

# 輸出到 output.txt
with open("output.txt", "w", encoding="utf-8") as f:
    f.write(json.dumps(result, ensure_ascii=False, indent=2))

print("\n✅ 轉換完成，已輸出為 output.txt")

try:
    import pyperclip
    with open("output.txt", "r", encoding="utf-8") as f:
        pyperclip.copy(f.read())
    print("\n📋 已自動複製到剪貼簿！")
except ImportError:
    import subprocess
    import sys
    print("\n⚠️ 未安裝 pyperclip，正在自動安裝...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyperclip"])
    try:
        import pyperclip
        with open("output.txt", "r", encoding="utf-8") as f:
            pyperclip.copy(f.read())
        print("\n📋 已自動複製到剪貼簿！")
    except Exception as e:
        print(f"\n❌ 自動安裝 pyperclip 失敗：{e}")

