#!/usr/bin/env python3
"""
Sweep driver for wsn-comparative-sim (ns-3.45 scratch executable).

Runs the six schemes across a node-density sweep and a traffic-load sweep,
each with independent RNG seeds, in parallel across cores. Every run appends
one row to data/wsn_raw_results.csv via the simulator's own CSV writer (the
simulator opens the file in append mode and writes a header only if the file
doesn't already exist yet, so concurrent processes racing on file creation
would corrupt the header -- this driver avoids that by pre-touching the file
with the header before launching any workers).

Resumable: before building the job list, reads whatever rows already exist
in OUT_CSV and skips any (scheme, numNodes, dataRateKbps, rngRun) tuple
already present -- so a killed/interrupted run can just be re-invoked with
the same --stage and it picks up where it left off, rather than
re-running (and duplicating) everything. Results are written incrementally
per-run already (each completed job is merged into OUT_CSV as soon as it
finishes, not batched at the end), so a kill at any point leaves OUT_CSV
usable as-is.

Usage:
    python3 scripts/run_sweep.py --stage smoke   # single run, sanity check
    python3 scripts/run_sweep.py --stage density # node-density sweep
    python3 scripts/run_sweep.py --stage traffic # traffic-load sweep
    python3 scripts/run_sweep.py --stage all      # both sweeps
"""
import argparse
import csv
import os
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed

NS3_ROOT = os.path.expanduser("~/ns-3.45")
OUT_CSV = os.path.join(os.path.dirname(__file__), "..", "data", "wsn_raw_results.csv")
OUT_CSV = os.path.abspath(OUT_CSV)

SCHEMES = ["IAGAPC-Enhanced", "AGAPC", "EGATS-N", "RCGA-ABC", "DGA-M", "CGAPD"]

# Kept in sync with the csv << "scheme,numNodes,..." line in
# scratch/wsn-comparative-sim.cc -- if that line changes, update this too,
# or the driver's own pre-touched header will silently mismatch the data
# rows written by the simulator binary.
CSV_HEADER = (
    "scheme,numNodes,areaWidth,areaHeight,simTime,dataRateKbps,packetSize,"
    "sinkVelocity,rngRun,gaBestFitness,packetsGenerated,packetsBufferedSent,"
    "packetsSent,packetsReceived,bufferOverflowDrops,"
    "pdrPercent,throughputKbps,avgDelaySec,totalEnergyConsumedJ,minRemainingEnergyJ,"
    "fndTimeSec,hndTimeSec,lndTimeSec,avgTurningAngleDeg,processingTimeMs,"
    "arpL3Drops,arpCacheDrops\n"
)

NUM_SEEDS = 10  # non-negotiable per plan: >=10 independent runs per config


def load_completed_tuples():
    """(scheme, numNodes, dataRateKbps, rngRun) tuples already in OUT_CSV."""
    done = set()
    if not os.path.exists(OUT_CSV):
        return done
    with open(OUT_CSV) as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                key = (
                    row["scheme"],
                    int(float(row["numNodes"])),
                    float(row["dataRateKbps"]),
                    int(float(row["rngRun"])),
                )
                done.add(key)
            except (KeyError, ValueError):
                continue  # malformed/partial row from a prior kill, ignore
    return done


def run_one(scheme, num_nodes, sim_time, data_rate_kbps, packet_size, sink_velocity, rng_run, run_tag):
    """Run a single ns-3 invocation with a private output file, return its path."""
    private_out = os.path.join(
        os.path.dirname(OUT_CSV),
        f"_tmp_{run_tag}_{scheme}_{num_nodes}_{data_rate_kbps}_{rng_run}.csv",
    )
    cmd_args = (
        f"wsn-comparative-sim "
        f"--scheme={scheme} --numNodes={num_nodes} --simTime={sim_time} "
        f"--dataRateKbps={data_rate_kbps} --packetSize={packet_size} "
        f"--sinkVelocity={sink_velocity} --rngRun={rng_run} "
        f"--outputFile={private_out}"
    )
    result = subprocess.run(
        ["./ns3", "run", cmd_args],
        cwd=NS3_ROOT,
        capture_output=True,
        text=True,
        timeout=600,
    )
    if result.returncode != 0:
        sys.stderr.write(
            f"[FAIL] {scheme} n={num_nodes} rate={data_rate_kbps} run={rng_run}\n"
            f"STDOUT: {result.stdout[-2000:]}\nSTDERR: {result.stderr[-2000:]}\n"
        )
        return None
    return private_out


def merge_and_cleanup(private_out):
    """Append a completed run's private CSV into OUT_CSV immediately, then
    delete the private file. Called as each job finishes, not batched --
    this is what makes progress durable across a kill."""
    if private_out is None or not os.path.exists(private_out):
        return
    with open(private_out) as f:
        lines = f.readlines()
    data_lines = lines[1:] if lines and lines[0].startswith("scheme,") else lines
    with open(OUT_CSV, "a") as out:
        out.writelines(data_lines)
        out.flush()
        os.fsync(out.fileno())
    os.remove(private_out)


def build_jobs(stage, completed):
    jobs = []
    skipped = 0

    def maybe_add(scheme, num_nodes, sim_time, data_rate_kbps, packet_size, sink_velocity, rng_run, run_tag):
        nonlocal skipped
        key = (scheme, num_nodes, float(data_rate_kbps), rng_run)
        if key in completed:
            skipped += 1
            return
        jobs.append(dict(scheme=scheme, num_nodes=num_nodes, sim_time=sim_time,
                          data_rate_kbps=data_rate_kbps, packet_size=packet_size,
                          sink_velocity=sink_velocity, rng_run=rng_run, run_tag=run_tag))

    if stage in ("smoke",):
        maybe_add("IAGAPC-Enhanced", 30, 60, 20, 512, 10, 1, "smoke")
    if stage in ("density", "all"):
        # 250 kbps matches the draft's own stated Table 5.1 parameter, and
        # closes the ~10x radio-model mismatch found in methods-delta.md.
        for n in [100, 200, 300, 500]:
            for scheme in SCHEMES:
                for seed in range(1, NUM_SEEDS + 1):
                    maybe_add(scheme, n, 300, 250, 512, 10, seed, "density")
    if stage in ("traffic", "all"):
        # Re-centered around 250kbps (was centered on the old 20kbps
        # default) so the traffic-sensitivity sweep spans a comparable
        # relative range (~10-20x) while including the draft's own rate.
        for rate in [50, 125, 250, 500, 1000]:
            for scheme in SCHEMES:
                for seed in range(1, NUM_SEEDS + 1):
                    maybe_add(scheme, 200, 300, rate, 512, 10, seed, "traffic")
    return jobs, skipped


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", required=True, choices=["smoke", "density", "traffic", "all"])
    ap.add_argument("--workers", type=int, default=os.cpu_count() or 4)
    args = ap.parse_args()

    os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)
    if not os.path.exists(OUT_CSV):
        with open(OUT_CSV, "w") as f:
            f.write(CSV_HEADER)

    completed = load_completed_tuples()
    jobs, skipped = build_jobs(args.stage, completed)
    print(f"Stage '{args.stage}': {len(jobs)} runs to do, {skipped} already done (resuming), "
          f"{args.workers} parallel workers.")

    if not jobs:
        print("Nothing to do -- all requested runs already present in", OUT_CSV)
        return

    if args.stage == "smoke":
        out = run_one(**jobs[0])
        merge_and_cleanup(out)
        print("Smoke run complete. Check", OUT_CSV)
        return

    completed_n, failed = 0, 0
    with ProcessPoolExecutor(max_workers=args.workers) as ex:
        futures = {ex.submit(run_one, **j): j for j in jobs}
        for fut in as_completed(futures):
            out = fut.result()
            merge_and_cleanup(out)
            if out is None:
                failed += 1
            else:
                completed_n += 1
            if (completed_n + failed) % 20 == 0:
                print(f"  progress: {completed_n} ok, {failed} failed, {completed_n+failed}/{len(jobs)}")

    print(f"Done. {completed_n} succeeded, {failed} failed. Output: {OUT_CSV}")


if __name__ == "__main__":
    main()
