#!/usr/bin/env python3
"""
Google Ads Search Terms Analyzer
Analyzes search terms and identifies the worst performing ones based on:
- Highest CPC (Cost Per Click)
- Lowest conversions
"""

import argparse
import sys
from typing import List, Dict
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
import yaml


class SearchTermsAnalyzer:
    """Analyzes Google Ads search terms to identify poor performers."""

    def __init__(self, config_path: str, customer_id: str):
        """
        Initialize the analyzer.

        Args:
            config_path: Path to google-ads.yaml configuration file
            customer_id: Google Ads customer ID (without hyphens)
        """
        self.client = GoogleAdsClient.load_from_storage(config_path)
        self.customer_id = customer_id

    def fetch_search_terms(self, days: int = 30) -> List[Dict]:
        """
        Fetch search terms data from Google Ads.

        Args:
            days: Number of days to look back (default: 30)

        Returns:
            List of dictionaries containing search term data
        """
        ga_service = self.client.get_service("GoogleAdsService")

        query = f"""
            SELECT
                search_term_view.search_term,
                metrics.clicks,
                metrics.impressions,
                metrics.cost_micros,
                metrics.conversions,
                metrics.average_cpc
            FROM search_term_view
            WHERE segments.date DURING LAST_{days}_DAYS
                AND metrics.impressions > 0
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
                    metrics = row.metrics

                    # Calculate CPC in currency units (from micros)
                    cpc = metrics.average_cpc / 1_000_000 if metrics.average_cpc else 0
                    cost = metrics.cost_micros / 1_000_000 if metrics.cost_micros else 0

                    search_terms.append({
                        'search_term': search_term,
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

    def get_worst_terms(self, days: int = 30, top_n: int = 10) -> List[Dict]:
        """
        Get the worst performing search terms.

        Args:
            days: Number of days to analyze
            top_n: Number of worst terms to return

        Returns:
            List of worst performing search terms with scores
        """
        print(f"Fetching search terms data for the last {days} days...")
        search_terms = self.fetch_search_terms(days)

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

    def print_results(self, terms: List[Dict]):
        """
        Print the analysis results in a readable format.

        Args:
            terms: List of search terms to display
        """
        if not terms:
            print("\nNo results to display.")
            return

        print("\n" + "="*100)
        print(f"{'RANK':<6} {'SEARCH TERM':<30} {'CPC':<10} {'COST':<10} {'CLICKS':<8} {'CONV':<8} {'SCORE':<10}")
        print("="*100)

        for idx, term in enumerate(terms, 1):
            print(
                f"{idx:<6} "
                f"{term['search_term'][:28]:<30} "
                f"${term['cpc']:<9.2f} "
                f"${term['cost']:<9.2f} "
                f"{term['clicks']:<8} "
                f"{term['conversions']:<8.1f} "
                f"{term['badness_score']:<10.2f}"
            )

        print("="*100)
        print("\nLegend:")
        print("  CPC   = Cost Per Click")
        print("  COST  = Total cost spent on this search term")
        print("  CONV  = Number of conversions")
        print("  SCORE = Badness score (higher = worse performing)")
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
            fieldnames = ['rank', 'search_term', 'cpc', 'cost', 'clicks',
                         'impressions', 'conversions', 'badness_score']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for idx, term in enumerate(terms, 1):
                writer.writerow({
                    'rank': idx,
                    'search_term': term['search_term'],
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
        description='Analyze Google Ads search terms to find worst performers'
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
        help='Google Ads customer ID (without hyphens, e.g., 1234567890)'
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

    try:
        # Initialize analyzer
        analyzer = SearchTermsAnalyzer(args.config, customer_id)

        # Get worst performing terms
        worst_terms = analyzer.get_worst_terms(days=args.days, top_n=args.top)

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
