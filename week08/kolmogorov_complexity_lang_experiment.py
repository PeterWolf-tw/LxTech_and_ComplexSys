#!/usr/bin/env python3
# -*- coding:utf-8 -*-


import zlib
import gzip
import bz2
import random
import string
from typing import Union, Dict

class KolmogorovComplexity:
    """
    使用壓縮演算法來近似 Kolmogorov Complexity
    """

    @staticmethod
    def compress_length(text: str, method: str = 'zlib') -> int:
        """
        計算文本壓縮後的長度

        Args:
            text: 輸入文本
            method: 壓縮方法 ('zlib', 'gzip', 'bz2')

        Returns:
            壓縮後的字節長度
        """
        data = text.encode('utf-8')

        if method == 'zlib':
            compressed = zlib.compress(data)
        elif method == 'gzip':
            compressed = gzip.compress(data)
        elif method == 'bz2':
            compressed = bz2.compress(data)
        else:
            raise ValueError(f"不支援的壓縮方法: {method}")

        return len(compressed)

    @staticmethod
    def kolmogorov_complexity(text: str, method: str = 'zlib') -> float:
        """
        計算文本的 Kolmogorov Complexity 近似值

        Args:
            text: 輸入文本
            method: 壓縮方法

        Returns:
            複雜度值(壓縮後長度)
        """
        return KolmogorovComplexity.compress_length(text, method)

    @staticmethod
    def normalized_compression_distance(text1: str, text2: str, method: str = 'zlib') -> float:
        """
        計算兩個文本之間的標準化壓縮距離 (NCD)
        NCD(x,y) = [C(xy) - min(C(x),C(y))] / max(C(x),C(y))

        值越小表示兩個文本越相似

        Args:
            text1: 第一個文本
            text2: 第二個文本
            method: 壓縮方法

        Returns:
            NCD 距離值 (0-1 之間)
        """
        c_x = KolmogorovComplexity.compress_length(text1, method)
        c_y = KolmogorovComplexity.compress_length(text2, method)
        c_xy = KolmogorovComplexity.compress_length(text1 + text2, method)

        ncd = (c_xy - min(c_x, c_y)) / max(c_x, c_y)
        return ncd

    @staticmethod
    def compression_ratio(text: str, method: str = 'zlib') -> float:
        """
        計算壓縮率

        Args:
            text: 輸入文本
            method: 壓縮方法

        Returns:
            壓縮率 (壓縮後大小 / 原始大小)
        """
        original_size = len(text.encode('utf-8'))
        compressed_size = KolmogorovComplexity.compress_length(text, method)
        return compressed_size / original_size if original_size > 0 else 0

    @staticmethod
    def is_human_like(text: str, method: str = 'zlib') -> Dict[str, Union[float, bool, str]]:
        """
        判斷文本是否像人類語言

        人類語言的特徵:
        - 壓縮率通常在 0.3 到 0.7 之間
        - 既有結構(可壓縮)又有變化(不完全重複)

        Args:
            text: 輸入文本
            method: 壓縮方法

        Returns:
            包含判斷結果的字典
        """
        if len(text) < 50:
            return {
                'is_human_like': None,
                'compression_ratio': None,
                'confidence': 'low',
                'reason': '文本太短,無法可靠判斷(建議至少50字符)'
            }

        ratio = KolmogorovComplexity.compression_ratio(text, method)

        # 人類語言的壓縮率通常在這個範圍
        # 這些閾值基於經驗觀察
        LOWER_BOUND = 0.35  # 太低表示過度重複
        UPPER_BOUND = 0.85  # 太高表示過於隨機

        is_human = LOWER_BOUND <= ratio <= UPPER_BOUND

        # 判斷置信度
        if ratio < 0.2:
            confidence = 'high'
            reason = '極度重複,不像自然語言'
        elif ratio < LOWER_BOUND:
            confidence = 'medium'
            reason = '重複性較高,可能是生成文本或模板'
        elif ratio > 0.9:
            confidence = 'high'
            reason = '近乎隨機,不像自然語言(可能是加密或亂碼)'
        elif ratio > UPPER_BOUND:
            confidence = 'medium'
            reason = '隨機性較高,結構性不足'
        else:
            confidence = 'medium'
            reason = '符合自然語言的壓縮特徵'

        return {
            'is_human_like': is_human,
            'compression_ratio': ratio,
            'confidence': confidence,
            'reason': reason
        }

    @staticmethod
    def analyze_text_type(text: str, method: str = 'zlib') -> str:
        """
        分析文本類型

        Args:
            text: 輸入文本
            method: 壓縮方法

        Returns:
            文本類型的描述
        """
        ratio = KolmogorovComplexity.compression_ratio(text, method)

        if ratio < 0.2:
            return "極度重複型 (如: aaaa... 或簡單模式)"
        elif ratio < 0.35:
            return "高重複型 (可能是模板或自動生成)"
        elif ratio < 0.5:
            return "結構化自然語言 (正常人類寫作)"
        elif ratio < 0.7:
            return "多樣化自然語言 (豐富詞彙)"
        elif ratio < 0.85:
            return "高熵文本 (技術文檔或混合語言)"
        else:
            return "近隨機型 (亂碼、加密或極度不規則)"


# 使用範例
if __name__ == "__main__":
    print("=" * 70)
    print("Kolmogorov Complexity 用於判斷文本是否像人類語言")
    print("=" * 70)

    # 測試文本範例
    test_cases = [
        ("正常英文", "The quick brown fox jumps over the lazy dog. " * 5),
        ("正常中文", "人工智慧是電腦科學的一個分支,它試圖理解智慧的本質,並製造出具有智慧的機器。" * 3),
        ("重複文本", "hello " * 50),
        ("極度重複", "a" * 200),
        ("隨機文本", ''.join(random.choices(string.ascii_letters + string.digits, k=200))),
        ("混合文本", "AI and ML are transforming 科技產業 in many ways. " * 4),
    ]

    print("\n【文本類型判斷】\n")

    for name, text in test_cases:
        result = KolmogorovComplexity.is_human_like(text)
        text_type = KolmogorovComplexity.analyze_text_type(text)

        print(f"測試: {name}")
        print(f"  文本預覽: {text[:50]}{'...' if len(text) > 50 else ''}")
        print(f"  文本長度: {len(text)} 字符")
        print(f"  壓縮率: {result['compression_ratio']:.3f}")
        print(f"  是否像人類語言: {'✓ 是' if result['is_human_like'] else '✗ 否'}")
        print(f"  置信度: {result['confidence']}")
        print(f"  判斷理由: {result['reason']}")
        print(f"  文本類型: {text_type}")
        print()

    # 實際應用範例
    print("=" * 70)
    print("【實際應用:檢測 AI 生成文本 vs 人類文本】")
    print("=" * 70)

    human_text = """
    今天天氣真好,我決定出去走走。路過公園時,看到許多小朋友在玩耍,
    他們的笑聲讓整個公園都充滿了活力。我買了一杯咖啡,坐在長椅上,
    享受這難得的悠閒時光。偶爾有微風吹過,帶來陣陣花香,讓人心情愉悅。
    """

    ai_like_text = """
    天氣很好。我出去了。我看到公園。公園有小孩。小孩在玩。小孩很開心。
    我買咖啡。我坐下。我喝咖啡。有風。風很舒服。我很高興。今天真好。
    天氣很好。我出去了。我看到公園。公園有小孩。小孩在玩。小孩很開心。
    """

    repetitive_text = "這是一個測試。" * 30

    print("\n人類寫作風格:")
    result = KolmogorovComplexity.is_human_like(human_text)
    print(f"  壓縮率: {result['compression_ratio']:.3f}")
    print(f"  判斷: {result['reason']}")

    print("\nAI 簡單生成風格:")
    result = KolmogorovComplexity.is_human_like(ai_like_text)
    print(f"  壓縮率: {result['compression_ratio']:.3f}")
    print(f"  判斷: {result['reason']}")

    print("\n過度重複文本:")
    result = KolmogorovComplexity.is_human_like(repetitive_text)
    print(f"  壓縮率: {result['compression_ratio']:.3f}")
    print(f"  判斷: {result['reason']}")

    print("\n" + "=" * 70)
    print("註: 此方法適合作為輔助工具,需結合其他 NLP 技術才能更準確判斷")
    print("=" * 70)