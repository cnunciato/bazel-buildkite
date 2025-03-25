from buildkite_sdk import Pipeline, CommandStep
from emojis.emojis import bazel, buildkite


def generate_pipeline(version):
    pipeline = Pipeline()

    pipeline.add_agent("queue", "hosted-macos")

    pipeline.add_step(
        CommandStep(
            label=f"{bazel} Build the pipeline binary",
            commands=["bazel build //pipeline:main"],
        )
    )

    pipeline.add_step(
        CommandStep(
            label=f"{bazel} Test the pipeline binary",
            commands=["bazel test //pipeline:test_main"],
        )
    )

    pipeline.add_step(
        CommandStep(
            key="build",
            label=f"{bazel} Build the emoji library",
            commands=["bazel build //emojis:emojis --build_event_json_file=bazel-events.json"],
            plugins=[
                {
                    "mcncl/bazel-annotate#v0.1.0": {
                        "bep_file": "bazel-events.json",
                        "skip_if_no_bep": True,
                    }
                },
            ],
        )
    )

    pipeline.add_step(
        CommandStep(
            key="test",
            label=f"{bazel} Test the emoji library",
            commands=["bazel test //emojis:test_emojis"],
        )
    )

    pipeline.add_step(
        CommandStep(
            key="sign",
            label=f"{buildkite} Generate attestation",
            commands=[
                "bazel build //emojis:all",
            ],
            artifact_paths=[f"bazel-bin/emojis/dist/emojis-{version}-py3-none-any.whl"],
            plugins=[
                {
                    "generate-provenance-attestation#v1.1.0": {
                        "artifacts": f"bazel-bin/emojis/dist/emojis-{version}-py3-none-any.whl",
                        "attestation_name": "attestation.json",
                    }
                },
            ],
            depends_on=[
                "test",
                "build",
            ],
        )
    )

    pipeline.add_step(
        CommandStep(
            label=f"{buildkite} Upload the package",
            commands=[
                "bazel build //emojis:all",
            ],
            plugins=[
                {
                    "publish-to-packages#v2.2.0": {
                        "artifacts": f"bazel-bin/emojis/dist/emojis-{version}-py3-none-any.whl",
                        "registry": "nunciato/bazel-buildkite-emojis",
                        "attestations": [
                            "attestation.json",
                        ],
                    }
                }
            ],
            depends_on=[
                "sign",
            ],
        )
    )

    return pipeline.to_json()


print(generate_pipeline("0.0.12"))
