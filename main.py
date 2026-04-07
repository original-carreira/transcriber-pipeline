from app.core.pipeline import Pipeline
from app.core.container import ServiceContainer


def main():
    services = ServiceContainer()
    pipeline = Pipeline(services)

    pipeline.run(
        input_file="data/input/input.mp4",
        output_dir="data/output"
    )


if __name__ == "__main__":
    main()