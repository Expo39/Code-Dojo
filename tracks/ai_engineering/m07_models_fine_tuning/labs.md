# Labs: m07_models_fine_tuning

Real services, your own accounts, your own money (`../labs/README.md`: set up, budget alerts, tagging and the
teardown routine first). A lab gives the goal and the checks, never the steps. Estimate the cost before you
start, then compare with the bill the next morning; prices are from 26/11/2026 and change.

## L7.1: Serve an open model on a rented GPU

- **Goal:** Start a GPU instance (a `g6.xlarge` at about $0.80 per hour on demand), serve a small open model with an inference server, load-test it, and compute your cost per million output tokens against a hosted model of similar quality.
- **Services:** one GPU instance, a security group limited to your address, a storage volume
- **Estimated cost:** $3 to $8 (3 to 5 hours of GPU time plus the volume; spot instances can halve the compute)
- **Time:** about 5 hours
- **Done when:** tokens per second at 1, 8 and 32 concurrent requests, GPU memory used, and cost per million output tokens at your measured throughput and at 20% utilisation
- **Teardown:** **terminate the instance and delete its volume**; stopping is not enough because the volume keeps billing; check by tag

## L7.2: A LoRA fine-tune you can measure

- **Goal:** Fine-tune a 1 to 3 billion parameter model with LoRA on 1,000 to 2,000 examples for one narrow format task; compare it with the same model prompted, and with a hosted model, on a held-out set.
- **Services:** one GPU instance (a `g5.xlarge` is about $1.006 per hour), a fine-tuning library, an experiment log
- **Estimated cost:** $5 to $20 (2 to 6 hours of GPU time plus data preparation and evaluation)
- **Time:** about 8 hours
- **Done when:** a table: held-out score for prompted, fine-tuned and hosted models, training cost, and the one case where fine-tuning was not worth it
- **Teardown:** as L7.1; also delete saved checkpoints and snapshots
