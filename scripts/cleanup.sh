#!/bin/bash

# CloudShellのすべてのファイルを削除するスクリプト

echo "========================================"
echo "CloudShell クリーンアップスクリプト"
echo "========================================"
echo ""
echo "警告: このスクリプトは現在のディレクトリのすべてのファイルを削除します"
echo "本当に削除しますか？ (yes/no)"
read -p "> " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "キャンセルしました"
    exit 0
fi

echo ""
echo "削除中..."
rm -rf *
rm -rf .*

echo "✓ すべてのファイルを削除しました"
echo ""
echo "現在のファイル一覧:"
ls -la
