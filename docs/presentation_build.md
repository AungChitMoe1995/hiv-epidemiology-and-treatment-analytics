# Presentation source and rebuild

The analytical pipeline uses the public Python packages in requirements.txt. It can reproduce analysis, figures, reports and the notebook from the stored snapshot without presentation authoring dependencies.

The editable presentation uses the bundled JavaScript `@oai/artifact-tool` runtime. It is an optional local authoring dependency and is not publicly installable from the Python requirements. Set `ARTIFACT_TOOL_MODULE` to the absolute path of its `dist/artifact_tool.mjs`, with Node.js on PATH, then run `python src/create_presentation.py` or `python src/run_pipeline.py --presentation`.

`src/create_presentation.py` prepares chart/table values from stored outputs and invokes `src/create_presentation.mjs`. The builder uses source-labelled data, excludes censored point values, and puts sources and the snapshot fingerprint in slide notes. The default analytics pipeline preserves the reviewed deck only when its stored snapshot fingerprint matches.

The deck contains 22 slides, seven editable native charts and five editable tables. Finalization materializes literal chart workbooks from the plotted values for editing in PowerPoint. Full source tables and lineage remain in the repository. The reviewed deck was opened and rendered in Microsoft PowerPoint. Artifact Tool package and layout checks supplement that visual review.
