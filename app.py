from flask import Flask, render_template_string, request
import metro  # import your metro.py module

app = Flask(__name__)

# Tailwind (dark theme) + Tom Select for searchable dropdown

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Metro Train Times</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://cdn.jsdelivr.net/npm/tom-select/dist/css/tom-select.css" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/tom-select/dist/js/tom-select.complete.min.js"></script>
</head>
<body class="bg-gray-900 text-gray-100 min-h-screen p-6">
  <div class="max-w-3xl mx-auto">
    <h1 class="text-3xl font-bold mb-6 text-center">🚇 Metro Train Times</h1>

    <form method="get" action="/" class="mb-6">
      <label for="station" class="block mb-2 text-lg">Select a station:</label>
      <select id="station" name="station" class="w-full p-2 rounded text-gray-900">
        {% for code, name in stations.items() %}
          <option value="{{code}}" {% if code == station_code %}selected{% endif %}>
            {{name}} ({{code}})
          </option>
        {% endfor %}
      </select>
      <button type="submit" class="mt-4 w-full bg-blue-600 hover:bg-blue-500 text-white py-2 rounded shadow">
        Show Trains
      </button>
    </form>

    {% if station_code %}
      <h2 class="text-2xl font-semibold mb-4">{{ stations[station_code] }} ({{ station_code }})</h2>
      {% for platform, trains in platform_data.items() %}
        <div class="mb-6 p-4 bg-gray-800 rounded-lg shadow">
          <h3 class="text-xl font-semibold mb-2">Platform {{ platform }}</h3>
          {% if trains %}
            {% for t in trains[:3] %}
              {% set line_color =
                'text-yellow-400' if t["line"] == "YELLOW"
                else 'text-green-400' if t["line"] == "GREEN"
                else 'text-gray-400' %}
              <div class="border-b border-gray-700 py-2">
                <p class="font-bold">
                  🚆 Train {{t["trn"]}} → {{t["destination"]}}
                  <span class="{{ line_color }}">({{t["line"]}} line)</span>
                </p>
                <p>⏳ Due in {{t["dueIn"]}} min</p>
                <p class="text-sm text-gray-400">📍 {{t["lastEvent"]}} at {{t["lastEventLocation"]}}</p>
              </div>
            {% endfor %}
          {% else %}
            <p class="text-gray-400">No trains found.</p>
          {% endif %}
        </div>
      {% endfor %}
    {% endif %}
  </div>

  <script>
    new TomSelect("#station", {
      create: false,
      sortField: {
        field: "text",
        direction: "asc"
      },
      maxOptions: 200
    });
  </script>
</body>
</html>
"""


@app.route("/", methods=["GET"])
def index():
    station_code = request.args.get("station")
    platform_data = {}

    if station_code and station_code.upper() in metro.stations:
        station_code = station_code.upper()
        for platform in [1, 2]:
            trains = metro.fetch_trains(station_code, platform)
            platform_data[platform] = trains

    return render_template_string(
        TEMPLATE,
        stations=metro.stations,
        station_code=station_code,
        platform_data=platform_data
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

