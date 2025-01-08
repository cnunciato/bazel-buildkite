from buildkite_sdk import Pipeline

def generate_pipeline():
	pipeline = Pipeline()

	pipeline.add_command_step({
		"label": ":bazel: Run Bazel build",
		"command": "bazel build //:main",
	})
	
	pipeline.add_command_step({
		"label": ":bazel: Run Bazel tests",
		"command": "bazel test //:test_main",
	})
	
	return pipeline.to_json()

print(generate_pipeline())
