import streamlit as st
import json
from typing import Any, Dict, Set, List

st.title("JSON比較ツール")
st.write("複数のJSONを入力して、キーと型を比較します。")

# JSONの数を選択
num_jsons = st.number_input("比較するJSONの数", min_value=2, max_value=5, value=2, step=1)

# JSON入力エリア
json_inputs = []
json_data = []

for i in range(int(num_jsons)):
    st.subheader(f"JSON {i + 1}")
    json_text = st.text_area(
        f"JSON {i + 1}を入力してください",
        key=f"json_{i}",
        height=150,
        placeholder='{"name": "example", "age": 30, "active": true}'
    )
    json_inputs.append(json_text)

def get_type_name(value: Any) -> str:
    """値の型名を取得"""
    if value is None:
        return "null"
    elif isinstance(value, bool):
        return "boolean"
    elif isinstance(value, int):
        return "integer"
    elif isinstance(value, float):
        return "float"
    elif isinstance(value, str):
        return "string"
    elif isinstance(value, list):
        return "array"
    elif isinstance(value, dict):
        return "object"
    else:
        return type(value).__name__

def extract_keys_and_types(data: Any, prefix: str = "") -> Dict[str, str]:
    """JSONからキーと型を抽出（ネストされた構造にも対応）"""
    result = {}

    if isinstance(data, dict):
        for key, value in data.items():
            full_key = f"{prefix}.{key}" if prefix else key
            result[full_key] = get_type_name(value)

            # ネストされたオブジェクトや配列の場合、再帰的に処理
            if isinstance(value, dict):
                result.update(extract_keys_and_types(value, full_key))
            elif isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict):
                result.update(extract_keys_and_types(value[0], f"{full_key}[0]"))

    return result

# 比較ボタン
if st.button("比較する", type="primary"):
    # JSONをパース
    parsed_jsons = []
    all_valid = True

    for i, json_text in enumerate(json_inputs):
        if not json_text.strip():
            st.error(f"JSON {i + 1}が入力されていません")
            all_valid = False
            continue

        try:
            parsed = json.loads(json_text)
            parsed_jsons.append(parsed)
        except json.JSONDecodeError as e:
            st.error(f"JSON {i + 1}のパースエラー: {str(e)}")
            all_valid = False

    if all_valid and len(parsed_jsons) == int(num_jsons):
        # 各JSONからキーと型を抽出
        all_keys_and_types = []
        for parsed in parsed_jsons:
            keys_and_types = extract_keys_and_types(parsed)
            all_keys_and_types.append(keys_and_types)

        # 全てのキーを収集
        all_keys: Set[str] = set()
        for keys_and_types in all_keys_and_types:
            all_keys.update(keys_and_types.keys())

        # 結果を表示
        st.success("✅ 比較完了")

        # 比較結果をテーブルで表示
        st.subheader("比較結果")

        # データフレーム用のデータを準備
        comparison_data = []
        for key in sorted(all_keys):
            row = {"キー": key}

            for i, keys_and_types in enumerate(all_keys_and_types):
                if key in keys_and_types:
                    row[f"JSON {i + 1}"] = keys_and_types[key]
                else:
                    row[f"JSON {i + 1}"] = "❌ なし"

            comparison_data.append(row)

        # スタイル付きで表示
        st.dataframe(
            comparison_data,
            use_container_width=True,
            height=400
        )

        # 統計情報
        st.subheader("統計情報")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("総キー数", len(all_keys))

        with col2:
            # 全JSONに共通するキー
            common_keys = set(all_keys_and_types[0].keys())
            for keys_and_types in all_keys_and_types[1:]:
                common_keys &= set(keys_and_types.keys())
            st.metric("共通キー数", len(common_keys))

        with col3:
            # 型の不一致があるキー
            type_mismatch = 0
            for key in all_keys:
                types = set()
                for keys_and_types in all_keys_and_types:
                    if key in keys_and_types:
                        types.add(keys_and_types[key])
                if len(types) > 1:
                    type_mismatch += 1
            st.metric("型不一致", type_mismatch)

        # 共通キーのリスト
        if common_keys:
            with st.expander("📋 全JSONに共通するキー"):
                for key in sorted(common_keys):
                    st.write(f"- `{key}`: {all_keys_and_types[0][key]}")

        # 型が異なるキー
        type_mismatches = []
        for key in all_keys:
            types = {}
            for i, keys_and_types in enumerate(all_keys_and_types):
                if key in keys_and_types:
                    types[f"JSON {i + 1}"] = keys_and_types[key]
            if len(set(types.values())) > 1:
                type_mismatches.append((key, types))

        if type_mismatches:
            with st.expander("⚠️ 型が異なるキー"):
                for key, types in type_mismatches:
                    st.write(f"**`{key}`**")
                    for json_name, type_name in types.items():
                        st.write(f"  - {json_name}: `{type_name}`")

# 使用例
with st.expander("💡 使用例"):
    st.code('''
JSON 1:
{
  "id": 1,
  "name": "Alice",
  "age": 30,
  "active": true,
  "address": {
    "city": "Tokyo",
    "zip": "100-0001"
  }
}

JSON 2:
{
  "id": 2,
  "name": "Bob",
  "age": "25",
  "email": "bob@example.com",
  "address": {
    "city": "Osaka"
  }
}
''', language="json")
    st.write("上記のようなJSONを入力すると、キーの有無や型の違いを比較できます。")
