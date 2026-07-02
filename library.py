"""Curated, ordered library of top system-design / engineering articles.

The bot works through this list IN ORDER, one per day. Each send marks the
previous one complete (advances the cursor stored in sent_articles.json) and
moves to the next. When the library is exhausted, the bot falls back to the
live RSS feeds in feeds.py.

To grow your collection toward hundreds of articles, just append more
{"title", "url", "source"} entries below. Broken/paywalled links are skipped
automatically, so it's safe to add generously.
"""

LIBRARY = [
    # ============================================================= #
    # Hello Interview — System Design in a Hurry (free core)
    # ============================================================= #
    {"title": "System Design in a Hurry: Introduction", "url": "https://www.hellointerview.com/learn/system-design/in-a-hurry/introduction", "source": "Hello Interview"},
    {"title": "How to Prepare for System Design Interviews", "url": "https://www.hellointerview.com/learn/system-design/in-a-hurry/how-to-prepare", "source": "Hello Interview"},
    {"title": "The Delivery Framework", "url": "https://www.hellointerview.com/learn/system-design/in-a-hurry/delivery", "source": "Hello Interview"},
    {"title": "Key Technologies", "url": "https://www.hellointerview.com/learn/system-design/in-a-hurry/key-technologies", "source": "Hello Interview"},
    {"title": "Core Concepts", "url": "https://www.hellointerview.com/learn/system-design/in-a-hurry/core-concepts", "source": "Hello Interview"},
    {"title": "Numbers You Should Know", "url": "https://www.hellointerview.com/learn/system-design/core-concepts/numbers-to-know", "source": "Hello Interview"},

    # Hello Interview — Patterns
    {"title": "Pattern: Realtime Updates", "url": "https://www.hellointerview.com/learn/system-design/patterns/realtime-updates", "source": "Hello Interview"},

    # Hello Interview — Deep dives (some premium; auto-skipped if locked)
    {"title": "Deep Dive: Vector Databases", "url": "https://www.hellointerview.com/learn/system-design/deep-dives/vector-databases", "source": "Hello Interview"},
    {"title": "Deep Dive: Redis", "url": "https://www.hellointerview.com/learn/system-design/deep-dives/redis", "source": "Hello Interview"},
    {"title": "Deep Dive: Kafka", "url": "https://www.hellointerview.com/learn/system-design/deep-dives/kafka", "source": "Hello Interview"},
    {"title": "Deep Dive: Cassandra", "url": "https://www.hellointerview.com/learn/system-design/deep-dives/cassandra", "source": "Hello Interview"},
    {"title": "Deep Dive: Elasticsearch", "url": "https://www.hellointerview.com/learn/system-design/deep-dives/elasticsearch", "source": "Hello Interview"},
    {"title": "Deep Dive: DynamoDB", "url": "https://www.hellointerview.com/learn/system-design/deep-dives/dynamodb", "source": "Hello Interview"},

    # Hello Interview — Problem breakdowns (some premium; auto-skipped if locked)
    {"title": "Design a Ride-Sharing Service (Uber)", "url": "https://www.hellointerview.com/learn/system-design/problem-breakdowns/uber", "source": "Hello Interview"},
    {"title": "Design a Distributed Rate Limiter", "url": "https://www.hellointerview.com/learn/system-design/problem-breakdowns/distributed-rate-limiter", "source": "Hello Interview"},
    {"title": "Design Instagram", "url": "https://www.hellointerview.com/learn/system-design/problem-breakdowns/instagram", "source": "Hello Interview"},
    {"title": "Design Yelp", "url": "https://www.hellointerview.com/learn/system-design/problem-breakdowns/yelp", "source": "Hello Interview"},
    {"title": "Design a Web Crawler", "url": "https://www.hellointerview.com/learn/system-design/problem-breakdowns/web-crawler", "source": "Hello Interview"},
    {"title": "Design an Ad Click Aggregator", "url": "https://www.hellointerview.com/learn/system-design/problem-breakdowns/ad-click-aggregator", "source": "Hello Interview"},
    {"title": "Design Dropbox", "url": "https://www.hellointerview.com/learn/system-design/problem-breakdowns/dropbox", "source": "Hello Interview"},
    {"title": "Design Ticketmaster", "url": "https://www.hellointerview.com/learn/system-design/problem-breakdowns/ticketmaster", "source": "Hello Interview"},
    {"title": "Staff-Level System Design", "url": "https://www.hellointerview.com/blog/staff-level-system-design", "source": "Hello Interview"},

    # ============================================================= #
    # AWS Builders' Library — production reliability essentials
    # ============================================================= #
    {"title": "Timeouts, Retries, and Backoff with Jitter", "url": "https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/", "source": "AWS Builders' Library"},
    {"title": "Challenges with Distributed Systems", "url": "https://aws.amazon.com/builders-library/challenges-with-distributed-systems/", "source": "AWS Builders' Library"},
    {"title": "Avoiding Fallback in Distributed Systems", "url": "https://aws.amazon.com/builders-library/avoiding-fallback-in-distributed-systems/", "source": "AWS Builders' Library"},
    {"title": "Using Load Shedding to Avoid Overload", "url": "https://aws.amazon.com/builders-library/using-load-shedding-to-avoid-overload/", "source": "AWS Builders' Library"},
    {"title": "Caching Challenges and Strategies", "url": "https://aws.amazon.com/builders-library/caching-challenges-and-strategies/", "source": "AWS Builders' Library"},
    {"title": "Workload Isolation Using Shuffle-Sharding", "url": "https://aws.amazon.com/builders-library/workload-isolation-using-shuffle-sharding/", "source": "AWS Builders' Library"},
    {"title": "Implementing Health Checks", "url": "https://aws.amazon.com/builders-library/implementing-health-checks/", "source": "AWS Builders' Library"},
    {"title": "Leader Election in Distributed Systems", "url": "https://aws.amazon.com/builders-library/leader-election-in-distributed-systems/", "source": "AWS Builders' Library"},
    {"title": "Reliability, Constant Work, and a Good Cup of Coffee", "url": "https://aws.amazon.com/builders-library/reliability-and-constant-work/", "source": "AWS Builders' Library"},
    {"title": "Ensuring Rollback Safety During Deployments", "url": "https://aws.amazon.com/builders-library/ensuring-rollback-safety-during-deployments/", "source": "AWS Builders' Library"},
    {"title": "Making Retries Safe with Idempotent APIs", "url": "https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/", "source": "AWS Builders' Library"},
    {"title": "Instrumenting Distributed Systems for Operational Visibility", "url": "https://aws.amazon.com/builders-library/instrumenting-distributed-systems-for-operational-visibility/", "source": "AWS Builders' Library"},
    {"title": "Static Stability Using Availability Zones", "url": "https://aws.amazon.com/builders-library/static-stability-using-availability-zones/", "source": "AWS Builders' Library"},
    {"title": "Avoiding Insurmountable Queue Backlogs", "url": "https://aws.amazon.com/builders-library/avoiding-insurmountable-queue-backlogs/", "source": "AWS Builders' Library"},
    {"title": "Fairness in Multi-Tenant Systems", "url": "https://aws.amazon.com/builders-library/fairness-in-multi-tenant-systems/", "source": "AWS Builders' Library"},
    {"title": "Automating Safe, Hands-Off Deployments", "url": "https://aws.amazon.com/builders-library/automating-safe-hands-off-deployments/", "source": "AWS Builders' Library"},

    # ============================================================= #
    # Google SRE Book — reliability engineering
    # ============================================================= #
    {"title": "Embracing Risk", "url": "https://sre.google/sre-book/embracing-risk/", "source": "Google SRE Book"},
    {"title": "Service Level Objectives", "url": "https://sre.google/sre-book/service-level-objectives/", "source": "Google SRE Book"},
    {"title": "Eliminating Toil", "url": "https://sre.google/sre-book/eliminating-toil/", "source": "Google SRE Book"},
    {"title": "Monitoring Distributed Systems", "url": "https://sre.google/sre-book/monitoring-distributed-systems/", "source": "Google SRE Book"},
    {"title": "Handling Overload", "url": "https://sre.google/sre-book/handling-overload/", "source": "Google SRE Book"},
    {"title": "Addressing Cascading Failures", "url": "https://sre.google/sre-book/addressing-cascading-failures/", "source": "Google SRE Book"},
    {"title": "Managing Critical State (Distributed Consensus)", "url": "https://sre.google/sre-book/managing-critical-state/", "source": "Google SRE Book"},
    {"title": "Load Balancing in the Datacenter", "url": "https://sre.google/sre-book/load-balancing-datacenter/", "source": "Google SRE Book"},
    {"title": "Load Balancing at the Frontend", "url": "https://sre.google/sre-book/load-balancing-frontend/", "source": "Google SRE Book"},
    {"title": "Data Integrity: What You Read Is What You Wrote", "url": "https://sre.google/sre-book/data-integrity/", "source": "Google SRE Book"},
    {"title": "Release Engineering", "url": "https://sre.google/sre-book/release-engineering/", "source": "Google SRE Book"},
    {"title": "Simplicity", "url": "https://sre.google/sre-book/simplicity/", "source": "Google SRE Book"},

    # ============================================================= #
    # Martin Fowler — architecture patterns
    # ============================================================= #
    {"title": "Microservices", "url": "https://martinfowler.com/articles/microservices.html", "source": "Martin Fowler"},
    {"title": "CQRS", "url": "https://martinfowler.com/bliki/CQRS.html", "source": "Martin Fowler"},
    {"title": "Event Sourcing", "url": "https://martinfowler.com/eaaDev/EventSourcing.html", "source": "Martin Fowler"},
    {"title": "Circuit Breaker", "url": "https://martinfowler.com/bliki/CircuitBreaker.html", "source": "Martin Fowler"},
    {"title": "Strangler Fig Application", "url": "https://martinfowler.com/bliki/StranglerFigApplication.html", "source": "Martin Fowler"},
    {"title": "Bounded Context", "url": "https://martinfowler.com/bliki/BoundedContext.html", "source": "Martin Fowler"},
    {"title": "Monolith First", "url": "https://martinfowler.com/bliki/MonolithFirst.html", "source": "Martin Fowler"},
    {"title": "Polyglot Persistence", "url": "https://martinfowler.com/bliki/PolyglotPersistence.html", "source": "Martin Fowler"},
    {"title": "Patterns of Distributed Systems: Write-Ahead Log", "url": "https://martinfowler.com/articles/patterns-of-distributed-systems/write-ahead-log.html", "source": "Martin Fowler"},
    {"title": "Serverless Architectures", "url": "https://martinfowler.com/articles/serverless.html", "source": "Martin Fowler"},
    {"title": "Blue Green Deployment", "url": "https://martinfowler.com/bliki/BlueGreenDeployment.html", "source": "Martin Fowler"},
    {"title": "Feature Toggles (Feature Flags)", "url": "https://martinfowler.com/articles/feature-toggles.html", "source": "Martin Fowler"},
    {"title": "How to Move Beyond a Monolith Data Layer (Data Mesh)", "url": "https://martinfowler.com/articles/data-mesh-principles.html", "source": "Martin Fowler"},

    # ============================================================= #
    # Distributed systems classics
    # ============================================================= #
    {"title": "Amazon's Dynamo", "url": "https://www.allthingsdistributed.com/2007/10/amazons_dynamo.html", "source": "Werner Vogels"},
    {"title": "Eventually Consistent", "url": "https://www.allthingsdistributed.com/2008/12/eventually_consistent.html", "source": "Werner Vogels"},
    {"title": "The Twelve-Factor App", "url": "https://12factor.net/", "source": "12factor"},
    {"title": "Files Are Fraught with Peril", "url": "https://danluu.com/deconstruct-files/", "source": "Dan Luu"},
    {"title": "Reading Postmortems", "url": "https://danluu.com/postmortem-lessons/", "source": "Dan Luu"},
    {"title": "How Web Bloat Impacts Users with Slow Devices", "url": "https://danluu.com/web-bloat/", "source": "Dan Luu"},
    {"title": "Latency and the Tail (p99) Problem", "url": "https://danluu.com/percentile-latency/", "source": "Dan Luu"},

    # ============================================================= #
    # Real-world engineering deep-dives (how big systems really work)
    # ============================================================= #
    {"title": "How Discord Stores Billions of Messages", "url": "https://discord.com/blog/how-discord-stores-billions-of-messages", "source": "Discord"},
    {"title": "How Discord Stores Trillions of Messages", "url": "https://discord.com/blog/how-discord-stores-trillions-of-messages", "source": "Discord"},
    {"title": "How Discord Scaled Elixir to 5,000,000 Concurrent Users", "url": "https://discord.com/blog/how-discord-scaled-elixir-to-5-000-000-concurrent-users", "source": "Discord"},
    {"title": "How Discord Handles 2.5M Concurrent Voice Users with WebRTC", "url": "https://discord.com/blog/how-discord-handles-two-and-half-million-concurrent-voice-users-using-webrtc", "source": "Discord"},
    {"title": "How Discord Indexes Billions of Messages", "url": "https://discord.com/blog/how-discord-indexes-billions-of-messages", "source": "Discord"},
    {"title": "How Discord Supercharges Network Disks for Extreme Low Latency", "url": "https://discord.com/blog/how-discord-supercharges-network-disks-for-extreme-low-latency", "source": "Discord"},
    {"title": "The Story of One Latency Spike", "url": "https://blog.cloudflare.com/the-story-of-one-latency-spike/", "source": "Cloudflare"},
    {"title": "Counting Things: A Lot of Different Things (Rate Limiting)", "url": "https://blog.cloudflare.com/counting-things-a-lot-of-different-things/", "source": "Cloudflare"},
    {"title": "How We Scaled nginx and Saved the World 54 Years Every Day", "url": "https://blog.cloudflare.com/how-we-scaled-nginx-and-saved-the-world-54-years-every-day/", "source": "Cloudflare"},
    {"title": "A Question of Timing", "url": "https://blog.cloudflare.com/a-question-of-timing/", "source": "Cloudflare"},
    {"title": "Strong Consistency Models", "url": "https://aphyr.com/posts/313-strong-consistency-models", "source": "Aphyr (Kyle Kingsbury)"},
    {"title": "The Network is Reliable", "url": "https://aphyr.com/posts/288-the-network-is-reliable", "source": "Aphyr (Kyle Kingsbury)"},
    {"title": "The USE Method (Performance Analysis)", "url": "https://www.brendangregg.com/usemethod.html", "source": "Brendan Gregg"},
    {"title": "CPU Utilization is Wrong", "url": "https://www.brendangregg.com/blog/2017-05-09/cpu-utilization-is-wrong.html", "source": "Brendan Gregg"},
    {"title": "Consistency Models", "url": "https://jepsen.io/consistency", "source": "Jepsen"},
    {"title": "Raft: In Search of an Understandable Consensus Algorithm", "url": "https://raft.github.io/", "source": "Raft"},
    {"title": "Apache Kafka: Internals & Design", "url": "https://kafka.apache.org/documentation/", "source": "Apache Kafka"},
    {"title": "PostgreSQL MVCC: Multi-Version Concurrency Control", "url": "https://www.postgresql.org/docs/current/mvcc-intro.html", "source": "PostgreSQL"},
    {"title": "TAO: The Power of the Graph", "url": "https://engineering.fb.com/2013/06/25/core-infra/tao-the-power-of-the-graph/", "source": "Meta Engineering"},
    {"title": "Scaling Services with Shard Manager", "url": "https://engineering.fb.com/2020/08/24/production-engineering/scaling-services-with-shard-manager/", "source": "Meta Engineering"},
    {"title": "Building Mobile-First Infrastructure for Messenger", "url": "https://engineering.fb.com/2014/10/09/production-engineering/building-mobile-first-infrastructure-for-messenger/", "source": "Meta Engineering"},
    {"title": "Designing Robust and Predictable APIs with Idempotency", "url": "https://stripe.com/blog/idempotency", "source": "Stripe"},
    {"title": "Scaling Your API with Rate Limiters", "url": "https://stripe.com/blog/rate-limiters", "source": "Stripe"},
    {"title": "Online Migrations at Scale", "url": "https://stripe.com/blog/online-migrations", "source": "Stripe"},
    {"title": "APIs as Infrastructure: Future-Proofing with Versioning", "url": "https://stripe.com/blog/api-versioning", "source": "Stripe"},
    {"title": "Canonical Log Lines", "url": "https://stripe.com/blog/canonical-log-lines", "source": "Stripe"},
    {"title": "How Figma's Multiplayer Technology Works", "url": "https://www.figma.com/blog/how-figmas-multiplayer-technology-works/", "source": "Figma"},
    {"title": "Rust in Production at Figma", "url": "https://www.figma.com/blog/rust-in-production-at-figma/", "source": "Figma"},
    {"title": "Sharding Postgres at Notion", "url": "https://www.notion.so/blog/sharding-postgres-at-notion", "source": "Notion"},
    {"title": "The Great Re-shard", "url": "https://www.notion.so/blog/the-great-re-shard", "source": "Notion"},
    {"title": "Goodbye Microservices: From 100s of Problem Children to 1 Superstar", "url": "https://segment.com/blog/goodbye-microservices/", "source": "Segment"},
    {"title": "Partitioning GitHub's Relational Databases to Scale", "url": "https://github.blog/2021-09-27-partitioning-githubs-relational-databases-scale/", "source": "GitHub Engineering"},
    {"title": "Rewriting the Heart of Our Sync Engine", "url": "https://dropbox.tech/infrastructure/rewriting-the-heart-of-our-sync-engine", "source": "Dropbox"},
    {"title": "How Slack Built Real-time Messaging", "url": "https://slack.engineering/real-time-messaging/", "source": "Slack"},
]
