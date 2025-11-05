#!/usr/bin/env python3
"""
Google Ads Search Terms Analyzer
Analyzes search terms and identifies the worst performing ones based on:
- Highest CPC (Cost Per Click)
- Lowest conversions

Supports both direct account access and MCC (Manager) account access.
"""

import argparse
import sys
from typing import List, Dict, Optional
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
import yaml


class SearchTermsAnalyzer:
    """Analyzes Google Ads search terms to identify poor performers."""

    def __init__(self, config_path: str, customer_id: str, login_customer_id: Optional[str] = None):
        """
        Initialize the analyzer.

        Args:
            config_path: Path to google-ads.yaml configuration file
            customer_id: Google Ads customer ID to analyze (without hyphens)
            login_customer_id: Optional MCC account ID for authentication (without hyphens).
                              If not provided, uses the value from config file.
        """
        # Load client configuration
        self.client = GoogleAdsClient.load_from_storage(config_path)

        # Override login_customer_id if provided via command line
        if login_customer_id:
            self.client.login_customer_id = login_customer_id
            print(f"Using MCC account {login_customer_id} to access customer {customer_id}")

        self.customer_id = customer_id

    def list_campaigns(self) -> List[Dict]:
        """
        List all campaigns in the account.

        Returns:
            List of dictionaries containing campaign information
        """
        ga_service = self.client.get_service("GoogleAdsService")

        query = """
            SELECT
                campaign.id,
                campaign.name,
                campaign.status,
                metrics.impressions,
                metrics.clicks,
                metrics.cost_micros
            FROM campaign
            WHERE campaign.status != 'REMOVED'
            ORDER BY campaign.name
        """

        campaigns = []

        try:
            stream = ga_service.search_stream(
                customer_id=self.customer_id,
                query=query
            )

            for batch in stream:
                for row in batch.results:
                    campaign = row.campaign
                    metrics = row.metrics

                    campaigns.append({
                        'id': campaign.id,
                        'name': campaign.name,
                        'status': campaign.status.name,
                        'impressions': metrics.impressions,
                        'clicks': metrics.clicks,
                        'cost': metrics.cost_micros / 1_000_000 if metrics.cost_micros else 0
                    })

        except GoogleAdsException as ex:
            print(f"Error fetching campaigns: {ex}")
            for error in ex.failure.errors:
                print(f"\tError: {error.message}")
            sys.exit(1)

        return campaigns

    def fetch_search_terms(self, days: int = 30, campaign_ids: Optional[List[str]] = None) -> List[Dict]:
        """
        Fetch search terms data from Google Ads.

        Args:
            days: Number of days to look back (default: 30)
            campaign_ids: Optional list of campaign IDs to filter by

        Returns:
            List of dictionaries containing search term data
        """
        ga_service = self.client.get_service("GoogleAdsService")

        # Build the WHERE clause
        where_conditions = [
            f"segments.date DURING LAST_{days}_DAYS",
            "metrics.impressions > 0"
        ]

        # Add campaign filter if specified
        if campaign_ids:
            campaign_filter = " OR ".join([f"campaign.id = {cid}" for cid in campaign_ids])
            where_conditions.append(f"({campaign_filter})")

        where_clause = " AND ".join(where_conditions)

        query = f"""
            SELECT
                search_term_view.search_term,
                campaign.id,
                campaign.name,
                metrics.clicks,
                metrics.impressions,
                metrics.cost_micros,
                metrics.conversions,
                metrics.average_cpc
            FROM search_term_view
            WHERE {where_clause}
            ORDER BY metrics.cost_micros DESC
        """

        search_terms = []

        try:
            stream = ga_service.search_stream(
                customer_id=self.customer_id,
                query=query
            )

            for batch in stream:
                for row in batch.results:
                    search_term = row.search_term_view.search_term
                    campaign = row.campaign
                    metrics = row.metrics

                    # Calculate CPC in currency units (from micros)
                    cpc = metrics.average_cpc / 1_000_000 if metrics.average_cpc else 0
                    cost = metrics.cost_micros / 1_000_000 if metrics.cost_micros else 0

                    search_terms.append({
                        'search_term': search_term,
                        'campaign_id': campaign.id,
                        'campaign_name': campaign.name,
                        'clicks': metrics.clicks,
                        'impressions': metrics.impressions,
                        'cost': cost,
                        'conversions': metrics.conversions,
                        'cpc': cpc
                    })

        except GoogleAdsException as ex:
            print(f"Error fetching search terms: {ex}")
            for error in ex.failure.errors:
                print(f"\tError: {error.message}")
            sys.exit(1)

        return search_terms

    def calculate_score(self, term: Dict) -> float:
        """
        Calculate a "badness" score for a search term.
        Higher score = worse performing term

        Score is based on:
        - High CPC (weighted)
        - Low conversions (weighted)
        - Cost without conversions

        Args:
            term: Dictionary containing search term data

        Returns:
            Badness score (higher is worse)
        """
        cpc = term['cpc']
        conversions = term['conversions']
        cost = term['cost']
        clicks = term['clicks']

        # Avoid division by zero
        if clicks == 0:
            return 0

        # Calculate conversion rate
        conversion_rate = conversions / clicks if clicks > 0 else 0

        # Calculate cost per conversion (if any conversions exist)
        cost_per_conversion = cost / conversions if conversions > 0 else float('inf')

        # Badness score components:
        # 1. High CPC is bad (weight: 30%)
        # 2. Low conversion rate is bad (weight: 40%)
        # 3. High cost without conversions is bad (weight: 30%)

        cpc_score = cpc * 30
        conversion_score = (1 - conversion_rate) * 40
        waste_score = (cost if conversions == 0 else cost_per_conversion * 0.1) * 30

        return cpc_score + conversion_score + waste_score

    def get_worst_terms(self, days: int = 30, top_n: int = 10, campaign_ids: Optional[List[str]] = None) -> List[Dict]:
        """
        Get the worst performing search terms.

        Args:
            days: Number of days to analyze
            top_n: Number of worst terms to return
            campaign_ids: Optional list of campaign IDs to filter by

        Returns:
            List of worst performing search terms with scores
        """
        if campaign_ids:
            print(f"Fetching search terms data for {len(campaign_ids)} campaign(s) over the last {days} days...")
        else:
            print(f"Fetching search terms data for all campaigns over the last {days} days...")

        search_terms = self.fetch_search_terms(days, campaign_ids)

        if not search_terms:
            print("No search terms found.")
            return []

        print(f"Analyzing {len(search_terms)} search terms...")

        # Calculate scores for all terms
        for term in search_terms:
            term['badness_score'] = self.calculate_score(term)

        # Sort by badness score (descending) and get top N
        worst_terms = sorted(
            search_terms,
            key=lambda x: x['badness_score'],
            reverse=True
        )[:top_n]

        return worst_terms

    def print_campaigns(self, campaigns: List[Dict]):
        """
        Print the list of campaigns in a readable format.

        Args:
            campaigns: List of campaigns to display
        """
        if not campaigns:
            print("\nNo campaigns found.")
            return

        print("\n" + "="*120)
        print(f"{'ID':<12} {'CAMPAIGN NAME':<50} {'STATUS':<12} {'IMPR':<12} {'CLICKS':<10} {'COST':<10}")
        print("="*120)

        for campaign in campaigns:
            print(
                f"{campaign['id']:<12} "
                f"{campaign['name'][:48]:<50} "
                f"{campaign['status']:<12} "
                f"{campaign['impressions']:<12,} "
                f"{campaign['clicks']:<10,} "
                f"${campaign['cost']:<9,.2f}"
            )

        print("="*120)
        print(f"\nTotal campaigns: {len(campaigns)}")
        print("\nUse --campaign-id with one or more campaign IDs to analyze specific campaigns.")

    def print_results(self, terms: List[Dict]):
        """
        Print the analysis results in a readable format.

        Args:
            terms: List of search terms to display
        """
        if not terms:
            print("\nNo results to display.")
            return

        print("\n" + "="*130)
        print(f"{'RANK':<6} {'SEARCH TERM':<30} {'CAMPAIGN':<25} {'CPC':<10} {'COST':<10} {'CLICKS':<8} {'CONV':<8} {'SCORE':<10}")
        print("="*130)

        for idx, term in enumerate(terms, 1):
            print(
                f"{idx:<6} "
                f"{term['search_term'][:28]:<30} "
                f"{term['campaign_name'][:23]:<25} "
                f"${term['cpc']:<9.2f} "
                f"${term['cost']:<9.2f} "
                f"{term['clicks']:<8} "
                f"{term['conversions']:<8.1f} "
                f"{term['badness_score']:<10.2f}"
            )

        print("="*130)
        print("\nLegend:")
        print("  CPC      = Cost Per Click")
        print("  COST     = Total cost spent on this search term")
        print("  CONV     = Number of conversions")
        print("  SCORE    = Badness score (higher = worse performing)")
        print("  CAMPAIGN = Campaign name where this search term appeared")
        print("\nConsider adding these terms as negative keywords to improve campaign performance.")

    def export_to_csv(self, terms: List[Dict], filename: str = "worst_search_terms.csv"):
        """
        Export results to CSV file.

        Args:
            terms: List of search terms to export
            filename: Output CSV filename
        """
        import csv

        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['rank', 'search_term', 'campaign_id', 'campaign_name', 'cpc', 'cost',
                         'clicks', 'impressions', 'conversions', 'badness_score']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for idx, term in enumerate(terms, 1):
                writer.writerow({
                    'rank': idx,
                    'search_term': term['search_term'],
                    'campaign_id': term['campaign_id'],
                    'campaign_name': term['campaign_name'],
                    'cpc': f"{term['cpc']:.2f}",
                    'cost': f"{term['cost']:.2f}",
                    'clicks': term['clicks'],
                    'impressions': term['impressions'],
                    'conversions': f"{term['conversions']:.1f}",
                    'badness_score': f"{term['badness_score']:.2f}"
                })

        print(f"\nResults exported to {filename}")


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Analyze Google Ads search terms to find worst performers',
        epilog='For MCC (Manager) account access, specify --login-customer-id with your MCC account ID'
    )
    parser.add_argument(
        '--config',
        type=str,
        default='google-ads.yaml',
        help='Path to google-ads.yaml configuration file (default: google-ads.yaml)'
    )
    parser.add_argument(
        '--customer-id',
        type=str,
        required=True,
        help='Google Ads customer ID to analyze (without hyphens, e.g., 1234567890)'
    )
    parser.add_argument(
        '--login-customer-id',
        type=str,
        help='MCC (Manager) account ID for authentication (without hyphens). '
             'Use this when accessing client accounts through a manager account. '
             'If not provided, uses the login_customer_id from config file.'
    )
    parser.add_argument(
        '--campaign-id',
        type=str,
        action='append',
        dest='campaign_ids',
        help='Campaign ID to analyze (can be specified multiple times). '
             'If not specified, analyzes all campaigns. Use --list-campaigns to see available campaigns.'
    )
    parser.add_argument(
        '--list-campaigns',
        action='store_true',
        help='List all campaigns in the account and exit'
    )
    parser.add_argument(
        '--days',
        type=int,
        default=30,
        help='Number of days to analyze (default: 30)'
    )
    parser.add_argument(
        '--top',
        type=int,
        default=10,
        help='Number of worst terms to display (default: 10)'
    )
    parser.add_argument(
        '--export',
        type=str,
        help='Export results to CSV file (optional)'
    )

    args = parser.parse_args()

    # Validate customer ID format
    customer_id = args.customer_id.replace('-', '')
    if not customer_id.isdigit():
        print("Error: Customer ID must contain only digits")
        sys.exit(1)

    # Validate login customer ID format if provided
    login_customer_id = None
    if args.login_customer_id:
        login_customer_id = args.login_customer_id.replace('-', '')
        if not login_customer_id.isdigit():
            print("Error: Login Customer ID must contain only digits")
            sys.exit(1)

    try:
        # Initialize analyzer
        analyzer = SearchTermsAnalyzer(args.config, customer_id, login_customer_id)

        # Handle list campaigns mode
        if args.list_campaigns:
            print("Fetching campaigns...")
            campaigns = analyzer.list_campaigns()
            analyzer.print_campaigns(campaigns)
            sys.exit(0)

        # Validate campaign IDs if provided
        campaign_ids = None
        if args.campaign_ids:
            campaign_ids = []
            for cid in args.campaign_ids:
                cid_clean = cid.replace('-', '')
                if not cid_clean.isdigit():
                    print(f"Error: Campaign ID '{cid}' must contain only digits")
                    sys.exit(1)
                campaign_ids.append(cid_clean)

        # Get worst performing terms
        worst_terms = analyzer.get_worst_terms(days=args.days, top_n=args.top, campaign_ids=campaign_ids)

        # Display results
        analyzer.print_results(worst_terms)

        # Export if requested
        if args.export:
            analyzer.export_to_csv(worst_terms, args.export)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
