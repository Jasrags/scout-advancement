#!/usr/bin/env python3
"""
Cub Scout Advancement List Processor
Processes one or more CSVs of awarded advancements and groups them by scout.

Input: One or more CSV files with columns including First Name, Last Name, Den Type, and Item Name
Output: CSV with format: "Full Name", "Den Type", "Item Names (comma-separated)"
"""

import csv
import sys
from collections import OrderedDict


def process_advancements(input_files, output_file):
    """
    Read one or more advancement CSVs and group awards by scout.
    
    Args:
        input_files: List of paths to input CSV files
        output_file: Path to output CSV file
    """
    # Define den type rank order
    DEN_TYPE_ORDER = {
        'lion': 1,
        'tiger': 2,
        'wolf': 3,
        'bear': 4,
        'webelos': 5,
        'webelos 2': 6,
        'arrow of light': 6,  # Same rank as webelos 2
    }
    
    # Use OrderedDict to maintain the order scouts appear in the input
    scouts = OrderedDict()
    
    for input_file in input_files:
        try:
            print(f"  Reading: {input_file}")
            with open(input_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                row_count = 0
                for row in reader:
                    first_name = row['First Name'].strip()
                    last_name = row['Last Name'].strip()
                    den_type = row['Den Type'].strip()
                    item_name = row['Item Name'].strip()
                    
                    # Create unique key for each scout
                    scout_key = (first_name, last_name, den_type)
                    
                    # Initialize list if this is the first time we see this scout
                    if scout_key not in scouts:
                        scouts[scout_key] = []
                    
                    # Add the item name to this scout's list
                    scouts[scout_key].append(item_name)
                    row_count += 1
                
                print(f"    ✓ {row_count} advancements found")
                
        except FileNotFoundError:
            print(f"  ✗ Error: Could not find input file '{input_file}'")
            sys.exit(1)
        except KeyError as e:
            print(f"  ✗ Error: Missing required column in CSV: {e}")
            print("    Required columns: First Name, Last Name, Den Type, Item Name")
            sys.exit(1)
        except Exception as e:
            print(f"  ✗ Error processing file: {e}")
            sys.exit(1)
    
    # Write output CSV
    try:
        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            
            # Write header
            writer.writerow(['Label'])
            
            # Sort scouts by den type rank, then by name
            def sort_key(scout_tuple):
                (first_name, last_name, den_type), items = scout_tuple
                den_rank = DEN_TYPE_ORDER.get(den_type.lower(), 999)  # Unknown dens go to end
                return (den_rank, last_name.lower(), first_name.lower())
            
            sorted_scouts = sorted(scouts.items(), key=sort_key)
            
            # Write each scout's formatted label
            for (first_name, last_name, den_type), items in sorted_scouts:
                full_name = f"{first_name} {last_name}"
                items_list = ', '.join(items)
                
                # Create formatted label text
                label_text = f"{full_name} - {den_type}\n{items_list}"
                
                writer.writerow([label_text])
        
        print(f"\n✓ Successfully processed {len(scouts)} scouts")
        print(f"✓ Scouts grouped by den type: Lion → Tiger → Wolf → Bear → Webelos")
        print(f"✓ Labels formatted as: [Name] - [Den Type]\\n[Advancements]")
        print(f"✓ Output written to: {output_file}")
        
    except Exception as e:
        print(f"\n✗ Error writing output file: {e}")
        sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print("Usage: python advancement_processor.py <input_file1.csv> [input_file2.csv ...] [-o output_file.csv]")
        print("\nExamples:")
        print("  # Single file")
        print("  python advancement_processor.py advancements.csv")
        print()
        print("  # Multiple files combined")
        print("  python advancement_processor.py january.csv february.csv march.csv")
        print()
        print("  # Multiple files with custom output")
        print("  python advancement_processor.py jan.csv feb.csv -o q1_advancements.csv")
        sys.exit(1)
    
    # Parse arguments
    args = sys.argv[1:]
    output_file = 'advancement_list.csv'
    input_files = []
    
    # Check if -o flag is present for custom output filename
    if '-o' in args:
        o_index = args.index('-o')
        if o_index + 1 >= len(args):
            print("Error: -o flag requires an output filename")
            sys.exit(1)
        output_file = args[o_index + 1]
        # Remove -o and the output filename from args
        input_files = args[:o_index] + args[o_index + 2:]
    else:
        input_files = args
    
    if not input_files:
        print("Error: At least one input file is required")
        sys.exit(1)
    
    print(f"Processing {len(input_files)} file(s)")
    print(f"Output to: {output_file}")
    print("-" * 50)
    
    process_advancements(input_files, output_file)


if __name__ == '__main__':
    main()
