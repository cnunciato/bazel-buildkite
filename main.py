from buildkite_sdk import Pipeline

def generate_pipeline():
	pipeline = Pipeline()
	pipeline.add_command_step({"command": "echo 'Hello, world!'"})

	return pipeline.to_json()

if __name__ == "__main__":
    print(generate_pipeline())
