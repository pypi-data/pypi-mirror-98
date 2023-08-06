# Pink Belt

Pink Belt is an CLI tool for opinionated product development. It glues together Trello, GitHub and Slack for a CLI-driven development. 


## Installation & Usage

* `pip install pinkbelt`

### Testing

`paver test`

If you ran `pb init` and you want to do "discovery testing" with the integration tests,
set `FORCE_DISCOVERY`environment variable to `1`.

### Troubleshooting

If you try run `paver bump` and get error `TypeError: 'map' object is not subscriptable` you may need to run run `./venv/bin/paver bump` to fix this.

### Release

When the time is right, run `paver bump`.

When adding new feature (command etc), run `paver bump major` instead.

After it, just call `paver release` and enjoy your PyPI.

Note: GPG must be properly configured for usage with `git tag -s` and you must be project maintainer on PyPI.


## Acknowledgements

Pink Belt is a fork of unmaintained [Black Belt](https://github.com/apiaryio/black-belt). It's like Black Belt, but with more optimism.
