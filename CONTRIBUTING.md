# 貢献ガイド

NIFCLOUD SDK for Python へのご貢献ありがとうございます。このドキュメントでは、開発環境のセットアップから、コードの提交までのプロセスを説明します。

## 開発環境のセットアップ

### 必要なツール

- Python 3.8 以上
- [uv](https://docs.astral.sh/uv/) - パッケージ管理
- [git](https://git-scm.com/) - バージョン管理

### セットアップ手順

1. **リポジトリをクローン**

```bash
git clone https://github.com/norikmb/nifcloud-sdk-python.git
cd nifcloud-sdk-python
```

2. **開発環境を構築**

```bash
# uv でプロジェクト依存関係をインストール
uv sync

# pre-commit フックをセットアップ
pre-commit install
```

3. **セットアップの確認**

```bash
# テストを実行
make test

# リント、型チェックを実行
make lint
```

## 開発ワークフロー

### ブランチ戦略

- **main**: リリース済みコード（保護されたブランチ）
- **develop**: 開発ブランチ（base branch）
- **feature/\***: 新機能開発用ブランチ
- **fix/\***: バグ修正用ブランチ

### ブランチ作成例

```bash
# develop ブランチから新しいフィーチャーブランチを作成
git checkout develop
git pull origin develop
git checkout -b feature/my-feature

# または

git checkout -b fix/my-bugfix
```

## コード品質基準

### リント・フォーマット

このプロジェクトは以下のツールを使用しています：

- **ruff**: 統合 Linter・フォーマッター
- **mypy**: 型チェッカー
- **bandit**: セキュリティスキャナー
- **pre-commit**: 自動フック

コミット前に以下を実行してください：

```bash
# 自動修正
make format

# リント・型チェック・セキュリティチェック
make lint
```

または、手動で実行：

```bash
# ruff でリント＆フォーマット
uv run ruff check . --fix
uv run ruff format .

# mypy で型チェック
uv run mypy --ignore-missing-imports nifcloud

# bandit でセキュリティチェック
uv run bandit -r nifcloud -ll
```

### ドキュメント

すべてのモジュール、クラス、関数には **Google スタイル** の docstring を追加してください。

#### 例

```python
"""Module description here."""

def my_function(param1: str, param2: int) -> bool:
    """Brief description of the function.

    Longer description if needed. Explain the purpose,
    behavior, and any important notes.

    Args:
        param1 (str): Description of param1.
        param2 (int): Description of param2.

    Returns:
        bool: Description of the return value.

    Raises:
        ValueError: When some condition is met.

    Example:
        >>> result = my_function("test", 42)
        >>> print(result)
        True
    """
    pass
```

## Conventional Commits

このプロジェクトは **Conventional Commits** 形式でコミットメッセージを標準化しています。

### フォーマット

```
<type>(<scope>): <subject>

<body>

<footer>
```

### タイプ一覧

| タイプ     | 説明                                 | 例                                      |
| ---------- | ------------------------------------ | --------------------------------------- |
| `feat`     | 新機能                               | `feat(auth): add OAuth2 support`        |
| `fix`      | バグ修正                             | `fix(serialize): correct JSON encoding` |
| `chore`    | ビルド、CI、バージョン等             | `chore: update dependencies`            |
| `docs`     | ドキュメント変更                     | `docs: update README`                   |
| `style`    | フォーマット、コードスタイル変更     | `style: apply ruff fixes`               |
| `refactor` | 機能追加やバグ修正がない、コード改善 | `refactor: simplify parsing`            |
| `perf`     | パフォーマンス改善                   | `perf: optimize loop`                   |
| `test`     | テスト追加・修正                     | `test: add auth tests`                  |
| `ci`       | CI/CD 設定変更                       | `ci: add bandit to workflow`            |

### スコープ

省略可能ですが、以下のスコープを推奨します：

- `auth` - 認証・認可
- `serialize` - シリアライザー
- `parsers` - パーサー
- `session` - セッション管理
- `config` - 設定・プロバイダー
- `docs` - ドキュメント
- `deps` - 依存関係管理

### コミットメッセージの例

```bash
# 新機能
git commit -m "feat(auth): add SigV4 signature support"

# バグ修正
git commit -m "fix(parsers): handle null timestamps correctly"

# チェンジログに含めない変更
git commit -m "chore: update pre-commit configuration"

# 複数行メッセージ
git commit -m "feat(serialize): support batch API operations

- Add BatchOperation class
- Implement request batching logic
- Support response aggregation

Closes #123"
```

## テスト

### テスト実行

```bash
# すべてのテストを実行
make test

# 特定のテストファイルを実行
uv run pytest tests/unit/test_serialize_computing.py

# カバレッジ付きで実行
uv run pytest --cov=nifcloud tests/unit

# 特定のテストだけ実行
uv run pytest tests/unit/test_serialize_computing.py::test_serialize -v
```

### テストカバレッジ目標

目標カバレッジは **80%** です。以下で確認できます：

```bash
uv run pytest --cov=nifcloud --cov-report=html tests/unit
# htmlcov/index.html をブラウザで開く
```

### テスト作成ガイド

- テストはファイル名を `test_*.py` または `*_test.py` とします
- テスト関数は `test_` で始める
- テストには説明的な名前を付ける

```python
def test_serialize_computing_auth_with_valid_parameters():
    """Test serializing computing auth with valid parameters."""
    serializer = ComputingSerializer()
    result = serializer.serialize(test_params)
    assert result is not None
```

## プルリクエスト

### プルリクエスト作成時のチェックリスト

- [ ] ブランチ名は `feature/*` または `fix/*` から開始
- [ ] コミットメッセージが Conventional Commits 形式
- [ ] テストが追加/更新されている
- [ ] すべてのテストが成功している
- [ ] `make lint` でエラーがない
- [ ] ドキュメントが更新されている（必要に応じて）
- [ ] CHANGELOG への追加が検討されている（オプション）

### PR のテンプレート

プルリクエストの説明には、以下を含めてください：

```markdown
## 説明

何を変更したか、なぜ変更したかを簡潔に説明します。

## 関連する Issue

Closes #<issue_number>

## 変更内容

- 変更 1
- 変更 2

## テスト

- テスト 1
- テスト 2

## チェックリスト

- [ ] ローカルでテスト実行済み
- [ ] リント・型チェック成功
- [ ] ドキュメント更新済み
```

## ドキュメント

### README の更新

プロジェクトの使用方法に関する大きな変更があれば、`README.md` を更新してください。

### Sphinx ドキュメント

API ドキュメントは `docs/source/` にあります。大規模な新機能の場合、対応するドキュメントを追加してください。

```bash
# ドキュメント生成
cd docs
make html

# ブラウザで確認
# _build/html/index.html
```

## リリースプロセス

リリースは `main` ブランチから行われます。メンテナーが以下のステップで対応します：

1. `develop` から `main` へ PR を作成
2. PR のレビュー
3. マージ後、自動的に PyPI へ公開
4. タグが自動作成され、GitHub Release が生成

詳細は [Releases](https://github.com/norikmb/nifcloud-sdk-python/releases) を参照。

## コードレビュー

### レビューポイント

- コード品質（リント、型チェック）
- テストカバレッジ
- ドキュメント完全性
- パフォーマンスと互換性

### コメント時の配慮

- 建設的で丁寧なコメントを心がける
- 質問形式で改善案を提示
- 個人的な好みではなく、プロジェクトの基準を基準にする

## バグ報告

バグを見つけた場合：

1. [GitHub Issues](https://github.com/norikmb/nifcloud-sdk-python/issues) で類似の Issue を検索
2. 見つからなければ、新しい Issue を作成
3. 以下の情報を含めてください：
   - Python バージョン
   - nifcloud-sdk バージョン
   - 再現手順
   - 期待される動作
   - 実際の動作

## セキュリティ脆弱性報告

セキュリティ上の問題を発見した場合、public な Issue ではなく、メンテナーに直接ご連絡ください。

## ライセンス

このプロジェクトに貢献することで、あなたは自分の貢献が Apache License 2.0 の下でライセンスされることに同意します。

---

ご質問や不明な点があれば、Issue を作成するか、メンテナーにご連絡ください。
