# Lab 5 Analysis Questions

## Q1: Plaintext vs TLS pcap comparison

Three things visible in the plaintext capture but hidden in the TLS capture:
1. The MQTT topic name (iot/lab/topic) is visible as readable text in the plaintext pcap but completely absent in the TLS pcap.
2. The JSON payload content including temperature and humidity values (e.g. {"device": "rpi-sensor", "temp": 22.0, "humid": 48.0, "unit": "C"}) is readable ASCII in the plaintext pcap but appears as random binary data in the TLS pcap.
3. The device identifier ("rpi-sensor") and all field names are visible in plaintext but encrypted in the TLS capture.

For an attacker intercepting traffic between the Pi and broker, the plaintext capture means they can read all sensor data, learn the topic structure, identify device names, and potentially inject spoofed messages. With TLS, the attacker only sees encrypted binary data and cannot read any payload content.

## Q2: require_certificate true

When require_certificate true is set, any client that tries to connect without providing a valid certificate signed by the CA is immediately rejected. Running mosquitto_sub -h <VM_IP> -p 8883 -t '#' without --cafile, --cert, and --key flags produces an SSL error such as "SSL Error: error:14094410:SSL routines:ssl3_read_bytes:sslv3 alert handshake failure" because the broker rejects the connection during the TLS handshake.

This is a significant security improvement over allow_anonymous true because anonymous connections allow any device anywhere to publish or subscribe to any topic without authentication. With require_certificate true, only devices holding a certificate signed by the trusted CA can connect, meaning an attacker cannot connect even if they know the broker's IP address and port.

## Q3: What Suricata can observe on TLS port 8883

Even though Suricata cannot decrypt the payload on port 8883, it can still observe useful metadata from TLS traffic:
- Connection frequency and rate: Suricata can count how many TLS connections are made per minute from each source IP. A flood of TLS connections from one device could trigger a rate-based rule similar to SID 2000001 but targeting port 8883.
- Packet size patterns: Unusually large TLS records could indicate buffer overflow probes, even without seeing the payload content.
- TLS handshake metadata: Suricata can inspect the TLS ClientHello to see the SNI (Server Name Indication), TLS version, and cipher suites offered.
- Connection duration and volume: Abnormally long connections or high byte counts can indicate data exfiltration.

To detect threats on port 8883, I would write a Suricata rule using the threshold keyword to alert on more than 50 TLS connections per minute from a single source IP, and another rule to alert on TLS records larger than a threshold size that could indicate a buffer overflow attempt.
