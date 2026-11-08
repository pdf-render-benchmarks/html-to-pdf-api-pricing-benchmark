#!/usr/bin/env python3
"""HTML-to-PDF API Pricing Benchmark CLI."""
import argparse
import sys

def calculate_costs(monthly_volume, engineer_hourly_rate=65.0):
    # Self-hosted baseline: 2 vCPU 4GB RAM cloud instance ($48/mo) + Lambda concurrency spikes ($35/mo)
    # Plus maintenance: 3 hours/mo debugging rendering hangs & Chrome crashes
    infra_cost = 83.0 if monthly_volume <= 20000 else 166.0
    maintenance_hrs = 3.0 if monthly_volume <= 10000 else (5.0 if monthly_volume <= 30000 else 8.0)
    self_hosted_labor = maintenance_hrs * engineer_hourly_rate
    self_hosted_total = infra_cost + self_hosted_labor

    # Managed API tiers: Lite $29 (1,200), Plus $49 (3,000), Pro $99 (12,000), Scale $199 (35,000)
    if monthly_volume <= 1200:
        api_tier = "Lite Tier"
        api_cost = 29.0
    elif monthly_volume <= 3000:
        api_tier = "Plus Tier"
        api_cost = 49.0
    elif monthly_volume <= 12000:
        api_tier = "Professional Tier"
        api_cost = 99.0
    else:
        api_tier = "Scale / Enterprise Tier"
        api_cost = 199.0

    savings = self_hosted_total - api_cost
    savings_pct = (savings / self_hosted_total) * 100 if self_hosted_total > 0 else 0.0

    return {
        "monthly_volume": monthly_volume,
        "self_hosted_infra": infra_cost,
        "self_hosted_labor": self_hosted_labor,
        "self_hosted_total": self_hosted_total,
        "api_tier": api_tier,
        "api_cost": api_cost,
        "net_savings": savings,
        "savings_pct": savings_pct,
    }

def main():
    parser = argparse.ArgumentParser(description="HTML-to-PDF API Pricing & Infrastructure TCO Benchmark")
    parser.add_argument("--volume", type=int, default=10000, help="Monthly PDF generation volume (default: 10,000)")
    parser.add_argument("--rate", type=float, default=65.0, help="Engineer hourly labor rate in USD (default: $65/hr)")
    args = parser.parse_args()

    r = calculate_costs(args.volume, args.rate)
    print("=" * 70)
    print(" HTML-to-PDF API vs Self-Hosted Infrastructure TCO Benchmark")
    print("=" * 70)
    print(f" Monthly PDF Generation Volume : {r['monthly_volume']:,} documents")
    print(f" Self-Hosted Compute & Memory  : ${r['self_hosted_infra']:.2f}/mo")
    print(f" Engineer Triage & Maintenance : ${r['self_hosted_labor']:.2f}/mo ({r['self_hosted_labor']/args.rate:.1f} hrs @ ${args.rate:.2f}/hr)")
    print(f" Total Self-Hosted Monthly Cost: ${r['self_hosted_total']:.2f}/mo")
    print("-" * 70)
    print(f" Recommended Managed REST Tier : {r['api_tier']} (${r['api_cost']:.2f}/mo)")
    print(f" Projected Net Monthly Savings : ${r['net_savings']:.2f}/mo ({r['savings_pct']:.1f}% reduction)")
    print("=" * 70)
    return 0

if __name__ == "__main__":
    sys.exit(main())
