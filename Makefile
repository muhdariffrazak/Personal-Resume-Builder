IMAGE := resume-builder
VARIANT ?= full
VARIANTS := full mha-drone ai-ml-focused robotics-embedded-focused
DOCKER_RUN := docker run --rm -v $(CURDIR):/work -w /work --user $(shell id -u):$(shell id -g) $(IMAGE)

.PHONY: build-image build build-all docs reference-docx shell

build-image:
	docker build -t $(IMAGE) .

build: build-image
	$(DOCKER_RUN) python3 scripts/build.py --variant $(VARIANT)

build-all: build-image
	@for v in $(VARIANTS); do \
		echo "== building $$v =="; \
		$(DOCKER_RUN) python3 scripts/build.py --variant $$v || exit 1; \
	done

docs:
	python3 scripts/render_docs.py

reference-docx: build-image
	$(DOCKER_RUN) python3 scripts/build_reference_docx.py

shell: build-image
	docker run --rm -it -v $(CURDIR):/work -w /work --user $(shell id -u):$(shell id -g) $(IMAGE) bash
