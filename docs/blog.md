# Redis Streams: Simple to Sophisticated

### Ideas
- start simple and build out to something feature rich.
- Can we host this in an interactive app?

### Structure
1. Introduction
    - Setting up streaming can be an intimidating exercise
    - Often people reach for tools that are way overkill (aka Kafka, myself included)
2. Let's explore the simplest way to build a streaming pipeline
3. Redis basics
    - XADD
    - XREAD
    - XLEN
    - Consumer groups
        - It is very important to understand that Redis consumer groups have nothing to do, from an implementation standpoint, with Kafka (TM) consumer groups. Yet they are similar in functionality, so I decided to keep Kafka's (TM) terminology, as it originally popularized this idea.
        - XGROUP
        - XREADGROUP
        - XACK
        - XPENDING
3. Adding Stream processing
3. Adding scaling (kubernetes)
    - consumer groups
    - increase throughput
3. Adding Persistence
4. Adding Replication/failover


5. Comparison with Kafka

