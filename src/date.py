#!/usr/bin/env python3
"""
日付表示プログラム
現在の日付を表示します
"""

from datetime import datetime

def display_current_date():
    """現在の日付を表示する関数"""
    current_date = datetime.now()
    print(f"現在の日付: {current_date.strftime('%Y年%m月%d日')}")
    print(f"現在の時刻: {current_date.strftime('%H:%M:%S')}")

if __name__ == "__main__":
    display_current_date()