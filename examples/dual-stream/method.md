# Fictional method: dual-stream classification

This is a synthetic teaching example, not a published method or an evaluated result.

An RGB image and a depth image are processed by separate encoders.

The two feature vectors are concatenated and passed to a classifier to predict a class.

During training only, an alignment loss is computed from the two feature vectors. The alignment loss is not evaluated during inference.

No shared weights, gradient routing, loss formula, tensor dimensions, metrics, or superiority claims are specified. The diagram must not invent them.
