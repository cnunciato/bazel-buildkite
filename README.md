# bazel-buildkite

An example of using Bazel with Buildkite! :kite:

```bash
$ bazel build //:main

INFO: Analyzed target //:main (0 packages loaded, 0 targets configured).
INFO: Found 1 target...
Target //:main up-to-date:
  bazel-bin/main
INFO: Elapsed time: 0.132s, Critical Path: 0.00s
INFO: 1 process: 1 internal.
INFO: Build completed successfully, 1 total action
```

```bash
$ bazel test //:test_main

INFO: Analyzed target //:test_main (0 packages loaded, 2 targets configured).
INFO: Found 1 test target...
Target //:test_main up-to-date:
  bazel-bin/test_main
INFO: Elapsed time: 0.108s, Critical Path: 0.00s
INFO: 1 process: 1 internal.
INFO: Build completed successfully, 1 total action
//:test_main                                                    (cached) PASSED in 0.3s
```

```bash
$ bazel run //:main
...

INFO: Running command line: bazel-bin/main
{
    "steps": [
        {
            "command": "echo 'Hello, world!'"
        }
    ]
}
```