from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import csv
import io
import os

HOST = "localhost"
PORT = 8000


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":
            try:
                with open("index.html", "rb") as file:
                    content = file.read()

                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.send_header("Content-Length", len(content))
                self.end_headers()

                self.wfile.write(content)

            except FileNotFoundError:
                self.send_error(404, "index.html not found")

    def do_POST(self):
        if self.path != "/convert":
            self.send_error(404)
            return

        # Read request body
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        try:
            # Find the JSON data sent by the browser
            body_text = body.decode("utf-8")

            # The browser sends raw JSON
            data = json.loads(body_text)

            # If a single object is provided
            if isinstance(data, dict):
                data = [data]

            if not isinstance(data, list):
                raise ValueError(
                    "JSON must contain an object or a list of objects."
                )

            if len(data) == 0:
                raise ValueError("JSON file is empty.")

            # Make sure every item is a dictionary
            for item in data:
                if not isinstance(item, dict):
                    raise ValueError(
                        "JSON array must contain objects."
                    )

            # Get all column names
            columns = []

            for item in data:
                for key in item.keys():
                    if key not in columns:
                        columns.append(key)

            # Create CSV
            output = io.StringIO()

            writer = csv.DictWriter(
                output,
                fieldnames=columns
            )

            writer.writeheader()

            for item in data:
                writer.writerow(item)

            csv_data = output.getvalue().encode("utf-8")

            # Send CSV back to browser
            self.send_response(200)
            self.send_header("Content-Type", "text/csv")
            self.send_header(
                "Content-Disposition",
                'attachment; filename="converted.csv"'
            )
            self.send_header(
                "Content-Length",
                len(csv_data)
            )
            self.end_headers()

            self.wfile.write(csv_data)

        except Exception as e:

            error = json.dumps({
                "error": str(e)
            }).encode("utf-8")

            self.send_response(400)
            self.send_header(
                "Content-Type",
                "application/json"
            )
            self.send_header(
                "Content-Length",
                len(error)
            )
            self.end_headers()

            self.wfile.write(error)


if __name__ == "__main__":

    server = HTTPServer((HOST, PORT), Handler)

    print(f"Server running at http://{HOST}:{PORT}")
    print("Press Ctrl+C to stop.")

    server.serve_forever()