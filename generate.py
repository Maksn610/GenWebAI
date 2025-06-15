import argparse
from app.generator import generate_website_content
from app.logger_config import logger


def main():
    parser = argparse.ArgumentParser(description="Generate static websites using LLM")
    parser.add_argument("--topic", type=str, required=True, help="Main topic of the websites")
    parser.add_argument("--count", type=int, default=1, help="Number of sites to generate")
    parser.add_argument("--style", type=str, choices=["educational", "marketing", "technical"], required=True)
    parser.add_argument("--max_tokens", type=int, default=800)
    parser.add_argument("--temperature", type=float, default=0.9)
    parser.add_argument("--top_p", type=float, default=0.95)
    parser.add_argument("--variation_seed", type=int, help="Optional seed to control variation")

    args = parser.parse_args()

    for i in range(args.count):
        try:
            logger.info(f"[CLI] Generating site {i + 1} of {args.count} for topic='{args.topic}'")
            result = generate_website_content(
                topic=args.topic,
                style=args.style,
                max_tokens=args.max_tokens,
                temperature=args.temperature,
                top_p=args.top_p,
                variation_seed=args.variation_seed,
            )
            logger.info(f"[CLI] Site saved to: {result['file_path']}")
            print(f"\n[✔] Site {i + 1}/{args.count}")
            print(f"    📄 Title: {result['title']}")
            print(f"    📝 Meta: {result['meta_description']}")
            print(f"    📁 Path: {result['file_path']}")
        except Exception as e:
            logger.error(f"Error generating site {i + 1}: {e}")
            print(f"[!] Failed to generate site {i + 1}: {e}")


if __name__ == "__main__":
    main()
