from gpt.analyzer import PortScanAnalyzer
from portScan.port_scan import PortScanner
from softwareScan.software_scan import SoftwareScanner
import argparse
import logging
import time
from utils.banner import banner

print(banner())
# 配置日志记录器
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="A vulnerability scanning tool combined with artificial intelligence for Xin-Chuang"
    )
    parser.add_argument("--ip", type=str, help="Target IP")
    parser.add_argument("--port", type=str, help="Target Port")
    parser.add_argument(
        "--choice",
        type=int,
        default=3,
        help="Enter choice of scan (1-5):\n\
        1: Host Discover (-sP -T4) - Only performs host discovery\n \
        2: TCP SYN Scan (-Pn -sV -T4 -sS) - Recommended, most common, requires root\n\
        3: TCP Connect() Scan (-Pn -T4 -sV -sT) - Uses system call, full TCP connection, will be logged\n\
        4: UDP Scan (-Pn -sV -T4 -sU) - Probes UDP services, very slow, not recommended, requires root\n\
        5: TCP ACK Scan (-Pn -sV -T4 -sA) - Cannot detect open ports, used to check firewall rules, requires root\n",
    )
    # parser.add_argument('--analyzer', type=str, help='Llm for analyzing the result of the scan')

    return parser.parse_args()


def main():
    # Nmap port scan 端口扫描
    logging.info("Starting Nmap port scan...")
    args = parse_arguments()
    port_scan = PortScanner()
    analyzer = PortScanAnalyzer()
    response = port_scan.scanner(args.ip, args.port, args.choice, analyzer)
    print(response)

    # nikto software-vul scan
    logging.info("Starting Nikto software scan...")
    start_time = time.time()
    softwareScanner = SoftwareScanner()
    to_be_analyse_by_gpt = softwareScanner.nikto_scanner(target=args.ip)
    end_time = time.time()
    execution_time = end_time - start_time
    # time count, nikto may cost many time i'm afraid
    logging.info(f"Execution time: {execution_time} seconds")
    # 这里返回了nikto的扫描结果，需要进一步交给gpt处理
    print(to_be_analyse_by_gpt)


if __name__ == "__main__":
    main()
