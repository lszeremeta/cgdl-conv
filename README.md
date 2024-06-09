# CGDL-conv

Common Graph Definition Language converter for many other formats including [JSON](https://www.json.org/), [CBOR](http://cbor.io/) (binary JSON), [XML](https://www.w3.org/XML/), [TOML](https://github.com/toml-lang/), [YAML](https://yaml.org/) and (PG)[SHACL](https://www.w3.org/TR/shacl/). Written in [Python](https://www.python.org/) 3. Works from CLI.

For examples see [`examples` directory](https://github.com/lszeremeta/cgdl-conv/blob/main/examples).

## Usage

```shell
usage: cgdl-conv.py [-h]
                    (-m | -j | -pj | -cb | -x | -px | -t | -y | -c | -g | -s)
                    file
```

### Positional arguments

```shell
  file               a CGDL file
```

### Optional arguments

```shell
  -h, --help         show this help message and exit
  -m, --metadata     display CGDL metadata
  -j, --json         display CGDL in JSON
  -pj, --prettyjson  display CGDL in pretty JSON
  -cb, --cbor        display CGDL in CBOR (binary JSON)
  -x, --xml          display CGDL in XML
  -px, --prettyxml   display CGDL in pretty XML
  -t, --toml         display TOML
  -y, --yaml         display CGDL in compact YAML
  -c, --cgdl         display CGDL (in YAML)
  -g, --graphql      display GraphQL
  -s, --shacl        display (PG)SHACL (in RDF)
```

Available options may vary depending on the version. To display all available options with their descriptions use ``cgdl-conv.py -h``.

## Contribution

Would you like to improve this project? Great! We are waiting for your help and suggestions. If you are new to open source contributions, read [How to Contribute to Open Source](https://opensource.guide/how-to-contribute/).

## License

Distributed under [MIT license](https://github.com/lszeremeta/cgdl-conv/blob/main/LICENSE).

The code, examples and this README were adapted from the [PGDL-conv](https://github.com/domel/PGDL-conv) by [Łukasz Szeremeta](https://github.com/lszeremeta) and [Dominik Tomaszuk](https://github.com/domel), distributed under the [MIT license](https://github.com/domel/PGDL-conv/blob/master/LICENSE).
