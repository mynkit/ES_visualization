# ES_visualization

## Deploy

### 開発環境

以下コマンド実行後，http://localhost にアクセス

```sh
make run env=local
```

### 本番環境(未実装)

```sh
make run env=prd
```

## Test

```sh
make test
```

## Stop Server

```sh
make stop
```

## Format

autopep8

```sh
make format
```

## Linter

flake8

```sh
make lint
```