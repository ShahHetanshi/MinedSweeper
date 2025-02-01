import argparse
import time
from modules.orchestrator import ProcessingPipeline
from config import DEFAULT_PARAMS

def main():
    parser = argparse.ArgumentParser(
        description="PDF to Multimedia Converter",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('input_pdf', help="Path to input PDF file")
    parser.add_argument('-l', '--languages', nargs='+',
                       default=DEFAULT_PARAMS['languages'],
                       choices=DEFAULT_PARAMS['languages'],
                       help="Output languages")
    parser.add_argument('-o', '--output', 
                       help="Custom output directory path")
    
    args = parser.parse_args()
    
    print("\n" + "="*50)
    print(f"📚 Processing PDF: {args.input_pdf}")
    print(f"🌐 Languages: {', '.join(args.languages)}")
    print("="*50 + "\n")
    
    start_time = time.time()
    pipeline = ProcessingPipeline(args.input_pdf)
    result_dir = pipeline.run_pipeline(args.languages)
    
    if result_dir:
        print("\n" + "="*50)
        print(f"✅ Successfully generated outputs in: {result_dir}")
        print(f"⏱ Total processing time: {time.time()-start_time:.2f} seconds")
        print("="*50)
        return 0
    else:
        print("\n❌ Processing failed")
        return 1

if __name__ == "__main__":
    main()