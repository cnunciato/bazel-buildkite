from buildkite_sdk import Pipeline, CommandStep
from emojis.emojis import bazel, buildkite, books


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
            commands=["bazel build //emojis:emojis"],
        )
    )

    pipeline.add_step(
        CommandStep(
            key="test",
            label=f"{bazel} Test the emoji library",
            commands=["bazel test //emojis:test_emojis"],
        )
    )

    optional = Pipeline()
    optional.add_step(
        CommandStep(
            label=f"{books} Build and deploy the docs",
            commands=[
                "echo 'Building the docs...'",
            ],
        )
    )

    pipeline.add_step(
        CommandStep(
            key="sign",
            label=f"{buildkite} Generate attestation",
            commands=[f"""cat "{optional.to_yaml()}" | buildkite-agent pipeline upload"""],
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


print(generate_pipeline("0.0.13"))
