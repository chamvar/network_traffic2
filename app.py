from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

import psutil
import time


def list_network_interfaces():
  interfaces = psutil.net_if_stats()
  print("Available network interfaces:")
  for interface, stats in interfaces.items():
    print(f"{interface}: {stats}")


@app.route("/", methods=["GET", "POST"])
def network_traffic():
  inf = "Wi-Fi"
  try:
    net_stat = psutil.net_io_counters(pernic=True, nowrap=True)[inf]
    net_in_1 = net_stat.bytes_recv
    net_out_1 = net_stat.bytes_sent
    time.sleep(1)
    net_stat = psutil.net_io_counters(pernic=True, nowrap=True)[inf]
    net_in_2 = net_stat.bytes_recv
    net_out_2 = net_stat.bytes_sent
    net_in = round((net_in_2 - net_in_1) / 1024 / 1024, 3)
    net_out = round((net_out_2 - net_out_1) / 1024 / 1024, 3)
    return render_template("home.html", net_in=net_in, net_out=net_out)
  except KeyError:
    return render_template(f"Error: Network interface '{inf}' not found.")
    list_network_interfaces()


if __name__ == "__main__":
  app.run(debug=True)
