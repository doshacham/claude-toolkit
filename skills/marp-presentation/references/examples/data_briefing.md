---
marp: true
theme: dashboard
paginate: true
header: "Q1 Activation Review"
footer: "growth@example.com · 2026-04-12"
---

<!-- _class: lead -->

# Activation is up 12.4% — new users drove 73% of the lift

### Growth briefing · Q1 2026

<!--
EXAMPLE — golden example for the data-briefing mode.
Outline:
1. Headline in the title (the recommendation is implicit)
2. Big number
3. Source + window
4. Where it came from (chart + cohort)
5. Drill-down (regions, channels)
6. Anomalies
7. Recommendation
Keep it 8 slides. Executives don't read past slide 8.
-->

---

<!-- _class: lead -->

# 12.4%

### week-over-week activation lift

---

## Source

**Period**: 2026-03-01 to 2026-03-31
**Definition**: user completes onboarding + performs ≥1 core action within 24h
**Sample**: 412k new signups, 89k returning

Data source: `growth.activation_daily`
Query: `sql/activation_q1.sql`

---

## Where the lift came from

![bg right:55% w:90%](./charts/activation_breakdown.png)

- **New users**: +18% (drove 73% of absolute gain)
- **Returning**: +4% (small)
- **Dormant reactivations**: +9% (meaningful in absolute terms)

---

## Drill-down by region

| Region  | Before | After | Δ     |
|---------|--------|-------|-------|
| NA      | 41.2%  | 48.3% | +7.1  |
| EMEA    | 38.4%  | 42.8% | +4.4  |
| APAC-NE | 52.1%  | 58.0% | +5.9  |
| APAC-SE | 44.0%  | 41.9% | **−2.1** |

<!-- Walk through: APAC-SE is the anomaly. Everything else moved in the same direction. -->

---

## The anomaly

**APAC-SE dropped 2.1 points.**

Root cause hypothesis: the new onboarding copy references cultural context that doesn't translate. The Indonesian and Vietnamese funnels both regressed at the copy-heavy step.

Owner: @loc-team
ETA for A/B: 2026-04-19

---

## Mobile Safari shows no lift

Desktop +14%. Mobile Chrome +11%. **Mobile Safari: 0%.**

Likely: a layout regression in the new onboarding card on iOS. We have a reproduction. Fix is queued.

---

## Recommendation

**Keep the new onboarding flow.** It works everywhere except two edge cases, both of which have owners.

Roll forward. Don't roll back for the edge cases. Fix them in parallel.

<!-- Stop here. Everything below is backup if asked. -->

---

## Backup: cohort detail

| Signup channel | Lift (W1→W4) |
|----------------|---------------|
| Organic search | +16.8%        |
| Paid social    | +9.2%         |
| Referral       | +21.3%        |
| Direct         | +7.1%         |

---

<!-- _class: lead -->

# Questions?

Dashboards: `grafana.internal/d/activation`
