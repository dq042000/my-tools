# 檔名：convert_class_data.py

import sys
import json

print("請貼上資料，貼完後按 Ctrl+D (macOS/Linux) 或 Ctrl+Z 再 Enter (Windows)：")

# 讀取多行輸入
raw_data = sys.stdin.read()

# 處理每一行
lines = raw_data.strip().split('\n')

# 跳過第一行標題
data_lines = lines[1:]

result = []

for line in data_lines:
    values = line.strip().split('\t')
    if len(values) < 6:
        continue
    item = {
        "學年度": int(values[0]),
        "學校代碼": values[1],
        "學校類別": values[2],
        "年級": int(values[3]),
        "班級名稱": values[4],
        "班級排序": int(values[5])
    }
    result.append(item)

# 將結果轉成 JSON 字串
json_output = json.dumps(result, ensure_ascii=False, indent=2)

# 輸出到 output.txt
with open("output.txt", "w", encoding="utf-8") as f:
    f.write(json_output)

print("\n✅ 轉換完成，結果已儲存到 output.txt")

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

