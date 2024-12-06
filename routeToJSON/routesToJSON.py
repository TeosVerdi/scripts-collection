import json
import os


def mask_to_cidr(mask):
    binary = ''.join([bin(int(x))[2:].zfill(8) for x in mask.split('.')])
    return str(binary.count('1'))


def convert_route_to_cidr(route_line):
    parts = route_line.strip().lower().split()
    if len(parts) < 5:
        return None

    try:
        ip_index = parts.index('add') + 1
        mask_index = parts.index('mask') + 1
    except ValueError:
        return None

    ip = parts[ip_index]
    mask = parts[mask_index]

    cidr = mask_to_cidr(mask)
    return {"hostname": f"{ip}/{cidr}", "ip": ""}


def process_route_file(filepath):
    with open(filepath, 'r') as f:
        routes = f.readlines()

    cidrs = []
    for route in routes:
        cidr = convert_route_to_cidr(route)
        if cidr:
            cidrs.append(cidr)

    return cidrs


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    routes_dir = os.path.join(script_dir, 'routes')

    if not os.path.exists(routes_dir):
        os.makedirs(routes_dir)
        print(f"Created 'routes' directory at {routes_dir}")
        return

    files = [f for f in os.listdir(routes_dir)]
    file_paths = [os.path.join(routes_dir, f) for f in files]

    all_cidrs = []
    for filepath in file_paths:
        try:
            cidrs = process_route_file(filepath)
            all_cidrs.extend(cidrs)
        except Exception as e:
            print(f"Error processing {filepath}: {e}")

    output_path = os.path.join(script_dir, 'cidrs.json')
    with open(output_path, 'w') as f:
        json.dump(all_cidrs, f, indent=2)


if __name__ == "__main__":
    main()
