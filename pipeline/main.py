from buildkite_sdk import Pipeline, CommandStep
from emojis.emojis import bazel, buildkite


def generate_pipeline():
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

    pipeline.add_step(
        CommandStep(
            label="{} Upload the package".format(buildkite),
            commands=[
                "bazel build //emojis:all",
                (
					"curl --request POST https://api.buildkite.com/v2/packages/organizations/nunciato/registries/bazel-buildkite-emojis/packages "
						"--header \"Authorization: Bearer $(buildkite-agent oidc request-token "
						"--audience 'https://packages.buildkite.com/nunciato/bazel-buildkite-emojis' "
						"--lifetime 300)\" "
						"--form file=@bazel-bin/emojis/dist/emojis-0.0.6-py3-none-any.whl "
						"--fail"
				),
            ],
            depends_on=[
                "test",
                "build",
            ],
        )
    )

    return pipeline.to_json()


print(generate_pipeline())
