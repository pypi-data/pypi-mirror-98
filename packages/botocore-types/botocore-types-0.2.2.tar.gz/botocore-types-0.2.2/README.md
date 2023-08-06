# botocore-types [![PyPI](https://img.shields.io/pypi/v/botocore-types.svg)](https://pypi.org/project/botocore-types/)

Type stubs for [`botocore`][0].

For boto3 stubs checkout [`mypy_boto3_builder`][1].

## dev

```sh
s/lint
```

### publish new version

1. increment version in `pyproject.toml`
2. update `CHANGELOG.md`
3. publish to pypi

   ```
   poetry publish --build
   ```

## generating stubs

1. stubgen

2. delete the `docs` folder as that's internal

3. replace vendored imports with normal package imports. Don't want to have
   to type `requests` when types for it already exist in `typeshed`.

[0]: https://github.com/boto/botocore
[1]: https://github.com/vemel/mypy_boto3_builder
