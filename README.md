# Internet Measurement — coursework and projects

Selected work from the **Internet Measurement** course at the University of Tehran (Spring 2024). This repository collects my five individual homework reports and three project reports prepared with **Amir Amin**. The reports are in Persian; this README provides an English guide for readers reviewing my academic work.

## Projects

| Phase | Topic | Artifact |
| --- | --- | --- |
| 1 | Device and network-traffic monitoring with the Elastic stack | [Report](projects/01-network-monitoring/report-fa.pdf), [Elastic lab](projects/elastic-stack-lab/README.md) |
| 2 | Network threat detection using Elasticsearch, Kibana, and Filebeat | [Report](projects/02-threat-detection/report-fa.pdf), [Elastic lab](projects/elastic-stack-lab/README.md) |
| 3 | Linux performance profiling with `perf` and flame graphs | [Report](projects/03-linux-profiling/report-fa.pdf), [benchmark code](projects/03-linux-profiling/sort_benchmark.cpp) |

The phase-three benchmark compares insertion, selection, and bubble sort. The source in this repository is a portfolio edition of the original small C++ benchmark: it uses a fixed random seed, repeated wall-clock measurements, equal input for every algorithm, and a sorted-output check. This improves reproducibility; the original 2024 measurements in the report are not claimed to have been produced by the updated source.

The shared [Elastic Stack lab](projects/elastic-stack-lab/README.md) is a newly written, runnable reconstruction of the monitoring and threat-event workflow from phases one and two. The archived submissions contained reports and screenshots, but no original Elastic configuration files. Its events are synthetic, and its local Docker integration has not been executed on this machine because Docker is not installed here.

### Reproduce the phase-three benchmark

On a system with a C++17 compiler:

```bash
g++ -std=c++17 -O2 -Wall -Wextra projects/03-linux-profiling/sort_benchmark.cpp -o sort_benchmark
./sort_benchmark 1000 5
```

The optional arguments are the number of integers and repetitions. The program prints CSV rows containing the median runtime in milliseconds. Runtime varies by machine, compiler, background load, and CPU frequency scaling, so compare algorithms under the same conditions.

## Individual homework

| Homework | Topic | Report |
| --- | --- | --- |
| 1 | Linux setup and packet capture with `tcpdump` | [PDF](homework/01-tcpdump.pdf) |
| 2 | Packet inspection with Wireshark | [PDF](homework/02-wireshark.pdf) |
| 3 | Distributed tracing concepts and Jaeger | [PDF](homework/03-jaeger.pdf) |
| 4 | Timing experiments and dynamic voltage/frequency scaling | [PDF](homework/04-timing-dvfs.pdf) |
| 5 | Data-cleaning workflow in Python | [PDF](homework/05-data-cleaning.pdf), [runnable code](homework/05-data-cleaning/README.md) |

## Scope and attribution

The reports are selected from my own 2024 submissions. The three project reports were coauthored with Amir Amin. Student ID numbers have been removed from these public PDF copies. I served as a teaching assistant in a later term; student submissions and teaching materials from that term are excluded. Course handouts, third-party templates, videos, binaries, and datasets are also excluded. The homework-five script is a cleaned, runnable edition of my original notebook; its patient-level input and notebook outputs are omitted.
